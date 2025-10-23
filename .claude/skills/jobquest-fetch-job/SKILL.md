---
name: jobquest-fetch-job
description: This skill should be used when the user provides a specific job posting URL or asks to look up details for a particular job opening. It fetches job descriptions, extracts key information, and creates properly formatted job-description.md files with metadata.
---

# Job Finder

## Overview

This skill fetches and formats job postings into standardized job-description.md files with YAML frontmatter metadata. Use this when the user provides a job URL or asks you to look up a specific job opening.

## When to Use This Skill

Activate this skill when the user:
- Provides a job posting URL and asks you to save/format it
- Says "look up this job: [URL]"
- Asks to create a job description file for a specific opening
- Wants to extract job details from a careers page

## Workflow

### Step 1: Obtain the Job URL

If user provides URL directly, use it. Otherwise:
1. Use WebSearch to find the company's careers page
2. Navigate to the specific job posting
3. Extract the direct link to the job

### Step 2: Fetch Job Details

Use WebFetch to retrieve the job posting and extract:
- **Job title/role**
- **Company name**
- **Location** (Remote, city, hybrid, etc.)
- **Employment type** (Full-time, Contract, Part-time, etc.)
- **Job description** (responsibilities, requirements, benefits, etc.)
- **Application process** (if mentioned)
- **Salary range** (if provided)

### Step 3: Create Job Description File

Format the content as a markdown file with YAML frontmatter:

```yaml
---
job_url: "{full URL to job posting}"
accessed_date: "{YYYY-MM-DD}"
company: "{Company Name}"
role: "{Job Title}"
location: "{Location}"
employment_type: "{Full-time|Contract|Part-time|etc}"
---

# {Job Title} - {Company Name}

{Formatted job description content}
```

### Step 4: Determine File Location

Ask the user where to save the file:
- **Option A**: Create new application folder: `job_applications/{company}/{job-role}/job-description.md`
- **Option B**: Save to specified path
- **Option C**: Current directory

Use the job role (kebab-case, lowercase) as the filename or folder name.

### Step 5: Create File

1. Write the formatted job-description.md file
2. Confirm the file path to the user
3. Show a brief summary of the job (title, company, location)

## Formatting Guidelines

### Job Title Normalization
- Remove company name from title if redundant
- Keep role level (Senior, Lead, Principal, etc.)
- Example: "Senior Product Manager - AI" not "Keyrock Senior Product Manager - AI"

### Content Structure

Use clear sections:
- **About the Organization** - Company background
- **Core Responsibilities** - Main duties
- **Essential Qualifications** - Required skills/experience
- **Beneficial Background** - Nice-to-have qualifications
- **Application Process** - Interview stages if mentioned
- **Compensation & Benefits** - If provided

### Location Formatting
- Be specific: "Remote (US only)", "Hybrid - London", "Dubai"
- If multiple locations: list them or note "Multiple locations"

## Best Practices

1. **Preserve original content** - Don't summarize or paraphrase the job description
2. **Clean formatting** - Remove excessive whitespace, fix markdown formatting
3. **Extract metadata accurately** - Ensure YAML frontmatter is complete
4. **Use today's date** - For `accessed_date` field
5. **Verify URL** - Make sure the job_url is the direct link to the posting

## Example

**User input:** "Can you save this job: https://jobs.company.com/posting/123"

**Actions:**
1. Fetch job details from URL
2. Extract: "Senior ML Engineer - Applied AI", Company: "Acme Corp", Location: "Remote", Type: "Full-time"
3. Create: `job_applications/acme-corp/senior-ml-engineer-applied-ai/job-description.md`
4. Confirm: "✅ Created job description for Senior ML Engineer - Applied AI at Acme Corp"
