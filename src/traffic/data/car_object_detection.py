import pathlib
from kaggle.api.kaggle_api_extended import KaggleApi


def main():
    api = KaggleApi()
    api.authenticate()

    dataset_owner = "sshikamaru"
    dataset_name = "car-object-detection"

    download_path = (
        pathlib.Path(__file__).parent.parent.parent.parent / "data" / "traffic"
    )

    api.dataset_download_files(
        f"{dataset_owner}/{dataset_name}",
        path=download_path,
        quiet=False,
        force=False,
        unzip=True,
    )

    # by default, dataset goes into a "data" folder
    # this changes "data" to dataset_name
    (download_path / "data").rename(download_path / dataset_name)


if __name__ == "__main__":
    main()
