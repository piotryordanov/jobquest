"""Job board scrapers for various ATS platforms."""

import asyncio
from typing import Protocol

from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError

from src.models import JobListing


class JobScraper(Protocol):
    """Protocol for job board scrapers."""

    async def scrape(self, page: Page, url: str, company: str) -> list[JobListing]:
        """Scrape jobs from a careers page."""
        ...


class LeverScraper:
    """Scraper for Lever ATS (jobs.lever.co)."""

    async def scrape(self, page: Page, url: str, company: str) -> list[JobListing]:
        """
        Scrape jobs from a Lever careers page.

        Args:
            page: Playwright page instance
            url: URL to scrape (e.g., https://jobs.lever.co/company-name)
            company: Company name

        Returns:
            List of JobListing objects
        """
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
        except PlaywrightTimeoutError:
            # Try with domcontentloaded if networkidle times out
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Wait for job listings to load
        try:
            await page.wait_for_selector(".posting", timeout=10000)
        except PlaywrightTimeoutError:
            # No jobs found or different structure
            return []

        # Extract all job listings
        jobs_data = await page.evaluate("""
            () => {
                const listings = Array.from(document.querySelectorAll('.posting'));
                return listings.map(posting => {
                    const titleEl = posting.querySelector('.posting-title h5');
                    const linkEl = posting.querySelector('a.posting-title');
                    const categoriesEl = posting.querySelector('.posting-categories');

                    // Extract location and department from categories
                    let location = null;
                    let department = null;

                    if (categoriesEl) {
                        const locationEl = categoriesEl.querySelector('.location');
                        const departmentEl = categoriesEl.querySelector('.department, .team');

                        location = locationEl ? locationEl.textContent.trim() : null;
                        department = departmentEl ? departmentEl.textContent.trim() : null;
                    }

                    return {
                        title: titleEl ? titleEl.textContent.trim() : null,
                        url: linkEl ? linkEl.href : null,
                        location: location,
                        department: department
                    };
                }).filter(job => job.title && job.url);
            }
        """)

        return [
            JobListing(
                title=job["title"],
                location=job["location"],
                url=job["url"],
                department=job["department"],
                company=company,
                source=url,
            )
            for job in jobs_data
        ]


class GreenhouseScraper:
    """Scraper for Greenhouse ATS (boards.greenhouse.io)."""

    async def scrape(self, page: Page, url: str, company: str) -> list[JobListing]:
        """Scrape jobs from a Greenhouse careers page."""
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
        except PlaywrightTimeoutError:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Wait for job sections
        try:
            await page.wait_for_selector(".opening", timeout=10000)
        except PlaywrightTimeoutError:
            return []

        jobs_data = await page.evaluate("""
            () => {
                const listings = Array.from(document.querySelectorAll('.opening'));
                return listings.map(opening => {
                    const linkEl = opening.querySelector('a');
                    const locationEl = opening.querySelector('.location');

                    return {
                        title: linkEl ? linkEl.textContent.trim() : null,
                        url: linkEl ? linkEl.href : null,
                        location: locationEl ? locationEl.textContent.trim() : null
                    };
                }).filter(job => job.title && job.url);
            }
        """)

        return [
            JobListing(
                title=job["title"],
                location=job["location"],
                url=job["url"],
                company=company,
                source=url,
            )
            for job in jobs_data
        ]


class AshbyScraper:
    """Scraper for Ashby ATS (jobs.ashbyhq.com)."""

    async def scrape(self, page: Page, url: str, company: str) -> list[JobListing]:
        """Scrape jobs from an Ashby careers page."""
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
        except PlaywrightTimeoutError:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Ashby uses different selectors - this is a generic approach
        try:
            await page.wait_for_selector("a[href*='/jobs/']", timeout=10000)
        except PlaywrightTimeoutError:
            return []

        jobs_data = await page.evaluate("""
            () => {
                const jobLinks = Array.from(document.querySelectorAll("a[href*='/jobs/']"));
                const uniqueJobs = new Map();

                jobLinks.forEach(link => {
                    const url = link.href;
                    if (!uniqueJobs.has(url)) {
                        const title = link.textContent.trim();
                        // Try to find location nearby
                        let location = null;
                        const parent = link.closest('div');
                        if (parent) {
                            const locationText = parent.textContent;
                            // Simple heuristic: look for common location indicators
                            const locationMatch = locationText.match(/(Remote|Hybrid|On-site|[A-Z][a-z]+,\\s*[A-Z]{2}|[A-Z][a-z]+\\s*-\\s*[A-Z][a-z]+)/);
                            if (locationMatch) {
                                location = locationMatch[0];
                            }
                        }

                        uniqueJobs.set(url, {
                            title: title,
                            url: url,
                            location: location
                        });
                    }
                });

                return Array.from(uniqueJobs.values()).filter(job => job.title && job.url);
            }
        """)

        return [
            JobListing(
                title=job["title"],
                location=job["location"],
                url=job["url"],
                company=company,
                source=url,
            )
            for job in jobs_data
        ]


class GenericScraper:
    """Fallback scraper for unknown ATS platforms."""

    async def scrape(self, page: Page, url: str, company: str) -> list[JobListing]:
        """
        Generic scraping attempt for unknown platforms.
        Looks for common patterns in job listings.
        """
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
        except PlaywrightTimeoutError:
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # Wait a bit for dynamic content
        await asyncio.sleep(2)

        jobs_data = await page.evaluate("""
            () => {
                // Look for common job listing patterns
                const potentialSelectors = [
                    'a[href*="/job"]',
                    'a[href*="/jobs"]',
                    'a[href*="/position"]',
                    'a[href*="/careers"]',
                    'a[href*="/apply"]',
                    '.job-listing a',
                    '.job-item a',
                    '.position a',
                    '[class*="job"] a',
                ];

                const uniqueJobs = new Map();

                for (const selector of potentialSelectors) {
                    const links = document.querySelectorAll(selector);
                    links.forEach(link => {
                        const url = link.href;
                        const title = link.textContent.trim();

                        // Filter out navigation links and very short titles
                        if (title.length > 5 && !title.match(/^(Home|About|Contact|Login|Sign|Menu|Back)$/i)) {
                            uniqueJobs.set(url, {
                                title: title,
                                url: url,
                                location: null
                            });
                        }
                    });
                }

                return Array.from(uniqueJobs.values());
            }
        """)

        return [
            JobListing(
                title=job["title"],
                location=job["location"],
                url=job["url"],
                company=company,
                source=url,
            )
            for job in jobs_data
        ]


def detect_platform(url: str) -> str:
    """
    Detect ATS platform from URL.

    Args:
        url: Careers page URL

    Returns:
        Platform name: 'lever', 'greenhouse', 'ashby', 'workday', or 'generic'
    """
    url_lower = url.lower()

    if "lever.co" in url_lower:
        return "lever"
    elif "greenhouse.io" in url_lower or "grnh.se" in url_lower:
        return "greenhouse"
    elif "ashbyhq.com" in url_lower:
        return "ashby"
    elif "myworkdayjobs.com" in url_lower:
        return "workday"
    else:
        return "generic"


def get_scraper(platform: str) -> JobScraper:
    """
    Get appropriate scraper for platform.

    Args:
        platform: Platform name from detect_platform()

    Returns:
        Scraper instance
    """
    scrapers = {
        "lever": LeverScraper(),
        "greenhouse": GreenhouseScraper(),
        "ashby": AshbyScraper(),
        "generic": GenericScraper(),
    }

    return scrapers.get(platform, GenericScraper())
