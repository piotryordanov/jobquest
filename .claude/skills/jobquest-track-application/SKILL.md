---
name: jobquest-track-application
description: This skill should be used when the user provides updates about job applications, such as sending resumes, receiving emails from recruiters, scheduling interviews, or any interaction with stakeholders during a job search. It also handles researching company job boards to find relevant positions and creating new application tracking structures. It manages timeline.yaml files that record stakeholders, interactions, and resume versions sent.
---

# Job Application Tracker

## Overview

This skill enables systematic tracking of job applications by managing timeline.yaml files that record all stakeholders and interactions throughout the application process. Use this skill when the user mentions job application activities like sending resumes, talking to recruiters, scheduling interviews, or any communication with potential employers.

## When to Use This Skill

Activate this skill when the user:
- Asks to research job openings at a specific company
- Mentions sending a resume or application to a company
- Reports receiving communication from a recruiter or hiring manager
- Describes an interview, call, or meeting with a company representative
- Wants to update or review their job application status
- References specific job applications by company name or role
- Asks about tracking application interactions or timeline
- Wants to create a new job application tracking folder

## Job Application Structure

Job applications follow this directory structure:

```
job_applications/{company}/{job-role}/
├── timeline.yaml              # Main tracking file (REQUIRED)
├── job-description.md        # Job posting with metadata (URL, access date)
├── {Resume PDF filename}.pdf  # Resume version(s) sent
├── resume/                   # Source files for resume (LaTeX, Word, etc.)
├── cover-letter/             # Cover letter materials
│   └── cover-letter.md
└── communications/           # Emails, transcripts, messages
    └── README.md
```

## Researching Company Jobs (New Application)

When the user asks to research jobs at a specific company:

### Step 1: Find the Company Careers Page

1. Use WebSearch or the provided URL to locate the company's careers/jobs page
2. Extract the URL to their job board or applicant tracking system
3. Use WebFetch to retrieve job listings from the page

### Step 2: Extract and Filter Job Listings

1. Extract all job postings with: title, location, job URL, brief description
2. Filter by location preferences:
   - Read `configs/preferences.yaml` for allowed locations
   - Default to: Remote, Dubai (if preferences file doesn't exist)
   - Keep only jobs matching location criteria

### Step 3: Match Jobs to User Profile

1. Read the `bio/` folder to understand the user's background:
   - `bio/introduction.mdx` - Overview of experience
   - `bio/leadership/` - Leadership capabilities
   - Project-specific folders - Technical skills and domains

2. For each filtered job:
   - Compare job requirements/description with user's achievements
   - Score relevance (high/medium/low match)
   - Note specific achievement alignments

3. Present ranked list of relevant jobs with:
   - Job title and link
   - Location
   - Relevance score and reasoning
   - Which achievements/skills align

### Step 4: Create Job Description File

When user selects a job to apply for:

1. Use the `assets/job-application-template/` to create new application folder
2. Fetch full job description and save to `job-description.md` with frontmatter:
   ```yaml
   ---
   job_url: "{actual URL}"
   accessed_date: "{YYYY-MM-DD}"
   company: "{Company Name}"
   role: "{Job Title}"
   location: "{Location}"
   employment_type: "{Full-time/Contract/etc}"
   ---
   ```

3. Create the complete folder structure from template
4. Initialize `timeline.yaml` with empty stakeholders and interactions

## Tracking Existing Applications

### Step 1: Locate the Job Application

When the user mentions a job application:

1. Identify the company and job role from the user's message
2. Search for the corresponding application directory at `job_applications/{company}/{job-role}/`
3. If the directory doesn't exist, ask the user if they want to create a new application tracking structure
4. Read the existing `timeline.yaml` file to understand the current state

### Step 2: Parse the User's Update

Extract key information from the user's message:

- **Date/time** of the interaction (ask if not provided, or use current date/time)
- **Stakeholder** involved (recruiter name, hiring manager, etc.)
- **Type of interaction**: email_sent, email_received, call, interview, message, application_submitted
- **Subject/topic** of the interaction
- **Summary** of what happened
- **Resume sent** (if applicable - which PDF file)
- **Duration** (for calls/interviews)
- **Next steps** or follow-up actions

### Step 3: Update timeline.yaml

Read the `references/timeline_schema.md` file for the complete YAML schema structure.

To update the timeline:

1. Read the existing `timeline.yaml` file
2. Add new stakeholder to the `stakeholders` list if not already present
3. Append the new interaction to the `interactions` list in chronological order
4. Update the `status` section if applicable (current_stage, last_updated, next_action, deadline)
5. Use the Edit tool to add the new content

**Important formatting rules:**
- Use ISO date format: `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD`
- Keep interactions chronologically ordered
- Use multi-line YAML format (`|`) for summaries
- Reference communication files as relative paths: `communications/YYYY-MM-DD_description.ext`

### Step 4: Manage Communication Artifacts

If the user provides or mentions emails, transcripts, or messages:

1. Offer to save the content to the `communications/` directory
2. Use the naming convention: `YYYY-MM-DD_description.ext`
   - Emails: `.eml` or `.txt`
   - Transcripts: `.md`
   - Messages: `.txt`
   - Screenshots: `.png`
3. Reference the file in the interaction's `attachments` field

### Step 5: Confirm and Summarize

After updating:
1. Confirm what was added to the timeline
2. Summarize the current application status
3. Mention any next actions or follow-ups from the timeline

## Example Interactions

**Example 1: Initial Application**
```
User: "I just applied to Keyrock for the Product Manager role, sent my resume to john@keyrock.com"

Actions:
1. Locate job_applications/keyrock/product-manager/timeline.yaml
2. Add stakeholder "John" if not present
3. Add interaction with type: "application_submitted"
4. Note which resume PDF was sent
5. Confirm update
```

**Example 2: Interview Update**
```
User: "I had an interview with Jane Smith today, she's the hiring manager. It went well, we talked about my AI work for 45 minutes."

Actions:
1. Locate the relevant timeline.yaml
2. Add Jane Smith as stakeholder (role: Hiring Manager)
3. Add interaction with:
   - type: "interview"
   - duration: "45 min"
   - summary: summarize the user's description
4. Ask if user wants to save detailed notes to communications/
```

**Example 3: Status Check**
```
User: "What's the status of my Keyrock application?"

Actions:
1. Read job_applications/keyrock/*/timeline.yaml
2. Summarize:
   - Current stage from status section
   - Last interaction date and type
   - All stakeholders involved
   - Next action or deadline if any
```

## Resources

### references/timeline_schema.md
Complete YAML schema documentation for timeline.yaml structure, including all fields, types, and examples. Read this file when creating or updating timeline files.

### assets/timeline_template.yaml
A clean template for initializing new job application timelines. Use when creating tracking for a new application.

## Best Practices

1. **Always confirm ambiguous information** - If dates, names, or details are unclear, ask the user
2. **Be concise but complete** - Summaries should capture key points without excessive detail
3. **Preserve chronological order** - Always maintain timeline order by date
4. **Reference communication files** - When users provide emails or transcripts, save them and reference in timeline
5. **Track resume versions** - Note which PDF file was sent in each interaction
6. **Update status fields** - Keep the status section current with each significant update
