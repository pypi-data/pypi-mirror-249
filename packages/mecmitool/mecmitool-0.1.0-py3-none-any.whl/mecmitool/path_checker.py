"""make input and output file path legal"""


import os


class PathChecker:
    @staticmethod
    def _check_slash(path: str, is_folder: bool = False):
        """Return a legal path, ensuring it exists."""
        path = path.replace("\\", "/")
        if is_folder and path[-1] != "/":
            path += "/"
        return path

    @classmethod
    def check_infile(cls, file_path: str):
        """return legal flie path."""
        file_path = cls._check_slash(file_path)
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"cannot find file: {file_path}")
        return file_path

    @classmethod
    def check_inpath(cls, folder_path: str):
        """return legal folder path, end with '/'."""
        folder_path = cls._check_slash(folder_path, is_folder=True)
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"cannot find folder: {folder_path}")
        return folder_path

    @classmethod
    def check_outpath(
        cls, folder_path: str, overwriting: bool = True, creating: bool = True
    ):
        """Create a folder if it does not exist. Return legal folder path."""
        folder_path = cls._check_slash(folder_path, is_folder=True)
        if os.path.exists(folder_path) and not overwriting:
            raise FileExistsError(f"file existed: {folder_path}")
        elif not os.path.exists(folder_path):
            if creating:
                os.makedirs(folder_path)
            else:
                raise FileNotFoundError(f"cannot find folder: {folder_path}")
        return folder_path

    @classmethod
    def check_outfile(
        cls, file_path: str, overwriting: bool = True, creating: bool = True
    ):
        """Create a folder if it does not exist. Return legal file path."""
        file_path = cls._check_slash(file_path, is_folder=False)
        folder_path = os.path.dirname(file_path)
        if os.path.exists(file_path) and not overwriting:
            raise FileExistsError(f"file existed: {file_path}")
        cls.check_outpath(folder_path, creating=creating)
        return file_path

    @classmethod
    def check_inany(cls, inpath: str):
        """return legal input path."""
        if os.path.isdir(inpath):
            return cls._check_slash(inpath, is_folder=True)
        elif os.path.isfile(inpath):
            return cls._check_slash(inpath)
        else:
            raise FileNotFoundError(f"cannot find file or folder: {inpath}")

    @staticmethod
    def basename(inpath: str):
        """return basename of input file."""
        return os.path.splitext(os.path.basename(inpath))[0]

    @staticmethod
    def dirname(inpath: str):
        """return folder name which input folder path, while return file located folder name."""
        if inpath[-1] != "/":
            return os.path.basename(os.path.dirname(inpath))
        else:
            return os.path.basename(inpath)

    @staticmethod
    def dirpath(inpath: str):
        """return folder path which input folder path, while return file located folder path."""
        if inpath[-1] != "/":
            return f"{os.path.dirname(inpath)}/"
        else:
            return f"{os.path.dirname(os.path.dirname(inpath))}/"


if __name__ == "__main__":
    path = PathChecker.check_outfile(r"D:\data\RE_part\111\6para.pkl")
    print(PathChecker.basename(path))
    print(PathChecker.dirname(path))
    print(PathChecker.dirpath(path))
