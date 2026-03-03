import json
import os
import time
import requests
from playwright.sync_api import sync_playwright

USERNAME = "shizenboueigun"

LOGIN_ID = os.getenv("X_ID")
LOGIN_PASS = os.getenv("X_PASS")
WEBHOOK = os.getenv("DISCORD_WEBHOOK")


def login(page):
    page.goto("https://x.com/login")
    page.wait_for_timeout(3000)

    page.fill('input[name="text"]', LOGIN_ID)
    page.keyboard.press("Enter")
    page.wait_for_timeout(3000)

    page.fill('input[name="password"]', LOGIN_PASS)
    page.keyboard.press("Enter")
    page.wait_for_timeout(5000)


def scroll(page):
    last_height = 0
    for _ in range(15):  # スクロール回数（調整可）
        page.mouse.wheel(0, 3000)
        time.sleep(2)

        height = page.evaluate("document.body.scrollHeight")
        if height == last_height:
            break
        last_height = height


def get_following():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        login(page)

        page.goto(f"https://x.com/{USERNAME}/following")
        page.wait_for_timeout(5000)

        scroll(page)

        links = page.locator('a[href^="/"]').all()
        users = []

        for l in links:
            href = l.get_attribute("href")
            if href and href.count("/") == 1:
                users.append(href.replace("/", ""))

        browser.close()
        return list(set(users))


def load_old():
    if os.path.exists("data.json"):
        with open("data.json", "r") as f:
            return json.load(f)
    return []


def save(data):
    with open("data.json", "w") as f:
        json.dump(data, f)


def notify(added, removed):
    if not added and not removed:
        return

    msg = ""

    if added:
        msg += "🆕 フォロー追加:\n" + "\n".join(added) + "\n\n"

    if removed:
        msg += "❌ フォロー解除:\n" + "\n".join(removed)

    requests.post(WEBHOOK, json={"content": msg})


def main():
    for _ in range(3):  # リトライ
        try:
            old = load_old()
            new = get_following()

            added = list(set(new) - set(old))
            removed = list(set(old) - set(new))

            notify(added, removed)
            save(new)
            return

        except Exception as e:
            print("エラー:", e)
            time.sleep(10)

    print("3回失敗")


if __name__ == "__main__":
    main()
