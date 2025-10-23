# JobQuest - Claude Code Job Search Plugin

**Complete job search automation toolkit for Claude Code**

Automate your entire job search workflow with AI-powered skills that find jobs, match them to your profile, build tailored resumes, and track applications.

## Features

### 🔍 Job Discovery
- **Find Careers Pages**: Automatically discover company careers URLs using Playwright
- **Scrape Job Listings**: Extract all jobs from any careers page (Lever, Greenhouse, Ashby, custom)
- **Fetch Single Jobs**: Pull specific job postings with full descriptions

### 🎯 Intelligent Matching
- **Profile Analysis**: Extract your skills, experience, and achievements from bio folder
- **Job Matching**: Score and rank jobs based on skills, domain, level, and interest alignment
- **Smart Filtering**: Filter by location, employment type, and keywords

### 📄 Resume Building
- **Tailored Resumes**: Generate LaTeX resumes customized for each position
- **Cover Letters**: Create personalized cover letters with strategic recommendations
- **Two-Stage Approval**: Review and approve content before generation

### 📊 Application Tracking
- **Timeline Management**: Track stakeholders, interactions, and communications
- **Interview Prep**: Analyze job descriptions and prepare targeted talking points
- **Status Updates**: Monitor application progress across companies

## Installation

### Quick Install

```bash
# Add the marketplace
/plugin marketplace add piotryordanov/jobquest

# Install the plugin
/plugin install jobquest@jobquest-marketplace
```

### Manual Install

```bash
# Clone the repository
git clone https://github.com/piotryordanov/jobquest.git

# Add as local marketplace
/plugin marketplace add ./jobquest

# Install
/plugin install jobquest
```

## Quick Start

### 1. Initialize Configuration (Automatic or Manual)

**Option A: Automatic Setup (Recommended)**

Just start using JobQuest! The first time you search for jobs, Claude will automatically ask for your preferences and create the config files:

```bash
"Find jobs at Aktek"

# Claude will automatically:
# 1. Ask where you're looking for jobs (Remote? Specific cities?)
# 2. Ask what employment types you want (Full-time? Contract?)
# 3. Create all config files with your preferences
# 4. Then proceed to find jobs
```

**Option B: Manual Setup**

Run the setup script:

```bash
cd your-project
./setup.sh
```

Or copy the example configs:

```bash
cp configs/preferences.example.yaml configs/preferences.yaml
cp configs/companies.example.yaml configs/companies.yaml
cp configs/job_boards.example.yaml configs/job_boards.yaml

# Edit preferences.yaml with your locations and preferences
```

**What gets created:**

- `configs/preferences.yaml` - Your job search preferences (locations, employment types)
- `configs/companies.yaml` - Tracked companies (auto-populated as you search)
- `configs/job_boards.yaml` - Job boards you use (pre-filled with popular boards)

### 2. Create Your Bio (Optional but Recommended)

Create achievement pages in the `bio/` folder to power intelligent job matching:

```
bio/
├── introduction.mdx          # Your professional summary
├── leadership/              # Leadership achievements
├── engineering/             # Technical projects
└── [company]/              # Company-specific work
```

**Note:** The bio folder is optional but enables intelligent job matching. Without it, JobQuest will still find and scrape jobs, but won't be able to score them based on your background.

### 3. Start Your Job Search (That's It!)

```bash
# Find jobs at a company
"Find all remote jobs at Aktek"

# Claude will automatically:
# 1. Use jobquest-find-careers-url to find their careers page
# 2. Use jobquest-fetch-jobs to scrape all listings
# 3. Use jobquest-analyze-profile to understand your background
# 4. Use jobquest-match-jobs to rank jobs by relevance

# Build a tailored resume
"Create a resume for the Aktek Senior Full Stack role"

# Create a cover letter
"Write a cover letter for this position"

# Track your application
"I sent my resume to Aktek today for the Senior Full Stack role"
```

## Skills Included

### Core Skills

| Skill | Description | Trigger |
|-------|-------------|---------|
| `jobquest-find-careers-url` | Discovers company careers pages | "Find jobs at [Company]" |
| `jobquest-fetch-jobs` | Scrapes job listings with Playwright | "Get all jobs from [URL]" |
| `jobquest-analyze-profile` | Analyzes your bio for matching | Auto-invoked before matching |
| `jobquest-match-jobs` | Ranks jobs by relevance | "Which jobs are relevant to me?" |
| `jobquest-build-resume` | Creates tailored LaTeX resumes | "Create a resume for [job]" |
| `jobquest-build-cover-letter` | Generates cover letters | "Write a cover letter for [job]" |
| `jobquest-fetch-job` | Fetches single job posting | "Look up this job: [URL]" |
| `jobquest-track-application` | Manages application timeline | "I sent my resume to [company]" |
| `jobquest-prep-interview` | Prepares interview talking points | "Help me prep for [company] interview" |

### Shared Tools

The plugin includes a Python package (`jobquest-shared-tools`) with Playwright-based scrapers for various ATS platforms.

## File Structure

After installation and use, your project will look like:

```
your-project/
├── configs/                     # Configuration files
│   ├── preferences.yaml        # Job search preferences
│   ├── companies.yaml          # Known careers URLs
│   └── job_boards.yaml         # Job board tracking
│
├── bio/                        # Your achievements/portfolio
│   ├── introduction.mdx
│   ├── leadership/
│   └── engineering/
│
├── job_applications/           # Application tracking
│   ├── company-name/
│   │   └── job-role/
│   │       ├── timeline.yaml           # Application timeline
│   │       ├── job-description.md      # Job posting
│   │       ├── resume/                 # LaTeX source
│   │       │   ├── resume.tex
│   │       │   ├── executive_summary.tex
│   │       │   └── experiences/
│   │       ├── cover-letter/
│   │       │   └── cover-letter.md
│   │       └── communications/         # Emails, messages
│
└── tex/                        # Global resume templates
    ├── partials/               # Shared LaTeX partials
    └── experiences/            # Reusable experience blocks
```

## Requirements

- **Python**: 3.12+
- **uv**: Python package manager (auto-installed if missing)
- **Playwright**: Browsers auto-installed on first use
- **LaTeX**: For PDF generation (tectonic or texlive)

## Configuration

### Python Dependencies

The plugin uses `uv` for dependency management. Dependencies are automatically installed when needed.

### Playwright Setup

On first use, Playwright will install required browsers:

```bash
cd .claude/skills/jobquest-shared-tools
uv run playwright install
```

## How It Works

### Job Discovery Workflow

1. **User**: "Find jobs at Wintermute"
2. **jobquest-find-careers-url**: Searches for careers page, saves to `configs/companies.yaml`
3. **jobquest-fetch-jobs**: Scrapes all listings, saves to `job_applications/wintermute/references/[date]/`
4. **jobquest-analyze-profile**: Reads `bio/` folder, creates profile summary
5. **jobquest-match-jobs**: Scores jobs, filters by location from `configs/preferences.yaml`, ranks by relevance
6. **Output**: Ranked list of jobs with match scores and reasoning

### Resume Building Workflow

1. **User**: "Create a resume for the Aktek MERN role"
2. **jobquest-build-resume**: Reads job description, analyzes bio
3. **Recommendation**: Presents strategy with key themes and experiences to include
4. **User Approval**: User reviews and approves
5. **Generation**: Creates LaTeX files, builds PDF
6. **Output**: `job_applications/aktek/senior-full-stack-engineer-mern/[Name] - Aktek MERN.pdf`

## Advanced Usage

### Custom Scraping

The shared tools support custom ATS platforms. Extend `src/scrapers.py` to add new platforms.

### Resume Templates

Customize LaTeX templates in `tex/partials/` to match your design preferences.

### Batch Operations

Process multiple companies at once:

```bash
"Find jobs at these companies: Wintermute, Aktek, Keyrock"
```

## Troubleshooting

### Playwright Issues

```bash
# Reinstall browsers
cd .claude/skills/jobquest-shared-tools
uv run playwright install --force
```

### Missing Dependencies

```bash
# Reinstall Python dependencies
cd .claude/skills/jobquest-shared-tools
uv sync --reinstall
```

### LaTeX Build Errors

Ensure you have tectonic or texlive installed:

```bash
# Install tectonic (recommended)
brew install tectonic  # macOS
# or
cargo install tectonic
```

## Examples

### Complete Job Search Flow

```bash
# 1. Find and match jobs
"Find all remote jobs at Aktek and tell me which are relevant"

# 2. Build resume
"Create a resume for the Senior Full Stack Engineer role at Aktek"

# 3. Write cover letter
"Write a cover letter for this position"

# 4. Track application
"I submitted my application to Aktek for the Senior Full Stack role today"

# 5. Prep for interview
"I have an interview with Aktek next week. Help me prepare."
```

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add/update skills in `.claude/skills/`
4. Update documentation
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

- **Issues**: [GitHub Issues](https://github.com/piotryordanov/jobquest/issues)
- **Docs**: [Full Documentation](https://github.com/piotryordanov/jobquest/docs)

## Acknowledgments

Built with:
- [Claude Code](https://docs.claude.com/claude-code) - AI-powered CLI
- [Playwright](https://playwright.dev/) - Web scraping automation
- [uv](https://github.com/astral-sh/uv) - Python package management

---

**Happy job hunting! 🎯**
