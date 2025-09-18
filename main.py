from flask import Flask, request, jsonify
from botasaurus.browser import browser, Driver
import time
from markdownify import markdownify as md


@browser
def get_page_html_task(driver: Driver, url: str):
    tab = driver.get(url, bypass_cloudflare=True)
    for _ in range(10):
        if "you're not a bot" not in driver.title.lower():
            break
        time.sleep(.5)
        print('Solving Anubis challenge...')
    time.sleep(.5)
    return tab.get_content()


app = Flask(__name__)

@app.route('/md')
def scrape_page_route_markdown():
    url_to_scrape = request.args.get('url')
    try:
        if not url_to_scrape.startswith(('http://', 'https://')):
            url_to_scrape = 'http://' + url_to_scrape
        return md(get_page_html_task(url_to_scrape))
    except Exception as e:
        print(f"Error during scraping: {e}") 
        return jsonify({"error": f"An unexpected error occurred while scraping: {str(e)}"}), 500

@app.route('/')
def scrape_page_route():
    url_to_scrape = request.args.get('url')
    if not url_to_scrape:
        return """<h1>This is a simple proxy server to solve most common anti-bot mechanisms</h1><br>
        Use the /?url=<your_url> endpoint to get the HTML of a page.<br><br>
        Use /md to display as markdown instead of html."""

    try:
        if not url_to_scrape.startswith(('http://', 'https://')):
            url_to_scrape = 'http://' + url_to_scrape
        return get_page_html_task(url_to_scrape)
    except Exception as e:
        print(f"Error during scraping: {e}") 
        return jsonify({"error": f"An unexpected error occurred while scraping: {str(e)}"}), 500
