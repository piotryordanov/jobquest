"""
Find a company's careers page URL using Playwright web browsing.

Usage:
    uv run python -m src.find_careers_page "<Company Name>"

Example:
    uv run python -m src.find_careers_page "Wintermute"
"""

import asyncio
import sys
from urllib.parse import urlparse

from playwright.async_api import async_playwright


async def find_careers_page(company_name: str) -> str | None:
    """
    Find careers page URL for a company using web browsing.

    Args:
        company_name: Name of the company

    Returns:
        Careers page URL or None if not found
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Try common patterns first
        company_slug = company_name.lower().replace(" ", "-").replace(".", "")
        common_patterns = [
            f"https://{company_slug}.com/careers",
            f"https://{company_slug}.com/jobs",
            f"https://jobs.{company_slug}.com",
            f"https://careers.{company_slug}.com",
            f"https://jobs.lever.co/{company_slug}",
            f"https://jobs.lever.co/{company_slug}-trading",
            f"https://boards.greenhouse.io/{company_slug}",
            f"https://jobs.ashbyhq.com/{company_slug}",
        ]

        # Test each pattern
        for url in common_patterns:
            try:
                response = await page.goto(url, timeout=10000, wait_until="domcontentloaded")
                if response and response.ok:
                    # Check if it looks like a careers page
                    has_jobs = await page.evaluate("""
                        () => {
                            const text = document.body.textContent.toLowerCase();
                            return text.includes('job') ||
                                   text.includes('career') ||
                                   text.includes('position') ||
                                   text.includes('opening');
                        }
                    """)

                    if has_jobs:
                        await browser.close()
                        return url
            except Exception:
                # URL didn't work, try next one
                continue

        # If no common pattern worked, try Google search simulation
        try:
            search_url = f"https://www.google.com/search?q={company_name}+careers+jobs"
            await page.goto(search_url, timeout=15000, wait_until="domcontentloaded")

            # Extract first few search results
            careers_url = await page.evaluate("""
                () => {
                    const links = Array.from(document.querySelectorAll('a[href]'));

                    // Look for career-related links
                    for (const link of links) {
                        const href = link.href;
                        const text = link.textContent.toLowerCase();

                        if ((href.includes('careers') ||
                             href.includes('jobs') ||
                             href.includes('lever.co') ||
                             href.includes('greenhouse.io') ||
                             href.includes('ashbyhq.com')) &&
                            !href.includes('google.com')) {
                            return href;
                        }
                    }

                    return null;
                }
            """)

            await browser.close()
            return careers_url

        except Exception as e:
            await browser.close()
            return None


def main() -> None:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: uv run python -m src.find_careers_page \"<Company Name>\"")
        print()
        print("Example:")
        print('  uv run python -m src.find_careers_page "Wintermute"')
        sys.exit(1)

    company_name = sys.argv[1]

    # Find careers page
    careers_url = asyncio.run(find_careers_page(company_name))

    if careers_url:
        print(careers_url)
    else:
        print(f"Error: Could not find careers page for {company_name}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
