"""
This module implements the main functionality of sma_rsi_indicators.

Author: Yavuz Selim
"""
import csv

def convert_to_dict(csv_file_path):
    """
    Converts the properly given csv file into a python list of dictionaries.
    """
    list_of_data = []
    with open(csv_file_path, "rt") as readfile:
        reader = csv.DictReader(readfile)
        for row in reader:
            list_of_data.append(row)
    return list_of_data

def calculate_sma(list_of_data, sma_file):
    """
    Calculates Simple Moving Averages for a 5-day window given a list of dictionaries and outputs it
    to a csv file with dates and simple moving averages.
    """
    # Calculate sma
    for day in range(4, len(list_of_data)):
        total_of_five = 0
        for offset in range(0,5):
            total_of_five += float(list_of_data[day-offset]["Close"])
        sma = total_of_five / 5
        list_of_data[day]["SMA"] = sma
    # Return sma file
    with open(sma_file, "wt", newline="") as writefile:
        fieldnames = ["Date", "SMA"]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)

        writer.writeheader()
        for element in list_of_data:
            writer.writerow({"Date": element.get("Date"), "SMA": element.get("SMA")})

def calculate_rsi(list_of_data, rsi_file):
    """
    Calculates Relative Strength Indices for a 14-day window given a list of dictionaries and outputs it
    to a csv file with dates and relative strength indices.
    """
    for day in range(1, len(list_of_data)):
        current_day_close = float(list_of_data[day]["Close"])
        prev_day_close = float(list_of_data[day-1]["Close"])
        # Calculate the change and gain/loss depending on the sign of change
        change = current_day_close - prev_day_close
        gain = change if change > 0 else 0
        loss = -change if change < 0 else 0
        # Assign the gain and loss
        list_of_data[day]["Gain"] = gain
        list_of_data[day]["Loss"] = loss

    # Calculate average gain/loss and RS for the 15th day
    total_gain = 0
    total_loss = 0
    for day in range(1, 15):
        total_gain += float(list_of_data[day]["Gain"])
        total_loss += float(list_of_data[day]["Loss"])
    avg_gain = total_gain / 14
    avg_loss = total_loss / 14

    list_of_data[14]["Avg Gain"] = avg_gain
    list_of_data[14]["Avg Loss"] = avg_loss
    rs = avg_gain / avg_loss
    list_of_data[14]["RSI"] = 100 - (100 / (1 + rs))

    # Calculate average gain/loss for the remaining days
    for day in range(15, len(list_of_data)):
        current_day = list_of_data[day]
        current_gain = float(current_day["Gain"])
        current_loss = float(current_day["Loss"])

        # Calculating average gain
        prev_avg_gain = float(list_of_data[day-1]["Avg Gain"])
        avg_gain = (prev_avg_gain * 13 + current_gain) / 14

        # Calculating average loss
        prev_avg_loss = float(list_of_data[day-1]["Avg Loss"])
        avg_loss = (prev_avg_loss * 13 + current_loss) / 14

        current_day["Avg Gain"] = avg_gain
        current_day["Avg Loss"] = avg_loss
        # Calculate RS (Avg Gain / Avg Loss)
        rs = avg_gain / avg_loss
        # Calculate RSI (100 - (100 / (1 + RS)))
        current_day["RSI"] = 100 - (100 / (1 + rs))

    with open(rsi_file, "wt", newline="") as writefile:
        fieldnames = ["Date", "RSI"]
        writer = csv.DictWriter(writefile, fieldnames=fieldnames)

        writer.writeheader()
        for element in list_of_data:
            writer.writerow({"Date": element.get("Date"), "RSI": element.get("RSI")})