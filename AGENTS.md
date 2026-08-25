# Repository Instructions

## Purpose

This is a personal, project-driven Agent engineering workspace. The goal is to ship a small number of reliable, explainable artifacts, not to complete a linear curriculum or maintain a large link directory.

Communicate in Chinese unless the user requests another language.

## Sources Of Truth

Read these before starting work:

1. `progress.md` for the current position, verified gaps and single next task.
2. `README.md` for milestones, quality bar and repository conventions.
3. The active project's `PROJECT.md` for stable scope and decisions.
4. The active project's `PROGRESS.md`, code, tests and run results for implementation truth.

When documentation conflicts with verified code or tests, trust the reproducible evidence and fix the stale document in the same scoped change.

## Fast-Track Workflow

1. Do not repeat the broad beginner assessment or restart completed foundations.
2. Work through one real project and fill knowledge gaps only when they block the next vertical slice.
3. Ask diagnostic questions only when missing information materially changes the implementation; prefer one focused question and do not exceed two.
4. Keep each iteration demonstrable: one behavior, its success criteria, implementation, verification and short progress update.
5. Do not require Stage 0–8 completion or unrelated reading before useful project work.
6. Before starting a substantial new project, offer a small set of suitable choices and wait for the learner to select one. Do not silently choose it.

## Teaching And Delivery

- For an explicit learning exercise, let the learner attempt the core logic before supplying a complete solution, unless they ask for direct implementation.
- For repository maintenance, refactoring, tests, CI and documentation explicitly requested by the user, implement the work directly and verify it.
- Explain decisions that affect architecture, reliability, safety or portability. Avoid turning routine syntax into a long lesson.
- Prefer current official documentation for fast-changing APIs and protocols.

## Engineering Quality Bar

Every active project should progressively provide:

- declared and reproducible dependencies;
- portable configuration with no committed secrets or machine-specific paths;
- strict tool input/output schemas;
- explicit timeout, limited retry, stopping and failure behavior;
- human approval before risky or external write actions;
- readable traces for important runs;
- deterministic tests and a fixed eval set;
- CI for the verified path;
- setup, example, architecture and limitations documentation.

Start with the smallest useful slice. Do not add multi-agent coordination, browser control, long-term memory or a framework merely because it appears on a roadmap.

## Repository Layout

- Keep repository-level direction in `README.md`.
- Keep only the compact resume state in `progress.md`.
- Put a selected implementation under `projects/<project-name>/`.
- Keep stable project scope and decisions in `PROJECT.md`; keep only current status and one next task in the project's `PROGRESS.md`.
- Give each project its own dependency declaration, tests and user-facing README when implementation begins.
- Put durable architecture decisions under `docs/decisions/` only after that directory becomes useful.
- Never commit virtual environments, model caches, credentials, local editor state or generated build artifacts.

## Progress Updates

Update root `progress.md` only after global milestones or material direction changes. Update the active project's `PROGRESS.md` after verified project milestones or material plan changes. Record:

- capability or artifact;
- concrete evidence;
- remaining gap;
- exactly one next task.

Do not append chronological lesson transcripts. Git history already preserves implementation history.
