"""Data models for job scraping."""

from msgspec import Struct


class JobListing(Struct, kw_only=True):
    """A job listing from a careers page."""

    title: str
    """Job title"""

    location: str | None = None
    """Location (e.g., 'Remote', 'London', 'New York')"""

    url: str
    """Direct URL to the full job posting"""

    description: str | None = None
    """Full job description (if fetched)"""

    department: str | None = None
    """Department or team (e.g., 'Engineering', 'Product')"""

    employment_type: str | None = None
    """Employment type (e.g., 'Full-time', 'Contract')"""

    company: str | None = None
    """Company name"""

    source: str | None = None
    """Source URL where this was found"""


class ScrapingResult(Struct, kw_only=True):
    """Result of scraping a careers page."""

    company: str
    """Company name"""

    source_url: str
    """URL that was scraped"""

    jobs: list[JobListing]
    """List of jobs found"""

    error: str | None = None
    """Error message if scraping failed"""

    platform: str | None = None
    """Detected ATS platform (e.g., 'lever', 'greenhouse')"""
