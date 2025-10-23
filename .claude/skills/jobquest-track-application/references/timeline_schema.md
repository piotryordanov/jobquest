# Timeline.yaml Schema Reference

This document defines the complete schema for the `timeline.yaml` file used to track job applications.

## File Structure

```yaml
stakeholders:
  - # List of people involved in the application process

interactions:
  - # Chronological list of all interactions

status:
  # Current application status tracking
```

## Stakeholders Section

List of all people involved in the application process.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Full name of the person |
| `role` | string | Yes | Their role (e.g., "Recruiter", "Hiring Manager", "CTO") |
| `email` | string | No | Email address |
| `linkedin` | string | No | LinkedIn profile URL |
| `notes` | string | No | Any relevant context about this person |

### Example

```yaml
stakeholders:
  - name: "John Doe"
    role: "Recruiter"
    email: "john@company.com"
    linkedin: "https://linkedin.com/in/johndoe"
    notes: "Primary recruiter, very responsive"

  - name: "Jane Smith"
    role: "Hiring Manager - AI Products"
    email: "jane@company.com"
    notes: "Technical background, worked at Google previously"
```

## Interactions Section

Chronological list of all interactions with the company during the application process.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `date` | string | Yes | ISO format: `YYYY-MM-DDTHH:MM:SS` or `YYYY-MM-DD` |
| `stakeholder` | string | Yes | Name of person from stakeholders list |
| `type` | string | Yes | See "Interaction Types" below |
| `subject` | string | No | Email subject or meeting title |
| `duration` | string | No | For calls/interviews: "45 min", "1 hour", etc. |
| `summary` | string | Yes | Brief description of what happened (use multi-line `\|`) |
| `resume_sent` | string | No | Filename of resume PDF if sent |
| `attachments` | array | No | List of paths to files in communications/ |
| `notes` | string | No | Follow-up actions, important details |

### Interaction Types

Use these standardized types:

- `application_submitted` - Initial job application
- `email_sent` - You sent an email
- `email_received` - You received an email
- `message` - LinkedIn/Slack/other messaging platform
- `call` - Phone call
- `interview` - Formal interview (phone, video, or in-person)
- `offer` - Job offer received
- `rejection` - Application rejected
- `follow_up` - Follow-up communication

### Example

```yaml
interactions:
  - date: "2025-10-21T10:30:00"
    stakeholder: "John Doe"
    type: "email_sent"
    subject: "Application for Product Manager - AI"
    summary: |
      Sent initial application with tailored resume and cover letter.
      Emphasized AI/ML experience at OTS Capital and TradeBrix platform work.
      Highlighted experience leading technical teams and shipping ML products.
    resume_sent: "Piotr Yordanov - Keyrock PM.pdf"
    attachments:
      - "communications/2025-10-21_initial-application.txt"
    notes: "Waiting for response. Follow up in 1 week if no reply."

  - date: "2025-10-23T16:00:00"
    stakeholder: "Jane Smith"
    type: "interview"
    subject: "First Round Technical Discussion"
    duration: "45 min"
    summary: |
      Technical interview with hiring manager. Discussed:
      - TradeBrix architecture and scaling challenges
      - Agentic AI implementation at OTS Capital
      - Product management approach for ML features
      - Team leadership philosophy

      Jane was particularly interested in how we scaled the trading platform
      from prototype to production. Positive signals throughout the conversation.
    attachments:
      - "communications/2025-10-23_interview-jane-smith-notes.md"
    notes: "Follow up on ML infrastructure questions she asked. Next step: meet with CTO."
```

## Status Section

Tracks the current state of the application.

### Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `current_stage` | string | No | Current stage in process (see "Application Stages" below) |
| `last_updated` | string | No | Date of last update (ISO format) |
| `next_action` | string | No | What needs to happen next |
| `deadline` | string | No | Any deadline for response or decision (ISO format) |

### Application Stages

Common stages (customize as needed):

- `researching` - Researching the company/role
- `preparing` - Preparing application materials
- `applied` - Application submitted
- `screening` - Initial screening/phone screen
- `interview_1` - First round interview
- `interview_2` - Second round interview
- `interview_final` - Final round interview
- `offer` - Offer received
- `accepted` - Offer accepted
- `rejected` - Application rejected
- `withdrawn` - Application withdrawn

### Example

```yaml
status:
  current_stage: "interview_1"
  last_updated: "2025-10-23"
  next_action: "Wait for Jane to schedule CTO interview"
  deadline: "2025-10-30"
```

## Complete Example

```yaml
# Timeline for Company - Job Role Application

stakeholders:
  - name: "John Doe"
    role: "Recruiter"
    email: "john@company.com"
    linkedin: "https://linkedin.com/in/johndoe"

  - name: "Jane Smith"
    role: "Hiring Manager - AI Products"
    email: "jane@company.com"

interactions:
  - date: "2025-10-21T10:30:00"
    stakeholder: "John Doe"
    type: "email_sent"
    subject: "Application for Product Manager - AI"
    summary: |
      Sent initial application with tailored resume and cover letter.
      Emphasized AI/ML experience and technical leadership.
    resume_sent: "Piotr Yordanov - Company PM.pdf"
    attachments:
      - "communications/2025-10-21_initial-application.txt"
    notes: "Waiting for response"

  - date: "2025-10-22T14:15:00"
    stakeholder: "John Doe"
    type: "email_received"
    subject: "Re: Application for Product Manager - AI"
    summary: |
      Recruiter responded positively. Requested availability for
      first round interview with hiring manager.
    attachments:
      - "communications/2025-10-22_recruiter-response.txt"

  - date: "2025-10-23T16:00:00"
    stakeholder: "Jane Smith"
    type: "interview"
    subject: "First Round Technical Discussion"
    duration: "45 min"
    summary: |
      Technical interview with hiring manager. Discussed past projects,
      technical approach, and team leadership. Very positive conversation.
    attachments:
      - "communications/2025-10-23_interview-notes.md"
    notes: "Next step: meet with CTO"

status:
  current_stage: "interview_1"
  last_updated: "2025-10-23"
  next_action: "Wait for scheduling of CTO interview"
  deadline: "2025-10-30"
```

## Best Practices

1. **Keep summaries concise but informative** - Capture key points without excessive detail
2. **Maintain chronological order** - Always add new interactions in date order
3. **Use consistent formatting** - Follow the multi-line `|` format for summaries
4. **Update status regularly** - Keep the status section current after each interaction
5. **Save communication artifacts** - Store emails, transcripts, and notes in communications/
6. **Track resume versions** - Always note which PDF was sent in each interaction
7. **Add stakeholders proactively** - Create stakeholder entries as soon as you interact with new people
