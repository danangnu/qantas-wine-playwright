# main.py
from flask import Flask, jsonify
from scraper.qantas_scraper import scrape_products

app = Flask(__name__)

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(scrape_products())

if __name__ == "__main__":
    app.run(debug=True, port=5000)
