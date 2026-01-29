import os
from playwright.sync_api import sync_playwright, Playwright, Browser, expect


def _launch_browser(playwright: Playwright) -> Browser:
    if True:
        chrome_path = os.environ.get(
            "CHROME_PATH",
            r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        )
        return playwright.chromium.launch(
            executable_path=chrome_path,
            headless=False,
            args=["--start-maximized"],
        )
    return playwright.chromium.launch(headless=False)


def test_example_homepage():
    base_url = os.environ.get("BASE_URL", "https://example.com\\n")

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
