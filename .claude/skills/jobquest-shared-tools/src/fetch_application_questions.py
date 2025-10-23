"""
Fetch application form questions from a job posting URL.

Usage:
    uv run python -m src.fetch_application_questions <job_url>

Example:
    uv run python -m src.fetch_application_questions https://jobs.lever.co/wintermute-trading/a2e875dc-be19-4c4e-b933-951a15528355
"""

import asyncio
import sys
from playwright.async_api import async_playwright


async def fetch_application_questions(url: str) -> dict:
    """
    Navigate to job posting and extract application form questions.

    Returns:
        Dictionary with application form questions and fields
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            # Go to the job posting page
            await page.goto(url, wait_until="networkidle", timeout=30000)

            # Look for "Apply" button and click it
            apply_button_selectors = [
                'a.postings-btn.template-btn-submit',
                'a[href*="apply"]',
                'button:has-text("Apply")',
                'a:has-text("Apply")',
                '.apply-button',
                '.posting-apply-button'
            ]

            apply_clicked = False
            for selector in apply_button_selectors:
                try:
                    button = page.locator(selector).first
                    if await button.count() > 0:
                        await button.click()
                        apply_clicked = True
                        # Wait for form to load
                        await page.wait_for_timeout(2000)
                        break
                except:
                    continue

            if not apply_clicked:
                # Maybe we're already on the application page
                print("Note: Could not find apply button, checking current page for form", file=sys.stderr)

            # Extract application form questions
            form_data = await page.evaluate("""
                () => {
                    const allQuestions = [];

                    // Try to get the question cards which contain textareas
                    const questionCards = document.querySelectorAll('.application-question');

                    questionCards.forEach((card, index) => {
                        const question = {};

                        // Get the label - try multiple strategies
                        let labelText = '';

                        // Strategy 1: Look for label element
                        const labelEl = card.querySelector('label');
                        if (labelEl) {
                            labelText = labelEl.textContent.trim();
                        }

                        // Strategy 2: Look for .application-label
                        if (!labelText) {
                            const appLabel = card.querySelector('.application-label');
                            if (appLabel) {
                                labelText = appLabel.textContent.trim();
                            }
                        }

                        // Strategy 3: Look for any text before the input
                        if (!labelText) {
                            const textNodes = [];
                            card.childNodes.forEach(node => {
                                if (node.nodeType === 3 && node.textContent.trim()) {
                                    textNodes.push(node.textContent.trim());
                                }
                            });
                            if (textNodes.length > 0) {
                                labelText = textNodes[0];
                            }
                        }

                        // Get input element
                        const input = card.querySelector('input, textarea, select');
                        if (input) {
                            question.label = labelText || `Question ${index + 1}`;
                            question.type = input.tagName.toLowerCase();
                            question.inputType = input.type || (input.tagName.toLowerCase() === 'textarea' ? 'textarea' : 'text');
                            question.name = input.name || '';
                            question.required = input.required || input.getAttribute('aria-required') === 'true' || labelText.includes('✱') || labelText.includes('*');
                            question.placeholder = input.placeholder || '';

                            // For select, get options
                            if (input.tagName.toLowerCase() === 'select') {
                                question.options = Array.from(input.querySelectorAll('option'))
                                    .map(opt => opt.textContent.trim())
                                    .filter(opt => opt);
                            }

                            allQuestions.push(question);
                        }
                    });

                    // Get all visible text to help understand the form
                    const formText = document.querySelector('.application-form, form')?.textContent || '';

                    return {
                        questions: allQuestions,
                        totalQuestions: allQuestions.length,
                        url: window.location.href,
                        formPreview: formText.slice(0, 500)
                    };
                }
            """)

            await browser.close()
            return form_data

        except Exception as e:
            await browser.close()
            raise Exception(f"Failed to fetch application questions: {e}")


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: uv run python -m src.fetch_application_questions <job_url>")
        print()
        print("Example:")
        print("  uv run python -m src.fetch_application_questions https://jobs.lever.co/wintermute-trading/a2e875dc-be19-4c4e-b933-951a15528355")
        sys.exit(1)

    url = sys.argv[1]

    try:
        form_data = asyncio.run(fetch_application_questions(url))

        # Print as JSON for easy parsing
        import json
        print(json.dumps(form_data, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
