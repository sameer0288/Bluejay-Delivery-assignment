import pandas as pd
import os


def analyze_timecard(file_path):
    """
    Analyzes the timecard file and prints employees based on certain conditions.

    Parameters:
    - file_path (str): Path to the timecard file.

    Returns:
    - Tuple of lists: Employees for each category (consecutive_seven_days, less_than_10_hours, more_than_14_hours).
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read the CSV file and handle encoding
    data = pd.read_csv(
        file_path,
        parse_dates=["Time", "Time Out", "Pay Cycle Start Date", "Pay Cycle End Date"],
    )

    # Initialize empty lists for different categories
    consecutive_seven_days = []
    less_than_10_hours = []
    more_than_14_hours = []

    # Check conditions and categorize employees
    for index, row in data.iterrows():
        # Check for 7 consecutive days
        if index + 6 < len(data):
            if (
                data["Time"][index + 6 : index - 1 : -1]
                - data["Time Out"][index + 7 : index][::-1]
            ).dt.days.sum() == 7:
                consecutive_seven_days.append(
                    (data["Employee Name"][index], data["Position ID"][index])
                )

        # Check for less than 10 hours between shifts but greater than 1 hour
        if (
            index > 0
            and (row["Time"] - data["Time Out"][index - 1]).seconds / 3600 > 1
            and (row["Time"] - data["Time Out"][index - 1]).seconds / 3600 < 10
        ):
            less_than_10_hours.append(
                (data["Employee Name"][index], data["Position ID"][index])
            )

        # Check for more than 14 hours in a single shift
        if (row["Time Out"] - row["Time"]).seconds / 3600 > 14:
            more_than_14_hours.append(
                (data["Employee Name"][index], data["Position ID"][index])
            )

    return consecutive_seven_days, less_than_10_hours, more_than_14_hours


def main():
    # Prompt user for file path
    file_path = "/Users\Sameer Ali\Desktop\Bluejay Assignment\Assignment_Timecard.xlsx - Sheet1.csv"

    try:
        # Analyze the timecard file
        (
            consecutive_seven_days,
            less_than_10_hours,
            more_than_14_hours,
        ) = analyze_timecard(file_path)

        # Print the results
        print("\nEmployees who have worked for 7 consecutive days:")
        if consecutive_seven_days:
            for employee, position in consecutive_seven_days:
                print(f"{employee} - {position}")
        else:
            print("No employee found.")

        print(
            "\nEmployees who have less than 10 hours but greater than 1 hour between shifts:"
        )
        if less_than_10_hours:
            for employee, position in less_than_10_hours:
                print(f"{employee} - {position}")
        else:
            print("No employee found.")

        print("\nEmployees who have worked for more than 14 hours in a single shift:")
        if more_than_14_hours:
            for employee, position in more_than_14_hours:
                print(f"{employee} - {position}")
        else:
            print("No employee found.")

        # Write the output to a text file
        with open("output.txt", "w") as output_file:
            output_file.write("Employees who have worked for 7 consecutive days:\n")
            if consecutive_seven_days:
                for employee, position in consecutive_seven_days:
                    output_file.write(f"{employee} - {position}\n")
            else:
                output_file.write("No employee found.\n")

            output_file.write(
                "\nEmployees who have less than 10 hours but greater than 1 hour between shifts:\n"
            )
            if less_than_10_hours:
                for employee, position in less_than_10_hours:
                    output_file.write(f"{employee} - {position}\n")
            else:
                output_file.write("No employee found.\n")

            output_file.write(
                "\nEmployees who have worked for more than 14 hours in a single shift:\n"
            )
            if more_than_14_hours:
                for employee, position in more_than_14_hours:
                    output_file.write(f"{employee} - {position}\n")
            else:
                output_file.write("No employee found.\n")

        print("Output written to output.txt")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
