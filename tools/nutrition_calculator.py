import pandas as pd 

FILE_PATH = "data/vegetarian_meal_planning_food_database.csv"

def load_food_dataset():
    return pd.read_csv(FILE_PATH)

def calculate_nutrition(food_name, quantity_grams):
    df = load_food_dataset()

    food = df[df["food"].str.lower() == food_name.lower()]

    if food.empty:
        return None

    food = food.iloc[0]

    multiplier = quantity_grams / food["serving_size_g"]

    nutrition = {
        "food": food["food"],
        "quantity_g": quantity_grams,
        "calories": float(round(food["calories"] * multiplier, 2)),
        "protein_g": float(round(food["protein_g"] * multiplier, 2)),
        "carbs_g": float(round(food["carbs_g"] * multiplier, 2)),
        "fat_g": float(round(food["fat_g"] * multiplier, 2)),
        "fiber_g": float(round(food["fiber_g"] * multiplier, 2))
    }
    return nutrition

def calculate_meal_nutrition(meal_items):
    
    #Calculate total nutrition for multiple foods.
    

    total = {
        "calories": 0.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 0.0,
        "fiber_g": 0.0
    }

    food_details = []

    for item in meal_items:

        result = calculate_nutrition(
            item["food"],
            item["quantity"]
        )

        if result is None:
            print(f"Food not found: {item['food']}")
            continue

        food_details.append(result)

        total["calories"] += result["calories"]
        total["protein_g"] += result["protein_g"]
        total["carbs_g"] += result["carbs_g"]
        total["fat_g"] += result["fat_g"]
        total["fiber_g"] += result["fiber_g"]

    # Round final values
    for key in total:
        total[key] = round(total[key], 2)

    return {
        "foods": food_details,
        "total": total
    }