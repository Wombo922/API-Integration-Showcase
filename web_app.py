from flask import Flask, render_template, jsonify, request
from app import Dashboard

app = Flask(__name__)
dashboard = Dashboard()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    """API endpoint to get dashboard data"""
    category = request.args.get('category', 'technology')
    data = dashboard.fetch_all_data(use_cache=True, news_category=category)
    return jsonify(data)

@app.route('/api/refresh')
def refresh_data():
    """Force refresh data"""
    category = request.args.get('category', 'technology')
    data = dashboard.fetch_all_data(use_cache=False, news_category=category)
    return jsonify(data)

if __name__ == '__main__':
    # For local development only
    # In production, use a WSGI server like Gunicorn or uWSGI
    import os
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, port=7000)
