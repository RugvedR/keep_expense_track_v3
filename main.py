from expenses_utils import update_expenses, update_monthly_expenses

# Define file paths
daily_expenses_file = "expenses.xlsx"
monthly_expenses_file = "monthly_expenses.xlsx"
notes_file = "note.txt"

def main():
    # Read notes from the file
    try:
        with open(notes_file, 'r') as file:
            note = file.read().strip()
    except FileNotFoundError:
        print(f"Error: The file '{notes_file}' does not exist.")
        return
    
    # Update daily expenses
    new_entries = update_expenses(note, daily_expenses_file)
    if new_entries > 0:
        print(f"{new_entries} new entries appended to '{daily_expenses_file}'.")
    else:
        print("No new entries to append.")

    # Update monthly expenses
    updated_monthly_data = update_monthly_expenses(daily_expenses_file, monthly_expenses_file)
    print(updated_monthly_data)

if __name__ == "__main__":
    main()
