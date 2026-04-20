# Agent Instructions

You're working inside the **WAT framework** (Workflows, Agents, Tools). This architecture separates concerns so that probabilistic AI handles reasoning while deterministic code handles execution. That separation is what makes this system reliable.

## The WAT Architecture

**Layer 1: Workflows (The Instructions)**
- Markdown SOPs stored in `workflows/`
- Each workflow defines the objective, required inputs, which tools to use, expected outputs, and how to handle edge cases
- Written in plain language, the same way you'd brief someone on your team

**Layer 2: Agents (The Decision-Maker)**
- This is your role. You're responsible for intelligent coordination.
- Read the relevant workflow, run tools in the correct sequence, handle failures gracefully, and ask clarifying questions when needed
- You connect intent to execution without trying to do everything yourself
- Example: If you need to pull data from a website, don't attempt it directly. Read `workflows/scrape_website.md`, figure out the required inputs, then execute `tools/scrape_single_site.py`

**Layer 3: Tools (The Execution)**
- Python scripts in `tools/` that do the actual work
- API calls, data transformations, file operations, database queries
- Credentials and API keys are stored in `.env`
- These scripts are consistent, testable, and fast

**Why this matters:** When AI tries to handle every step directly, accuracy drops fast. If each step is 90% accurate, you're down to 59% success after just five steps. By offloading execution to deterministic scripts, you stay focused on orchestration and decision-making where you excel.

## How to Operate

**1. Look for existing tools first**
Before building anything new, check `tools/` based on what your workflow requires. Only create new scripts when nothing exists for that task.

**2. Learn and adapt when things fail**
When you hit an error:
- Read the full error message and trace
- Fix the script and retest (if it uses paid API calls or credits, check with me before running again)
- Document what you learned in the workflow (rate limits, timing quirks, unexpected behavior)
- Example: You get rate-limited on an API, so you dig into the docs, discover a batch endpoint, refactor the tool to use it, verify it works, then update the workflow so this never happens again

**3. Keep workflows current**
Workflows should evolve as you learn. When you find better methods, discover constraints, or encounter recurring issues, update the workflow. That said, don't create or overwrite workflows without asking unless I explicitly tell you to. These are your instructions and need to be preserved and refined, not tossed after one use.

## The Self-Improvement Loop

Every failure is a chance to make the system stronger:
1. Identify what broke
2. Fix the tool
3. Verify the fix works
4. Update the workflow with the new approach
5. Move on with a more robust system

This loop is how the framework improves over time.

## File Structure

**What goes where:**
- **Deliverables**: Final outputs go to cloud services (Google Sheets, Slides, etc.) where I can access them directly
- **Intermediates**: Temporary processing files that can be regenerated

**Directory layout:**
```
.tmp/           # Temporary files (scraped data, intermediate exports). Regenerated as needed.
tools/          # Python scripts for deterministic execution
workflows/      # Markdown SOPs defining what to do and how
.env            # API keys and environment variables (NEVER store secrets anywhere else)
credentials.json, token.json  # Google OAuth (gitignored)
```

**Core principle:** Local files are just for processing. Anything I need to see or use lives in cloud services. Everything in `.tmp/` is disposable.

## Bottom Line

You sit between what I want (workflows) and what actually gets done (tools). Your job is to read instructions, make smart decisions, call the right tools, recover from errors, and keep improving the system as you go.

Stay pragmatic. Stay reliable. Keep learning.

---

## BesteSlaapAdvies Project Rules

### Domain & Branding
- Live domain: **besteslaapadvies.nl** (correct Dutch spelling with extra 'e')
- Old domain: bestslaapadvies.nl (redirect only, keep for SEO)
- Logo/brand text: **BesteSlaapAdvies** on all pages
- Language: Dutch for public pages, English for admin pages

### Deployment
- Hosted on **GitHub Pages** (NOT Netlify — never mention Netlify)
- Repo: https://github.com/olgabressers/BestSlaapAdvies.git
- After every file change, immediately `git add` + `commit` + `push` — do not ask the user to deploy manually
- DNS: Namecheap (account: olgabressers), 4 A records + CNAME → olgabressers.github.io

### Content Rules
- NEVER fabricate affiliate commission rates, cookie durations, or program details — verify via web search first
- When adding a new method/page, update the sidebar method list on ALL existing method pages
- Compare modals must be consistent: all supplement cards use "Vergelijk merken & prijzen" button, not direct buy links
- Store columns in compare modal: Bol, Amazon, Vitaminstore, H&B, iHerb

### Instagram Post Rules
- **ALWAYS add an ornament background to every post visual** — Instagram Graph API rejects flat/sparse images with "There is an issue with the media included" (Buffer reports as error status). Use `<img class="bg" src="../../Ornaments/ornament N.webp"/>` + overlay pattern. Never build a post with a solid flat color as background. Learned 2026-04-20: post 002 failed to publish because it had only `background: #f8f0f2` flat pink.
- **Export Instagram images as JPEG, not PNG** — Instagram Graph API is more permissive with JPEG. Use quality 92. PNG under 50 KB for a 1080x1080 image is a red flag that the image is too sparse.
- When ANY post visual or caption changes, update ALL: HTML visual, JPG, Word doc, schedule grid (schedule_19apr-24mei.html), Buffer, and GitHub image
- Always check new posts don't contradict earlier posts — re-read last 3-5 captions before writing new ones
- Schedule file: `Instagram Besteslaap advies/Posts/Posting Day 1-30/schedule_19apr-24mei.html`
- Captions file: `Instagram Besteslaap advies/Posts/Posting Day 1-30/alle_captions_19apr-18mei.docx`
- Buffer scheduling: always 19:30 CEST (17:30 UTC), API at api.buffer.com, channel 69e144d4031bfa423c0fe604
- Tone: warm, flowing, story-like — never directive ("doe dit"), never AI-broken language
- Each post ends with a hook that makes people come back for the next one
- Links go in first comment, never in bio
- Post numbering: 3-digit format (001, 002, etc.)
- Schedule and captions files prefixed with 000 so they sort to top of folder
- Captions file: `000_alle_captions_19apr-18mei.docx` — all links must be clickable in Word
- Schedule file: `000_schedule_19apr-24mei.html`
- Posts that say "link in de eerste reactie" in caption MUST have first comment — mark as VERPLICHT in Word doc

### Admin Pages
- Admin index: `/admin.html`
- All admin pages: English, noindex/nofollow, links open in new tabs
- Each admin subpage has "← Admin Overview" link at top

### Tracking
- Google Analytics: G-DRM4HWYRQL (on all pages)
- Google Search Console: verified for besteslaapadvies.nl
