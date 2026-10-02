def get_user_profile():

    print("\n")
    print("=" * 60)
    print("                 MEAL PLANNING AGENT")
    print("=" * 60)

    # Basic information
    age = int(input("\nEnter your age: "))

    weight = float(input("Enter your weight (kg): "))

    height = float(input("Enter your height (cm): "))

    # Gender
    print("\nGender:")
    print("1. Male")
    print("2. Female")

    gender_choice = input("Choose an option (1/2): ")

    if gender_choice == "1":
        gender = "male"
    else:
        gender = "female"

    # Activity level
    print("\nActivity Level:")
    print("1. Sedentary")
    print("2. Light")
    print("3. Moderate")
    print("4. Active")

    activity_choice = input("Choose an option (1-4): ")

    activity_map = {
        "1": "sedentary",
        "2": "light",
        "3": "moderate",
        "4": "active"
    }

    activity_level = activity_map.get(
        activity_choice,
        "sedentary"
    )

    # Goal
    print("\nGoal:")
    print("1. Weight Loss")
    print("2. Maintenance")
    print("3. Muscle Gain")

    goal_choice = input("Choose an option (1-3): ")

    goal_map = {
        "1": "weight_loss",
        "2": "maintenance",
        "3": "muscle_gain"
    }

    goal = goal_map.get(
        goal_choice,
        "maintenance"
    )

    # Diet
    print("\nDiet:")
    print("1. Vegetarian")
    print("2. Vegan")

    diet_choice = input("Choose an option (1/2): ")

    if diet_choice == "2":
        diet = "vegan"
    else:
        diet = "vegetarian"

    # Number of meals
    print("\nNumber of meals per day:")
    print("3. Breakfast + Lunch + Dinner")
    print("4. Breakfast + Lunch + Snack + Dinner")
    print("5. Breakfast + Lunch + Snack + Dinner + Snack")

    meals = int(
        input("Choose number of meals (3-5): ")
    )

    if meals < 3 or meals > 5:
        meals = 3

    # Foods to avoid
    avoid_foods = input(
        "\nFoods to avoid "
        "(comma separated, or press Enter): "
    )

    if avoid_foods.strip():

        avoid_foods = [
            food.strip().lower()
            for food in avoid_foods.split(",")
        ]

    else:
        avoid_foods = []

    profile = {

        "age": age,

        "weight_kg": weight,

        "height_cm": height,

        "gender": gender,

        "activity_level": activity_level,

        "goal": goal,

        "diet": diet,

        "meals_per_day": meals,

        "avoid_foods": avoid_foods
    }

    return profile