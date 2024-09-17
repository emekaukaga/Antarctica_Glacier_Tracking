import requests
import os
from datetime import datetime, timedelta

# Create the Data folder if it doesn't exist
data_dir = "Data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)


# Function to generate the URL based on a date
def generate_url(date):
    return f"https://usicecenter.gov/File/DownloadArchive?prd=134{date.strftime('%m%d%Y')}"


# Current date
current_date = datetime.now()

# Calculate the date two years ago
two_years_ago = current_date - timedelta(days=2 * 365)

# Iterate through each day from the current date to two years ago
current = current_date
while current >= two_years_ago:
    # Generate the download URL
    download_url = generate_url(current)

    # Generate the filename
    file_name = os.path.join(data_dir, f"AntarcticIcebergs_{current.strftime('%m%d%Y')}.csv")

    # Check if the file already exists
    if not os.path.exists(file_name):
        # Download the file
        response = requests.get(download_url)

        if response.status_code == 200:
            # If the file is found, save it
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded: {file_name}")
        else:
            print(f"File not found for date: {current.strftime('%m-%d-%Y')}")

    # Move to the previous day
    current -= timedelta(days=1)

print("Download process completed.")
