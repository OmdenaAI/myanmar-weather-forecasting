import pathlib
import requests
from bs4 import BeautifulSoup


def main():
    # Define the URL of the Berkeley Earth data page
    url = "https://berkeleyearth.org/data/"

    data_path = (
        pathlib.Path(__file__).parent.parent.parent.parent  # Repository root
        / "data"
        / "weather"
        / "berkely_earth"
    )

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the link for the high-resolution gridded data
    link = soup.find(href="https://berkeley-earth-temperature-hr.s3.amazonaws.com/Gridded/Asia_TAVG_Gridded_1.nc")

    if link:
        # Extract the URL of the Asia data from the link's href attribute
        asia_data_url = link.get("href")
        print("Asia data URL:", asia_data_url)
    else:
        print("Asia data not found on the page.")
        
    # Send a GET request to the Asia data URL
    response = requests.get(asia_data_url)

    # Downloads and writes the data if successful. Prints an error message if unsuccessful
    if response.status_code == 200:
        
        # Split the file name of the ASIA data. This is used to extract the data file (netCDF File)
        file_name = asia_data_url.split('/')[-1]
        file_path = data_path / file_name
        
        with open(file_path, "wb") as file:
            file.write(response.content)
        print("Data downloaded successfully.")
    else:
        print("Failed to download the data.")
        
    
if __name__ == '__main__':
    main()