# Companies Reference System

## Overview

The `companies.yaml` file stores known careers page URLs for companies you've researched. This prevents re-discovering the same URLs repeatedly and speeds up job searches.

## Workflow

### When searching for jobs:

1. **Check configs first**
   ```bash
   grep -A 5 'name: "Company Name"' configs/companies.yaml
   ```

2. **If found:** Use the stored `careers_url` directly

3. **If not found:**
   - Run `find_careers_page.py` to discover URL
   - Append company to `companies.yaml`

4. **Always update:** Set `last_searched` to today's date

## File Format

```yaml
companies:
  - name: "Company Name"
    careers_url: "https://jobs.lever.co/company-name"
    added_date: "2025-10-22"        # When first discovered
    last_searched: "2025-10-22"     # Last time we searched this company
    platform: "lever"                # ATS platform type
    notes: "Optional notes"          # Any additional context
```

## Platform Types

- `lever` - jobs.lever.co
- `greenhouse` - boards.greenhouse.io
- `ashby` - jobs.ashbyhq.com
- `generic` - Custom/unknown ATS

## Benefits

1. **Faster searches** - No need to re-discover URLs
2. **Tracking** - Know when you last searched each company
3. **Reference** - Build your list of target companies
4. **Reusability** - Share reference file across devices

## Maintenance

- **Add manually:** You can add companies before searching them
- **Update URLs:** If a company changes their careers page, update the URL
- **Archive:** Comment out (`#`) companies you're no longer interested in
- **Clean up:** Periodically review and remove old/irrelevant companies
