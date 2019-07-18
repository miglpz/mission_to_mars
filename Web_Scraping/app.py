from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")



@app.route("/")
def index():
    mars_info = mongo.db.mars_info.find_one()
    return render_template("index.html", mars_info = mars_info)


@app.route("/scrape")
def scrape():    
    mars_data = scrape_mars.mars_news()
    mars_data = scrape_mars.mars_image()
    mars_data = scrape_mars.mars_facts()
    mars_data = scrape_mars.mars_weather()
    mars_data = scrape_mars.mars_hemispheres()
    mongo.db.mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)
