import os
import csv

def main():
    root_dir= "root/path/to/dataset"
    save_dir= "path/to/save"
    file_name= "singapore-traffic-density.csv"
    csv_path= os.path.join(save_dir, file_name)

    with open(csv_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["img_path", "split", "label"])

        for split in os.listdir(root_dir):
            subdir_path = os.path.join(root_dir, split)
            if os.path.isdir(subdir_path):
                for label in os.listdir(subdir_path):
                    label_dirs = os.path.join(subdir_path, label)
                    if os.path.isdir(label_dirs):
                        for img_name in os.listdir(label_dirs):
                            img_path = os.path.join(label_dirs, img_name)
                            if os.path.isfile(img_path):
                                writer.writerow([img_path, split,  label])


if __name__ == "__main__":
    main()