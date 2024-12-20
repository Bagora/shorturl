from flask import Flask, render_template, request, redirect
import shortuuid
import pyshorteners

app = Flask(__name__)

class URLShortener:
    def __init__(self):
        self.url_mapping = {}

    def shorten_url(self, long_url):
        short_url = shortuuid.uuid()[:8]  # Shorten the identifier to the first 8 characters
        self.url_mapping[short_url] = long_url
        return short_url

    def expand_url(self, short_url):
        return self.url_mapping.get(short_url, None)

url_shortener = URLShortener()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form['url']
    
    # Use pyshorteners to generate TinyURL
    s = pyshorteners.Shortener()
    tiny_url = s.tinyurl.short(long_url)

    short_url = url_shortener.shorten_url(long_url)
    full_short_url = request.url_root + short_url  # Construct full short URL with HTTPS
    return render_template('index.html', short_url=full_short_url, tiny_url=tiny_url)

@app.route('/<short_url>')
def redirect_to_original(short_url):
    long_url = url_shortener.expand_url(short_url)
    if long_url:
        return redirect(long_url)
    else:
        return "URL not found"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Run with HTTPS enabled
