---
name: jobquest-build-cover-letter
description: This skill should be used when the user asks to write or draft a cover letter for a specific job application. It analyzes job requirements against bio, recommends key points to emphasize, gets user approval, then generates a tailored cover letter connecting the user's background to the role.
---

# Cover Letter Generator

## Overview

This skill creates tailored cover letters by analyzing job descriptions against the user's achievements, recommending key talking points and structure, and generating compelling narratives that connect experience to role requirements. It uses a **two-stage approach**: first recommend what to emphasize and get approval, then write the letter.

## When to Use This Skill

Activate this skill when the user:
- Says "write a cover letter for [job/company]"
- Asks to "draft a cover letter for [role]"
- Requests "create cover letter for this application"
- Wants to "generate cover letter for [company]"
- References a job application and asks for cover letter help

## Two-Stage Workflow

### Stage 1: Recommendation & Approval

#### Step 1: Locate Job Application

1. Identify company and role from user's message
2. Find the job application folder: `job_applications/{company}/{role}/`
3. Read `job-description.md` to understand requirements

#### Step 2: Analyze Job Requirements

Extract from job description:
- **Company context** (industry, stage, mission, culture)
- **Role specifics** (title, level, key responsibilities)
- **Requirements** (must-haves vs nice-to-haves)
- **Emphasized qualities** (what they repeat or highlight)
- **Pain points** (what problems does this role solve?)
- **Unique aspects** (what makes this role/company special?)

#### Step 3: Analyze User's Achievements

Read the `bio/` folder:

**Always read:**
- `bio/introduction.mdx` - Overall background and experience summary
- `bio/cto-leadership/overview.mdx` - Leadership capabilities
- `bio/leadership/*.mdx` - Specific leadership achievements

**Project-specific** (based on role requirements):
- `bio/ots-capital/*.mdx` - If fintech/trading/quant relevant
- `bio/tradebrix/*.mdx` - If product/SaaS/engineering relevant
- Any other relevant project folders

**Extract:**
- Experiences directly matching job requirements
- Specific metrics and accomplishments
- Stories demonstrating required skills
- Domain expertise overlap
- Unique value propositions

#### Step 4: Research Company (Optional but Recommended)

If needed for stronger cover letter:
- Use WebSearch to find recent company news, funding, product launches
- Check company blog, recent press releases
- Identify current initiatives or challenges

**Note:** Don't overdo this - keep it relevant and authentic.

#### Step 5: Create Recommendation

Present a structured recommendation:

```markdown
## Cover Letter Strategy for {Company} - {Role}

### Opening Hook (Proposed)
[Draft opening sentence that grabs attention]
**Why this works:** [Explain the strategy]

### Key Themes to Emphasize

**Theme 1: {e.g., "Technical Leadership in Fintech"}**
- **Their need:** [What the job description emphasizes]
- **Your evidence:**
  - {Specific achievement from bio folder}
  - {Metric or outcome}
- **Connection:** [How this directly addresses their need]

**Theme 2: {e.g., "AI/ML Product Innovation"}**
- **Their need:** [Another key requirement]
- **Your evidence:**
  - {Relevant project or accomplishment}
  - {Specific impact}
- **Connection:** [Why this matters for this role]

**Theme 3: {e.g., "Building High-Performing Teams"}**
- **Their need:** [Leadership aspect they need]
- **Your evidence:**
  - {Team building achievement}
  - {Scale or scope}
- **Connection:** [How this translates to their context]

### Structure Recommendation

**Paragraph 1: Opening + Why This Role**
- Hook that demonstrates understanding of their challenge/mission
- Express genuine interest in the specific role (not generic)

**Paragraph 2: Theme 1 - Primary Match**
- Lead with strongest alignment to job requirements
- Specific achievement with metrics
- Direct connection to what they need

**Paragraph 3: Theme 2 - Secondary Match**
- Second strongest alignment
- Different dimension (if Theme 1 was technical, make this leadership, or vice versa)
- Another specific example

**Paragraph 4: Theme 3 - Unique Value (Optional)**
- What sets you apart from other candidates
- Could be: unique technical combination, domain expertise, specific approach
- Keep it authentic, not boastful

**Paragraph 5: Closing**
- Reiterate enthusiasm
- Forward-looking statement about contribution
- Call to action (subtle)

### Tone Recommendation
Based on company culture signals:
- **Formality level:** [Professional/Conversational/Technical]
- **Voice:** [Confident but humble/Bold/Analytical]
- **Length:** [3-4 paragraphs / 5 paragraphs / 1 page max]

### Questions Before Writing:
1. Should we mention [specific recent company news/product]?
2. Do you want to emphasize [aspect A] or [aspect B] more?
3. Any specific story from your experience you want highlighted?
4. Is there anything from the job description you're less qualified for that we should address?

**Approval needed before writing the cover letter.**
```

#### Step 6: Get User Approval

Wait for user to:
- Approve the strategy as-is
- Request modifications (change themes, reorder, adjust tone)
- Provide additional context or stories
- Clarify what to emphasize or de-emphasize

### Stage 2: Generation

Once user approves the strategy:

#### Step 7: Write the Cover Letter

Generate `cover-letter/cover-letter.md` following the approved structure.

**Format:**
```markdown
# Cover Letter: {Role Title}
**{Company Name}**

---

{Paragraph 1: Opening}

{Paragraph 2: Theme 1}

{Paragraph 3: Theme 2}

{Paragraph 4: Theme 3 or additional theme if needed}

{Paragraph 5: Closing}

---

**Note to self:** [Optional section with key talking points if you get an interview]
```

#### Step 8: Writing Principles

**Opening Paragraph:**
- Hook with specific insight about company/role (not generic)
- Demonstrate you've done research
- Express genuine enthusiasm for the SPECIFIC opportunity
- Keep it concise (3-4 sentences)

**Body Paragraphs (Themes):**
- **Lead with impact** - Start with the outcome/achievement
- **Provide context** - Briefly explain the situation
- **Use specific metrics** - Numbers make it concrete
- **Connect to their needs** - Always tie back to job requirements
- **Be concrete, not generic** - "Led 30-person team" not "experienced leader"

**Closing Paragraph:**
- Reiterate fit and enthusiasm
- Forward-looking (what you'll contribute, not what you want)
- Gracious and confident, not desperate
- Subtle call to action

**Overall Tone:**
- Confident but not arrogant
- Specific but not verbose
- Enthusiastic but professional
- Authentic voice (not corporate template)

#### Step 9: Quality Checks

Before finalizing, verify:
- ✅ Cover letter addresses 3-4 key job requirements explicitly
- ✅ Every claim is backed by specific achievement/metric
- ✅ Demonstrates understanding of company/role beyond job posting
- ✅ Maintains authentic voice (not overly formal or generic)
- ✅ No typos or grammatical errors
- ✅ Length appropriate (typically 0.75 - 1 page, max 500 words)
- ✅ Connects your background to their specific needs

#### Step 10: Save and Confirm

1. Write to `cover-letter/cover-letter.md`
2. Confirm completion:
   ```
   ✅ Created cover letter for {Company} - {Role}
   Location: job_applications/{company}/{role}/cover-letter/cover-letter.md

   Key themes emphasized:
   - {Theme 1}
   - {Theme 2}
   - {Theme 3}

   Length: ~{X} words
   Tone: {Description}

   The letter connects:
   - {Specific achievement} → {Their requirement}
   - {Another achievement} → {Their need}
   ```

## Best Practices

### Content

1. **Specificity over generality**
   - ❌ "I'm an experienced leader"
   - ✅ "Built and managed 30-person technical team across 6 business units"

2. **Metrics make it memorable**
   - ❌ "Improved efficiency"
   - ✅ "Reduced operational costs 50% through strategic team restructuring"

3. **Match their language**
   - Use terminology from the job description
   - Mirror their emphasis (if they mention AI 3x, you should too)

4. **Show don't tell**
   - ❌ "I'm passionate about fintech"
   - ✅ "Spent the last year building trading infrastructure for a hedge fund..."

5. **Be authentic**
   - Don't claim interest in things you don't care about
   - Use your real voice, not a corporate template
   - Let personality show (appropriately)

### Structure

1. **Front-load value** - Most important points in first 2 paragraphs
2. **One theme per paragraph** - Don't mix multiple points
3. **Transition smoothly** - Connect paragraphs logically
4. **Vary sentence length** - Mix short punchy sentences with longer explanations
5. **White space matters** - Break into digestible paragraphs

### Common Mistakes to Avoid

1. ❌ **Generic opening** - "I am writing to express my interest..."
2. ❌ **Repeating resume** - Cover letter should complement, not duplicate
3. ❌ **Focusing on what you want** - Focus on what you'll contribute
4. ❌ **Too long** - Respect their time (aim for under 500 words)
5. ❌ **Typos/errors** - Proofread carefully
6. ❌ **Desperate tone** - Confident but not cocky
7. ❌ **Vague claims** - Always back up with specifics

## Tone Calibration by Company Type

### Startup (Early Stage)
- **Tone:** Conversational, energetic, scrappy
- **Emphasize:** Speed of execution, wearing multiple hats, building from scratch
- **Example opening:** "Building a hedge fund's entire tech stack from scratch while managing 6 business units taught me..."

### Established Company (Enterprise)
- **Tone:** Professional, strategic, measured
- **Emphasize:** Scale, process, stakeholder management, business impact
- **Example opening:** "Scaling technical teams and infrastructure while maintaining 99.9% uptime for 45K users requires..."

### Finance/Trading Firm
- **Tone:** Precise, metrics-focused, technical but accessible
- **Emphasize:** Performance metrics, domain expertise, risk management
- **Example opening:** "Architecting HFT infrastructure that reduced backtest time from hours to minutes while managing..."

### Product/Tech Company
- **Tone:** User-focused, innovative, practical
- **Emphasize:** Shipped products, user metrics, cross-functional collaboration
- **Example opening:** "Shipping a SaaS CRM in 2 months while establishing product-market fit taught me..."

## Example Good vs Bad

### Bad Example (Generic, Resume-Repeating):
```
I am writing to express my interest in the Product Manager position at your company.
I have 5+ years of experience in technology and leadership. In my previous role
as CTO, I managed teams and built products. I am passionate about AI and fintech.
I believe I would be a great fit for this role.
```

**Problems:** Generic, no specifics, repeats resume, focuses on "I want", no connection to company.

### Good Example (Specific, Connected):
```
Keyrock's focus on "LLMs, MCP, and state-of-the-art automation" in market making
mirrors the exact challenge I tackled at OTS Capital: how do you integrate AI
into financial operations without breaking what already works?

As CTO managing technology across a hedge fund and 3 prop firms, I didn't have
the luxury of slow AI adoption. I spearheaded agentic AI initiatives that 10x'd
development speed using custom LLMs and MCPs—not as experiments, but as production
systems handling real capital. This included building self-learning trading strategies
and AI-assisted infrastructure that reduced backtest time from hours to minutes.

What drew me to this role is the intersection of two domains I've lived in: digital
asset infrastructure (managed trading across 80+ exchanges at OTS) and intelligent
automation at scale. Your technical stack challenge—integrating AI into market
making operations—is precisely what I've been solving, just at smaller scale.
Now I want to tackle it at Keyrock's level.
```

**Strengths:** Specific hook, concrete achievements, connects background to their needs, demonstrates understanding, authentic voice.

## Error Handling

**If job-description.md missing:**
- Ask user to provide job description or run job-finder skill first

**If bio folder incomplete:**
- Ask user what specific experiences to highlight
- Work with what's available but note limitations

**If user rejects strategy:**
- Iterate on recommendation with their feedback
- Don't proceed to writing without approval

**If can't find strong connections:**
- Be honest about weaker alignment
- Focus on transferable skills
- Ask user for insights on hidden connections

## Example Interaction

**User:** "Write a cover letter for the Keyrock PM role"

**Assistant:**
1. Reads `job_applications/keyrock/product-manager-ai-intelligent-automation/job-description.md`
2. Analyzes: AI automation focus, market making domain, product strategy + technical depth needed
3. Reads achievements: OTS CTO, agentic AI initiatives, fintech background
4. Presents strategy with 3 themes:
   - AI/ML integration in production (agentic AI work)
   - Fintech/trading domain expertise (hedge fund, prop firms)
   - Product delivery under constraints (Tradebrix 2-month SaaS)
5. Gets user approval
6. Writes cover letter connecting each theme to job requirements
7. Saves to cover-letter/cover-letter.md
8. Confirms with summary of approach

---

**Remember:** Always get user approval on the strategy before writing the cover letter. The recommendation stage ensures the letter focuses on what matters most to the user.
