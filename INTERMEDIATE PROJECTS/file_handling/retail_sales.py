# ==================================================
# PROJECT 01: RETAIL SALES FILE PROCESSING
# ==================================================

# Objective:
# Read, process, validate and clean a CSV file
# using Core Python.

import csv
from datetime import datetime


# ==================================================
# TASK 1: Read the CSV file.
# ==================================================

def read_file(file_name):

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            return file.read()

    except (OSError, UnicodeDecodeError) as e:
        print(f"Error reading file: {e}")
        return None


# ==================================================
# TASK 2: Extract column names.
# ==================================================

def get_columns(data):

    if data is None or data.strip() == "":
        return []

    # Separate the string into individual lines.
    lines = data.splitlines()

    # Select the first line.
    header = lines[0]

    # Separate column names into a list.
    columns = header.split(",")

    return columns


# ==================================================
# TASK 3: Extract sales records without the header.
# ==================================================

def get_records(data):

    if data is None or data.strip() == "":
        return []

    lines = data.splitlines()

    # Select all lines except the first line.
    records = lines[1:]

    return records


# ==================================================
# TASK 4: Convert records into a list of lists.
# ==================================================

def parse_records(records):

    parsed_records = []

    for record in records:

        # Separate individual values.
        values = record.split(",")

        parsed_records.append(values)

    return parsed_records


# ==================================================
# TASK 5: Convert records into a list of dictionaries.
# ==================================================

def create_dictionaries(columns, parsed_records):

    sales_records = []

    for values in parsed_records:

        # Check whether columns and values match.
        if len(columns) != len(values):
            print("Invalid record:", values)
            continue

        # Match column names with values.
        record = dict(zip(columns, values))

        sales_records.append(record)

    return sales_records


# ==================================================
# TASK 6: Convert numeric data types.
# ==================================================

def convert_data_types(sales_records):

    converted_records = []

    for record in sales_records:

        # Protect the original dictionary.
        new_record = record.copy()

        try:
            new_record["quantity"] = int(record["quantity"])
            new_record["unit_price"] = float(record["unit_price"])
            new_record["discount"] = float(record["discount"])

        except (ValueError, TypeError, KeyError) as e:
            print(f"Invalid record: {record}. Error: {e}")
            continue

        converted_records.append(new_record)

    return converted_records


# ==================================================
# TASK 7: Identify missing and empty values.
# ==================================================

def validate_missing_values(converted_records, columns):

    valid_records = []
    invalid_records = []

    for record in converted_records:

        missing_fields = []

        # Check every column in the current record.
        for column in columns:

            value = record.get(column)

            if value is None or str(value).strip() == "":
                missing_fields.append(column)

        # Classify the record after checking all columns.
        if len(missing_fields) > 0:

            invalid_records.append({
                "record": record,
                "missing_fields": missing_fields
            })

        else:
            valid_records.append(record)

    return valid_records, invalid_records


# ==================================================
# TASK 8: Validate order dates.
# ==================================================

def validate_dates(valid_records):

    valid_dates = []
    invalid_dates = []

    for record in valid_records:

        try:
            order_date = record["order_date"]

            # Convert the string into a datetime object.
            date = datetime.strptime(order_date, "%Y-%m-%d")

            # Check the exact date format.
            if date.strftime("%Y-%m-%d") != order_date:
                raise ValueError("Incorrect date format")

            valid_dates.append(record)

        except (ValueError, TypeError, KeyError) as e:

            invalid_dates.append({
                "record": record,
                "error": str(e)
            })

    return valid_dates, invalid_dates


# ==================================================
# TASK 9: Identify and separate duplicate records.
# ==================================================

def remove_duplicates(valid_dates):

    seen_ids = set()
    unique_records = []
    duplicate_records = []

    for record in valid_dates:

        order_id = record["order_id"]

        # Check whether the order ID already exists.
        if order_id in seen_ids:
            duplicate_records.append(record)

        else:
            seen_ids.add(order_id)
            unique_records.append(record)

    return unique_records, duplicate_records


# ==================================================
# TASK 10: Save the clean dataset.
# ==================================================

def save_clean_data(records, columns, file_name):

    try:
        with open(file_name, "w", newline="", encoding="utf-8") as file:

            # Create a writer for dictionaries.
            writer = csv.DictWriter(file, fieldnames=columns)

            # Write column names.
            writer.writeheader()

            # Write all records.
            writer.writerows(records)

        print("Clean dataset saved successfully.")

    except (OSError, ValueError, csv.Error) as e:
        print(f"Error saving file: {e}")


# ==================================================
# EXECUTE ALL FUNCTIONS
# ==================================================

# Task 1
sales_data = read_file("retail_sales.csv")

if sales_data is not None and sales_data.strip() != "":

    # Task 2
    columns = get_columns(sales_data)

    # Task 3
    records = get_records(sales_data)

    # Task 4
    parsed_records = parse_records(records)

    # Task 5
    sales_records = create_dictionaries(columns, parsed_records)

    # Task 6
    converted_records = convert_data_types(sales_records)

    # Task 7
    valid_records, missing_records = validate_missing_values(
        converted_records, columns
    )

    # Task 8
    valid_dates, invalid_dates = validate_dates(valid_records)

    # Task 9
    unique_records, duplicate_records = remove_duplicates(valid_dates)

    # Task 10
    save_clean_data(unique_records, columns, "clean_sales.csv")

    # Processing summary
    print("\n----- PROCESSING SUMMARY -----")
    print("Original records:", len(records))
    print("Clean records:", len(unique_records))
    print("Rejected records:", len(records) - len(unique_records))

else:
    print("Error: No data available for processing.")
