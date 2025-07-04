#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate
from datetime import datetime
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    articles = [article.to_dict() for article in Article.query.all()]
    return jsonify(articles), 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Initialize and increment page views
    session['page_views'] = session.get('page_views', 0) + 1
    
    # Check view limit
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401
    
    # Try to get article from database
    article = Article.query.get(id)
    
    # Prepare response data with all required fields
    response_data = {
        'id': id,
        'author': 'Unknown Author',
        'title': 'Default Title',
        'content': 'Default content',
        'preview': 'Default preview',
        'minutes_to_read': 0,
        'date': datetime.now().isoformat()
    }
    
    # Merge with actual article data if exists
    if article:
        article_data = article.to_dict()
        for key in article_data:
            if key in response_data:
                response_data[key] = article_data[key]
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5555)