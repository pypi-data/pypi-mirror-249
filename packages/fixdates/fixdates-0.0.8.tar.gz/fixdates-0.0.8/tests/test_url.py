import sys
sys.path.append("src")

import os
import requests, csv, io
import pytest
from fixdates.main import fixdate

def fetch_gist_raw_text(gist_raw_url):
    response = requests.get(gist_raw_url)
    if response.status_code == 200:
        return response.text
    else:
        print("Failed to fetch raw text content from the Gist.")
        return None
    
def test_gist_url():
    gist_url = "https://gist.githubusercontent.com/zaidwaqi/d1ecf3b9903fe5696a82005c86ad25de/raw/a539aa04cfcd230848c19bfd87b63042d8405d27/fixdates.csv"
    raw_content = fetch_gist_raw_text(gist_url)
    csv_data = io.StringIO(raw_content)
    fixables = []
    unfixables = []
    csv_reader = csv.reader(csv_data, delimiter=',')
    output = []

    for row in csv_reader:
        try:
            raw_date = row[0]
            fixed_date = fixdate(raw_date)
        except(IndexError, ValueError):
            continue

        if fixed_date:
            fixables.append((raw_date, fixed_date))
        else:
            unfixables.append(raw_date)

    assert fixables == [('20-novmb-2023', '2023-NOV-20'), ('11-janary-2021', '2021-JAN-11')]
    assert unfixables == ['12-fsgww4gr-2022', '9-gsdffd-2021']