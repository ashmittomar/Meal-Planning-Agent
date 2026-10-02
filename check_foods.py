import pandas as pd

FILE_PATH = "data/vegetarian_meal_planning_food_database.csv"

df = pd.read_csv(FILE_PATH)

categories = [
    "Grains",
    "Pulses",
    "Plant Protein",
    "Dairy",
    "Vegetables",
    "Fruits",
    "Nuts & Seeds",
    "Breads",
    "Indian Main Course",
    "Salads",
    "Beverages",
    "Snacks"
]

for category in categories:

    print(f"\n===== {category} =====")

    foods = df[df["category"] == category]

    for food in foods["food"]:
        print(food)