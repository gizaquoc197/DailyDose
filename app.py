from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        search_query = request.form.get('search_query')
        search_type = extract_search_type(search_query)
        result = get_search_result(search_query, search_type)

    return render_template('index.html', result=result, search_query=request.form.get('search_query'))
def extract_search_type(search_query):
    prefix = "Random"
    if search_query.startswith(prefix):
        return search_query[len(prefix):].strip.lower()
    else:
        return "default"
def get_search_result(search_query, search_type):
    API_KEY = open('API_KEY').read()
    SEARCH_ENGINE_ID = open('SEARCH_ENGINE_ID').read()

    target_sites = {
        'memes': 'https://www.memedroid.com/memes/',
        'quotes': 'https://www.brainyquote.com/',
        'jokes': 'https://icanhazdadjoke.com/',
        'videos': 'https://www.youtube.com/',
        'music': 'https://www.spotify.com/',
        'default': ''
    }

    if search_type not in target_sites:
        return "Invalid search type"

    target_site = target_sites[search_type]
    url = 'https://www.googleapis.com/customsearch/v1'

    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ENGINE_ID,
        'dataRestrict': "d[0]",
        'gl': "us",
        'lr': "lang_en",
        'num': 1,
        'siteSearch': target_site
    }

    response = requests.get(url, params=params)
    results = response.json()

    if 'items' in results:
        return results['items'][0]['link']
    else:
        return "No result found"

if __name__ == '__main__':
    app.run(debug=True)