import gzip
import pathlib
import requests
import xarray as xr
import pandas as pd

import functools
import pathlib
import shutil
import requests
from tqdm.auto import tqdm


# https://stackoverflow.com/a/63831344/
def download(url, file_path, overwrite=False, unzip=False):
    """Downloads a file from url and save it to file_path"""

    path = pathlib.Path(file_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    if unzip:
        # remove .gz suffix from path, so we save the unzipped file without .gz
        path = path.with_suffix("")

    if not overwrite and path.exists():
        print(f"File {file_path} already exists, skipping...")
        return path

    r = requests.get(url, stream=True, allow_redirects=True)
    if r.status_code != 200:
        r.raise_for_status()  # Will only raise for 4xx codes, so...
        raise RuntimeError(f"Request to {url} returned status code {r.status_code}")

    file_size = int(r.headers.get("Content-Length", 0))

    desc = "(Unknown total file size)" if file_size == 0 else ""
    r.raw.read = functools.partial(
        r.raw.read, decode_content=True
    )  # Decompress if needed

    with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
        with path.open("wb") as f:
            if unzip:
                gzip_file = gzip.GzipFile(fileobj=r_raw)
                shutil.copyfileobj(gzip_file, f)
            else:
                shutil.copyfileobj(r_raw, f)

    return path


def main():
    def convert_date(fdate):
        """Converts a decimal year to month-year format"""
        year = int(fdate)
        month = int((fdate - year) * 12) + 1
        return f"{month:02d}{year:04d}"

    # # Define the URL of the CRU and Berkely Earth data page
    url_cru = "https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.07/cruts.2304141047.v4.07/tmp/cru_ts4.07.1901.2022.tmp.dat.nc.gz"
    url_berk = "https://berkeley-earth-temperature-hr.s3.amazonaws.com/Gridded/Asia_TAVG_Gridded_1.nc"

    data_path = (
        pathlib.Path(__file__).parent.parent.parent.parent  # Repository root
        / "data"
        / "weather"
    )

    cru_filename, berk_filename = url_cru.split("/")[-1], url_berk.split("/")[-1]

    print("Downloading CRU data...")
    cru_path = download(url_cru, data_path / cru_filename, overwrite=True, unzip=True)
    print("Downloading Berkley data...")
    berk_path = download(url_berk, data_path / berk_filename)

    ds_cru = xr.open_dataset(cru_path)
    df_berk = xr.open_dataset(berk_path)

    # Slice the CRU data for Myanmar
    ds_myanmar_cru = ds_cru["tmp"].sel(lat=slice(10, 30), lon=slice(92, 102))

    # Berkley's "time" column needs to be converted
    df_berk["time"] = pd.to_datetime(
        xr.apply_ufunc(convert_date, df_berk["time"], vectorize=True), format="%m%Y"
    )
    # Slice the Berkley data for Myanmar
    df_myanmar_berk = df_berk["temperature"].sel(
        latitude=slice(10, 30), longitude=slice(92, 102)
    )

    cru_output = "preprocessed_cru_myanmar.dat"
    berk_output = "preprocessed_berk_myanmar.dat"
    ds_myanmar_cru.to_netcdf(data_path / cru_output)
    df_myanmar_berk.to_netcdf(data_path / berk_output)


if __name__ == "__main__":
    main()
