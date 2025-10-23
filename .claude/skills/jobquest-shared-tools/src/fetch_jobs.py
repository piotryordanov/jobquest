"""
CLI tool to scrape jobs from company careers pages.

Usage:
    uv run python -m src.fetch_jobs <url> [--company NAME]
    uv run python -m src.fetch_jobs <url> --fetch-descriptions [--company NAME]

Examples:
    # Fetch job listings only
    uv run python -m src.fetch_jobs https://jobs.lever.co/wintermute-trading --company Wintermute

    # Fetch listings + full descriptions in parallel
    uv run python -m src.fetch_jobs https://jobs.lever.co/wintermute-trading --company Wintermute --fetch-descriptions
"""

import asyncio
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import msgspec
from playwright.async_api import async_playwright

from src.models import JobListing, ScrapingResult
from src.scrapers import detect_platform, get_scraper


async def fetch_job_description(url: str, browser: Any) -> str | None:
    """
    Fetch full job description from a job posting URL.

    Args:
        url: Job posting URL
        browser: Playwright browser instance

    Returns:
        Job description text or None if failed
    """
    page = await browser.new_page()
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)

        # Wait a bit for content to load
        await asyncio.sleep(1)

        # Try to extract main content
        description = await page.evaluate("""
            () => {
                // Common selectors for job descriptions
                const selectors = [
                    '.posting-description',
                    '.job-description',
                    '.description',
                    '[class*="description"]',
                    'main',
                    'article',
                    '.content',
                ];

                for (const selector of selectors) {
                    const el = document.querySelector(selector);
                    if (el && el.textContent.length > 200) {
                        return el.textContent.trim();
                    }
                }

                // Fallback: get body text
                return document.body.textContent.trim();
            }
        """)

        return description

    except Exception as e:
        print(f"Warning: Failed to fetch description for {url}: {e}", file=sys.stderr)
        return None
    finally:
        await page.close()


async def fetch_all_descriptions(
    jobs: list[JobListing], max_concurrent: int = 5
) -> list[JobListing]:
    """
    Fetch descriptions for all jobs in parallel.

    Args:
        jobs: List of job listings
        max_concurrent: Maximum number of concurrent requests

    Returns:
        List of jobs with descriptions filled in
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Create semaphore to limit concurrency
        semaphore = asyncio.Semaphore(max_concurrent)

        async def fetch_with_semaphore(job: JobListing) -> JobListing:
            async with semaphore:
                description = await fetch_job_description(job.url, browser)
                return JobListing(
                    title=job.title,
                    location=job.location,
                    url=job.url,
                    description=description,
                    department=job.department,
                    employment_type=job.employment_type,
                    company=job.company,
                    source=job.source,
                )

        # Fetch all descriptions in parallel
        jobs_with_descriptions = await asyncio.gather(
            *[fetch_with_semaphore(job) for job in jobs]
        )

        await browser.close()

        return jobs_with_descriptions


async def scrape_careers_page(
    url: str, company: str | None = None, fetch_descriptions: bool = False
) -> ScrapingResult:
    """
    Scrape jobs from a careers page.

    Args:
        url: Careers page URL
        company: Company name (optional, will be extracted from URL if not provided)
        fetch_descriptions: Whether to fetch full descriptions for each job

    Returns:
        ScrapingResult with jobs and metadata
    """
    # Detect platform
    platform = detect_platform(url)

    # Extract company from URL if not provided
    if not company:
        # Simple extraction from domain
        from urllib.parse import urlparse

        parsed = urlparse(url)
        domain_parts = parsed.netloc.split(".")
        company = domain_parts[0] if domain_parts else "Unknown"

    # Get appropriate scraper
    scraper = get_scraper(platform)

    # Scrape job listings
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            jobs = await scraper.scrape(page, url, company)

            # Fetch descriptions if requested
            if fetch_descriptions and jobs:
                await page.close()
                await browser.close()
                jobs = await fetch_all_descriptions(jobs)
            else:
                await page.close()
                await browser.close()

            return ScrapingResult(
                company=company,
                source_url=url,
                jobs=jobs,
                platform=platform,
            )

        except Exception as e:
            await page.close()
            await browser.close()

            return ScrapingResult(
                company=company,
                source_url=url,
                jobs=[],
                error=str(e),
                platform=platform,
            )


def slugify(text: str) -> str:
    """Convert text to a URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def load_previous_jobs(references_dir: Path) -> dict[str, str]:
    """
    Load all previously saved jobs from all snapshot dates.

    Args:
        references_dir: Path to the references directory

    Returns:
        Dictionary mapping job_url -> description content
    """
    previous_jobs = {}

    if not references_dir.exists():
        return previous_jobs

    # Iterate through all dated snapshot folders
    for snapshot_dir in references_dir.iterdir():
        if not snapshot_dir.is_dir():
            continue

        # Read all markdown files in this snapshot
        for md_file in snapshot_dir.glob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8")

                # Extract job_url from frontmatter
                if content.startswith("---"):
                    frontmatter_end = content.find("---", 3)
                    if frontmatter_end != -1:
                        frontmatter = content[3:frontmatter_end]
                        for line in frontmatter.split("\n"):
                            if line.startswith("job_url:"):
                                job_url = line.split(":", 1)[1].strip().strip('"')
                                # Store the entire content for comparison
                                previous_jobs[job_url] = content
                                break
            except Exception as e:
                print(f"Warning: Failed to read {md_file}: {e}", file=sys.stderr)
                continue

    return previous_jobs


def write_job_to_markdown(job: JobListing, output_dir: Path) -> Path:
    """
    Write a job listing to a markdown file.

    Args:
        job: Job listing to write
        output_dir: Directory to write the file to

    Returns:
        Path to the created markdown file
    """
    # Create filename from job title
    filename = f"{slugify(job.title)}.md"
    filepath = output_dir / filename

    # Prepare markdown content
    content = f"""---
job_url: "{job.url}"
accessed_date: "{datetime.now().strftime('%Y-%m-%d')}"
company: "{job.company}"
role: "{job.title}"
location: "{job.location}"
"""

    if job.department:
        content += f'department: "{job.department}"\n'
    if job.employment_type:
        content += f'employment_type: "{job.employment_type}"\n'

    content += "---\n\n"
    content += f"# {job.title}\n\n"

    if job.description:
        content += job.description
    else:
        content += f"*Description not available. Visit the [job posting]({job.url}) for full details.*\n"

    # Write to file
    filepath.write_text(content, encoding="utf-8")
    return filepath


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: uv run python -m src.fetch_jobs <url> [--company NAME] [--fetch-descriptions]")
        print()
        print("Examples:")
        print("  uv run python -m src.fetch_jobs https://jobs.lever.co/wintermute-trading")
        print("  uv run python -m src.fetch_jobs https://jobs.lever.co/wintermute-trading --company Wintermute --fetch-descriptions")
        sys.exit(1)

    url = sys.argv[1]

    # Parse optional arguments
    company = None
    fetch_descriptions = False

    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == "--company" and i + 1 < len(sys.argv):
            company = sys.argv[i + 1]
        elif arg == "--fetch-descriptions":
            fetch_descriptions = True

    # Run scraper
    result = asyncio.run(scrape_careers_page(url, company, fetch_descriptions))

    # Determine output directory structure
    # Navigate up to the project root (documents.resume)
    # From: .claude/skills/job-quest/jq-search-jobs/src/fetch_jobs.py
    # Go up 6 levels: src -> jq-search-jobs -> job-quest -> skills -> .claude -> documents.resume
    script_dir = Path(__file__).parent.parent.parent.parent.parent.parent
    job_applications_dir = script_dir / "job_applications"
    company_slug = slugify(result.company)
    company_dir = job_applications_dir / company_slug
    references_dir = company_dir / "references"
    today = datetime.now().strftime('%Y-%m-%d')
    snapshot_dir = references_dir / today

    # Create snapshot directory
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    # Load all previously saved jobs for delta detection
    previous_jobs = load_previous_jobs(references_dir)

    # Process jobs and detect deltas
    new_jobs = []
    changed_jobs = []
    unchanged_jobs = []
    written_files = []

    for job in result.jobs:
        # Generate the content that would be written
        # (we need this to compare with previous versions)
        filename = f"{slugify(job.title)}.md"
        filepath = snapshot_dir / filename

        content = f"""---
job_url: "{job.url}"
accessed_date: "{today}"
company: "{job.company}"
role: "{job.title}"
location: "{job.location}"
"""
        if job.department:
            content += f'department: "{job.department}"\n'
        if job.employment_type:
            content += f'employment_type: "{job.employment_type}"\n'

        content += "---\n\n"
        content += f"# {job.title}\n\n"

        if job.description:
            content += job.description
        else:
            content += f"*Description not available. Visit the [job posting]({job.url}) for full details.*\n"

        # Check if this job exists in previous snapshots
        if job.url in previous_jobs:
            # Job existed before - check if content changed
            previous_content = previous_jobs[job.url]

            # Normalize for comparison (ignore accessed_date differences)
            def normalize_content(c: str) -> str:
                # Remove accessed_date line for comparison
                lines = c.split('\n')
                return '\n'.join(l for l in lines if not l.startswith('accessed_date:'))

            if normalize_content(content) == normalize_content(previous_content):
                # Content is identical - skip writing
                unchanged_jobs.append(job.title)
                continue
            else:
                # Content changed - write the update
                changed_jobs.append(job.title)
        else:
            # Brand new job - write it
            new_jobs.append(job.title)

        # Write the file (either new or changed)
        filepath.write_text(content, encoding="utf-8")
        written_files.append(filepath)

    # Print summary to stdout
    total_fetched = len(result.jobs)
    total_written = len(written_files)
    total_skipped = len(unchanged_jobs)

    print(f"✓ Fetched {total_fetched} jobs from {result.company} ({result.platform})")
    print(f"✓ New jobs: {len(new_jobs)}")
    print(f"✓ Changed jobs: {len(changed_jobs)}")
    print(f"✓ Unchanged (skipped): {total_skipped}")
    print(f"✓ Written {total_written} files to: {snapshot_dir}")

    if result.error:
        print(f"⚠ Error: {result.error}", file=sys.stderr)


if __name__ == "__main__":
    main()
