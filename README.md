# Coffee Recipes Flask App

## Purpose

This Flask web application provides simple coffee recipes for:
- Drip coffee  
- Iced coffee  
- Hot latte  
- Iced latte  
- Cortado  

Users can customize their drink by selecting a coffee type and a flavor
(e.g., Vanilla, Caramel, Hazelnut, Mocha, or None). The app generates a
custom recipe and stores each selection in a JSON file (`data/selections.json`).

The UI uses the **Lux theme** from **Bootswatch** via the Bootstrap CDN and
includes a navigation menu with:
- Dashboard
- Customize Coffee
- History (saved selections)

## How Generative AI Was Used

Generative AI (ChatGPT) was used to:
- Help design the Flask routes and application structure
- Generate the HTML templates using the Lux Bootstrap theme
- Create the Python logic for building custom recipes and saving data in JSON
- Draft this README and basic styling suggestions

All code was reviewed and can be modified or extended by the developer.

## How to Run

1. Create and activate a virtual environment (optional but recommended).

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate
