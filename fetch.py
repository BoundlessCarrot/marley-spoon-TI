import contentful as cf
import json
from flask import Flask, render_template

# app = Flask(__name__)


def get_credentials() -> dict:
    with open("credentials.json", "r") as fp:
        credentials = json.load(fp)

    client = cf.Client(
        credentials.get("space_id"), credentials.get("access_token"), timeout_s=10
    )

    return client


# @app.route("/")
def get_all_recipes() -> list:
    client = get_credentials()
    recipes = [
        (x.title, client.asset(x.photo.id).url())
        for x in client.entries({"content_type": "recipe"})
    ]

    print(recipes)

    # return render_template("recipes.html", recipes=recipes)


# @app.route("/<name>")
def get_detailed_view(name=None):
    client = get_credentials()
    entry_id = list(
        filter(
            lambda x: x.title == name,
            [entry for entry in client.entries({"content_type": "recipe"})],
        )
    )[0].id
    target_entry = client.entry(entry_id)

    print(
        # target_entry.title,
        # [a.name for a in target_entry.tags],
        # target_entry.items()
        [x for x in client.entries({"content_type": "chef"})][0].metadata
        # target_entry.description,
        # target_entry.name,
    )

    # render_template("detailed_view.html", recipe_title=target_entry.title, tags=target_entry.tags, )


if __name__ == "__main__":
    # app.run(debug=True)
    # get_all_recipes()
    get_detailed_view("White Cheddar Grilled Cheese with Cherry Preserves & Basil")
