import pandas as pd

FILE_PATH = "data/vegetarian_meal_planning_food_database.csv"

df = pd.read_csv(FILE_PATH)

print("\n===== FOOD CATEGORIES =====\n")

print(df["category"].value_counts())

print("\n===== UNIQUE CATEGORIES =====\n")

for category in df["category"].unique():
    print(category)