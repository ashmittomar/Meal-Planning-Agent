from agents.meal_agent import MealPlanningAgent


agent = MealPlanningAgent()

result = agent.run()

requirements = result["requirements"]
meal_plan = result["meal_plan"]
evaluation = result["evaluation"]


daily_total = {
    "calories": 0.0,
    "protein_g": 0.0,
    "carbs_g": 0.0,
    "fat_g": 0.0,
    "fiber_g": 0.0
}


print("\n")
print("=" * 70)
print("                    YOUR DAILY MEAL PLAN")
print("=" * 70)

print()

print(
    f"Daily Calories Required : "
    f"{requirements['daily_calories']} kcal"
)

print(
    f"Daily Protein Required  : "
    f"{requirements['protein_target_g']} g"
)


for meal in meal_plan["meals"]:

    print("\n")
    print("-" * 70)

    print(
        meal["meal_type"].upper()
    )

    print(
        f"Meal: {meal['name']}"
    )

    print("-" * 70)

    print("\nIngredients:")

    for ingredient in meal["ingredients"]:

        print(
            f"  {ingredient['food']} "
            f"- {round(ingredient['quantity_g'], 1)} g"
        )

    nutrition = meal["nutrition"]

    print("\nNutrition:")

    print(
        f"  Calories : "
        f"{nutrition['calories']} kcal"
    )

    print(
        f"  Protein  : "
        f"{nutrition['protein_g']} g"
    )

    print(
        f"  Carbs    : "
        f"{nutrition['carbs_g']} g"
    )

    print(
        f"  Fat      : "
        f"{nutrition['fat_g']} g"
    )

    print(
        f"  Fiber    : "
        f"{nutrition['fiber_g']} g"
    )

    for key in daily_total:

        daily_total[key] += nutrition[key]


print("\n")
print("=" * 70)
print("                    DAILY NUTRITION")
print("=" * 70)

print()

print(
    f"Calories : "
    f"{round(daily_total['calories'], 1)} kcal"
)

print(
    f"Protein  : "
    f"{round(daily_total['protein_g'], 1)} g"
)

print(
    f"Carbs    : "
    f"{round(daily_total['carbs_g'], 1)} g"
)

print(
    f"Fat      : "
    f"{round(daily_total['fat_g'], 1)} g"
)

print(
    f"Fiber    : "
    f"{round(daily_total['fiber_g'], 1)} g"
)


print("\n")
print("=" * 70)
print("                    PLAN EVALUATION")
print("=" * 70)

print()

print(
    f"Reason : {evaluation['reason']}"
)

print(
    f"Calorie Difference : "
    f"{evaluation['calorie_difference_percent']}%"
)

print(
    f"Protein Difference : "
    f"{evaluation['protein_difference_percent']}%"
)


print("\n")
print("=" * 70)
print("                 MEAL PLAN COMPLETE")
print("=" * 70)