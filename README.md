
Start Commands

Terminal 1: Backend

cd /mnt/d/Working/TBTesu/TuViApp/backend
pip install -r requirements.txt
# Set API key for AI generation (optional — will skip AI if not set)
export ANTHROPIC_API_KEY="sk-ant-..."
# Need Playwright system deps (one-time, requires sudo)
sudo playwright install-deps
uvicorn app.main:app --reload --port 8000

Terminal 2: Frontend

cd /mnt/d/Working/TBTesu/TuViApp/frontend
npm install
npm run dev

URLs

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

Notes

- Backend cần sudo playwright install-deps lần đầu (install Chromium system libs cho WSL2)
- Nếu không set ANTHROPIC_API_KEY, pipeline vẫn chạy nhưng skip AI generation
- Frontend dùng mock data nếu backend chưa sẵn sàng (xem frontend/lib/mock-data.ts)
