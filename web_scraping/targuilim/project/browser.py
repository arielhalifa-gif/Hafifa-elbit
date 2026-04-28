import os
import json
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


INPUT_FILE = os.path.join("input", "urls.input")
OUTPUT_DIR = "output"


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )

    # Enable network tracking via CDP
    driver.execute_cdp_cmd("Network.enable", {})
    return driver


def process_url(url, index):
    folder_name = f"url_{index}"
    folder_path = os.path.join(OUTPUT_DIR, folder_name)
    os.makedirs(folder_path, exist_ok=True)

    driver = setup_driver()
    resources = []

    def capture_requests(request):
        try:
            resources.append(request["request"]["url"])
        except Exception:
            pass

    # Hook into CDP events
    driver.execute_cdp_cmd("Network.enable", {})
    driver.execute_cdp_cmd(
        "Network.setCacheDisabled", {"cacheDisabled": True}
    )

    driver.get(url)

    # Collect resource URLs from performance logs
    logs = driver.get_log("performance")
    for entry in logs:
        try:
            message = json.loads(entry["message"])["message"]
            if message["method"] == "Network.requestWillBeSent":
                resources.append(message["params"]["request"]["url"])
        except Exception:
            continue

    # HTML content
    html = driver.page_source

    # Screenshot
    screenshot_path = os.path.join(folder_path, "screenshot.png")
    driver.save_screenshot(screenshot_path)

    # Base64 encode screenshot
    with open(screenshot_path, "rb") as img_file:
        screenshot_base64 = base64.b64encode(img_file.read()).decode("utf-8")

    # Remove duplicate resources
    resources = list(set(resources))

    # Save JSON
    output_data = {
        "html": html,
        "resources": resources,
        "screenshot": screenshot_base64
    }

    json_path = os.path.join(folder_path, "browse.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    driver.quit()


def read_urls():
    if not os.path.exists(INPUT_FILE):
        return []

    with open(INPUT_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    urls = read_urls()

    if not urls:
        print("No URLs found.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    max_workers = min(5, len(urls))  # limit threads

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_url, url, i + 1)
            for i, url in enumerate(urls)
        ]

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error processing URL: {e}")


if __name__ == "__main__":
    main()