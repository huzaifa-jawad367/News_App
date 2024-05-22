from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
import os
import json
import random
from Searching.search import query_documents
import pysolr
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route("/home")
def home():
    directory = "data/nela-gt-2021/newsdata/train"

    all_files = os.listdir(directory)
    json_files = [file for file in all_files if file.endswith('.json')]
    selected_files = random.sample(json_files, 5)
    featured_articles = []
    for file in selected_files:
        file_path = os.path.join(directory, file)
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            random_dict = random.choice(data)
            featured_articles.append(random_dict)
    
    print(featured_articles)  # Debugging line
    return render_template("index.html", articles=featured_articles)

@app.route("/search_page")
def search_page():
    return render_template("search.html")

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    # Add your search functionality here

    results = query_documents(query)

    return render_template('search_results.html', results=results, q=query)

@app.route('/upload', methods=['POST'])
def upload_article():
    article = {
        "id": request.form['id'],
        "date": request.form['date'],
        "source": request.form['source'],
        "title": request.form['title'],
        "content": request.form['content'],
        "author": request.form['author'],
        "url": request.form['url'],
        "published": request.form['published'],
        "published_utc": request.form['published_utc'],
        "collection_utc": request.form['collection_utc']
    }

    print('article:', article['id'])
    
    solr_url = 'http://localhost:8983/solr'  # Replace with your Solr URL
    collection_name = 'nela-2021'
    solr = pysolr.Solr(f'{solr_url}/{collection_name}', always_commit=True, timeout=10)
    solr.add([article])
    # flash('Article has been successfully added!')
    flash('Article has been successfully added!', 'success')
    print('Article added successfully')
    return redirect(url_for('index'))

@app.route('/upload_form')
def upload_form():
    return render_template('update_form.html')

if __name__ == '__main__':
    app.run(debug=True)
