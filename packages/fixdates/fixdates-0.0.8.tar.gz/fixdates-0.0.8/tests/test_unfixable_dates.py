import sys
sys.path.append("src")

import os
import csv
import pytest
from fixdates.main import fixdate

def read_sample_data(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append(row)
    return data

def test_fixdate(filename="unfixable_dates.csv"):
    sample_data = read_sample_data("tests/data/" + filename)
    failed_results = []

    for row in sample_data:
        date_column = row[0]

        # Assuming 'fixdate' function processing and validation
        fixed = fixdate(date_column)
        if fixed is not None:  
            failed_results.append(f"Is fixable: Input: {date_column}, Results: {fixed}")  

    if failed_results:
        # Save failed results to a file in reports directory
        os.makedirs("tests/reports", exist_ok=True)
        report_file = "tests/reports/unfixable_dates_failures.txt"
        with open(report_file, "w") as file:
            file.write("Failed results:\n")
            for date in failed_results:
                file.write(date + "\n")

        pytest.fail(f"Failed results saved to {report_file}")        