# Marley Spoon Technical Interview

I've included a virtual environment (msti) with all of the python modules and the version of python that I used for this project. They are, in no particular order:

1. [Python](https://www.python.org/downloads/release/python-395/) 3.9.5
2. [Contentful](https://pypi.org/project/contentful/) 1.13.1
3. [Flask](https://pypi.org/project/Flask/) 2.1.3
4. [Markdown](https://pypi.org/project/Markdown/) 3.4.1

If you'd prefer to create your own virtual environment:

1. Create the venv -> `python3 -m venv [your desired venv name]`
2. Activate the venv -> `source [your desired venv name]/bin/activate`
3. Install the requirements -> `pip install -r requirements.txt`

Then, to run this application, simply run `python3 fetch.py` (from within the venv), and navigate to [127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser of choice

## Notes

* I would've rather put the API credentials into environment variables instead of a JSON file, but I haven't ever really worked with `.env` files before, so I decided to stick with what I know rather than try too many new things
* The way that the markdown is parsed is pretty unsafe, from my understanding. In order to make everything work, the markdown has to be converted in the backend, and passed to the frontend as HTML. The frontend then uses the `{{<var>|safe}}` keyword in order to actually process the passed HTML. This requires that we _absolutely trust_ the information being passed into the backend. In this microcosm we know what will be passed to the application, but in the real-world this would be vulnerable to cross-site scripting and is probably an infeasible solution (to this part of the problem)
* Currently, it seems that some recipes have a chef or tags entry while others don't. I decided to give the truth to the frontend in these cases - these portions of the webpage will simply read "Chef name unavailable!" or "No tags available!", respectively. In terms of personal philosophy/design, I'd rather display _incomplete_ information than guess at a chef or tags and display _incorrect_ information
* I would've liked to use `async` to grab data from the API and make the whole thing faster (I also remember reading about a sync function in the contentful module) but I didn't want to mess with it considering the time pressure. If I had more time, I would definitely try to figure that out either first or second
* Finally, just for fun, you guys almost got a very frustrating and unreadable lambda function to resolve an ID from the name of a recipe (just as a string)! I'm very happy I figured out how to change it to something much better and easier to understand, but if you want to check it out it should still be in one of the first two commits :-)

## Possible issues

* White Cheddar Grilled Cheese has no Chef
* Tofu Saag Paneer has no Chef or Tags
* Grilled Steak & Vegetables has no Tags
* Crispy Chicken and Rice works completely fine - this tells me the logic isn't necessarily broken, but the information either isn't there or is obscured somehow. If this isn't the expected behavior, please let me know!
* [Email me](mailto:jordan.streete@gmail.com)
