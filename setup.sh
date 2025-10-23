#!/bin/bash
# JobQuest Setup Script
# Quickly initialize configuration files

set -e

echo "🎯 JobQuest Setup"
echo ""

# Create configs directory
mkdir -p configs

# Check if configs already exist
if [ -f "configs/preferences.yaml" ]; then
    echo "⚠️  configs/preferences.yaml already exists"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Skipping preferences.yaml"
        SKIP_PREFS=1
    fi
fi

if [ -z "$SKIP_PREFS" ]; then
    echo "Creating configs/preferences.yaml..."
    cat > configs/preferences.yaml <<'EOF'
# Job Search Preferences

# Preferred job locations (case-insensitive)
locations:
  - "Remote"
  # Add your preferred cities:
  # - "Dubai"
  # - "London"
  # - "Singapore"

# Employment types
employment_types:
  - "Full-time"
  # - "Contract"
  # - "Part-time"

# Optional: Minimum salary filter
# min_salary: 150000
# currency: "USD"

# Optional: Keywords to prioritize
# prioritize_keywords:
#   - "AI"
#   - "Senior"
#   - "Lead"

# Optional: Keywords to avoid
# avoid_keywords:
#   - "Junior"
#   - "Intern"
EOF
    echo "✅ Created configs/preferences.yaml"
fi

# Create companies.yaml if it doesn't exist
if [ ! -f "configs/companies.yaml" ]; then
    echo "Creating configs/companies.yaml..."
    cat > configs/companies.yaml <<'EOF'
# Known Company Careers Pages
# Auto-populated as you search for jobs

companies: []
  # Companies will be added automatically
  # You can also manually add them:
  #
  # - name: "Company Name"
  #   careers_url: "https://careers.company.com"
  #   platform: "generic"
  #   added_date: "2025-10-23"
  #   last_searched: null
  #   notes: "Optional notes"
EOF
    echo "✅ Created configs/companies.yaml"
else
    echo "⏭️  configs/companies.yaml already exists (skipping)"
fi

# Create job_boards.yaml if it doesn't exist
if [ ! -f "configs/job_boards.yaml" ]; then
    echo "Creating configs/job_boards.yaml..."
    cat > configs/job_boards.yaml <<'EOF'
# Job Boards Reference

job_boards:
  - name: "RemoteOK"
    url: "https://remoteok.com/"
    category: "remote"
    effectiveness: null
    last_checked: null
    notes: "Popular remote job board"

  - name: "We Work Remotely"
    url: "https://weworkremotely.com/"
    category: "remote"
    effectiveness: null
    last_checked: null
    notes: "Remote-first companies"

  - name: "AngelList (Wellfound)"
    url: "https://wellfound.com/"
    category: "tech"
    effectiveness: null
    last_checked: null
    notes: "Startup-focused"

  # Add more boards as needed:
  # - name: "Cryptocurrency Jobs"
  #   url: "https://cryptocurrencyjobs.co/"
  #   category: "crypto"
  #   effectiveness: null
  #   last_checked: null
EOF
    echo "✅ Created configs/job_boards.yaml"
else
    echo "⏭️  configs/job_boards.yaml already exists (skipping)"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Configuration files created in configs/"
echo ""
echo "Next steps:"
echo "  1. Edit configs/preferences.yaml to set your preferred locations"
echo "  2. Start searching: 'Find jobs at [Company]'"
echo "  3. JobQuest will automatically track companies and job boards"
echo ""
