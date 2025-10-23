# Job Application Folder Structure

This folder tracks the complete application process for: **{Company} - {Job Role}**

## Folder Contents

### Core Files

- **timeline.yaml** - Main tracking file for all stakeholders and interactions
- **job-description.md** - Job posting details with metadata (URL, access date)
- **{Resume PDF}.pdf** - Resume version(s) sent to this company

### Folders

- **resume/** - Source files for resume (LaTeX, Word, etc.)
  - Contains the editable source files used to generate the PDF
  - May include LaTeX .tex files, justfile for building, etc.

- **cover-letter/** - Cover letter materials
  - `cover-letter.md` - The cover letter content
  - May include multiple versions or drafts

- **communications/** - All communication artifacts
  - Emails (`.eml` or `.txt`)
  - Interview transcripts (`.md`)
  - Messages from LinkedIn/Slack (`.txt`)
  - Screenshots (`.png`)
  - Follow naming convention: `YYYY-MM-DD_description.ext`

## How to Use

1. **Start**: Copy this template when beginning a new job application
2. **Track**: Update `timeline.yaml` after each interaction
3. **Store**: Save all communications in `communications/` folder
4. **Build**: Use `resume/` folder to maintain tailored resume source
5. **Version**: Keep each sent PDF in the root with clear filename

## File Naming Conventions

- Resume PDFs: `Your Name - Company Role.pdf`
- Communications: `YYYY-MM-DD_description.ext`
- Use descriptive names that make files easily identifiable

## Maintenance

Keep this folder updated throughout the application process:
- Add timeline entries immediately after interactions
- Save communications as they happen
- Update status in timeline.yaml after significant events
- Archive the complete folder once process concludes (hired, rejected, or withdrawn)
