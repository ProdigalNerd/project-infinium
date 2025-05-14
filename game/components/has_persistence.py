import yaml


class HasPersistence:
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def load_data(self):
        try:
            with open(self.file_path, "r") as file:
                all_data = yaml.safe_load(file)
                return all_data
        except FileNotFoundError:
            print("file not found.")
        except yaml.YAMLError as e:
            print(f"Error reading file: {e}")

        return None

    def save_data(self, data):
        try:
            with open(self.file_path, "a") as file:
                yaml.dump([data.toDict()], file, sort_keys=False)
        except FileNotFoundError:
            print("Save file not found.")
        except yaml.YAMLError as e:
            print(f"Error writing to file: {e}")