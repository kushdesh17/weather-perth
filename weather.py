from datetime import date

series_titles = [
    "Maximum temperature (Degree C)",
    "Minimum temperature (Degree C)",
    "Rainfall amount (millimetres)",
    "Temperature range (Degree C)"
]

def mean(in_series):
    pass

def variance(in_series):
    pass

def standard_deviation(in_series):
    pass

def filter_series(year_series, month_series, day_series, data_series, max_date=None, min_date=None):
    filtered_data = []

    for year, month, day, value in zip(year_series, month_series, day_series, data_series):
        current_date = date(int(year), int(month), int(day))

        if min_date is not None and current_date < min_date:
            continue

        if max_date is not None and current_date > max_date:
            continue

        filtered_data.append(value)

    return filtered_data

def add_temperature_range(data_table):
    max_series = data_table["Maximum temperature (Degree C)"]
    min_series = data_table["Minimum temperature (Degree C)"]

    temp_range_series = []
    for max_temp, min_temp in zip(max_series, min_series):
        if max_temp is None or min_temp is None:
            temp_range_series.append(None)
        else:
            temp_range_series.append(max_temp - min_temp)

    data_table["Temperature range (Degree C)"] = temp_range_series
    return data_table

def read_csv(file,default_value=None):
    data_table = {}
    with open(file) as f:
        lines = f.readlines()
    lines = [line.strip().split(',') for line in lines]
    for i in range(len(lines[0])):
        data_table[lines[0][i]] = [default_value if (len(line[i]) == 0) else float(line[i]) for line in lines[1:]]
    return data_table

def get_user_choice(options):
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")
    choice = input("Enter the number of your choice: ")
    if choice.lower() == 'exit':
        return None
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options):
        print("Invalid choice. Please try again.")
        return get_user_choice(options)
    choice = int(choice) - 1
    return options[choice]

def menu(data_table):
    print("Select a data series:")
    choice = get_user_choice(series_titles)
    series = data_table[choice]
    print(f"Mean: {mean(data_table[choice])}")

if __name__ == "__main__":
    data = read_csv('weather.csv')
    data = add_temperature_range(data)
    menu(data)