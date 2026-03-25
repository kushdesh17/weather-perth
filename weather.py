from datetime import date
import math

series_titles = [
    "Maximum temperature (Degree C)",
    "Minimum temperature (Degree C)",
    "Rainfall amount (millimetres)",
    "Temperature range (Degree C)"
]

stats_options = [
    "Mean", "Variance", "Standard Deviation", "Range", "Interquartile Range"
]

# --- Statistical Functions ---

def mean(in_series):
    clean_data = [x for x in in_series if x is not None]
    return sum(clean_data) / len(clean_data) if clean_data else 0

def variance(in_series):
    clean_data = [x for x in in_series if x is not None]
    if len(clean_data) < 2: return 0
    mu = mean(clean_data)
    return sum((x - mu) ** 2 for x in clean_data) / len(clean_data)

def standard_deviation(in_series):
    return math.sqrt(variance(in_series))

def calculate_range(in_series):
    clean_data = [x for x in in_series if x is not None]
    return max(clean_data) - min(clean_data) if clean_data else 0

def interquartile_range(in_series):
    clean_data = sorted([x for x in in_series if x is not None])
    n = len(clean_data)
    if n < 4: return 0
    
    def get_median(data):
        mid = len(data) // 2
        if len(data) % 2 == 0:
            return (data[mid-1] + data[mid]) / 2
        return data[mid]

    q1 = get_median(clean_data[:n//2])
    # For Q3, if n is odd, skip the middle element
    q3 = get_median(clean_data[(n+1)//2:]) if n % 2 != 0 else get_median(clean_data[n//2:])
    return q3 - q1

# --- Data Processing ---

def filter_series(year_series, month_series, day_series, data_series, min_date=None, max_date=None):
    filtered_data = []
    for y, m, d, value in zip(year_series, month_series, day_series, data_series):
        try:
            current_date = date(int(y), int(m), int(d))
            if (min_date and current_date < min_date) or (max_date and current_date > max_date):
                continue
            filtered_data.append(value)
        except ValueError:
            continue
    return filtered_data

def add_temperature_range(data_table):
    max_series = data_table.get("Maximum temperature (Degree C)", [])
    min_series = data_table.get("Minimum temperature (Degree C)", [])
    data_table["Temperature range (Degree C)"] = [
        (mx - mn) if (mx is not None and mn is not None) else None 
        for mx, mn in zip(max_series, min_series)
    ]
    return data_table

def read_csv(file, default_value=None):
    data_table = {}
    try:
        with open(file) as f:
            lines = [line.strip().split(',') for line in f.readlines()]
        headers = lines[0]
        for i, header in enumerate(headers):
            data_table[header] = [
                float(line[i]) if (i < len(line) and line[i]) else default_value 
                for line in lines[1:]
            ]
    except FileNotFoundError:
        print(f"Error: {file} not found.")
    return data_table

# --- UI Helpers ---

def get_user_choice(options, prompt="Enter the number of your choice: "):
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    choice = input(prompt)
    if choice.lower() == 'exit': return None
    if not choice.isdigit() or not (1 <= int(choice) <= len(options)):
        print("Invalid choice. Try again.")
        return get_user_choice(options, prompt)
    return options[int(choice) - 1]

def get_date_input(prompt):
    date_str = input(f"{prompt} (YYYY-MM-DD) or press Enter to skip: ")
    if not date_str: return None
    try:
        y, m, d = map(int, date_str.split('-'))
        return date(y, m, d)
    except ValueError:
        print("Invalid format. Skipping date filter.")
        return None

# --- Main Menu ---

def menu(data_table):
    while True:
        print("\n--- Weather Data Analysis ---")
        choice = get_user_choice(series_titles, "Select a data series (or type 'exit'): ")
        if choice is None: break

        calc_choice = get_user_choice(stats_options, "Select a calculation: ")
        
        print("\nFilter by date range?")
        start_date = get_date_input("Start date")
        end_date = get_date_input("End date")

        # Prepare the data
        raw_series = data_table[choice]
        filtered_series = filter_series(
            data_table['Year'], data_table['Month'], data_table['Day'], 
            raw_series, start_date, end_date
        )

        if not filtered_series:
            print("No data found for that criteria.")
            continue

        # Map choice to function
        results = {
            "Mean": mean(filtered_series),
            "Variance": variance(filtered_series),
            "Standard Deviation": standard_deviation(filtered_series),
            "Range": calculate_range(filtered_series),
            "Interquartile Range": interquartile_range(filtered_series)
        }

        print(f"\nResult for {choice} ({calc_choice}): {results[calc_choice]:.2f}")

if __name__ == "__main__":
    data = read_csv('weather.csv')
    if data:
        data = add_temperature_range(data)
        menu(data)
