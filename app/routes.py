from flask import render_template
import requests
from app import app


@app.route("/")
def index():
    cat = requests.get("https://api.thecatapi.com/v1/images/search").json()
    image = cat[0]['url']
    return render_template("index.html", title="Look at this cats", cat=image)
