import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
import random
from pathlib import Path
import platform
import time

# Initialize total_time as a global variable
total_time = 0

# Check both possible file locations
ec2_path = '/home/ec2-user/test.json'
local_path = '/Users/alexbielanski/pythonProject1/test.json'

SERVICE_ACCOUNT_FILE = ec2_path if Path(ec2_path).exists() else local_path
if not Path(SERVICE_ACCOUNT_FILE).exists():
    raise FileNotFoundError("Service account JSON file not found in either location")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)

SPREADSHEET_ID = '1oUOWFWj-nYWiXKMb4cD1cd4RPKAX5nmMrWcRbpL_cXI'



answer = input("Did you update the cells? (y/n): ").lower()
if answer == 'n':
    print("Program terminated. Please update cells before continuing.")
    exit()
elif answer == 'y':
    pass  # Program continues with existing code
else:
    print("Invalid input. Please enter 'y' or 'n'.")
    exit()


def generate_numbers():
    global total_time  # Declare we'll use the global total_time
    start_time = time.time()  # Start timing

    def repeat():
        a = random.randint(1, 4)
        b = random.randint(1, 6)
        c = random.randint(1, 8)
        d = random.randint(1, 10)
        e = random.randint(1, 12)
        f = random.randint(1, 20)
        return a == 4 and b == 6 and c == 8 and d == 10 and e == 12 and f == 20

    mylist = []

    for x in range(500):
        i = 0
        while True:
            i += 1
            if repeat():
                break

        mylist.append(i)
        if (x + 1) % 1 == 0:
            elapsed_time = time.time() - start_time
            print(f"Completed {x + 1} iterations in {elapsed_time:.2f} seconds")

    global total_time
    total_time = time.time() - start_time  # Assign to global variable
    print(f"\nTotal execution time: {total_time:.2f} seconds")
    return mylist


results = generate_numbers()
wrapped_results = [[value] for value in results]
RANGE_NAME = 'Sheet1!A29502:A30000'

body = {
    'values': wrapped_results
}

try:
    # Update the main results
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME,
        valueInputOption="RAW",
        body=body
    ).execute()
    print(f"{result.get('updatedCells')} cells updated.")

    # Add total time to cell AB44
    time_body = {
        'values': [[total_time]]
    }
    time_result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range='Sheet1!AB49',
        valueInputOption="RAW",
        body=time_body
    ).execute()
    print(f"Execution time ({total_time:.2f} seconds) written to cell AB48")

except Exception as e:
    print(f"An error occurred: {e}")

