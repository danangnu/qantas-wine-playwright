from flask import Flask, jsonify
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import re

app = Flask(__name__)

# Set your Australian proxy here (if needed)
PROXY_SERVER = "http://your-au-proxy:port"  # Example: http://au.proxy.com:8000
PROXY_USERNAME = "your_proxy_username"
PROXY_PASSWORD = "your_proxy_password"

TARGET_URL = "https://wine.qantas.com/c/browse-products?OnSale=1&sort=brand-asc"

@app.route("/products", methods=["GET"])
def scrape_products():
    j_results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--disable-http2"])  # Headful = fewer blocks

        page = browser.new_page()
        
        page.goto(TARGET_URL, timeout=60000)

        page_count = 1
        max_retry = 3
        retry = 0

        page.wait_for_selector("#__next", timeout=60000)

        if "no products found." in page.inner_text("#__next").lower():
            return

        while True:
            try:
                product_cards = page.query_selector_all("//div[contains(@data-testid, 'product-details-')]/parent::a[contains(@class, 'sc-')]/parent::div[contains(@class, 'sc-')]")

                for r in product_cards:
                    qty_elements = r.query_selector_all("a[class*='sc-'] div[class*='sc-'] div[class*='sc-'] p")
                    qty = 0
                    iqty = 0
                    print(f"Product Len: {len(qty_elements)}")

                    while iqty < len(qty_elements):
                        try:
                            text = qty_elements[iqty].inner_text().strip()
                            if text.isnumeric():
                                qty = int(text)
                        except:
                            qty = 0

                        if qty == 0:
                            continue

                        print(f"Product Qty: {qty}")
                        # while iqty < len(qty_elements):

                        # Link
                        href = ""
                        link_el = r.query_selector("a")
                        link = ""
                        if link_el:
                            href = link_el.get_attribute("a")
                            if href:
                                link = href + "?selected=" + str(qty)

                        # Bonus points
                        bonus_points = ""
                        bonus_el = r.query_selector("a span[class*='sc-']")
                        if bonus_el:
                            txt = bonus_el.inner_text().lower()
                            if "bonus points" in txt:
                                number = re.sub(r"[^\d]", "", txt)
                                if number.isnumeric():
                                    bonus_points = txt

                        # Product name
                        product_name = ""
                        name_el = r.query_selector("a[class*='sc-'] div[data-testid*='product-details-'] div[class*='sc-'] div h4[data-yieldify-id='product-card-title']")
                        if name_el:
                            product_name = name_el.inner_text().strip()

                        # Details
                        details = ""
                        detail_el = r.query_selector("a[class*='sc-'] div[data-testid*='product-details-'] div[class*='sc-'] div span[class*='sc-']")
                        if detail_el:
                            details = detail_el.inner_text().strip()

                        # Price + Points
                        price = ""
                        pts = ""
                        price_els = r.query_selector_all("a[class*='sc-'] div[class*='sc-'] div[class*='sc-'] div[class*='sc-'] div[class*='sc-'] div[class*='sc-'] span[class*='sc-']")

                        for pe in price_els:
                            price_temp = pe.inner_text().strip().lower()

                            if price_temp.startswith("$") and not (price_temp.endswith(" per bottle")):
                                price = price_temp

                            if price_temp.endswith("pts"):
                                pts = price_temp

                        # print(f"Product: {product_name}, Qty: {qty}, Link: {href}")
                        j_results.append({
                            "product_name": product_name.strip() if product_name else None,
                            "qty": qty if qty else None,
                            "price": price.strip() if price else None,
                            "points": pts if pts else None,
                            "url": f"https://wine.qantas.com{link}" if link else None,
                            "details": details.strip() if details else None
                        })

                        iqty +=1

                next_button = page.locator("a[data-testid='page-next']")
                if not next_button.is_visible():
                    print("✅ No more pages.")
                    break
                
                try:
                    next_button.click(timeout=10000)
                    page_count += 1
                    time.sleep(3)  # simulate delay after click
                except PlaywrightTimeoutError as e:
                    retry += 1
                    print(f"⚠️ Retry {retry}/{max_retry} - Failed to click next: {e}")
                    if retry >= max_retry:
                        print("❌ Max retries reached. Exiting...")
                        break

            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                break

                browser.close()

    return jsonify(j_results)
if __name__ == "__main__":
    app.run(debug=True, port=5000)
