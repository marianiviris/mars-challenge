from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

app = Flask(__name__)

conn = "mongodb+srv://marianiviris:Giovanni1207@cluster0-tkz4b.azure.mongodb.net/test"
mongo = PyMongo(app, uri=conn)


@app.route("/")
def home():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape/")
def scrape_fun():
    from scrape_mars import scrape
   
    mars = scrape()  
    mongo.db.collection.update({}, mars, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

