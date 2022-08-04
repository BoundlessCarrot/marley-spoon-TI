import json

import contentful as cf
import markdown as md
from flask import Flask, render_template

app = Flask(__name__)


def get_credentials() -> cf.Client:
    '''
    Gets the contentful API credentials from a JSON file in the current working directory.

    Returns: client object that can be used to access the API
    '''
    with open("credentials.json", "r") as fp:
        credentials = json.load(fp)

    client = cf.Client(
        credentials.get("space_id"), credentials.get("access_token"), timeout_s=10
    )

    return client


@app.route("/")
def get_all_recipes():
    '''
    Renders a webpage with a list of all available recipes, including their respective images and IDs

    Returns: technically a string, but realistically the rendered webpage using the template html file specified
    '''
    client = get_credentials()

    # Creates a tuple with each recipe's name, asset url and ID, which gets passed to the frontend
    recipes = [
        (entry.title, client.asset(entry.photo.id).url(), entry.id)
        for entry in client.entries({"content_type": "recipe"})
    ]

    return render_template("recipes.html", recipes=recipes)


@app.route("/<id>")
def get_detailed_view(id=None):
    '''
    Renders a webpage with detailed information about a single recipe
    :param: id: str = The ID of the recipe, used to resolve all info for the recipe. We usually get this from the URL, but it can be tested if you know the ID and pass it to the function

    Returns: technically a string, but realistically the rendered webpage using the template html file specified
    '''
    client = get_credentials()

    # Get the specific entry we want, using the ID
    target_entry = client.entry(id)

    # Flask was complaining that tags was uninitialized, so we init it here
    tags = []

    # This JSON schema isn't uniform across entries, so we account for some possible errors here
    try:
        tags = [str(tag.name) + ", " for tag in target_entry.tags]
    except AttributeError:
        tags = ["No tags available!"]
    
    try:
        chef = target_entry.fields()['chef'].name
    except KeyError:
        chef = "Chef name unavailable!"

    return render_template(
        "detailed_view.html", 
        recipe_title=target_entry.title, 
        tags=tags,
        image=client.asset(target_entry.photo.id).url(),
        description=md.markdown(target_entry.description),
        chef=chef
    )


if __name__ == "__main__":
    app.run()
