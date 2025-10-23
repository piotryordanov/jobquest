---
name: jobquest-build-resume
description: This skill should be used when the user asks to create or tailor a resume for a specific job application. It analyzes job requirements, recommends relevant bio experiences to include, gets user approval, then generates LaTeX resume files in the job application folder.
---

# Resume Builder

## Overview

This skill creates tailored resumes by analyzing job descriptions against the user's bio folder, recommending the most relevant content, and generating LaTeX resume files. It uses a **two-stage approach**: first recommend what to include and get approval (if needed), then generate the files.

**Configuration**: Resume generation settings are controlled by `.resume.config.yaml` in the project root. This file defines:
- Page limits and content constraints
- Required sections that must always be included
- Static section file paths
- Custom instructions per section
- Build settings and compiler options
- Approval workflow rules

Always read `.resume.config.yaml` first to understand project-specific requirements.

## When to Use This Skill

Activate this skill when the user:
- Says "create a resume for [job/company]"
- Asks to "tailor my resume for [role]"
- Requests "build a resume for this application"
- Wants to "generate resume for [company] [role]"
- References a specific job application and asks for resume help

## Core Principles

### Configuration-Driven Generation
**ALWAYS read `.resume.config.yaml` first** to understand:
- Page limits (default: 1 page strict)
- Required sections that must be included
- Maximum bullets per section
- Static section file paths
- Custom section instructions
- Build settings

### Resume Length Requirement
Check `constraints.max_pages` in `.resume.config.yaml` (typically 1 page). Condense content aggressively to fit.

### Static Sections (From Config)
Read `required_sections` from `.resume.config.yaml`. These sections MUST be included and never removed:
- Typically: **Education**, **Publications**, **Languages**, **Skills**
- File paths defined in `static_sections` config

**IMPORTANT**: Never remove required sections to save space. Instead, condense the Professional Experience section.

### Dynamic Sections (Tailored Per Job)
- **Executive Summary** - Concise sentences targeting the specific role (check `constraints.executive_summary_sentences`)
- **Professional Experience** - Selected experiences condensed (check `constraints.max_experience_bullets`)

### Section-Specific Instructions
Read `section_instructions` from `.resume.config.yaml` for custom guidelines per section (e.g., how to format education, what to emphasize in skills, bullet point style for experience).

## Two-Stage Workflow

### Stage 1: Recommendation & Approval

#### Step 0: Read Configuration

**FIRST, read the project configuration:**
```bash
.resume.config.yaml
```

Extract:
- `constraints.max_pages` - Page limit for resume
- `constraints.max_experience_bullets` - Maximum experience bullets
- `constraints.executive_summary_sentences` - Max summary sentences
- `required_sections` - Sections that must be included
- `static_sections` - File paths for static content
- `section_instructions` - Custom guidelines per section
- `approval.ask_approval_if` / `approval.skip_approval_if` - Approval workflow rules

Store these settings to use throughout the generation process.

#### Step 1: Locate Job Application

1. Identify company and role from user's message
2. Find the job application folder: `job_applications/{company}/{role}/`
3. Read `job-description.md` to understand requirements

#### Step 2: Analyze Job Requirements

Extract from job description:
- **Role type** (CTO, Product Manager, ML Engineer, Quant, etc.)
- **Key responsibilities**
- **Required skills** (technical and soft skills)
- **Experience level** (junior, senior, lead, executive)
- **Domain focus** (trading, AI/ML, fintech, product, leadership)
- **Emphasized qualities** (what they repeat or highlight)

#### Step 3: Analyze User's Achievements

Read the `bio/` folder:

**Always read:**
- `bio/introduction.mdx` - Overall CTO experience and team overview
- `bio/cto-leadership/overview.mdx` - Leadership capabilities
- `bio/leadership/*.mdx` - Leadership achievements

**Project-specific:**
- `bio/ots-capital/*.mdx` - Hedge fund/quant work
- `bio/tradebrix/*.mdx` - SaaS CRM platform
- Any other relevant project folders

**Extract:**
- Relevant experiences matching job requirements
- Specific metrics and accomplishments
- Technical skills demonstrated
- Leadership examples
- Domain expertise

#### Step 4: Create Recommendation

Present a structured recommendation to the user:

```markdown
## Resume Recommendation for {Company} - {Role}

### Executive Summary (Proposed)
[Draft 2-3 sentence summary targeting this specific role]

### Professional Experiences to Include

**Priority 1 (Must Include):**
1. **OTS Capital - CTO Leadership**
   - Why: [Explain relevance to job requirements]
   - Key bullets to emphasize:
     - [Specific bullet point from achievements]
     - [Another relevant achievement]

2. **Tradebrix - Product/Engineering**
   - Why: [Explain relevance]
   - Key bullets:
     - [Relevant accomplishment]

**Priority 2 (Recommended):**
3. [Another experience]
   - Why: [Explain relevance]

**Priority 3 (Optional - can include if space):**
4. [Experience that's less relevant but still valuable]

### Skills to Emphasize
Based on job requirements:
- [Skill from achievements that matches job]
- [Another matching skill]
- [Technical skill they need]

### Final Structure (1 Page - STRICT)
**All resumes will be condensed to fit on exactly 1 page:**
- Executive Summary: 2-3 concise sentences
- Professional Experience: 3-4 bullets (merged achievements)
- Skills, Publications, Education, Languages: Standard sections (always included)

**Questions (if any ambiguity):**
1. Do you want to include [specific experience]?
2. Should we emphasize [technical aspect] or [leadership aspect] more?
3. Any specific achievements from your work you want highlighted?

**Note**: If user says "create the resume please" or similar without questions, proceed directly to generation without asking for approval. Only ask approval if there are multiple valid approaches or unclear requirements.
```

#### Step 5: User Approval (OPTIONAL)

**Only request approval if:**
- There are multiple valid approaches (e.g., emphasize leadership vs technical)
- Job requirements are ambiguous
- User has not explicitly said to proceed

**Skip approval and proceed directly if:**
- User says "create the resume" or "build the resume"
- Requirements are clear and unambiguous
- There's an obvious best approach

### Stage 2: Generation

Once user approves the recommendation:

#### Step 6: Generate Executive Summary

Create concise 2-3 sentence executive summary in LaTeX format:
- First sentence: Core professional identity aligned with target role
- Second sentence: Key domain expertise and technical capabilities
- Third sentence (optional): Leadership scope or unique value proposition

**Examples:**

For PM role:
```
Product leader who drives AI/ML product strategy, builds technical roadmaps,
and ships scalable platforms at the intersection of finance and technology.
Led cross-functional teams delivering SaaS products serving 45K+ users with
99.9% uptime. Spearheads agentic AI initiatives to enhance product innovation
and operational efficiency.
```

For CTO role:
```
Executive technology leader who drives strategic tech decisions, builds
high-performing teams, and shapes product roadmaps aligned with business
objectives. Leads organizational design and performance management across
fintech and trading platforms. Spearheads agentic AI strategies to enhance
operational efficiency and product innovation.
```

#### Step 7: Generate Experience Files

For each approved experience, create a `.tex` file in the `resume/experiences/` folder.

**File naming:** `{company-slug}-{job-slug}.tex`

**Structure:**
```latex
\begin{twocolentry}{
    {Start Date} – {End Date}
  }
\textbf{Job Title}, Company Name — Location\end{twocolentry}

\begin{onecolentry}
  \begin{highlightsforbulletentries}
    \item \textbf{Action verb} key achievement with \textbf{metric} and impact
    \item Another achievement...
  \end{highlightsforbulletentries}
\end{onecolentry}
```

**Important formatting:**
- Bold key metrics and numbers
- Start bullets with strong action verbs (Led, Spearheaded, Architected, Delivered, etc.)
- Include quantifiable results where possible
- Keep bullets concise but impactful

**For multi-project companies** (like OTS Group with sub-projects):
```latex
% Main company header
\begin{twocolentry}{...}
\textbf{Chief Technology Officer}, OTS Capital Group — Dubai, UAE
\end{twocolentry}

% High-level bullets about the CTO role
\begin{onecolentry}
  \begin{highlightsforbulletentries}
    \item CTO-level achievements...
  \end{highlightsforbulletentries}
\end{onecolentry}

\vspace{0.15cm}

% Sub-project 1
\begin{onecolentry}
  \textit{\textbf{Project Name} — Company}
\end{onecolentry}

\begin{onecolentry}
  \begin{highlightsforbulletentries}
    \item Project-specific achievements...
  \end{highlightsforbulletentries}
\end{onecolentry}

% Repeat for other sub-projects
```

#### Step 8: Generate Main Resume File

Create `resume/resume.tex`:

```latex
\input{partials/includes.tex}

\begin{document}
\newcommand{\AND}{\unskip
  \cleaders\copy\ANDbox\hskip\wd\ANDbox
  \ignorespaces
}
\newsavebox\ANDbox
\sbox\ANDbox{$|$}

\input{partials/header.tex}

\section{Executive Summary}

\begin{onecolentry}
{Generated executive summary text}
\end{onecolentry}
\vspace{0.2 cm}

\section{Professional Experience}
\input{experiences/{experience-1}.tex}
\input{experiences/{experience-2}.tex}
% ... more experiences as approved

\input{partials/skills.tex}
\input{partials/publications.tex}
\input{partials/education.tex}
\input{partials/languages.tex}

\end{document}
```

#### Step 9: Create Build Configuration

If `resume/justfile` doesn't exist, create it:

```makefile
# Build resume PDF
build:
    cd .. && latexmk -pdf -output-directory=resume resume/resume.tex
    mv resume/resume.pdf "Your Name - Company Role.pdf"

# Clean build artifacts
clean:
    rm -f resume/*.aux resume/*.log resume/*.out resume/*.synctex.gz

# Build and clean
all: build clean
```

#### Step 10: Copy Static Partials

Read `static_sections` from `.resume.config.yaml` to get file paths.

Ensure these exist in `resume/partials/` (copy from configured paths if needed):
- `includes.tex`
- `header.tex`
- All sections listed in `required_sections` (typically: skills, education, publications, languages)

**Note:** These are static and should not be modified per job. Paths are defined in config.

#### Step 11: Build and Confirm

1. Offer to build the PDF:
   ```
   cd job_applications/{company}/{role}/resume
   just build
   ```

2. Confirm completion:
   ```
   ✅ Created resume files:
   - resume/resume.tex
   - resume/experiences/{company}-{role}.tex
   - Your Name - Company Role.pdf

   The resume emphasizes:
   - [Key theme 1]
   - [Key theme 2]
   - [Key theme 3]

   Total length: 1 page ✅

   Included sections:
   - Executive Summary
   - Professional Experience (condensed)
   - Skills
   - Publications ✅
   - Education ✅
   - Languages ✅
   ```

## Best Practices

### Content Selection
1. **Relevance over recency** - Include older experiences if highly relevant
2. **Metrics matter** - Prioritize achievements with quantifiable results
3. **Match their language** - Use terminology from job description
4. **Show progression** - Demonstrate growth in responsibility/scope

### Executive Summary
1. **Role-specific** - Match the target role (PM vs CTO vs Engineer)
2. **Concrete** - Mention specific domains/technologies, not generic traits
3. **Metric-backed** - Include scale (team size, users, systems managed)
4. **Concise** - 2-3 sentences maximum

### Bullet Points
1. **Action-first** - Start with strong verbs (Led, Architected, Delivered, Spearheaded)
2. **Bold metrics** - Make numbers and key terms stand out
3. **Context + Action + Result** - Complete stories, not just tasks
4. **Consistent voice** - Past tense for past roles, maintain professional tone

### Length Management
1. **MUST BE 1 PAGE** - Non-negotiable requirement, no exceptions
2. **Condense aggressively** - Merge related achievements, combine bullets, shorten sentences
3. **4 bullets maximum** - For professional experience section
4. **Never remove static sections** - Always keep Education, Publications, Languages
5. **Short executive summary** - 2-3 concise sentences, no fluff

## Common Patterns

### For CTO/Executive Roles
Emphasize:
- Team building and organizational design
- Strategic technical decisions
- Business impact and fundraising involvement
- Cross-functional leadership

### For Product Manager Roles
Emphasize:
- Product strategy and roadmaps
- Stakeholder management
- Technical-business bridge
- Shipped products and user metrics

### For Engineering Roles
Emphasize:
- Technical architecture and implementation
- Technology stack depth
- Performance optimization
- System scale and reliability

### For Quant/Trading Roles
Emphasize:
- Financial domain expertise
- Algorithmic development
- Performance metrics (PnL, Sharpe, execution speed)
- Technology stack (Python, Rust, C++)

## Error Handling

**If job-description.md missing:**
- Ask user to provide job description or run job-finder skill first

**If bio folder incomplete:**
- Ask user to update achievements before generating resume

**If user rejects recommendation:**
- Iterate on recommendation with their feedback
- Don't proceed to generation without approval

**If LaTeX build fails:**
- Check for syntax errors in generated .tex files
- Verify partials exist
- Provide debugging guidance

## Example Interaction

**User:** "Create a resume for the Keyrock Product Manager role"

**Assistant:**
1. Reads `job_applications/keyrock/product-manager-ai-intelligent-automation/job-description.md`
2. Analyzes: PM role, AI/ML focus, fintech domain, requires technical depth + product strategy
3. Reads achievements: OTS CTO experience, Tradebrix product delivery, agentic AI work
4. Presents recommendation with 3 priority tiers
5. Gets user approval
6. Generates executive_summary.tex focusing on PM + AI/ML
7. Creates ots-group-keyrock.tex with CTO highlights + Tradebrix + AI initiatives
8. Creates resume.tex pulling it all together
9. Builds PDF
10. Confirms completion with summary of emphasis

---

**Remember:** Always get user approval on the recommendation before generating any LaTeX files. The recommendation stage is where the user shapes the final resume direction.
