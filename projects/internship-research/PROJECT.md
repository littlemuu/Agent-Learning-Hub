# Internship Research Agent — Project Context

Status: selected; first vertical slice specified; implementation not started.

This file is the stable source of truth for project scope and decisions. Current work state and the single next task live in [PROGRESS.md](PROGRESS.md).

## Goal

Build a small, reliable Agent engineering portfolio project that helps a student decide whether a specific public internship is worth pursuing.

The project should improve a real decision, preserve evidence for every material claim and fail honestly when a job page does not provide enough information. It is not an automatic application system or a broad recruiting crawler.

## First Vertical Slice

One structured candidate profile plus one public job URL or pasted JD produces one evidence-backed decision card.

Initial flow:

1. Validate the profile and job input.
2. Acquire a read-only job snapshot, or use the pasted JD directly.
3. Extract normalized facts with source evidence.
4. Evaluate hard constraints and fit dimensions with transparent rules.
5. Render one concise decision card.

The first usable entry point should be a CLI. A blocked or unreadable URL is an explicit acquisition failure, not permission to infer missing content.

## Input And Output Contract

### Input

- CandidateProfile: non-sensitive skills, project evidence, role direction, location/work-mode preferences and availability constraints.
- JobInput: one public URL or one pasted JD.
- The public repository contains only examples or anonymized fixtures. A real personal profile belongs in a local ignored file.

### DecisionCard

- source URL or pasted-text identifier, observation time and content hash;
- confirmed company, role, location, work mode, responsibilities, requirements and timing;
- an evidence quote and source reference for every confirmed fact;
- explicit unknown fields;
- hard constraints marked met, not met or unknown;
- separate fit dimensions such as role direction, demonstrated skills, project relevance, location/work mode and availability;
- one verdict: worth applying, verify first or not a fit;
- one concrete next action.

There is no uncalibrated 0–100 total match score. Unknown information must not be converted into a negative match.

## Evidence And Decision Invariants

- A returned URL must come from the input or the acquired snapshot.
- Every confirmed factual field must carry evidence from the JD.
- Unsupported fields remain unknown; the model must not complete them from general knowledge.
- Facts, user preferences and derived judgments stay separate in the state.
- Hard constraints are evaluated deterministically after extraction.
- The final recommendation is generated from the validated state, not rewritten freely from intermediate summaries.
- The same validated state must produce the same verdict.

## Explicit Non-Goals

The first slice does not include:

- open-web job discovery or multiple-job ranking;
- automatic application, recruiting-site login or HR outreach;
- browser automation that bypasses access controls;
- Web UI, SSE, application CRM, notifications or scheduling;
- multi-agent orchestration, RAG, vector storage or long-term memory;
- long career reports or generic resume advice.

These capabilities require a separate decision after the evidence path passes its eval gate.

## Initial Eval Gate

Start with 10 fixed, anonymized JD fixtures and expand to at least 20 before completing the reliability milestone. Include complete JDs, missing fields, conflicting requirements, blocked-page substitutes and deliberately irrelevant text.

The verified path must provide:

- 100% schema-valid DecisionCard output;
- zero fabricated companies, roles or URLs in the fixed set;
- evidence coverage for every confirmed factual field;
- correct preservation of unknown fields;
- deterministic hard-constraint and verdict behavior for the same validated state;
- recorded latency, token use and failure class for real-model smoke runs.

Tests must evaluate field accuracy, evidence grounding and abstention. Checking that a report merely contains the expected headings is not a quality test.

## Legacy Branch Decision

The earlier implementation remains available at [littlemuu/hello-agents:internship-agent](https://github.com/littlemuu/hello-agents/tree/internship-agent). It is a historical reference, not the new codebase.

The audit found that it had valuable engineering work but an unreliable core evidence path:

- search mostly supplied DuckDuckGo or Tavily snippets rather than fetched JD pages;
- full candidate text and many generic keywords polluted search queries;
- source reliability and 0–100 match scores were uncalibrated heuristics;
- extracted URLs were not required to belong to the retrieved source set;
- the normal final-report prompt omitted the structured job items and search diagnostics;
- tests covered parsing, fallback, API and replay behavior but not retrieval precision, evidence accuracy or decision usefulness;
- UI, SSE, caching, replay and application tracking grew before the core quality was measured.

Retain as ideas:

- the product safety boundary;
- the JobItem schema as a starting reference;
- explicit unknown values, deterministic fallback and search diagnostics;
- fake, dry-run, replay, timeout, privacy-aware logging and contract-test practices.

Do not migrate wholesale:

- the four-task DeepResearch planner and multi-agent choreography;
- the old orchestrator and API compatibility burden;
- free-form numeric match scoring;
- free-form final report generation;
- the large Vue/SSE/application-tracking workbench.

The old branch is not to be rebased or merged into this project.

## Privacy And Safety

- Do not commit a real resume, phone number, personal email, full address or recruiting account data.
- Keep the real candidate profile in profile.local.*; the repository ignores this path.
- Do not fabricate user experience or job facts.
- Do not auto-apply, log into recruiting platforms, mass-contact HR or bypass platform rules.
- Treat job pages and pasted JD text as untrusted input.
- Any future external write action requires explicit human approval.

## Delivery Order

1. Define schemas and offline fixtures.
2. Implement one fixture-to-DecisionCard CLI path.
3. Add grounded extraction with a real model and readable trace.
4. Add a read-only public-page acquisition tool with timeout and explicit failure states.
5. Expand the fixed eval set, add CI and record cost/latency.
6. Consider job discovery only after the single-JD decision path meets its eval gate.

No abstraction or feature is added only because it may be useful later.
