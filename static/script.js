const form =
    document.getElementById("mealForm");


const generateButton =
    document.getElementById(
        "generateButton"
    );


const buttonText =
    document.getElementById(
        "buttonText"
    );


const buttonArrow =
    document.getElementById(
        "buttonArrow"
    );


const loadingMessage =
    document.getElementById(
        "loadingMessage"
    );


const errorMessage =
    document.getElementById(
        "errorMessage"
    );


const resultSection =
    document.getElementById(
        "resultSection"
    );


const mealsContainer =
    document.getElementById(
        "mealsContainer"
    );


/* =========================
   FORM SUBMISSION
========================= */

form.addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();


        /*
         * Hide previous messages
         */

        errorMessage.style.display =
            "none";


        resultSection.style.display =
            "none";


        /*
         * Get form data
         */

        const formData =
            new FormData(form);


        /*
         * Convert foods to avoid
         * into an array
         */

        const avoidFoods =
            formData
                .get("avoid_foods")
                .split(",")
                .map(
                    food =>
                        food.trim().toLowerCase()
                )
                .filter(
                    food =>
                        food.length > 0
                );


        /*
         * Create profile data
         */

        const data = {

            age:
                formData.get("age"),

            weight:
                formData.get("weight"),

            height:
                formData.get("height"),

            gender:
                formData.get("gender"),

            activity_level:
                formData.get(
                    "activity_level"
                ),

            goal:
                formData.get("goal"),

            diet:
                formData.get("diet"),

            meals_per_day:
                formData.get(
                    "meals_per_day"
                ),

            avoid_foods:
                avoidFoods
        };


        /*
         * Loading state
         */

        generateButton.disabled =
            true;


        buttonText.textContent =
            "Generating Plan...";


        buttonArrow.textContent =
            "";


        loadingMessage.style.display =
            "block";


        try {


            /*
             * Send data to Flask
             */

            const response =
                await fetch(
                    "/generate",
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify(data)

                    }
                );


            /*
             * Read JSON response
             */

            const result =
                await response.json();


            /*
             * Check for backend errors
             */

            if (
                !response.ok ||
                !result.success
            ) {

                throw new Error(
                    result.error ||
                    "Unable to generate meal plan."
                );

            }


            /*
             * Get agent result
             */

            const agentResult =
                result.result;


            const mealPlan =
                agentResult.meal_plan;


            const evaluation =
                agentResult.evaluation;


            /*
             * Display nutrition summary
             */

            document.getElementById(
                "dailyCalories"
            ).textContent =
                mealPlan.daily_calorie_target;


            document.getElementById(
                "proteinTarget"
            ).textContent =
                mealPlan.daily_protein_target;


            document.getElementById(
                "actualCalories"
            ).textContent =
                evaluation.calories;


            document.getElementById(
                "actualProtein"
            ).textContent =
                evaluation.protein_g;


            /*
             * Display evaluation reason
             */

            document.getElementById(
                "evaluationReason"
            ).textContent =
                evaluation.reason;


            /*
             * Display differences
             */

            document.getElementById(
                "calorieDifference"
            ).textContent =
                evaluation.calorie_difference_percent
                + "%";


            document.getElementById(
                "proteinDifference"
            ).textContent =
                evaluation.protein_difference_percent
                + "%";


            /*
             * Display status
             */

            document.getElementById(
                "evaluationStatus"
            ).textContent =
                evaluation.status;


            /*
             * Remove old meals
             */

            mealsContainer.innerHTML =
                "";


            /*
             * Create meal cards
             */

            mealPlan.meals.forEach(
                function(meal) {


                    const mealCard =
                        document.createElement(
                            "div"
                        );


                    mealCard.className =
                        "meal-card";


                    /*
                     * Create ingredients HTML
                     */

                    let ingredientsHTML =
                        "";


                    meal.ingredients.forEach(
                        function(ingredient) {

                            ingredientsHTML +=
                                `
                                <li>
                                    ${ingredient.food}
                                    <span>
                                        ${ingredient.quantity_g} g
                                    </span>
                                </li>
                                `;

                        }
                    );


                    /*
                     * Create meal card
                     */

                    mealCard.innerHTML =
                        `

                        <div class="meal-card-header">

                            <div>

                                <span class="meal-type">
                                    ${meal.meal_type}
                                </span>

                                <h3>
                                    ${meal.name}
                                </h3>

                            </div>

                        </div>


                        <div class="meal-content">


                            <div class="ingredients">

                                <h4>
                                    Ingredients
                                </h4>

                                <ul>
                                    ${ingredientsHTML}
                                </ul>

                            </div>


                            <div class="meal-nutrition">


                                <div>

                                    <span>
                                        Calories
                                    </span>

                                    <strong>
                                        ${meal.nutrition.calories}
                                    </strong>

                                    <small>
                                        kcal
                                    </small>

                                </div>


                                <div>

                                    <span>
                                        Protein
                                    </span>

                                    <strong>
                                        ${meal.nutrition.protein_g}
                                    </strong>

                                    <small>
                                        g
                                    </small>

                                </div>


                                <div>

                                    <span>
                                        Carbs
                                    </span>

                                    <strong>
                                        ${meal.nutrition.carbs_g}
                                    </strong>

                                    <small>
                                        g
                                    </small>

                                </div>


                                <div>

                                    <span>
                                        Fat
                                    </span>

                                    <strong>
                                        ${meal.nutrition.fat_g}
                                    </strong>

                                    <small>
                                        g
                                    </small>

                                </div>


                                <div>

                                    <span>
                                        Fiber
                                    </span>

                                    <strong>
                                        ${meal.nutrition.fiber_g}
                                    </strong>

                                    <small>
                                        g
                                    </small>

                                </div>


                            </div>


                        </div>

                        `;


                    /*
                     * Add card to page
                     */

                    mealsContainer.appendChild(
                        mealCard
                    );

                }
            );


            /*
             * Show result section
             */

            resultSection.style.display =
                "block";


            /*
             * Scroll to result
             */

            resultSection.scrollIntoView({
                behavior: "smooth"
            });


            /*
             * Log result for debugging
             */

            console.log(
                "Meal planning agent result:",
                result
            );

        }


        catch (error) {


            /*
             * Display error
             */

            console.error(
                "Error:",
                error
            );


            errorMessage.textContent =
                error.message;


            errorMessage.style.display =
                "block";

        }


        finally {


            /*
             * Restore button
             */

            generateButton.disabled =
                false;


            buttonText.textContent =
                "Generate My Meal Plan";


            buttonArrow.textContent =
                "→";


            loadingMessage.style.display =
                "none";

        }

    }
);