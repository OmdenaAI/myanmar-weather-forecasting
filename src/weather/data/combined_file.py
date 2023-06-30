import gzip
import pathlib
import requests
import xarray as xr


def main():
    # Function to convert decimal date to month-year format
    def convert_date(fdate):
        year = int(fdate)
        month = int((fdate - year) * 12) + 1
        return f'{month:02d}{year:04d}'
    
    # # Define the URL of the CRU and Berkely Earth data page
    url_cru = "https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.07/cruts.2304141047.v4.07/tmp/cru_ts4.07.1901.2022.tmp.dat.nc.gz"
    url_berk = "https://berkeley-earth-temperature-hr.s3.amazonaws.com/Gridded/Asia_TAVG_Gridded_1.nc"

    data_path = (
        pathlib.Path(__file__).parent.parent.parent.parent  # Repository root
        / "data"
        / "weather"
    )

    # Send a GET request to download the CRU data
    response_cru = requests.get(url_cru)
    
    # Decompress the gzipped data returned by CRU
    compressed_data_cru = response_cru.content
    uncompressed_data_cru = gzip.decompress(compressed_data_cru)
    
    # Check if the CRU data was downloaded successfully
    if response_cru.status_code == 200:
        file_name = url_cru.split('/')[-1]
        file_path = data_path / file_name
        
        # Save the uncompressed data to a file
        with open(file_path, "wb") as file:
            file.write(uncompressed_data_cru)
        
        # Open the dataset using xarray
        ds_cru = xr.open_dataset(file_path)
        
        # Slice the data for Myanmar
        ds_myanmar_cru = ds_cru['tmp'].sel(lat=slice(10, 30), lon=slice(92, 102))
        
        # Save the preprocessed data to a NetCDF file
        output_file = "preprocessed_cru_myanmar.dat"
        ds_myanmar_cru.to_netcdf(output_file)
        
        print('Data unzipped and preprocessed successfully. Preprocessed data saved to:', output_file)
    else:
        print('Error downloading data:', response_cru.status_code)
        
    # Send a GET request to download the Berkeley Earth data  
    response_berk = requests.get(url_berk)    
        
    # Check if the Berkeley Earth data was downloaded successfully
    if response_berk.status_code == 200:      
        file_name = url_berk.split('/')[-1]
        file_path = data_path / file_name
        
        # Save the data to a file
        with open(file_path, "wb") as file:
            file.write(response_berk.content)
            
        # Open the dataset using xarray
        df_berk = xr.open_dataset(file_path)
        
        # convert decimal date to month-year format using the function convert_date
        df_berk['time'] = pd.to_datetime(xr.apply_ufunc(convert_date, df_berk['time'], vectorize=True), format='%m%Y')
        
        # Slice the data for Myanmar
        df_myanmar_berk = df_berk['temperature'].sel(latitude=slice(10, 30), longitude=slice(92, 102))
        
        # Save the preprocessed data to a NetCDF file
        output_file = "preprocessed_berk_myanmar.dat"
        df_myanmar_berk.to_netcdf(output_file)
        
        print('Data unzipped and preprocessed successfully. Preprocessed data saved to:', output_file)
    else:
        print("Failed to download the data.")

if __name__ == '__main__':
    main()