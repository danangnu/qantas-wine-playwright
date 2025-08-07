# Qantas Wine Scraper API

A Python Flask API that scrapes wine product data from [Qantas Wine](https://wine.qantas.com) using Playwright.

---

## 📦 Features

* Headless or non-headless Playwright support
* Navigates through paginated product listings
* Extracts brand, details, price, points, bonus points, quantity, and product URL
* Outputs results in JSON format via a simple `/products` API endpoint

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/qantas-wine-scraper.git
cd qantas-wine-scraper
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
playwright install
```

### 4. Run the Flask API

```bash
python main.py
```

Then open in your browser: [http://localhost:5000/products](http://localhost:5000/products)

---

## ⚙️ Configuration

### Australian Proxy Support (Optional)

Edit `scraper/qantas_scraper.py` and set:

```python
PROXY_SERVER = "http://your-au-proxy:port"
PROXY_USERNAME = "your_username"
PROXY_PASSWORD = "your_password"
```

Leave blank or comment out if not using proxy.

### Headless Mode

Change:

```python
browser = p.chromium.launch(headless=True)
```

---

## 📋 Output Sample

```json
[
  {
    "product_name": "Alkina",
    "qty": 6,
    "price": "$120",
    "points": "19876 pts",
    "url": "https://wine.qantas.com/product?selected=6",
    "details": "Striato Shiraz 2022"
  }
]
```

---

## 🧾 License

MIT License
