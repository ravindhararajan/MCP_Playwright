import os
import time
from playwright.sync_api import sync_playwright


def launch_installed_chrome(playwright):
    """
    Launch system-installed Chrome instead of Playwright-downloaded Chromium.
    Helps in corporate networks where downloads are blocked.
    """
    chrome_path = os.environ.get(
        "CHROME_PATH",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    )

    if not os.path.exists(chrome_path):
        raise FileNotFoundError(
            f"Chrome not found at {chrome_path}. Set CHROME_PATH environment variable."
        )

    return playwright.chromium.launch(
        executable_path=chrome_path,
        headless=False,
        args=["--start-maximized"]
    )


def main():
    with sync_playwright() as p:
        browser = launch_installed_chrome(p)
        context = browser.new_context(viewport=None)
        page = context.new_page()

        print("Opening Google...")
        page.goto("https://www.google.com")

        # Wait so you can see the browser open
        time.sleep(5)

        context.close()
        browser.close()


if __name__ == "__main__":
    main()
