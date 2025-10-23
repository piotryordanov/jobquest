---
name: jobquest-find-careers-url
description: Use this skill when you need to find a company's careers page URL. Searches the web using Playwright, checks known references first, and saves discovered URLs to companies.yaml. Always use this before trying to scrape jobs from a company.
---

# Find Company Careers URL

## When to Use This Skill

Activate this skill when:
- User asks to "find jobs at [Company]"
- User wants to know "[Company]'s careers page"
- You need a careers URL before scraping jobs
- User provides a company name but no URL

## Workflow

### Step 1: Check Known References First

Before searching, check if we already know this company's URL:

```bash
grep -i "name: \"Company Name\"" configs/companies.yaml
```

**If found:**
- Extract the `careers_url` from the YAML
- Update `last_searched` to today's date
- Return the URL and skip to end

**If not found:**
- Proceed to Step 2

### Step 2: Use Playwright to Discover Careers Page

**IMPORTANT:** Use the shared Playwright tools - never use WebSearch or WebFetch for finding careers pages.

Run the Playwright-based discovery script:

```bash
cd .claude/skills/jobquest-shared-tools
uv run python -m src.find_careers_page "Company Name"
```

**What this does:**
- Uses Playwright to search Google for "Company Name careers"
- Navigates through search results with JavaScript support
- Identifies the careers page URL
- Returns the URL

**Example:**
```bash
uv run python -m src.find_careers_page "Aktek"
# Output: https://www.aktek.io/careers
```

### Step 3: Save to References

After discovering the URL, append it to `configs/companies.yaml`:

```yaml
  - name: "Company Name"
    careers_url: "<discovered URL>"
    added_date: "2025-10-22"
    last_searched: "2025-10-22"
    platform: "generic"  # or "lever", "greenhouse", "ashby" if detected
    notes: "Optional description about the company"
```

**Platform detection:**
- If URL contains `jobs.lever.co` → platform: "lever"
- If URL contains `boards.greenhouse.io` → platform: "greenhouse"
- If URL contains `jobs.ashbyhq.com` → platform: "ashby"
- Otherwise → platform: "generic"

### Step 4: Return the URL

Output to user:
```
Found careers page for Company Name: <URL>
Platform: <platform>
Saved to references.
```

## Best Practices

1. **Always check references first** - Saves time and API calls
2. **Use Playwright, not WebFetch** - Many careers pages use JavaScript rendering
3. **Update last_searched** - Even if URL was already known
4. **Save immediately** - Don't wait to save discovered URLs
5. **Include platform type** - Helps downstream skills scrape efficiently

## Error Handling

**If search fails:**
- Try alternative company names (e.g., "Aktek.io" vs "Aktek")
- Ask user for the correct company name or URL
- Check if company has a careers page at all

**If URL is found but invalid:**
- Verify URL is accessible
- Check if it redirects to a different domain
- Update companies.yaml with the final URL after redirects

## Example Interaction

**User:** "Find jobs at Lombard"

**Steps:**
1. Check `configs/companies.yaml` → Not found
2. Run: `uv run python -m src.find_careers_page "Lombard"`
3. Receives: `https://lombardfinance.com/careers`
4. Detect platform: `generic`
5. Save to `configs/companies.yaml`
6. Output: "Found careers page for Lombard: https://lombardfinance.com/careers (generic platform)"

---

**Next Steps:** After finding the URL, Claude will typically invoke `jobquest-fetch-jobs` to scrape the actual job listings.
