import pandas as pd

# Data for 20 common diseases and their restricted ingredients
data = {
    "Disease": [
        "Diabetes", "Hypertension", "Gluten Allergy", "Lactose Intolerant", "Obesity",
        "Heart Disease", "Kidney Disease", "PCOS", "Thyroid Disorder", "Gout",
        "Asthma", "Anemia", "Liver Disease", "GERD", "IBS",
        "Peptic Ulcer", "High Cholesterol", "Arthritis", "Migraine", "Gallstones"
    ],
    "Restricted Ingredients": [
        "sugar, jaggery, sweeteners",
        "salt, processed food, pickles",
        "wheat, barley, rye",
        "milk, cheese, butter",
        "sugar, fried food, soda",
        "red meat, salt, fried food",
        "potassium, sodium, phosphorus",
        "sugar, dairy, processed food",
        "soy, cabbage, cauliflower",
        "red meat, organ meat, alcohol",
        "cold drinks, preservatives, sulfites",
        "tea, coffee, high-fiber foods",
        "alcohol, fried food, high-fat dairy",
        "spicy foods, caffeine, chocolate",
        "gluten, dairy, fried foods",
        "spicy foods, caffeine, acidic foods",
        "butter, fried food, processed meat",
        "red meat, high-fat dairy, fried food",
        "chocolate, caffeine, alcohol",
        "fatty meats, fried food, refined carbs"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
file_name = "common_indian_diseases.xlsx"
df.to_excel(file_name, index=False)

print(f"Excel file '{file_name}' created successfully!")
