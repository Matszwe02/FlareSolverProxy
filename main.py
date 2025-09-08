from flask import Flask, request, jsonify
from botasaurus.browser import browser, Driver
import time

# Botasaurus task to get the full HTML of a page
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

@app.route('/')
def scrape_page_route():
    url_to_scrape = request.args.get('url')
    if not url_to_scrape:
        return "This is a Flask server that can scrape web pages. Use the /?url=<your_url> endpoint to get the HTML of a page."
        # return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        # Add http:// if not present to avoid errors with botasaurus
        if not url_to_scrape.startswith(('http://', 'https://')):
            url_to_scrape = 'http://' + url_to_scrape
        
        # Call the botasaurus task
        page_html = get_page_html_task(url_to_scrape)
        return page_html
    except Exception as e:
        # Log the exception for debugging
        print(f"Error during scraping: {e}") 
        return jsonify({"error": f"An unexpected error occurred while scraping: {str(e)}"}), 500

