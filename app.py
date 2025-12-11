import os
import json
from datetime import datetime
from Flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "change-me-in-production"  # needed for flash messages

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
SELECTIONS_FILE = os.path.join(DATA_DIR, "selections.json")

# Base recipes for each drink type
BASE_RECIPES = {
    "drip": {
        "name": "Drip Coffee",
        "ingredients": [
            "20g medium-ground coffee",
            "300ml hot water (~96°C)",
            "Filter and drip coffee maker"
        ],
        "steps": [
            "Place a filter in the drip coffee maker.",
            "Add 20g of medium-ground coffee to the filter.",
            "Pour 300ml of water into the reservoir.",
            "Start the machine and let the coffee brew.",
            "Serve immediately."
        ]
    },
    "iced_coffee": {
        "name": "Iced Coffee",
        "ingredients": [
            "20g medium-ground coffee",
            "200ml hot water (~96°C)",
            "A glass full of ice"
        ],
        "steps": [
            "Brew a strong cup of drip coffee using 20g coffee and 200ml water.",
            "Fill a glass with ice.",
            "Pour the hot coffee over the ice.",
            "Stir and serve."
        ]
    },
    "latte_hot": {
        "name": "Hot Latte",
        "ingredients": [
            "1 shot espresso (18–20g coffee)",
            "180–200ml steamed milk"
        ],
        "steps": [
            "Pull 1 shot of espresso into a cup.",
            "Steam the milk until it reaches 60–65°C with light microfoam.",
            "Pour steamed milk over the espresso, holding back the foam at first.",
            "Finish with a thin layer of foam on top."
        ]
    },
    "latte_iced": {
        "name": "Iced Latte",
        "ingredients": [
            "1 shot espresso",
            "150–180ml cold milk",
            "Ice cubes"
        ],
        "steps": [
            "Fill a tall glass with ice.",
            "Pull 1 shot of espresso.",
            "Pour cold milk over the ice.",
            "Add the espresso shot on top.",
            "Stir gently and serve."
        ]
    },
    "cortado": {
        "name": "Cortado",
        "ingredients": [
            "1 shot espresso",
            "Equal part steamed milk (30–40ml)"
        ],
        "steps": [
            "Pull 1 shot of espresso into a small glass.",
            "Steam a small amount of milk with very light foam.",
            "Pour an equal amount of milk into the espresso.",
            "Serve immediately."
        ]
    }
}

FLAVORS = ["None", "Vanilla", "Caramel", "Hazelnut", "Mocha"]


def ensure_data_dir_and_file():
    """Make sure data directory and selections.json exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(SELECTIONS_FILE):
        with open(SELECTIONS_FILE, "w") as f:
            json.dump([], f, indent=4)


def load_selections():
    ensure_data_dir_and_file()
    try:
        with open(SELECTIONS_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except json.JSONDecodeError:
        return []


def save_selections(selections):
    ensure_data_dir_and_file()
    with open(SELECTIONS_FILE, "w") as f:
        json.dump(selections, f, indent=4)


def build_custom_recipe(drink_key, flavor):
    """Create a custom recipe object based on base recipe and chosen flavor."""
    base = BASE_RECIPES.get(drink_key)
    if not base:
        return None

    flavor = flavor.strip()
    has_flavor = flavor.lower() != "none"

    # Clone base recipe
    ingredients = list(base["ingredients"])
    steps = list(base["steps"])

    if has_flavor:
        flavor_line = f"{15 if 'iced' in drink_key else 20}ml {flavor.lower()} syrup"
        ingredients.append(flavor_line)
        steps.append(f"Add {flavor.lower()} syrup to taste and stir well.")

    title = base["name"]
    if has_flavor:
        title = f"{flavor} {title}"

    return {
        "title": title,
        "ingredients": ingredients,
        "steps": steps,
    }


@app.route("/")
def index():
    # Dashboard page: shows available drinks and a quick link to customize
    return render_template("index.html", base_recipes=BASE_RECIPES)


@app.route("/customize", methods=["GET", "POST"])
def customize():
    custom_recipe = None

    if request.method == "POST":
        drink_key = request.form.get("drink_type")
        flavor = request.form.get("flavor") or "None"

        custom_recipe = build_custom_recipe(drink_key, flavor)
        if not custom_recipe:
            flash("Invalid drink selection. Please try again.", "danger")
            return redirect(url_for("customize"))

        # Save the user's selection in JSON format
        selections = load_selections()
        selections.append(
            {
                "drink_type": drink_key,
                "flavor": flavor,
                "recipe_title": custom_recipe["title"],
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }
        )
        save_selections(selections)

        flash("Your custom coffee recipe has been created and saved!", "success")

    return render_template(
        "page1.html",
        base_recipes=BASE_RECIPES,
        flavors=FLAVORS,
        custom_recipe=custom_recipe,
    )


@app.route("/history")
def history():
    # Show all stored selections from the JSON file
    selections = load_selections()
    return render_template("page2.html", selections=selections, base_recipes=BASE_RECIPES)


if __name__ == "__main__":
    app.run(debug=True)
