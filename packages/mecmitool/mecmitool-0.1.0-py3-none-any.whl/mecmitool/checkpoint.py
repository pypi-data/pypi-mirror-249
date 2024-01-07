import os
import pickle


def checkpoint(temp_path):
    if os.path.isdir(temp_path):
        temp_path = os.path.join(temp_path, "temp.pkl")

    def _checkpoint(func):
        def wrapper():
            if os.path.exists(temp_path):
                with open(temp_path, "rb") as f:
                    temp_data = pickle.load(f)
            else:
                temp_data = func()
                with open(temp_path, "wb") as f:
                    pickle.dump(temp_data, f)
            return temp_data

        return wrapper

    return _checkpoint
