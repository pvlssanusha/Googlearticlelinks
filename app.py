from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(name)

@app.route('/', methods=['GET'])
def article_search_view():
    if request.method == 'GET':
        api_key = os.getenv("GOOGLE_API_KEY")  # Replace with your actual Google API key
        custom_search_engine_id = os.getenv("CUSTOM_SEARCH_ENGINE_ID")  # Replace with your actual Custom Search Engine ID
        query = request.args.get('topic', '')

        if not query:
            return jsonify({'error': 'Please provide a search query'})

        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={api_key}&cx={custom_search_engine_id}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Extract and prepare relevant information from the response
            search_results = []
            for item in data.get("items", []):
                title = item.get("title")
                link = item.get("link")
                search_results.append({'title': title, 'link': link})

            return jsonify({'query': query, 'search_results': search_results})

        except requests.exceptions.RequestException as e:
            return jsonify({'error': f"Error connecting to the Google API: {e}"})

    else:
        return jsonify({'error': 'Invalid request method'})


if name == 'main':
    app.run(debug=True)
