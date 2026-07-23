def get_recommendation(risk_level):

    recommendations = {

        "Insufficient_Weight": """
Increase healthy calorie intake
Eat protein-rich foods
Include nuts and dairy products
Strength training recommended
        """,

        "Normal_Weight": """
Maintain balanced diet
Continue regular exercise
Drink enough water
Maintain healthy sleep schedule
        """,

        "Overweight_Level_I": """
Reduce sugar and junk food
Walk 30 mins daily
Increase vegetable intake
Avoid late-night eating
        """,

        "Overweight_Level_II": """
Start cardio exercises
Reduce calorie intake
Follow structured meal plans
Increase water consumption
        """,

        "Obesity_Type_I": """
Consult nutritionist
Start weight-loss exercises
Avoid sugary beverages
Daily physical activity required
        """,

        "Obesity_Type_II": """
Strict diet monitoring needed
Medical consultation recommended
Follow low-carb diet
Regular health checkups required
        """,

        "Obesity_Type_III": """
Immediate medical attention advised
Follow doctor-supervised diet
Controlled physical activity
Lifestyle intervention necessary
        """
    }

    return recommendations.get(risk_level, "Stay healthy!")


def get_diet_plan(risk_level):

    diet_plans = {

        "Underweight": [
            "Milk",
            "Banana",
            "Rice",
            "Eggs"
        ],

        "Normal": [
            "Fruits",
            "Vegetables",
            "Whole grains",
            "Lean protein"
        ],

        "Overweight": [
            "Oats",
            "Salads",
            "Brown rice",
            "Green tea"
        ],

        "Overweight High Risk": [
            "Low-carb meals",
            "Soup",
            "Boiled vegetables",
            "Chicken breast"
        ],

        "Obesity Level 1": [
            "High fiber foods",
            "Low sugar diet",
            "Vegetable soup",
            "Fish"
        ],

        "Obesity Level 2": [
            "Strict low-calorie diet",
            "Protein-rich foods",
            "Leafy vegetables",
            "Fruit salad"
        ],

        "Severe Obesity": [
            "Doctor-supervised diet",
            "Low fat foods",
            "Fresh vegetables",
            "Healthy smoothies"
        ]
    }

    return diet_plans.get(
        risk_level,
        ["Maintain balanced diet"]
    )

def get_exercise_plan(risk_level):

    exercise_plans = {

        "Underweight": [
            "Light yoga",
            "Walking",
            "Stretching"
        ],

        "Normal": [
            "Jogging",
            "Cycling",
            "Gym workout"
        ],

        "Overweight": [
            "Brisk walking",
            "Cardio",
            "Skipping"
        ],

        "Overweight High Risk": [
            "Running",
            "Cycling",
            "Swimming"
        ],

        "Obesity Level 1": [
            "Walking",
            "Yoga",
            "Low impact cardio"
        ],

        "Obesity Level 2": [
            "Daily walking",
            "Light gym",
            "Water exercises"
        ],

        "Severe Obesity": [
            "Medical fitness program",
            "Slow walking",
            "Breathing exercises"
        ]
    }

    return exercise_plans.get(
        risk_level,
        ["Daily walking"]
    )