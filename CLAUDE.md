<!-- GSD:project-start source:PROJECT.md -->
## Project

**Kinh Dịch × Tử Vi — AI Luận Giải MVP**

A web app that takes a user's birth data (ngày giờ sinh), generates a Vietnamese Tử Vi (astrology) chart with scores across life dimensions, and uses Claude AI to produce personalized narrative interpretations ("luận giải") for each dimension. This is an MVP for testing with ~20-50 existing clients of our expert partner — not a full product launch.

**Core Value:** Users receive personalized, expert-quality AI narrative interpretations of their Tử Vi chart across 7 life dimensions, grounded in real scoring data — empowering, not fear-inducing.

### Constraints

- **Timeline**: 2-4 weeks
- **Team**: 1 developer (using Claude Code), 1 domain expert (~5h availability)
- **Budget**: Minimal — free/cheap infrastructure (Vercel + Railway)
- **Language**: Vietnamese only for MVP
- **Test group**: ~20-50 existing clients of expert
- **Scraper dependency**: cohoc.net could change/block — need caching + error handling
- **Expert time**: Only ~5h total — must be pre-prepared and efficient
- **AI model**: Claude Sonnet API — 200K context window sufficient for structured prompt + inline KB
- **Tech stack**: Next.js (frontend) + Python FastAPI (backend) + SQLite/Supabase (cache) + Chart.js/Recharts (charts)
<!-- GSD:project-end -->

<!-- GSD:stack-start source:STACK.md -->
## Technology Stack

Technology stack not yet documented. Will populate after codebase mapping or first phase.
<!-- GSD:stack-end -->

<!-- GSD:conventions-start source:CONVENTIONS.md -->
## Conventions

Conventions not yet established. Will populate as patterns emerge during development.
<!-- GSD:conventions-end -->

<!-- GSD:architecture-start source:ARCHITECTURE.md -->
## Architecture

Architecture not yet mapped. Follow existing patterns found in the codebase.
<!-- GSD:architecture-end -->

<!-- GSD:workflow-start source:GSD defaults -->
## GSD Workflow Enforcement

Before using Edit, Write, or other file-changing tools, start work through a GSD command so planning artifacts and execution context stay in sync.

Use these entry points:
- `/gsd:quick` for small fixes, doc updates, and ad-hoc tasks
- `/gsd:debug` for investigation and bug fixing
- `/gsd:execute-phase` for planned phase work

Do not make direct repo edits outside a GSD workflow unless the user explicitly asks to bypass it.
<!-- GSD:workflow-end -->



<!-- GSD:profile-start -->
## Developer Profile

> Profile not yet configured. Run `/gsd:profile-user` to generate your developer profile.
> This section is managed by `generate-claude-profile` -- do not edit manually.
<!-- GSD:profile-end -->
