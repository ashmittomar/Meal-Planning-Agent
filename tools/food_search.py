import pandas as pd


FILE_PATH = "data/vegetarian_meal_planning_food_database.csv"


def load_food_database():
    return pd.read_csv(FILE_PATH)


def search_food(food_name):

    df = load_food_database()

    result = df[
        df["food"].str.contains(
            food_name,
            case=False,
            na=False
        )
    ]

    return result


def get_category_foods(category):

    df = load_food_database()

    result = df[
        df["category"].str.contains(
            category,
            case=False,
            na=False
        )
    ]

    return result


def get_vegan_foods():

    df = load_food_database()

    result = df[df["vegan"] == True]

    return result