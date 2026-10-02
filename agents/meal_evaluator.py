def evaluate_meal_plan(meal_plan, requirements):

    daily_nutrition = {
        "calories": 0.0,
        "protein_g": 0.0,
        "carbs_g": 0.0,
        "fat_g": 0.0,
        "fiber_g": 0.0
    }

    for meal in meal_plan["meals"]:

        nutrition = meal["nutrition"]

        for key in daily_nutrition:
            daily_nutrition[key] += nutrition[key]

    # Round daily values
    for key in daily_nutrition:
        daily_nutrition[key] = round(
            daily_nutrition[key],
            2
        )

    daily_calories = daily_nutrition["calories"]
    daily_protein = daily_nutrition["protein_g"]

    target_calories = requirements["daily_calories"]
    target_protein = requirements["protein_target_g"]

    # Calculate percentage differences
    calorie_difference = abs(
        daily_calories - target_calories
    )

    protein_difference = abs(
        daily_protein - target_protein
    )

    calorie_percentage = (
        calorie_difference /
        max(target_calories, 1)
    ) * 100

    protein_percentage = (
        protein_difference /
        max(target_protein, 1)
    ) * 100

    # Strict limits
    strict_calorie_limit = 15
    strict_protein_limit = 15

    # Flexible limits
    flexible_calorie_limit = 20
    flexible_protein_limit = 20

    # Check strict condition
    strict_calories_ok = (
        calorie_percentage <= strict_calorie_limit
    )

    strict_protein_ok = (
        protein_percentage <= strict_protein_limit
    )

    # Check flexible condition
    flexible_calories_ok = (
        calorie_percentage <= flexible_calorie_limit
    )

    flexible_protein_ok = (
        protein_percentage <= flexible_protein_limit
    )

    # Decide status
    if strict_calories_ok and strict_protein_ok:

        status = "accepted"

        reason = (
            "The meal plan is within the "
            "strict calorie and protein range."
        )

    elif flexible_calories_ok and flexible_protein_ok:

        status = "acceptable"

        reason = (
            "The meal plan is slightly outside "
            "the strict range but within the "
            "flexible range."
        )

    else:

        status = "replan"

        reasons = []

        if not strict_calories_ok:

            if daily_calories < target_calories:

                reasons.append(
                    "Calories are below the target."
                )

            else:

                reasons.append(
                    "Calories are above the target."
                )

        if not strict_protein_ok:

            if daily_protein < target_protein:

                reasons.append(
                    "Protein is below the target."
                )

            else:

                reasons.append(
                    "Protein is above the target."
                )

        reason = " ".join(reasons)

    return {

        "status": status,

        "reason": reason,

        "calories": daily_calories,

        "protein_g": daily_protein,

        "carbs_g":
            daily_nutrition["carbs_g"],

        "fat_g":
            daily_nutrition["fat_g"],

        "fiber_g":
            daily_nutrition["fiber_g"],

        "target_calories":
            target_calories,

        "target_protein_g":
            target_protein,

        "calorie_difference_percent":
            round(calorie_percentage, 2),

        "protein_difference_percent":
            round(protein_percentage, 2)
    }