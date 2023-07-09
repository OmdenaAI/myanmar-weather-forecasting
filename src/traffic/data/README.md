# Data
This folder contains scripts to download data. Simply run them with `python path/to/file_name.py` to download the data to the [`data/traffic`](/data/traffic/) directory. Refer to June 24th's meeting recording for an example on how to run scripts.

## `car_object_detection.py`
This script downloads the [Car Object Detection dataset](https://www.kaggle.com/datasets/sshikamaru/car-object-detection) from Kaggle. In order for it to work, you need to set up your Kaggle API credentials:

* Sign up for a Kaggle account at https://www.kaggle.com (if you don't have one).

* Go the 'Account' tab of your user profile (`https://www.kaggle.com/<username>/account`)

* Select 'Create API Token'. This will trigger the download of kaggle.json, a file containing your API credentials.

* Place this file in the location `~/.kaggle/kaggle.json` (On Windows, the location is `C:\Users\<Windows-username>\.kaggle\kaggle.json`).

## `singapore_traffic_data.py`
This script downloads two files from [Dataportal.asia](https://dataportal.asia/dataset/192521611_road-traffic-conditions) that contains data on the city of **Singapore**. The files are:

* `average-daily-traffic-volume-entering-the-city-2017-04-02T13-15-50Z.csv`: Contains daily traffic volume recorded between 7.30am-7.00pm on weekdays.

* `average-speed-during-peak-hours.csv`: Contains average speed in expressways and arterial roads for peak hour periods, i.e. 8 to 9am and 6 to 7pm on weekdays.

## Download Singapore Traffic Density Dataset

Run this command to download the dataset from kaggle: <br>
`!kaggle datasets download -d rahat52/traffic-density-singapore --unzip`