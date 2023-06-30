import pathlib
import json
import pandas as pd
import missingno


def main():
    data_path = pathlib.Path(__file__).parent.parent.parent.parent / "data" / "weather"
    input_file = data_path / "open_meteo.json"

    if not input_file.exists():
        raise FileNotFoundError(
            f'File "{input_file}" not found. Did you run the open_meteo.py scritp?'
        )

    with input_file.open("r") as f:
        data = json.load(f)

    df = pd.DataFrame(data["daily"])
    df["latitude"] = data["latitude"]
    df["longitude"] = data["longitude"]
    df["elevation"] = data["elevation"]
    df["country"] = "Myanmar"
    df["city"] = "Tha Phay Wa"

    df.to_csv(data_path / "open_meteo.csv", index=False)


if __name__ == "__main__":
    main()
