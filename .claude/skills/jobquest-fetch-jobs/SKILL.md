---
name: jobquest-fetch-jobs
description: Use this skill when you have a careers page URL and need to extract all job listings. Uses Playwright to scrape jobs with descriptions, handles JavaScript-rendered pages, and saves results to the company's references folder. Works with all ATS platforms (Lever, Greenhouse, Ashby, generic).
---

# Fetch Jobs from Careers Page

## When to Use This Skill

Activate this skill when:
- You have a careers page URL and need to get job listings
- User asks to "get all jobs from [URL]"
- User wants to "see what positions [Company] has open"
- After `jobquest-find-careers-url` discovers a URL

## Workflow

### Step 1: Fetch Job Listings with Playwright

**IMPORTANT:** Always use the Playwright-based scraper, never WebFetch. Many careers pages use React/JavaScript to render job listings.

Run the scraper:

```bash
cd .claude/skills/jobquest-shared-tools
uv run python -m src.fetch_jobs "<careers_url>" --company "<Company Name>" --fetch-descriptions
```

**Flags:**
- `--company` (required): Company name for organizing saved files
- `--fetch-descriptions` (recommended): Fetches full job descriptions in parallel

**What this does:**
- Uses Playwright to load the careers page (handles JavaScript)
- Automatically detects ATS platform (Lever, Greenhouse, Ashby, generic)
- Extracts all job listings with parallel fetching
- Fetches full descriptions for each job (5 concurrent requests)
- Saves to `job_applications/{company}/references/{date}/*.md`

**Example:**
```bash
uv run python -m src.fetch_jobs "https://www.aktek.io/careers" --company "Aktek" --fetch-descriptions
```

**Output:**
```
✓ Fetched 5 jobs from Aktek (generic)
✓ New jobs: 5
✓ Changed jobs: 0
✓ Unchanged (skipped): 0
✓ Written 5 files to: job_applications/aktek/references/2025-10-22
```

### Step 2: Review Extracted Jobs

The scraper saves each job as a markdown file with frontmatter:

```markdown
---
job_url: "https://www.aktek.io/careers/sr-full-stack-software-developer"
accessed_date: "2025-10-22"
company: "Aktek"
role: "Sr. Full Stack Software Engineer (MERN)"
location: "Remote"
---

# Sr. Full Stack Software Engineer (MERN)

[Full job description here...]
```

Files are saved to:
```
job_applications/{company}/references/{date}/
├── sr-full-stack-software-engineer-mern.md
├── devops-engineer.md
└── ...
```

### Step 3: Parse and Return Summary

Read the saved files and provide a summary:

```
Found X jobs at Company:

1. Job Title
   - Location: Remote
   - URL: ...

2. Another Job Title
   - Location: London
   - URL: ...
```

## Supported Platforms

The scraper automatically handles:

### Lever (jobs.lever.co)
- Multi-page pagination
- Department filtering
- Lazy loading

### Greenhouse (boards.greenhouse.io)
- Infinite scroll
- Department sections
- Application forms

### Ashby (jobs.ashbyhq.com)
- JavaScript-rendered content
- Dynamic loading
- API-based fetching

### Generic (custom careers pages)
- Common HTML patterns
- Schema.org markup
- Custom scraping logic

## Options and Flags

### Basic Usage (titles + URLs only)
```bash
uv run python -m src.fetch_jobs "<url>" --company "<Company>"
```

### With Full Descriptions (recommended)
```bash
uv run python -m src.fetch_jobs "<url>" --company "<Company>" --fetch-descriptions
```

### Force Re-fetch (ignore cache)
```bash
uv run python -m src.fetch_jobs "<url>" --company "<Company>" --force
```

## Output Format

**Console output shows:**
- Number of jobs fetched
- New vs changed vs unchanged jobs
- Where files were written

**Saved files contain:**
- YAML frontmatter with metadata
- Full job description in markdown
- All relevant job details

## Error Handling

**If scraper returns 0 jobs:**
- Page might use heavy JavaScript (Playwright should handle this)
- Page might require authentication
- Careers page might be empty (no current openings)
- URL might be incorrect

**Troubleshooting:**
1. Verify the URL is correct
2. Check if page loads in a browser manually
3. Look for "no openings" message on the page
4. Try re-running with `--force` flag

**If scraper fails:**
- Check if Playwright browsers are installed
- Verify network connectivity
- Check error message for specific issue

## Best Practices

1. **Always use --fetch-descriptions** - Full descriptions are needed for matching
2. **Run regularly** - Jobs change frequently, re-fetch weekly
3. **Check the output folder** - Verify files were created correctly
4. **Update companies.yaml** - Update `last_searched` date in `configs/companies.yaml` after successful fetch

## Example Interactions

### Example 1: Fetch Aktek Jobs

**User:** "Get all jobs from Aktek"

**Steps:**
1. Find URL using `jobquest-find-careers-url` → `https://www.aktek.io/careers`
2. Run: `uv run python -m src.fetch_jobs "https://www.aktek.io/careers" --company "Aktek" --fetch-descriptions`
3. Output: "Found 5 jobs at Aktek, saved to job_applications/aktek/references/2025-10-22/"

### Example 2: User Provides URL

**User:** "Scrape https://jobs.lever.co/wintermute-trading"

**Steps:**
1. Run: `uv run python -m src.fetch_jobs "https://jobs.lever.co/wintermute-trading" --company "Wintermute" --fetch-descriptions`
2. Output: "Found 12 jobs at Wintermute (Lever platform)"

---

**Next Steps:** After fetching jobs, Claude typically invokes:
- `jobquest-analyze-profile` to understand user's background
- `jobquest-match-jobs` to rank jobs by relevance
