def calculate_bmr(profile):
    """
    Calculate Basal Metabolic Rate using the Mifflin-St Jeor equation.
    """

    age = profile["age"]
    weight = profile["weight_kg"]
    height = profile["height_cm"]
    gender = profile["gender"]

    if gender == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5

    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161

    return round(bmr, 2)


def calculate_calories(profile):
    """
    Calculate estimated daily calorie requirement.
    """

    bmr = calculate_bmr(profile)

    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725
    }

    activity = profile["activity_level"]

    multiplier = activity_multipliers.get(activity, 1.2)

    maintenance_calories = bmr * multiplier

    goal = profile["goal"]

    if goal == "weight_loss":
        target_calories = maintenance_calories - 300

    elif goal == "muscle_gain":
        target_calories = maintenance_calories + 300

    else:
        target_calories = maintenance_calories

    return round(target_calories)


def calculate_protein_target(profile):
    """
    Estimate daily protein target.

    General project rule:
    weight loss / maintenance: 1.2 g/kg
    muscle gain: 1.6 g/kg
    """

    weight = profile["weight_kg"]
    goal = profile["goal"]

    if goal == "muscle_gain":
        protein_per_kg = 1.6

    else:
        protein_per_kg = 1.2

    protein = weight * protein_per_kg

    return round(protein, 1)


def calculate_nutrition_requirements(profile):

    bmr = calculate_bmr(profile)

    calories = calculate_calories(profile)

    protein = calculate_protein_target(profile)

    return {
        "bmr": bmr,
        "daily_calories": calories,
        "protein_target_g": protein
    }