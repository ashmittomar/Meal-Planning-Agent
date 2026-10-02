from flask import Flask, render_template, request, jsonify

from agents.meal_agent import MealPlanningAgent


app = Flask(__name__)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate_meal_plan():

    try:

        data = request.get_json()

        profile = {

            "age":
                int(data["age"]),

            "weight_kg":
                float(data["weight"]),

            "height_cm":
                float(data["height"]),

            "gender":
                data["gender"],

            "activity_level":
                data["activity_level"],

            "goal":
                data["goal"],

            "diet":
                data["diet"],

            "meals_per_day":
                int(data["meals_per_day"]),

            "avoid_foods":
                data["avoid_foods"]
        }

        agent = MealPlanningAgent()

        result = agent.run_with_profile(
            profile
        )

        return jsonify({
            "success": True,
            "result": result
        })

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 400


if __name__ == "__main__":

    app.run(
        debug=True
    )