from flask import Flask, jsonify, request
from scraper import get_latest_manga, get_recent_manga, get_all_titles, search_titles, get_categories

app = Flask(__name__)

@app.route('/latest', methods=['GET'])
def latest():
    page = request.args.get('page', default=1, type=int)
    data = get_latest_manga(page)
    return jsonify(data)

@app.route('/recent', methods=['GET'])
def recent():
    page = request.args.get('page', default=1, type=int)
    data = get_recent_manga(page)
    return jsonify(data)

@app.route('/titles', methods=['GET'])
def titles():
    page = request.args.get('page', default=1, type=int)
    category = request.args.get('category', default=None, type=str)
    data = get_all_titles(page, category)
    return jsonify(data)

@app.route('/titles/search', methods=['GET'])
def search():
    query = request.args.get('q')
    page = request.args.get('page', default=1, type=int)

    if not query:
        return jsonify({"error": "Missing 'q' parameter"}), 400

    data = search_titles(query, page)
    return jsonify(data)

@app.route('/categories', methods=['GET'])
def categories():
    data = get_categories()
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
