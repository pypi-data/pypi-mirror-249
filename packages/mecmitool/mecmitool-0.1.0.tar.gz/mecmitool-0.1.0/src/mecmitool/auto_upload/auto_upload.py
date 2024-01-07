import os
import sys
import build.__main__
from mecmitool.path_checker import check_inpath
import mecmitool.auto_upload._twine_main


def upload(path=check_inpath(sys.path[0])):
    files_before = []
    for root, dirs, files in os.walk(path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            print(file_path)
            if file_path not in files_before:
                files_before.append(file_path)
    build.__main__.main([path], "python -m build")
    try:
        mecmitool.auto_upload._twine_main.main(["upload", path + "dist/*"])
    finally:
        for root, dirs, files in os.walk(path, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path not in files_before:
                    os.remove(file_path)
        for root, dirs, files in os.walk(path, topdown=False):
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                if not os.listdir(dir_path):
                    os.rmdir(dir_path)


if __name__ == "__main__":
    upload()