# main.py
from flask import Flask, jsonify
from scraper.qantas_scraper import scrape_products

points_sale_url = "https://wine.qantas.com/c/browse-products?OnSale=1&sort=brand-asc"
bonus_points_url = "https://wine.qantas.com/c/browse-products?BonusPoints=1&sort=brand-asc"

app = Flask(__name__)

@app.route("/points-sale", methods=["GET"])
def get_points_sale():
    return jsonify(scrape_products(points_sale_url))

@app.route("/bonus-points", methods=["GET"])
def get_bonus_points():
    return jsonify(scrape_products(bonus_points_url))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
