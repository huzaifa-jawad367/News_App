from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import json
import random
from Searching.search import query_documents

app = Flask(__name__)

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

    for result in results:
        print(f" - {result.get('id', 'No ID')}: {result.get('title', 'No title')}")
        print(f" - {result.get('id', 'No ID')}: {result.get('url', 'No url')}")
        # print(f"   Content: {result.get('content', 'No content')}")
        # print(f"   Score: {result.get('score', 'No score')}")
        print("-" * 40)

        ans = {'title': result.get('title', 'No title'), 'url': result.get('url', 'No url'), 'source':result.get('source', 'No source')}
        print("ANS: ", ans)
    return render_template('search_results.html', results=results, q=query)

if __name__ == '__main__':
    app.run(debug=True)
