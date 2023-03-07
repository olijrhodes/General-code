import requests
import json
import threading
from socket import gaierror, gethostbyname
from multiprocessing.dummy import Pool as ThreadPool
from urllib.parse import urlparse
from flask import Flask, render_template, jsonify
from time import gmtime, strftime

def is_reachable(url):
    """ This function checks to see if a host name has a DNS entry
    by checking for socket info."""
    try:
        gethostbyname(url)
    except (gaierror):
        return False
    else:
        return True

def get_status_code(url):
    """ This function returns the status code of the url."""
    try:
        status_code = requests.get(url, timeout=30).status_code
        return status_code
    except requests.ConnectionError:
        return 'UNREACHABLE'

def check_single_url(url):
    if is_reachable(urlparse(url).hostname) == True:
        return str(get_status_code(url))
    else:
        return 'UNREACHABLE'

def get_status():
    statuses = {}
    temp_urls = []
    temp_statuses = []
    global returned_statuses
    global last_update_time

    t = threading.Timer
    t(60.0, get_status).start()
    for group, urls in checkurls.items():
        for url in urls:
            temp_urls.append(url)

    pool = ThreadPool(8)
    temp_list_statuses = pool.map(check_single_url, temp_urls)
    for i in range(len(temp_urls)):
        statuses[temp_urls[i]] = temp_list_statuses[i]
    last_update_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print(last_update_time)
    returned_statuses = statuses

app = Flask(__name__)

@app.route("/", methods=["GET"])
def display_statuses():
    return render_template("display_status.html",
    returned_statuses = returned_statuses,
    checkurls = checkurls,
    last_update_time = last_update_time)

with open("checkUrls.json") as f:
    checkurls = json.load(f)

returned_statuses = {}
last_update_time = 'time string'

if __name__ == "__main__":
    app.run(debug=True)
