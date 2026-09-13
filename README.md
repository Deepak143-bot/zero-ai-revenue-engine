# Zero-Cost AI Revenue Engine — v1

A phone-friendly, GitHub Actions based starter for building a legitimate AI-assisted micro-business with ₹0 upfront.

## What this does

Once per day, the workflow:

1. Pulls public RSS trend/news signals for a small set of commercial topics.
2. Sends the collected signals to Gemini when `GEMINI_API_KEY` is configured.
3. Produces a structured opportunity report:
   - demand signal
   - target buyer
   - product/service idea
   - price hypothesis
   - creation plan
   - listing copy
   - marketing posts
   - risk/copyright notes
4. Saves the report and a machine-readable queue in the repository.

It does **not**:
- guarantee income
- spam people
- create fake traffic/reviews
- scrape copyrighted datasets
- auto-charge customers
- bypass platform rules
- publish commercial listings without human approval

## Why this architecture

The user has only an Android phone, two USB drives, and no paid budget. Ollama is therefore not the core runtime because it normally needs a capable host computer. GitHub Actions can run scheduled automation, while Gemini's API has a free tier subject to model/rate limits. GitHub's standard hosted runners are free for public repositories.

## Setup from a phone

1. Create a **public GitHub repository** named `zero-ai-revenue-engine`.
2. Upload all files from this project.
3. In the repo, open **Settings → Secrets and variables → Actions**.
4. Create a repository secret:
   - Name: `GEMINI_API_KEY`
   - Value: a Gemini API key from Google AI Studio's free tier.
5. Open **Actions** and enable workflows if GitHub asks.
6. Run `Daily Opportunity Engine` manually once.
7. Review `reports/` before acting on anything.
8. Do not publish or sell anything until checking platform rules, licenses, originality, and factual claims.

## No-key mode

The workflow still runs without Gemini. It creates a deterministic opportunity report from the collected signals, but the AI-generated copy/product analysis will be limited.

## USB use

**USB 1 — SYSTEM**
- Keep a backup of this repository ZIP, prompts, workflow files, and important documentation.

**USB 2 — ASSET VAULT**
- Keep generated product files, thumbnails, videos, source assets, exports, and backups.

Only one USB needs to be connected at a time.

## Verified build

The included `engine/run.py` creates the `reports/` directory automatically on first run, so the workflow does not depend on that directory already existing.

## Next versions

v2 should add:
- a human-approval queue
- better trend scoring
- product templates
- a mobile-friendly dashboard
- optional marketplace adapters
- revenue/experiment tracking
- automatic rollback/error handling

The goal is to move from "AI generates ideas" to "AI runs a measurable business loop", while keeping money movement and irreversible publishing behind explicit human approval.
