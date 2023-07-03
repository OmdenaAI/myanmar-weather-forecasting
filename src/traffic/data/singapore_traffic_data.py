import requests
import pathlib
import shutil


def download(url, file_path, overwrite=False):
    """Downloads a file from url and save it to file_path"""

    path = pathlib.Path(file_path).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    if not overwrite and path.exists():
        print(f"File {file_path} already exists, skipping...")
        return path

    r = requests.get(url, stream=True, allow_redirects=True)
    if r.status_code != 200:
        r.raise_for_status()  # Will only raise for 4xx codes, so...
        raise RuntimeError(f"Request to {url} returned status code {r.status_code}")

    with path.open("wb") as f:
        r.raw.decode_content = True
        shutil.copyfileobj(r.raw, f)

    return path


def main():
    urls = [
        "https://storage.data.gov.sg/road-traffic-conditions/resources/average-daily-traffic-volume-entering-the-city-2017-04-02T13-15-50Z.csv",
        "https://data.gov.sg/dataset/8f0dbbe0-7788-4d77-a7a3-d741b115d12a/resource/bdfdb0b5-c3a4-4dc9-8a9a-ec130ba9fd0f/download/average-speed-during-peak-hours.csv",
    ]

    data_path = (
        pathlib.Path(__file__).parent.parent.parent.parent  # Repository root
        / "data"
        / "traffic"
    )

    for url in urls:
        print(f"Downloading {url}...")
        file_name = url.split("/")[-1]
        download(url, data_path / file_name)


if __name__ == "__main__":
    main()
