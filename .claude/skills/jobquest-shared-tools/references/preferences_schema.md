# Job Search Preferences Schema

Location: `configs/preferences.yaml`

This file configures user preferences for job research and filtering.

## Schema

```yaml
# Required: List of preferred job locations
locations:
  - "Remote"
  - "Dubai"
  - "City Name"

# Optional: Preferred employment types
employment_types:
  - "Full-time"
  - "Contract"
  - "Part-time"

# Optional: Minimum salary requirements
min_salary: 150000
currency: "USD"

# Optional: Keywords to prioritize in job matching
prioritize_keywords:
  - "AI"
  - "Machine Learning"
  - "Leadership"

# Optional: Keywords to avoid
avoid_keywords:
  - "Junior"
  - "Intern"
```

## Usage in Job Research

When researching company job boards:

1. **Location Filtering**: Only jobs matching locations in the `locations` list are considered
   - Matching is case-insensitive
   - Supports: "Remote", specific cities, regions
   - If preferences file doesn't exist, default to: ["Remote", "Dubai"]

2. **Employment Type**: If specified, filter by employment type

3. **Keyword Matching**: Use prioritize/avoid keywords to adjust relevance scoring

## Default Behavior

If `preferences.yaml` doesn't exist:
- Locations: ["Remote", "Dubai"]
- Employment types: All types accepted
- No keyword filtering
