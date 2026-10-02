from agents.nutrition_requirements import (
    calculate_nutrition_requirements
)

from agents.meal_planner import (
    create_meal_plan
)

from agents.meal_evaluator import (
    evaluate_meal_plan
)


class MealPlanningAgent:

    def __init__(self):

        self.profile = None
        self.requirements = None
        self.meal_plan = None
        self.evaluation = None

        self.max_attempts = 3

        self.adjustment = None


    def set_user_profile(self, profile):

        self.profile = profile


    def calculate_requirements(self):

        self.requirements = (
            calculate_nutrition_requirements(
                self.profile
            )
        )


    def generate_meal_plan(self):

        self.meal_plan = create_meal_plan(
            self.profile,
            self.requirements,
            self.adjustment
        )

        return self.meal_plan


    def evaluate_plan(self):

        self.evaluation = evaluate_meal_plan(
            self.meal_plan,
            self.requirements
        )

        return self.evaluation


    def analyze_failure(self):

        calories = self.evaluation["calories"]

        protein = self.evaluation["protein_g"]

        target_calories = (
            self.requirements["daily_calories"]
        )

        target_protein = (
            self.requirements["protein_target_g"]
        )

        calorie_error = abs(
            calories - target_calories
        )

        protein_error = abs(
            protein - target_protein
        )

        if protein_error > calorie_error:

            if protein < target_protein:
                return "increase_protein"

            return "reduce_protein"

        else:

            if calories < target_calories:
                return "increase_calories"

            return "reduce_calories"


    def create_and_evaluate_plan(self):

        best_plan = None
        best_evaluation = None

        best_error = float("inf")

        for attempt in range(
            1,
            self.max_attempts + 1
        ):

            self.generate_meal_plan()

            self.evaluate_plan()

            calorie_error = (
                self.evaluation[
                    "calorie_difference_percent"
                ]
            )

            protein_error = (
                self.evaluation[
                    "protein_difference_percent"
                ]
            )

            total_error = (
                calorie_error +
                protein_error
            )

            if total_error < best_error:

                best_error = total_error

                best_plan = self.meal_plan

                best_evaluation = (
                    self.evaluation
                )

            if self.evaluation["status"] in [
                "accepted",
                "acceptable"
            ]:

                return

            if attempt < self.max_attempts:

                self.adjustment = (
                    self.analyze_failure()
                )

        self.meal_plan = best_plan

        self.evaluation = best_evaluation


    def run_with_profile(self, profile):

        self.set_user_profile(profile)

        self.calculate_requirements()

        self.create_and_evaluate_plan()

        return {

            "profile":
                self.profile,

            "requirements":
                self.requirements,

            "meal_plan":
                self.meal_plan,

            "evaluation":
                self.evaluation
        }