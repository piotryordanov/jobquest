---
name: jobquest-prep-interview
description: This skill should be used when the user has an upcoming interview and needs to prepare. It analyzes the job requirements, extracts likely interview questions, maps the user's bio to answers, and generates a comprehensive prep document with talking points and questions to ask.
---

# Interview Prep

## Overview

This skill creates comprehensive interview preparation documents by analyzing job descriptions, predicting likely questions based on role requirements, and mapping the user's achievements to compelling answers. It generates prep materials saved to the communications folder for easy reference.

## When to Use This Skill

Activate this skill when the user:
- Says "prepare me for [company] interview"
- Asks "help me prep for interview with [person/company]"
- Mentions "I have an interview with [company] tomorrow/next week"
- Requests "create interview prep for [role]"
- References upcoming interview in timeline

## Workflow

### Step 1: Locate Job Application

1. Identify company and role from user's message
2. Find job application folder: `job_applications/{company}/{role}/`
3. Read `job-description.md` for role requirements
4. Read `timeline.yaml` to understand interview context (who, when, stage)

### Step 2: Analyze Role Requirements

Extract from job description:
- **Role type** (IC vs leadership, technical vs product, etc.)
- **Key responsibilities** (what they'll do day-to-day)
- **Required skills** (technical + soft skills)
- **Experience level** (seniority expectations)
- **Domain focus** (industry, technology, business area)
- **Company stage** (startup vs established - affects questions)

### Step 3: Identify Interview Type

Based on timeline and user input:
- **Recruiter screen** - Culture fit, basics, logistics
- **Hiring manager** - Role fit, experience deep-dive, team dynamics
- **Technical** - System design, coding, architecture
- **Executive** - Strategic thinking, leadership, business impact
- **Panel** - Mix of above, multiple perspectives

Tailor prep document to interview type.

### Step 4: Read User's Achievements

Read `bio/` folder focusing on relevant areas:
- `bio/introduction.mdx` - Overall background
- `bio/cto-leadership/*.mdx` - Leadership examples
- `bio/leadership/*.mdx` - Specific leadership scenarios
- Project folders matching job domain (ots-capital, tradebrix, etc.)

Extract:
- Specific accomplishments matching role requirements
- Metrics and outcomes
- Technical depth examples
- Leadership/collaboration stories
- Challenges overcome
- Domain expertise demonstrations

### Step 5: Generate Likely Questions

Based on role requirements and interview type, create questions in categories:

#### Technical Questions (for technical roles)
- Architecture/design questions
- Technology stack depth
- Problem-solving scenarios
- Trade-off discussions
- Performance/scale challenges

#### Experience Questions (all roles)
- "Tell me about a time when..."
- Past work deep-dives
- Specific achievements
- Role-relevant scenarios

#### Behavioral Questions
- Leadership and team dynamics
- Conflict resolution
- Prioritization and decision-making
- Handling failure/setbacks
- Cross-functional collaboration

#### Role-Specific Questions
- For PM: Product strategy, stakeholder management, roadmapping
- For CTO: Org design, technical strategy, team building
- For Engineer: Code quality, debugging, system design
- For Quant: Algorithm development, backtesting, risk management

### Step 6: Map Achievements to Answers

For each predicted question, identify which achievements provide strong answers.

**Format:**
```markdown
### Question: "Tell me about a time you had to make a difficult technical decision with limited information"

**Your Answer (from bio):**
- **Situation:** At OTS Capital, needed to choose deployment strategy (VPS vs K8s) for 6 business units
- **Challenge:** Limited budget, varied technical needs, tight timeline
- **Action:** Analyzed requirements per unit, prototyped both, measured trade-offs
- **Result:** Chose hybrid approach, saved $X/month, deployed in Y weeks
- **Source:** bio/cto-leadership/technical-decisions.mdx

**Key points to emphasize:**
- Decision framework used
- Stakeholder management across 6 units
- Cost-benefit analysis
- Execution speed

**Metrics to mention:**
- 50% cost reduction
- 6 business units
- Timeline: 2 weeks
```

### Step 7: Create "Questions to Ask Them"

Generate thoughtful questions the user should ask, based on:
- Company stage and challenges
- Role responsibilities
- Team structure
- Technology decisions
- Growth opportunities

**Categories:**
- About the role and day-to-day
- About the team and collaboration
- About technical/product challenges
- About company direction and strategy
- About success metrics and expectations

### Step 8: Add Company/Role Research

Include brief section with:
- Recent company news or funding
- Product developments
- Key people interviewing with (if known from timeline)
- Company values or mission (if relevant)

### Step 9: Generate Prep Document

Create comprehensive prep doc at:
`communications/YYYY-MM-DD_interview-prep-{interviewer-name}.md`

**Structure:**

```markdown
# Interview Prep: {Company} - {Role}
**Interviewer:** {Name} ({Title})
**Date:** {Interview Date}
**Type:** {Interview Type - e.g., Hiring Manager Round}

---

## Overview

**Role Summary:** {Brief 2-3 sentence summary of what they're looking for}

**Your Positioning:** {How to frame your background for this role}

---

## Likely Questions & Your Answers

### Technical/Experience Questions

#### Q: "Walk me through your experience with [key requirement]"
**Your Answer:**
- **Context:** {From achievements}
- **Details:** {Specific work}
- **Impact:** {Metrics/outcomes}

**Talking Points:**
- {Key point 1}
- {Key point 2}

**Source:** bio/{relevant-file}

---

#### Q: "Tell me about a time when [behavioral scenario]"
**Your Answer:** {STAR format response mapped from bio}

{Repeat for 8-12 likely questions}

---

## Questions to Ask Them

### About the Role
1. {Thoughtful question about day-to-day}
2. {Question about success metrics}
3. {Question about team dynamics}

### About Technical Challenges
1. {Question about current tech stack decisions}
2. {Question about scaling/architecture}

### About the Company
1. {Question about strategy/direction}
2. {Question about culture/values}

---

## Key Themes to Emphasize

Based on job requirements, make sure to highlight:
1. **{Theme 1}** - {Why it matters for this role}
   - Example from bio: {specific project}
2. **{Theme 2}** - {Why it matters}
   - Example: {another accomplishment}
3. **{Theme 3}** - {Why it matters}
   - Example: {third example}

---

## Your Unique Value Props

What sets you apart for THIS specific role:
1. {Unique combination of skills}
2. {Rare experience or domain knowledge}
3. {Specific achievement that's highly relevant}

---

## Company Research Summary

**Recent News:**
- {Recent development if found}

**About {Interviewer Name}:**
- {Background if available from LinkedIn/timeline}
- {What to know about them}

**Their Challenges:** (Based on job description)
- {Challenge 1 you can help solve}
- {Challenge 2}

---

## Red Flags to Address

**Potential Concerns:**
1. {Possible concern from your background}
   - How to address: {Your response}

2. {Another potential objection}
   - How to address: {Your response}

---

## Logistics

- **Format:** {Video/Phone/In-person}
- **Duration:** {Expected length}
- **What to bring:** {Portfolio/laptop/nothing}

---

## Pre-Interview Checklist

- [ ] Review this prep doc 1 hour before
- [ ] Review job description again
- [ ] Check interviewer's LinkedIn
- [ ] Prepare questions to ask (pick 5-7 from above)
- [ ] Have bio folder open for reference
- [ ] Test video/audio if virtual
- [ ] Get water, quiet space ready

---

## Post-Interview

**After the interview, document:**
- Questions they actually asked
- Topics they focused on
- Their reactions/concerns
- Next steps discussed
- Your assessment of fit

**Update timeline.yaml with this interaction.**
```

### Step 10: Save and Confirm

1. Write prep document to `communications/` folder
2. Confirm to user:
   ```
   ✅ Created interview prep for {Company} - {Role}
   Interviewer: {Name}
   Location: communications/YYYY-MM-DD_interview-prep-{name}.md

   Prepared {X} likely questions with answers mapped from your achievements
   Generated {Y} questions for you to ask them
   Highlighted {Z} key themes to emphasize

   Top 3 talking points:
   1. {Most important point}
   2. {Second priority}
   3. {Third priority}

   Review 1 hour before the interview. Good luck!
   ```

## Best Practices

### Question Prediction
1. **Focus on role requirements** - Don't generic-ize, tailor to JD
2. **Consider interview stage** - Early vs late rounds ask different questions
3. **Match interviewer** - Recruiter vs engineer vs exec ask different things
4. **Include 10-15 questions** - Enough to cover likely ground, not overwhelming

### Answer Mapping
1. **Be specific** - Point to exact achievements, not vague skills
2. **Include metrics** - Numbers make stories memorable
3. **Use STAR format** - Situation, Task, Action, Result
4. **Vary examples** - Don't reuse same project for every answer
5. **Match their language** - Use terminology from job description

### Questions to Ask
1. **Be genuine** - Only include questions user would actually ask
2. **Show depth** - Questions should demonstrate research/understanding
3. **Avoid basics** - Don't ask what's easily Googleable
4. **Be strategic** - Questions also sell your expertise
5. **Mix types** - Role, team, technical, company

### Document Length
- **Recruiter screen:** 2-3 pages (lighter prep)
- **Hiring manager:** 4-6 pages (comprehensive)
- **Technical:** Focus on technical questions, system design
- **Executive:** Focus on strategy, leadership, business impact

## Interview Type Specifics

### Recruiter/HR Screen (30 min)
**Focus:**
- Culture fit
- Salary expectations
- Logistics
- Basic qualifications

**Prep:**
- Elevator pitch (30 seconds)
- Why this company/role
- Salary range research
- Basic questions about role

### Hiring Manager (45-60 min)
**Focus:**
- Experience deep-dive
- Role fit
- Problem-solving approach
- Team collaboration

**Prep:**
- 8-10 behavioral questions
- Specific project deep-dives
- Questions about team/role
- Demonstrate domain knowledge

### Technical Interview (60-90 min)
**Focus:**
- System design
- Coding/algorithms
- Architecture decisions
- Technical depth

**Prep:**
- Review tech stack from bio
- Practice system design
- Prepare architecture examples
- Code samples if needed

### Executive Interview (30-45 min)
**Focus:**
- Strategic thinking
- Business impact
- Leadership philosophy
- Culture contribution

**Prep:**
- Big-picture achievements
- Business metrics
- Strategic decisions made
- Leadership examples

## Common Question Categories

### Experience Questions
- Walk me through your resume
- Tell me about your current/most recent role
- What's your biggest achievement?
- Describe a challenging project

### Behavioral Questions
- Tell me about a time you failed
- Describe a conflict with a teammate
- How do you prioritize competing demands?
- Give an example of leadership

### Technical Questions (for technical roles)
- How would you design [system]?
- Explain [technology] to a non-technical person
- What's your approach to [technical challenge]?
- Walk me through your debugging process

### Role-Specific Questions
**PM:**
- How do you prioritize features?
- Describe your product development process
- How do you work with engineering?

**CTO:**
- How do you build technical teams?
- Describe your technical strategy approach
- How do you balance tech debt vs features?

**Engineer:**
- Tell me about your code review process
- How do you ensure code quality?
- Describe a complex bug you solved

## Error Handling

**If job-description.md missing:**
- Create basic prep from timeline context
- Ask user for role details

**If achievements incomplete:**
- Work with available information
- Ask user for specific examples to add

**If interviewer unknown:**
- Generic prep document
- User can customize for specific person

**If interview type unclear:**
- Ask user what type of interview
- Default to hiring manager format

## Example Interaction

**User:** "I have an interview with Jane Smith at Keyrock tomorrow, she's the hiring manager for the PM role"

**Assistant:**
1. Reads `job_applications/keyrock/product-manager-ai-intelligent-automation/job-description.md`
2. Checks `timeline.yaml` for Jane Smith (Hiring Manager role noted)
3. Identifies: Hiring manager round, PM role, AI/ML focus, fintech domain
4. Reads achievements: OTS CTO work, Tradebrix, agentic AI
5. Generates likely questions:
   - Product strategy approach
   - AI/ML product experience
   - Stakeholder management in fintech
   - Team leadership examples
   - Technical-product bridge
6. Maps each question to specific achievements
7. Creates questions to ask about:
   - PM role scope at Keyrock
   - AI integration challenges
   - Product roadmap priorities
8. Highlights 3 key themes: AI product delivery, fintech domain, technical depth
9. Saves to `communications/2025-10-22_interview-prep-jane-smith.md`
10. Confirms with top talking points

---

**Remember:** This prep doc is a reference, not a script. The goal is to feel confident and prepared, while still being natural and conversational in the interview.
