import pandas as pd


FILE_PATH = "data/vegetarian_meal_planning_food_database.csv"


def load_food_database():
    return pd.read_csv(FILE_PATH)


def filter_foods(profile):
    """
    Filter foods according to the user's dietary preferences
    and foods they want to avoid.
    """

    df = load_food_database()

    # Vegetarian / vegan filtering
    if profile["diet"] == "vegetarian":
        df = df[df["vegetarian"] == True]

    elif profile["diet"] == "vegan":
        df = df[df["vegan"] == True]

    # Remove foods the user wants to avoid
    avoid_foods = profile["avoid_foods"]

    if avoid_foods:

        pattern = "|".join(avoid_foods)

        df = df[
            ~df["food"].str.contains(
                pattern,
                case=False,
                na=False
            )
        ]

    return df


def select_high_protein_foods(profile, number_of_foods=10):
    """
    Select foods with relatively high protein content.
    """

    df = filter_foods(profile)

    result = df.sort_values(
        by="protein_g",
        ascending=False
    )

    return result.head(number_of_foods)


def select_low_calorie_foods(profile, number_of_foods=10):
    """
    Select foods with relatively low calories.
    """

    df = filter_foods(profile)

    result = df.sort_values(
        by="calories",
        ascending=True
    )

    return result.head(number_of_foods)