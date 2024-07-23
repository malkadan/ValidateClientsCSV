from utils.validators import Validator
import csv
import yaml
import os


class ValidateCSV():

    def __init__(self):
        self.csv_path = self.get_csv_path_from_user()
        self.email_dict = {}
        self.config = self.read_config_file()

    def get_csv_path_from_user(self):
        # Prompt the user to enter the CSV file path
        csv_path = input("Enter the CSV file path: ").strip()
        return csv_path

    def try_except_decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Exception occurred in {func.__name__}: {str(e)}")
                raise e  # Raise the caught exception again

        return wrapper
    @try_except_decorator
    def read_config_file(self):
        with open('config.yml', 'r') as f:
            return yaml.safe_load(f)
    @try_except_decorator
    def read_csv_as_dict(self):
        with open(self.csv_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield(row)

    def run(self):
        for row in self.read_csv_as_dict():
            print(row)
            val = Validator(row)
            valid, row_as_dict = val.run()
            print(row_as_dict)
            print(valid)
            if not valid:
                self.write_dict_to_csv(self.config['CSVFiles']['invalid'], row_as_dict)
            else:
                self.write_dict_to_csv(self.config['CSVFiles']['valid'], row_as_dict)
            self.update_dict(row_as_dict)

    def is_duplicate(self, email):
        return self.email_dict.get(email, 0)

    def update_dict(self, row):
        if self.is_duplicate(row['email']) > 0:
            self.email_dict[row['email']] += 1
            self.write_dict_to_csv(self.config['CSVFiles']['duplicate'], row)
        else:
            self.email_dict[row['email']] = 1

    @staticmethod
    def write_dict_to_csv(filename, data):
        fieldnames = data.keys() if data else []
        file_exists = os.path.isfile(filename)
        with open(filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            writer.writerow(data)


if __name__ == "__main__":
    val_csv = ValidateCSV()
    val_csv.run()