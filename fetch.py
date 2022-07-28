import contentful as cf
import json
from flask import Flask, render_template
import markdown as md

app = Flask(__name__)


def get_credentials() -> dict:
    with open("credentials.json", "r") as fp:
        credentials = json.load(fp)

    client = cf.Client(
        credentials.get("space_id"), credentials.get("access_token"), timeout_s=10
    )

    return client


@app.route("/")
def get_all_recipes() -> list:
    client = get_credentials()
    recipes = [
        (x.title, client.asset(x.photo.id).url(), x.id)
        for x in client.entries({"content_type": "recipe"})
    ]

    return render_template("recipes.html", recipes=recipes)


@app.route("/<id>")
def get_detailed_view(id=None):
    client = get_credentials()

    # Get the specific entry we want, using the ID
    target_entry = client.entry(id)

    # Flask was complaining that tags was uninitialized, so we init it here
    tags = []

    # This JSON schema isn't identical across entries, so we account for some possible errors here
    try:
        chef = target_entry.fields()['chef'].name
        tags = [tag.name for tag in target_entry.tags]
    except KeyError:
        chef = "Chef name unavailable!"
    except AttributeError:
        tags = ["No tags available!"]

    return render_template(
        "detailed_view.html", 
        recipe_title=target_entry.title, 
        tags=tags, 
        image=client.asset(target_entry.photo.id).url(),
        description=md.markdown(target_entry.description),
        chef=chef
    )


if __name__ == "__main__":
    app.run(debug=True)
