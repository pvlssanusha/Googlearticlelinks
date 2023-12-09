from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/google_search', methods=['GET'])
def article_search_view():
    if request.method == 'GET':
        api_key = "GOOGLE_API_KEY"  # Replace with your actual Google API key
        custom_search_engine_id = "CUSTOM_SEARCH_ENGINE_ID"  # Replace with your actual Custom Search Engine ID
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

if __name__ == '__main__':
    app.run(debug=True)


# Define a Flask route for the API
@app.route('/articles_search', methods=['GET'])
def api_google_search():
    if request.method == 'GET':
        # Call your existing function
        result = article_search_view(request)

        # Return the result as JSON
        return jsonify(result)
    else:
        return jsonify({'error': 'Invalid request method'})

if __name__ == '__main__':
    app.run(debug=True)
