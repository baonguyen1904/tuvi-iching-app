"""Profile API routes — generate, status, get, feedback."""

import asyncio
import json
import logging
import os
from dataclasses import asdict
from datetime import datetime, date

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

from app import db
from app.services import scraper_browser

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

# Birth hour mapping: slug → (display_label, hour_int for cohoc, hour_int for tuvivn)
BIRTH_HOURS = {
    "ty": ("Giờ Tý (23:00-01:00)", 1, 23),
    "suu": ("Giờ Sửu (01:00-03:00)", 2, 1),
    "dan": ("Giờ Dần (03:00-05:00)", 3, 3),
    "mao": ("Giờ Mão (05:00-07:00)", 4, 5),
    "thin": ("Giờ Thìn (07:00-09:00)", 5, 7),
    "ty_": ("Giờ Tỵ (09:00-11:00)", 6, 9),
    "ngo": ("Giờ Ngọ (11:00-13:00)", 7, 11),
    "mui": ("Giờ Mùi (13:00-15:00)", 8, 13),
    "than": ("Giờ Thân (15:00-17:00)", 9, 15),
    "dau": ("Giờ Dậu (17:00-19:00)", 10, 17),
    "tuat": ("Giờ Tuất (19:00-21:00)", 11, 19),
    "hoi": ("Giờ Hợi (21:00-23:00)", 12, 21),
}


# --- Request/Response Models ---

class GenerateRequest(BaseModel):
    birthDate: str = Field(..., description="YYYY-MM-DD")
    birthHour: str = Field(..., description="ty, suu, dan, ...")
    gender: str = Field(..., description="male or female")
    name: Optional[str] = None
    namXem: int = Field(default=2026)


class GenerateResponse(BaseModel):
    profileId: str
    status: str


class StatusResponse(BaseModel):
    profileId: str
    status: str
    step: Optional[str] = None
    message: Optional[str] = None
    progress: Optional[int] = None


class FeedbackRequest(BaseModel):
    profileId: str
    rating: int
    comment: Optional[str] = None


STEP_MESSAGES = {
    "scraping_cohoc": "Đang lấy lá số từ cohoc.net...",
    "scraping_tuvivn": "Đang lấy lá số từ tuvi.vn...",
    "scoring": "Đang tính điểm...",
    "ai_generating": "Đang viết luận giải AI...",
}


@router.post("/generate", response_model=GenerateResponse)
async def generate_profile(req: GenerateRequest, background_tasks: BackgroundTasks):
    if req.birthHour not in BIRTH_HOURS:
        raise HTTPException(400, f"Invalid birthHour: {req.birthHour}")

    gender_vi = "Nam" if req.gender == "male" else "Nữ"

    # Check cache
    cached = db.find_cached(req.birthDate, req.birthHour, gender_vi, req.namXem)
    if cached:
        return GenerateResponse(profileId=cached["id"], status="completed")

    profile_id = db.make_profile_id(req.birthDate, req.birthHour, gender_vi, req.namXem)
    existing = db.get_status(profile_id)
    if existing and existing["status"] == "processing":
        return GenerateResponse(profileId=profile_id, status="processing")

    db.create_profile(profile_id, req.name or "", req.birthDate, req.birthHour, gender_vi, req.namXem)
    background_tasks.add_task(_run_pipeline, profile_id, req.birthDate, req.birthHour, gender_vi, req.name or "", req.namXem)

    return GenerateResponse(profileId=profile_id, status="processing")


@router.get("/profile/{profile_id}/status", response_model=StatusResponse)
async def get_profile_status(profile_id: str):
    status = db.get_status(profile_id)
    if not status:
        raise HTTPException(404, "Profile not found")

    step = status.get("current_step", "")
    message = STEP_MESSAGES.get(step, "")
    if step == "ai_generating":
        progress = status.get("ai_progress", 0)
        message = f"Đang viết luận giải AI... ({progress}/8)"
    else:
        progress = None

    return StatusResponse(
        profileId=profile_id,
        status=status["status"],
        step=step,
        message=message if status["status"] == "processing" else None,
        progress=progress,
    )


@router.get("/profile/{profile_id}")
async def get_profile_data(profile_id: str):
    profile = db.get_profile(profile_id)
    if not profile:
        raise HTTPException(404, "Profile not found")

    if profile["status"] != "completed":
        raise HTTPException(400, f"Profile not ready: {profile['status']}")

    return _format_profile_response(profile)


@router.post("/feedback")
async def submit_feedback(req: FeedbackRequest):
    logger.info("Feedback received: profileId=%s rating=%d comment=%s", req.profileId, req.rating, req.comment)
    return {"ok": True}


# --- Pipeline ---

async def _run_pipeline(profile_id: str, birth_date: str, birth_hour: str, gender: str, name: str, nam_xem: int):
    """Run full pipeline in background: scrape → score → AI."""
    try:
        hour_label, cohoc_time, tuvivn_hour = BIRTH_HOURS[birth_hour]
        dob = datetime.strptime(birth_date, "%Y-%m-%d")

        # Step 1: Scrape cohoc.net
        db.update_step(profile_id, "scraping_cohoc")
        from app.services.scraper_cohoc import get_page_detail as cohoc_scrape
        cohoc_data = await cohoc_scrape(dob, cohoc_time, gender)

        # Step 2: Scrape tuvi.vn
        db.update_step(profile_id, "scraping_tuvivn")
        from app.services.scraper_tuvivn import get_page_detail as tuvivn_scrape
        dob_with_hour = dob.replace(hour=tuvivn_hour)
        tuvivn_data = await tuvivn_scrape(dob_with_hour, gender, name, nam_xem=nam_xem)

        # Save scrape data
        metadata = {
            "nam": cohoc_data.get("nam"),
            "menh": cohoc_data.get("menh"),
            "cuc": cohoc_data.get("cuc"),
            "amDuong": cohoc_data.get("am_duong"),
            "menhChu": cohoc_data.get("menh_chu"),
            "thanChu": cohoc_data.get("than_chu"),
            "thanCu": cohoc_data.get("than_cu"),
        }

        cung_lifetime = cohoc_data.get("cung", [])
        cung_10yrs = cohoc_data.get("cung_10yrs", [])
        cung_12months = []
        if tuvivn_data.cung:
            cung_12months = [{"ten": c.ten, "sao": c.sao, "thang": c.thang} for c in tuvivn_data.cung.cung_12months]

        db.save_scrape_data(profile_id, metadata, cung_lifetime, cung_10yrs, cung_12months)

        # Step 3: Scoring
        db.update_step(profile_id, "scoring")
        from app.services.scoring import ScoringEngine
        from pathlib import Path
        xlsx_path = Path(__file__).resolve().parents[1] / "data" / "laso_points.xlsx"
        engine = ScoringEngine(xlsx_path=str(xlsx_path))

        scoring_result = engine.score(
            cung_lifetime=cung_lifetime,
            cung_10yrs=cung_10yrs,
            cung_12months=cung_12months,
            than_cu=cohoc_data.get("than_cu", ""),
        )

        scores_dict = {}
        alerts_list = []
        for dim_key, dim_scores in scoring_result.dimensions.items():
            scores_dict[dim_key] = {
                "label": dim_scores.label,
                "summaryScore": dim_scores.summary_score,
                "lifetime": [asdict(p) for p in dim_scores.lifetime],
                "decade": [asdict(p) for p in dim_scores.decade],
                "monthly": [asdict(p) for p in dim_scores.monthly],
            }

        for alert in scoring_result.all_alerts:
            alerts_list.append(asdict(alert))

        db.save_scores(profile_id, scores_dict, alerts_list)

        # Step 4: AI Generation
        db.update_step(profile_id, "ai_generating")
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            logger.warning("ANTHROPIC_API_KEY not set, skipping AI generation")
            db.save_ai_result(profile_id, "AI generation skipped (no API key)", {})
            return

        from app.services.ai_engine import AIEngine
        from app.models.schemas import UserProfile, LasoMetadata

        kb_dir = Path(__file__).resolve().parents[1] / "knowledge_base"
        ai_engine = AIEngine(kb_dir=str(kb_dir), api_key=api_key)

        today = date.today()
        age = today.year - dob.year
        user_profile = UserProfile(
            name=name or None,
            birth_date=dob.date() if hasattr(dob, 'date') else date(dob.year, dob.month, dob.day),
            birth_hour=birth_hour,
            birth_hour_label=hour_label,
            gender=gender,
            gender_label=gender,
            current_age=age,
            nam_xem=nam_xem,
        )

        laso_metadata = LasoMetadata(
            nam=metadata.get("nam", ""),
            menh=metadata.get("menh", ""),
            cuc=metadata.get("cuc", ""),
            am_duong=metadata.get("amDuong", ""),
            cung_menh=cung_lifetime[0]["ten"] if cung_lifetime else "",
        )

        progress_count = 0

        async def on_progress(dim_key: str):
            nonlocal progress_count
            progress_count += 1
            db.update_step(profile_id, "ai_generating", progress_count)

        ai_result = await ai_engine.generate_all(
            user=user_profile,
            metadata=laso_metadata,
            laso=cohoc_data,
            scoring=scoring_result,
            progress_callback=on_progress,
        )

        db.save_ai_result(profile_id, ai_result.overview, ai_result.dimensions)

    except Exception as e:
        logger.exception("Pipeline failed for profile %s", profile_id)
        db.set_error(profile_id, str(e))


def _format_profile_response(profile: dict) -> dict:
    """Format SQLite row into API response matching frontend types."""
    scores = json.loads(profile["scores"] or "{}")
    alerts = json.loads(profile["alerts"] or "[]")
    interpretations = json.loads(profile["interpretations"] or "{}")
    metadata = json.loads(profile["metadata"] or "{}")

    dimensions = {}
    for dim_key, dim_data in scores.items():
        dim_alerts = [a for a in alerts if a.get("dimension") == dim_key]

        def _format_scores(points: list) -> dict:
            return {
                "labels": [p["period"] for p in points],
                "duong": [p["duong"] for p in points],
                "am": [p["am"] for p in points],
                "tb": [p["tb"] for p in points],
            }

        dimensions[dim_key] = {
            "label": dim_data.get("label", dim_key),
            "summaryScore": dim_data.get("summaryScore", 0),
            "lifetime": _format_scores(dim_data.get("lifetime", [])),
            "decade": _format_scores(dim_data.get("decade", [])),
            "monthly": _format_scores(dim_data.get("monthly", [])),
            "alerts": dim_alerts,
            "interpretation": interpretations.get(dim_key),
        }

    hour_label = BIRTH_HOURS.get(profile["birth_hour"], ("", 0, 0))[0]

    return {
        "profileId": profile["id"],
        "name": profile["name"],
        "birthDate": profile["birth_date"],
        "birthHour": hour_label,
        "gender": profile["gender"],
        "metadata": metadata,
        "overview": {
            "summary": profile.get("overview_summary", ""),
        },
        "dimensions": dimensions,
        "createdAt": profile.get("created_at"),
    }
