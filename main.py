from expenses_utils import update_expenses, update_monthly_expenses

# Define file paths
daily_expenses_file = "expenses.xlsx"
monthly_expenses_file = "monthly_expenses.xlsx"

# Note for updating daily expenses
note = """
24.11.24
110/- lunch
160/- dinner

25.11.24
66/- lunch
500/- country delight milk
234/- peanut butter,etc
25/- neembu cucumber 

26.11.24
43/- Paratha
83/- dinner 

27.11.24
100/- clotrimazole cream
49/- paratha
75/- dinner
115/- bottle
55/- stock

28.11.24
166/- lunch
2222/- shoe, bine cover, trackpant
75/- dinner

29.11.24
211/- dalbati plus zomato gold
155/- dinner
12/- misc

30.11.24
25/- pohe
473/- healthy things grocery
80/- paneer and veggie

1.12.24
300/- petrol
Piyush home lunch, badmin 🔵
30/- pinapple juice from piyush, gore 🔴🔴
166/- dinner
790/- harmosa eats
450/- maid
6250/- rent

2.12.24
199/- Netflix 
151/- rice, aata
150/- dinner

3.12.24
70/- paratha
93/- dinner

4.12.24
111/- lunch
141/- dinner

5.12.24
Dinner to somesh 🔵

6.12.24
214/- electricity bill 
38/- cab for party
34/- misc

7.12.24
77/- lunch
"""

def main():
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
