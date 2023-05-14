from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
nltk.download('punkt')

app = Flask(__name__)

def get_word_frequencies(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all text within HTML tags
        text = ' '.join([element.text for element in soup.find_all(text=True)])
        # Tokenize words
        words = word_tokenize(text)
        # Remove punctuation and convert to lowercase
        words = [word.lower() for word in words if word.isalnum()]
        # Count word frequencies
        word_frequencies = Counter(words)
        return [{'word': word, 'frequency': count} for word, count in word_frequencies.items()]
    except Exception as e:
        return str(e)

@app.route('/word_frequencies', methods=['POST'])
def word_frequencies():
    url = request.json.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is missing.'}), 400

    word_frequencies = get_word_frequencies(url)
    if isinstance(word_frequencies, str):
        return jsonify({'error': 'Error retrieving web page: {}'.format(word_frequencies)}), 500

    return jsonify(word_frequencies)

if __name__ == '__main__':
    app.run()
