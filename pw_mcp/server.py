from __future__ import annotations

from textwrap import dedent
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pw-context-python", json_response=True)

# 1) Resource (context)


@mcp.resource("playwright://testing-guide")
def playwright_testing_guide() -> str:
    return dedent(
        """
        # Playwright + Pytest Tests-Only Guide

        - This repo contains TESTS ONLY. Do not generate application/backend code.
        - Prefer stable locators: get_by_role(), get_by_label(), data-testid when available.
        - Avoid time.sleep(). Use Playwright auto-waits + expect assertions.
        - Keep tests deterministic and independent.

        Corporate network note:
        - If Playwright browser downloads are blocked, launch installed Chrome via executable_path.
        - Avoid record_video_dir unless FFmpeg is available.
        """
    ).strip()

# 2) Tool (returns sample code)


@mcp.tool()
def generate_playwright_pytest_test(
    test_name: str,
    base_url: str = "https://example.com",
    use_installed_chrome: bool = True
) -> dict:
    code = dedent(
        f"""
        import os
        from playwright.sync_api import sync_playwright, Playwright, Browser, expect

        def _launch_browser(playwright: Playwright) -> Browser:
            if {use_installed_chrome}:
                chrome_path = os.environ.get(
                    "CHROME_PATH",
                    r"C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe",
                )
                return playwright.chromium.launch(
                    executable_path=chrome_path,
                    headless=False,
                    args=["--start-maximized"],
                )
            return playwright.chromium.launch(headless=False)

        def test_{test_name}():
            base_url = os.environ.get("BASE_URL", "{base_url}")

            with sync_playwright() as p:
                browser = _launch_browser(p)
                context = browser.new_context(viewport=None)
                page = context.new_page()

                page.goto(base_url)

                # TODO: replace with real steps
                # page.get_by_role("button", name="Submit").click()

                expect(page).to_have_url(base_url)

                context.close()
                browser.close()
        """
    ).strip()

    return {
        "suggested_path": f"tests/test_{test_name}.py",
        "language": "python",
        "code": code,
        "notes": [
            "sync_api + pytest style test template",
            "uses installed Chrome via CHROME_PATH (good for restricted networks)"
        ]
    }

# 3) Prompt (template)


@mcp.prompt()
def create_playwright_test(feature: str, url: str = "") -> str:
    target = f" Target URL: {url}." if url else ""
    return (
        f"Create a Playwright (Python sync_api) pytest test for: {feature}.{target} "
        "Use stable locators (get_by_role/get_by_label), avoid sleeps, and include assertions."
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
