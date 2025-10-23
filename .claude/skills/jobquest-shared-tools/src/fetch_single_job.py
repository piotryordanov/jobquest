"""
Fetch a single job description from a URL.

Usage:
    uv run python -m src.fetch_single_job <job_url>

Example:
    uv run python -m src.fetch_single_job https://jobs.lever.co/wintermute-trading/a2e875dc-be19-4c4e-b933-951a15528355
"""

import asyncio
import sys
from playwright.async_api import async_playwright


async def fetch_job_description(url: str) -> dict[str, str]:
    """
    Fetch job description from a single job posting URL.

    Returns:
        Dictionary with job metadata and description
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Extract job details from the page
            job_data = await page.evaluate("""
                () => {
                    // Get title
                    const titleEl = document.querySelector('.posting-headline h2, h1');
                    const title = titleEl ? titleEl.textContent.trim() : '';

                    // Get location
                    const locationEl = document.querySelector('.location, .posting-categories .location');
                    const location = locationEl ? locationEl.textContent.trim() : '';

                    // Get employment type
                    const typeEl = document.querySelector('.commitment, .posting-categories .commitment');
                    const employment_type = typeEl ? typeEl.textContent.trim() : '';

                    // Get department
                    const deptEl = document.querySelector('.team, .posting-categories .team');
                    const department = deptEl ? deptEl.textContent.trim() : '';

                    // Get company name from title or meta
                    const companyEl = document.querySelector('.main-header-text-company-logo, meta[property="og:site_name"]');
                    const company = companyEl ? (companyEl.getAttribute('content') || companyEl.textContent.trim()) : '';

                    // Get full description - try multiple selectors
                    let description = '';
                    const descSelectors = [
                        '.posting-description',
                        '.description',
                        '.content.description',
                        '[class*="description"]'
                    ];

                    for (const selector of descSelectors) {
                        const el = document.querySelector(selector);
                        if (el && el.textContent.length > 100) {
                            // Get HTML content to preserve formatting
                            description = el.innerHTML;
                            break;
                        }
                    }

                    // If still no description, try to get the main content area
                    if (!description) {
                        const mainEl = document.querySelector('main, .posting-page, .job-posting');
                        if (mainEl) {
                            description = mainEl.innerHTML;
                        }
                    }

                    // Clean up HTML - convert to markdown-ish format
                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = description;

                    // Extract text with basic formatting
                    const textContent = tempDiv.textContent || tempDiv.innerText || '';

                    return {
                        title,
                        location,
                        employment_type,
                        department,
                        company,
                        description: textContent.trim()
                    };
                }
            """)

            await browser.close()
            return job_data

        except Exception as e:
            await browser.close()
            raise Exception(f"Failed to fetch job: {e}")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: uv run python -m src.fetch_single_job <job_url>")
        print()
        print("Example:")
        print("  uv run python -m src.fetch_single_job https://jobs.lever.co/wintermute-trading/a2e875dc-be19-4c4e-b933-951a15528355")
        sys.exit(1)

    url = sys.argv[1]

    try:
        job_data = asyncio.run(fetch_job_description(url))

        # Print as JSON for easy parsing
        import json
        print(json.dumps(job_data, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
