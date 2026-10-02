import pandas as pd
import random

from agents.meal_recipes import MEAL_RECIPES


FILE_PATH = "data/vegetarian_meal_planning_food_database.csv"


MEAL_RATIOS = {
    "breakfast": 0.25,
    "lunch": 0.35,
    "snack": 0.10,
    "dinner": 0.30
}


def load_food_database():

    return pd.read_csv(FILE_PATH)


def filter_foods(profile):

    df = load_food_database()

    # Apply diet restriction
    if profile["diet"] == "vegetarian":

        df = df[
            df["vegetarian"] == True
        ]

    elif profile["diet"] == "vegan":

        df = df[
            df["vegan"] == True
        ]

    # Remove foods the user wants to avoid
    avoid_foods = profile["avoid_foods"]

    if avoid_foods:

        for food in avoid_foods:

            df = df[
                ~df["food"].str.contains(
                    food,
                    case=False,
                    na=False
                )
            ]

    return df


def get_food(df, food_name):

    result = df[
        df["food"].str.lower()
        == food_name.lower()
    ]

    if result.empty:

        return None

    return result.iloc[0]


def calculate_recipe_nutrition(recipe, df):

    total = {
        "calories": 0.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 0.0,
        "fiber_g": 0.0
    }

    ingredients = []

    for item in recipe["ingredients"]:

        food = get_food(
            df,
            item["food"]
        )

        # If one ingredient is unavailable,
        # this recipe cannot be used.
        if food is None:

            return None

        quantity = item["quantity"]

        multiplier = (
            quantity /
            float(food["serving_size_g"])
        )

        total["calories"] += (
            float(food["calories"])
            * multiplier
        )

        total["protein_g"] += (
            float(food["protein_g"])
            * multiplier
        )

        total["carbs_g"] += (
            float(food["carbs_g"])
            * multiplier
        )

        total["fat_g"] += (
            float(food["fat_g"])
            * multiplier
        )

        total["fiber_g"] += (
            float(food["fiber_g"])
            * multiplier
        )

        ingredients.append({
            "food": food["food"],
            "quantity_g": quantity
        })

    for key in total:

        total[key] = round(
            total[key],
            2
        )

    return {
        "nutrition": total,
        "ingredients": ingredients
    }


def calculate_score(
    nutrition,
    calorie_target,
    protein_target,
    adjustment
):

    calorie_difference = abs(
        nutrition["calories"]
        - calorie_target
    )

    protein_difference = abs(
        nutrition["protein_g"]
        - protein_target
    )

    # Normal score
    score = (
        calorie_difference
        +
        protein_difference * 10
    )

    # Agent feedback
    if adjustment == "increase_protein":

        # Strongly prefer high-protein meals
        if nutrition["protein_g"] < protein_target:

            score += (
                protein_target
                - nutrition["protein_g"]
            ) * 20

        else:

            score -= (
                nutrition["protein_g"]
                - protein_target
            ) * 5

    elif adjustment == "reduce_protein":

        if nutrition["protein_g"] > protein_target:

            score += (
                nutrition["protein_g"]
                - protein_target
            ) * 20

    elif adjustment == "increase_calories":

        if nutrition["calories"] < calorie_target:

            score += (
                calorie_target
                - nutrition["calories"]
            ) * 2

        else:

            score -= (
                nutrition["calories"]
                - calorie_target
            )

    elif adjustment == "reduce_calories":

        if nutrition["calories"] > calorie_target:

            score += (
                nutrition["calories"]
                - calorie_target
            ) * 2

    return score


def select_recipe(
    profile,
    meal_type,
    calorie_target,
    protein_target,
    used_meals,
    adjustment=None
):

    df = filter_foods(profile)

    recipes = MEAL_RECIPES[meal_type]

    candidates = []

    for recipe in recipes:

        # Avoid repeating meals
        if recipe["name"] in used_meals:

            continue

        result = calculate_recipe_nutrition(
            recipe,
            df
        )

        if result is None:

            continue

        score = calculate_score(
            result["nutrition"],
            calorie_target,
            protein_target,
            adjustment
        )

        candidates.append({
            "recipe": recipe,
            "result": result,
            "score": score
        })

    if not candidates:

        return None

    # Lowest score = best match
    candidates.sort(
        key=lambda x: x["score"]
    )

    # Keep some randomness
    # so every run does not look identical
    top_candidates = candidates[:5]

    selected = random.choice(
        top_candidates
    )

    return {
        "recipe": selected["recipe"],
        "result": selected["result"]
    }


def get_meal_types(meals_per_day):

    if meals_per_day == 3:

        return [
            "breakfast",
            "lunch",
            "dinner"
        ]

    if meals_per_day == 4:

        return [
            "breakfast",
            "lunch",
            "snack",
            "dinner"
        ]

    return [
        "breakfast",
        "lunch",
        "snack",
        "dinner",
        "snack"
    ]


def create_meal_plan(
    profile,
    requirements,
    adjustment=None
):

    daily_calories = (
        requirements["daily_calories"]
    )

    daily_protein = (
        requirements["protein_target_g"]
    )

    meal_types = get_meal_types(
        profile["meals_per_day"]
    )

    meal_plan = []

    used_meals = []

    for meal_type in meal_types:

        ratio = MEAL_RATIOS[
            meal_type
        ]

        meal_calories = (
            daily_calories
            * ratio
        )

        meal_protein = (
            daily_protein
            * ratio
        )

        selected = select_recipe(
            profile,
            meal_type,
            meal_calories,
            meal_protein,
            used_meals,
            adjustment
        )

        # If no unused recipe exists,
        # allow a previously used recipe.
        if selected is None:

            selected = select_recipe(
                profile,
                meal_type,
                meal_calories,
                meal_protein,
                [],
                adjustment
            )

        if selected is None:

            continue

        recipe = selected["recipe"]

        result = selected["result"]

        used_meals.append(
            recipe["name"]
        )

        meal_plan.append({

            "meal_type":
                meal_type,

            "name":
                recipe["name"],

            "ingredients":
                result["ingredients"],

            "nutrition":
                result["nutrition"]
        })

    return {

        "daily_calorie_target":
            daily_calories,

        "daily_protein_target":
            daily_protein,

        "meals":
            meal_plan
    }