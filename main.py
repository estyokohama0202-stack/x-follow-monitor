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

    embeds = []

    if added:
        embeds.append({
            "title": "🟢 DJSHIGEが新しくフォローしました",
            "description": "\n".join([f"[{u}](https://x.com/{u})" for u in added]),
            "color": 5763719,
            "footer": {"text": "Follow Monitor"}
        })

    if removed:
        embeds.append({
            "title": "🔴 DJSHIGEがフォロー解除しました",
            "description": "\n".join([f"[{u}](https://x.com/{u})" for u in removed]),
            "color": 15548997,
            "footer": {"text": "Follow Monitor"}
        })

    payload = {
        "content": "📡 フォロー変化検知",
        "embeds": embeds
    }

    requests.post(WEBHOOK, json=payload)

def main():
    for _ in range(3):
        try:
            old = load_old()
            new = get_following()

            # 初回だけ「最新1人だけ通知」
            if not old:
                if new:
                    notify([new[0]], [])
                save(new)
                return

            added = list(set(new) - set(old))

            # 新規があれば「一番上だけ通知」
            if added:
                latest = new[0]  # ←ここがポイント
                notify([latest], [])

            save(new)
            return

        except Exception as e:
            print("エラー:", e)
            time.sleep(10)

    print("3回失敗")
print("OLD:", old[:5])
print("NEW:", new[:5])
print("ADDED:", added if 'added' in locals() else "初回")

if __name__ == "__main__":
    main()
