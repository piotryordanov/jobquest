---
name: jobquest-analyze-profile
description: Use this skill when you need to understand the user's professional background, skills, and experience. Reads the bio folder to extract technical skills, domain expertise, years of experience, leadership scope, and project achievements. Used before matching jobs to create a profile summary.
---

# Analyze User Profile

## When to Use This Skill

Activate this skill when:
- You need to understand user's background before matching jobs
- User asks "what's my experience in [domain]?"
- You need to determine which jobs are relevant
- Before using `jobquest-match-jobs` to rank opportunities

## Workflow

### Step 1: Read Core Bio Files

Start by reading the user's overview:

```bash
bio/introduction.mdx
```

**Extract:**
- Current/most recent role and title
- Years of experience
- Team size managed (if applicable)
- High-level tech stack
- Industries worked in
- Key achievements with metrics

### Step 2: Read Project-Specific Experience

Read relevant project folders:

```bash
bio/tradebrix/overview.mdx
bio/tradebrix/tech-stack.mdx
bio/ots-capital/*.mdx
bio/engineering/*.mdx
```

**For each project, extract:**
- Technical stack used
- Project scope and scale (users, revenue, AUM, etc.)
- Specific achievements and metrics
- Responsibilities and role
- Duration

### Step 3: Read Leadership Experience (if applicable)

```bash
bio/cto-leadership/overview.mdx
bio/leadership/*.mdx
```

**Extract:**
- Team building and management experience
- Organizational design work
- Strategic decision-making
- Hiring and performance management
- Budget and cost optimization

### Step 4: Extract Technical Skills

From all bio files, compile:

**Programming Languages:**
- Primary languages (Python, TypeScript, Rust, etc.)
- Proficiency level (based on project descriptions)
- Years of experience with each

**Frameworks & Tools:**
- Frontend (React, Vue, etc.)
- Backend (Node.js, tRPC, Express, etc.)
- Databases (PostgreSQL, MongoDB, Redis, etc.)
- DevOps (Docker, Kubernetes, CI/CD, etc.)
- Cloud platforms (AWS, GCP, Railway, etc.)

**Technical Domains:**
- Trading systems
- DeFi/Blockchain
- SaaS platforms
- AI/ML
- System architecture
- Microservices
- etc.

### Step 5: Extract Domain Expertise

Identify specialized knowledge:
- Financial services (trading, hedge funds, fintech)
- Crypto/blockchain
- Product management
- Data engineering
- Quantitative development
- etc.

### Step 6: Determine Experience Level

Based on:
- Years in industry
- Leadership scope (team size)
- Project complexity
- Technical depth

Categorize as:
- **Junior**: 0-3 years
- **Mid-level**: 3-5 years
- **Senior**: 5-8 years
- **Staff/Principal**: 8-12 years
- **Lead/Executive**: 12+ years or CTO/VP level

### Step 7: Create Profile Summary

Generate a structured summary:

```markdown
## User Profile Summary

### Overview
- **Current Role**: Chief Technology Officer
- **Experience**: 10+ years in software engineering, 2 years in leadership
- **Team Leadership**: Managed 27-person technical organization
- **Industries**: Fintech, trading, SaaS, crypto/DeFi

### Technical Skills

**Primary Languages** (Deep expertise):
- TypeScript/JavaScript - 5+ years
- Python - 8+ years
- Rust - 2+ years

**Frameworks & Platforms**:
- React, Next.js, Tailwind CSS
- Node.js, tRPC, Express
- PostgreSQL, MongoDB, Redis
- Docker, Railway, GitHub Actions

**System Design**:
- Microservices architecture
- Event-driven systems
- Multi-tenant SaaS
- Real-time systems (HFT, trading)
- High-availability systems (99.9%+ uptime)

### Domain Expertise

**Strong Match For**:
- Full-stack engineering (React + Node.js/TypeScript)
- Trading systems and financial technology
- Crypto/DeFi infrastructure
- SaaS platform development
- CTO/technical leadership roles

**Experience With**:
- $20M AUM trading infrastructure
- 45K+ user SaaS platforms
- CI/CD and DevOps
- Team scaling (7→20 engineers)
- Cost optimization

### Notable Achievements
- Built production trading systems with 99.9%+ uptime
- Scaled engineering team 3x in compressed timeline
- Delivered multi-tenant SaaS in 3 months
- Crypto market-making with 3 successful token launches
- Reduced infrastructure costs by 50%

### Career Level
**Senior/Lead/Executive** - Suitable for senior IC, staff, lead, or executive roles
```

## Output Format

Return the profile summary as structured markdown that can be used by `jobquest-match-jobs` to score job relevance.

**Key sections:**
1. Overview (role, years, scope)
2. Technical skills (languages, frameworks, tools)
3. Domain expertise (industries, specializations)
4. Notable achievements (with metrics)
5. Career level (seniority)

## Best Practices

1. **Read multiple files** - Don't rely on just introduction.mdx
2. **Extract metrics** - Numbers make the profile concrete ($20M AUM, 45K users, etc.)
3. **Note technical depth** - Distinguish between "used once" and "expert level"
4. **Identify transferable skills** - MongoDB ↔ PostgreSQL, Express ↔ tRPC, etc.
5. **Consider breadth vs depth** - Full-stack + leadership vs specialized IC

## Example Interaction

**User:** "Find relevant jobs at Aktek for me"

**Claude automatically:**
1. Invokes `jobquest-analyze-profile`
2. Reads `bio/introduction.mdx`, `bio/tradebrix/*`, `bio/ots-capital/*`
3. Generates profile summary
4. Passes to `jobquest-match-jobs` for scoring

**Profile Output:**
```
Analyzed your profile:
- Senior full-stack engineer with CTO experience
- Strong: TypeScript, React, Node.js, system architecture
- Domain: Trading systems, SaaS, fintech
- Leadership: 27-person team, scaled 7→20 engineers
- Level: Senior/Staff/Executive
```

---

**Next Steps:** Pass this profile summary to `jobquest-match-jobs` to score and rank job opportunities.
