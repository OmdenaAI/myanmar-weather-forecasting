import gzip
import pathlib
import requests


def main():
    # # Define the URL of the CRU data page CRU
    url = "https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.07/cruts.2304141047.v4.07/tmp/cru_ts4.07.1901.2022.tmp.dat.nc.gz"

    data_path = (
        pathlib.Path(__file__).parent.parent.parent.parent  # Repository root
        / "data"
        / "weather"
        / "cru"
    )

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Uncompress the data
        with gzip.open("cru_ts4.07.1901.2022.tmp.dat.nc.gz", "rb") as file:
            data = gzip.decompress(file.read())

        # Save the uncompressed data to the specified file
        file_path = data_path / "cru_ts4.07.1901.2022.tmp.dat"
        with open(file_path, "wb") as file:
            file.write(data)
        print('Data unzipped successfully.')
    else:
        print('Error downloading data:', response.status_code)
        

if __name__ == '__main__':
    main()