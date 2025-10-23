---
name: jobquest-match-jobs
description: Use this skill when you have job listings and a user profile, and need to rank jobs by relevance. Scores jobs based on skills match, domain alignment, experience level, and identifies specific achievements that are relevant. Filters by location preferences and presents ranked results with match reasoning.
---

# Match Jobs to User Profile

## When to Use This Skill

Activate this skill when:
- You have job listings and need to determine which ones fit the user
- User asks "which of these jobs are relevant to me?"
- After `jobquest-fetch-jobs` gets listings
- After `jobquest-analyze-profile` creates a profile summary

## Prerequisites

Before using this skill, you need:
1. **Job listings** - From `jobquest-fetch-jobs` or saved references
2. **User profile** - From `jobquest-analyze-profile`
3. **Location preferences** - From `configs/preferences.yaml`

## Workflow

### Step 1: Read Location Preferences

```bash
configs/preferences.yaml
```

**Extract:**
```yaml
locations:
  - "Remote"
  - "Dubai"
```

**Default if file doesn't exist:** `["Remote", "Dubai"]`

### Step 2: Filter Jobs by Location

For each job, check if its location matches preferences:

**Location matching rules:**
- Case-insensitive matching
- "Remote" matches: "Remote", "Remote - US", "Fully Remote", "Work from anywhere"
- "Dubai" matches: "Dubai", "Dubai, UAE", "United Arab Emirates - Dubai"
- If uncertain, include the job (err on the side of inclusion)

**Remove jobs** that don't match any preferred location.

**Report:**
```
Total jobs found: X
After location filtering: Y (filtered out Z jobs)
```

### Step 3: Score Each Job

For each filtered job, score across 4 dimensions:

#### A. Skills Match (0-10 points)

Compare job's required skills to user's skills:

**Technical stack match:**
- Exact match (React → React): +2 points per skill
- Close match (tRPC → Express, PostgreSQL → MongoDB): +1 point per skill
- Related stack (TypeScript backend → Node.js backend): +1 point

**Required vs preferred:**
- User has ALL required skills: +3 points
- User has MOST required skills: +2 points
- User has SOME required skills: +1 point

**Example:**
Job requires: "React, Node.js, MongoDB, Docker"
User has: "React, TypeScript, tRPC, PostgreSQL, Docker"
- React: +2 (exact)
- Node.js: +1 (tRPC is Node.js-based)
- MongoDB: +1 (PostgreSQL → MongoDB transferable)
- Docker: +2 (exact)
= 6/10 points

#### B. Domain Match (0-10 points)

Compare job's industry/domain to user's experience:

**Direct domain experience:**
- Same domain (Fintech → Fintech): +5 points
- Related domain (Trading → Finance): +3 points
- Transferable domain (SaaS → SaaS): +4 points

**Company type:**
- Startup → Startup experience: +2 points
- Remote-first → Remote team experience: +1 point

**Example:**
Job: Intelligence/data solutions company, remote-first
User: Built trading systems, led remote teams
- Domain: Different (-0 points)
- Remote-first: +1 point
- System architecture: +3 points (transferable)
= 4/10 points

#### C. Level Match (0-10 points)

Compare job's seniority to user's level:

**Perfect level match:**
- Job: Senior, User: Senior → +10 points
- Job: Staff, User: Staff → +10 points

**Under-leveled:**
- Job: Mid, User: Senior → +5 points (can do but might be boring)
- Job: Junior, User: Senior → +2 points (significant under-level)

**Over-leveled:**
- Job: Principal, User: Senior → +7 points (stretch but achievable)
- Job: VP, User: Senior IC → +3 points (different track)

**Example:**
Job: Senior Full Stack Engineer (MERN)
User: CTO with senior IC experience
= 10/10 points (perfect IC level match)

#### D. Interest Alignment (0-10 points)

Look for alignment with user's demonstrated interests:

**Explicitly mentioned:**
- Job involves user's past projects: +3 points per match
- Job's tech stack matches user's preferred stack: +2 points
- Job's problems match user's experience: +4 points

**Example:**
Job: Build distributed systems, event-driven architecture
User: Built distributed trading systems, event-driven microservices
= 8/10 points (strong alignment)

### Step 4: Calculate Total Score

**Total = Skills + Domain + Level + Interest**
**Maximum: 40 points**

**Relevance Categories:**
- **High**: 30-40 points (⭐ Strong match)
- **Medium**: 20-29 points (Decent fit)
- **Low**: 0-19 points (Weak match)

### Step 5: Identify Specific Achievement Alignments

For each job, cite specific bio achievements that demonstrate relevance:

**Format:**
```
**Relevant experience:**
- [Achievement from bio] → Demonstrates [job requirement]
- [Project from bio] → Shows [job skill]
```

**Example:**
Job: "Build distributed systems with high availability"

**Relevant experience:**
- `bio/ots-capital/trading-systems.mdx` - Built production trading systems with 99.9%+ uptime managing $20M AUM → Demonstrates high-availability system design
- `bio/tradebrix/architecture.mdx` - Architected multi-tenant SaaS with microservices → Shows distributed systems experience

### Step 6: Present Ranked Results

Sort jobs by relevance (High → Medium → Low), then by score within each category.

**Format:**

```markdown
Found X jobs at Company, filtered to Y matching your location preferences (Remote, Dubai).

## High Relevance Matches (Z jobs)

### Job Title
**Location:** Remote
**Relevance:** ⭐ High (Score: 35/40)
**Link:** [URL]

**Why it matches:**
- [Specific skills alignment]
- [Domain expertise alignment]
- [Level appropriateness]

**Relevant experience:**
- `bio/path/file.mdx` - [Specific achievement that demonstrates fit]
- `bio/path/file.mdx` - [Another relevant project]

**Score breakdown:**
- Skills: 8/10 (React, TypeScript, Node.js match; MongoDB transferable from PostgreSQL)
- Domain: 7/10 (System architecture experience, different industry but transferable)
- Level: 10/10 (Perfect senior IC match)
- Interest: 10/10 (Distributed systems, event-driven architecture)

---

### Another Job Title
...

## Medium Relevance Matches (X jobs)
...

## Low Relevance Matches (X jobs)
...
```

### Step 7: Provide Summary and Next Steps

At the end:

```markdown
## Summary

- Total jobs found: X
- After location filtering: Y
- High relevance: Z jobs
- Medium relevance: A jobs
- Low relevance: B jobs

## Recommended Actions

1. Review high-relevance matches first
2. Would you like me to:
   - Create a tailored resume for any of these positions?
   - Save specific jobs to your application folders?
   - Fetch more details about a particular role?
```

## Scoring Guidelines

### Skills Match Tips
- Consider transferable skills (SQL databases are similar)
- Don't penalize for missing "nice-to-have" skills
- Weight required skills more heavily
- Recognize equivalent technologies (tRPC vs Express, Tailwind vs styled-components)

### Domain Match Tips
- Technical skills often transfer across domains
- System architecture knowledge is domain-agnostic
- Look for similar problem spaces, not just industries

### Level Match Tips
- Don't recommend jobs too far below user's level
- Stretch roles (+1 level up) are usually good
- IC vs Management are different tracks

### Interest Alignment Tips
- Use job description keywords to match bio content
- Look for problem-solving patterns (real-time systems, scaling, etc.)
- Consider user's trajectory (moving from X to Y)

## Example Interaction

**User:** "Which Aktek jobs are relevant to me?"

**Claude automatically:**
1. Gets jobs from `job_applications/aktek/references/2025-10-22/`
2. Gets profile from `jobquest-analyze-profile`
3. Reads `configs/preferences.yaml`
4. Filters jobs by location (Remote ✓)
5. Scores each job
6. Presents ranked results

**Output:**
```
Found 5 jobs at Aktek, all match your location preference (Remote).

## High Relevance Matches (2 jobs)

### Sr. Full Stack Software Engineer (MERN)
**Location:** Remote
**Relevance:** ⭐ High (Score: 32/40)
**Link:** https://www.aktek.io/careers/sr-full-stack-software-developer

**Why it matches:**
- Strong React + TypeScript + Node.js experience
- Built distributed systems with high availability
- Led architecture reviews and mentored teams

**Relevant experience:**
- `bio/tradebrix/tech-stack.mdx` - Built multi-tenant SaaS with React, TypeScript, tRPC
- `bio/ots-capital/trading-systems.mdx` - Architected event-driven microservices with 99.9%+ uptime

**Score breakdown:**
- Skills: 8/10 (React, TypeScript, Node.js exact; MongoDB transferable)
- Domain: 6/10 (Different domain but system architecture transfers)
- Level: 10/10 (Perfect senior IC match)
- Interest: 8/10 (Distributed systems, event-driven architecture)

---

[More jobs...]
```

---

**Next Steps:** User can then use `jobquest-build-resume` to create tailored resumes for high-relevance matches.
