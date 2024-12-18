import pandas as pd
import re
import os
import json

# Load categories from a JSON file
def load_categories(file_path="categories.json"):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {
        'Rent': ['rent', 'maid', 'cook', 'electricity', 'bill'],
        'Food & Necessities': ['lunch', 'dinner', 'snack', 'breakfast', 'milk', 'peanut butter', 'groceries', 'rice', 'aata', 'paratha', 'pohe', 'paneer'],
        'Transportation': ['petrol', 'cab'],
        'Personal Care': ['clotrimazole cream', 'health'],
        'Entertainment': ['movie', 'gaming', 'concert', 'Netflix'],
        'Shopping': ['shoe', 'bine cover', 'trackpant'],
        'Emergency': ['emergency'],
        'Miscellaneous': ['misc']
    }

# Save updated categories back to the JSON file
def save_categories(categories, file_path="categories.json"):
    with open(file_path, 'w') as f:
        json.dump(categories, f)

def categorize_expense(description, categories):
    """Categorizes an expense based on the description."""
    # Check if description matches any existing categories
    for cat, keywords in categories.items():
        if any(keyword in description.lower() for keyword in keywords):
            return cat
    
    # If no match found, prompt the user to choose a category
    print(f"Expense Description: {description}")
    print("Please select the category:")
    for idx, cat in enumerate(categories.keys(), 1):
        print(f"{idx}. {cat}")
    
    choice = int(input("Enter the number corresponding to the category: "))
    
    # Map the choice to the category
    selected_category = list(categories.keys())[choice - 1]
    
    # Add the new category to the list of keywords for this category
    categories[selected_category].append(description.lower())
    
    # Save the updated categories back to the JSON file
    save_categories(categories)
    
    return selected_category

def parse_expenses(note):
    """Parses the expense note into a DataFrame."""
    expenses = []
    current_date = None

    # Split the note by lines
    lines = note.strip().split("\n")
    
    # Load categories from file
    categories = load_categories()

    for line in lines:
        # Check for date format (dd.mm.yy)
        if re.match(r"\d{1,2}\.\d{1,2}\.\d{2}", line):
            current_date = line.strip()
        elif current_date:
            # Parse expenses for the current date
            match = re.match(r"(\d+)/- (.+)", line.strip())
            if match:
                amount, description = match.groups()
                # Categorize the expense
                category = categorize_expense(description.strip(), categories)
                
                expenses.append({
                    "date": current_date,
                    "amount": int(amount),
                    "description": description.strip(),
                    "category": category
                })
    return pd.DataFrame(expenses)

def update_expenses(note, excel_file):
    """Updates the Excel file with new expenses from the note."""
    # Parse the new expenses
    new_data = parse_expenses(note)
    
    # If the file exists, load existing data
    if os.path.exists(excel_file):
        existing_data = pd.read_excel(excel_file)
    else:
        existing_data = pd.DataFrame(columns=["date", "amount", "description", "category"])
    
    # Find new entries to append
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)
    combined_data = combined_data.drop_duplicates(subset=["date", "amount", "description", "category"])
    
    # Determine new rows only
    new_rows = combined_data[~combined_data.index.isin(existing_data.index)]
    
    # Update the Excel file
    with pd.ExcelWriter(excel_file, mode='w', engine='openpyxl') as writer:
        combined_data.to_excel(writer, index=False)
    
    return len(new_rows)

def update_monthly_expenses(daily_expenses_file, monthly_expenses_file):
    """Update the monthly expenses Excel file based on the daily expenses file."""
    # Load daily expenses
    if os.path.exists(daily_expenses_file):
        daily_data = pd.read_excel(daily_expenses_file)
    else:
        raise FileNotFoundError(f"The file '{daily_expenses_file}' does not exist.")
    
    # Ensure date is in datetime format
    daily_data['date'] = pd.to_datetime(daily_data['date'], format='%d.%m.%y')
    
    # Group by month and sum amounts
    monthly_data = (
        daily_data.groupby(daily_data['date'].dt.to_period('M'))
        .agg(total_amount=('amount', 'sum'))
        .reset_index()
    )
    monthly_data['month'] = monthly_data['date'].dt.strftime('%Y-%m')  # Convert period to string
    monthly_data.drop(columns=['date'], inplace=True)  # Remove the period column

    # Load existing monthly data if file exists
    if os.path.exists(monthly_expenses_file):
        existing_monthly_data = pd.read_excel(monthly_expenses_file)
    else:
        existing_monthly_data = pd.DataFrame(columns=["month", "total_amount"])

    # Merge existing data with new data
    updated_data = pd.concat([existing_monthly_data, monthly_data], ignore_index=True)
    updated_data = (
        updated_data.drop_duplicates(subset=["month"], keep="last")  # Keep latest totals for each month
        .reset_index(drop=True)
    )

    # Identify if any new data was added
    if updated_data.equals(existing_monthly_data):
        print("No changes in monthly data. File not updated.")
        return updated_data

    # Update the monthly expenses Excel file
    with pd.ExcelWriter(monthly_expenses_file, mode='w', engine='openpyxl') as writer:
        updated_data.to_excel(writer, index=False)

    print(f"Monthly expenses updated in '{monthly_expenses_file}'.")
    return updated_data
