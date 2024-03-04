from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from flask import Flask, render_template, request, url_for, redirect

from pymongo import MongoClient

from bson.objectid import ObjectId

# from bson.objectid import ObjectId
app = Flask(__name__)


uri = "mongodb+srv://samundraacharya920:F80ArsWLDIhexVxq@cluster0.5mpiqtl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.flask_database  # creating your flask database using your mongo client
todos = db.todos  # creating a collection called "todos"


@app.route("/", methods=('GET', 'POST'))
def index():
    if request.method == "POST":   # if the request method is post, then insert the todo document in todos collection
        content = request.form['content']
        degree = request.form['degree']
        todos.insert_one({'content': content, 'degree': degree})
        return redirect(url_for('index'))  # redirect the user to home page
    all_todos = todos.find()    # display all todo documents
    # render home page template with all todos
    return render_template('index.html', todos=all_todos)


# Delete Route
@app.post("/<id>/delete/")
def delete(id):  # delete function by targeting a todo document by its own id
    # deleting the selected todo document by its converted id
    todos.delete_one({"_id": ObjectId(id)})
    # again, redirecting you to the home page
    return redirect(url_for('index'))


db = client.flask_database  # creating your flask database using your mongo client
todos = db.todos  # creating a collection called "todos"
# The dunder if __name__ code block
if __name__ == "__main__":
    app.run(debug=True)
