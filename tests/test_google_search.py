import os
from playwright.sync_api import sync_playwright, Playwright, Browser, expect


def launch_installed_chrome(playwright: Playwright) -> Browser:
    chrome_path = os.environ.get(
        "CHROME_PATH",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    )

    return playwright.chromium.launch(
        executable_path=chrome_path,
        headless=False,
        args=["--start-maximized"]
    )


def run_google_search():
    with sync_playwright() as p:
        browser = launch_installed_chrome(p)
        context = browser.new_context(viewport=None)
        page = context.new_page()

        print("Opening Google...")
        page.goto("https://www.google.com")

        # Accept cookies if popup appears (Google sometimes shows it)
        try:
            page.get_by_role("button", name="Accept all").click(timeout=3000)
        except:
            pass

        print("Searching for Playwright...")
        page.get_by_role("textbox", name="Search").fill("Playwright Python")
        page.keyboard.press("Enter")

        # Wait for results
        expect(page).to_have_title(lambda t: "Playwright" in t)

        page.wait_for_timeout(5000)  # So you can see results

        context.close()
        browser.close()


# ------------------------------
# Pytest test version
# ------------------------------
def test_google_search():
    run_google_search()


# ------------------------------
# Standalone script version
# ------------------------------
def main():
    run_google_search()


if __name__ == "__main__":
    main()
