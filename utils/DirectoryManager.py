import json
from pathlib import Path
import os
from typing import Any


class DirectoryManager:
    def __init__(self, path: str):
        self.cwd = str(Path.cwd())
        self.img_dir = self.cwd + path
        self.image_repository: Any = {}

        with os.scandir(self.img_dir) as directories:
            for dir in directories:
                if os.path.isfile(dir):
                    continue
                final_dir = self.img_dir + dir.name
                entries = os.listdir(final_dir)
                temp_dir = {}

                for name_long in entries:
                    name = name_long.split(".")[0]
                    temp_dir[f"{name}"] = f"./img/{dir.name}/{name_long}"
                    setattr(self, f"{dir.name}", name)
                self.image_repository[f"{dir.name}"] = temp_dir

    def create_json(self, output_path: str):
        with open(output_path, "w") as outfile:
            json.dump(self.image_repository, outfile)

    def create_python(self, output_path: str):
        with open(output_path, "w") as file:
            file.write("image_repository = ")
            file.write(f"{self.image_repository}")

    def create_types(self, output_path: str):
        with open(f"{output_path}", "w") as file:
            file.write("from typing import Literal\n")
            all: list[str] = []
            keys: list[str] = []
            for key, iterable in self.image_repository.items():
                keys.append(f"'{key}'")
                # creating array of
                temp: list[str] = []
                for name_long in iterable:
                    name = name_long.split(".")[0]
                    all.append(f"'{name}'")
                    temp.append(f"'{name}'")
                string = ", ".join(temp)

                # create array literal
                file.write(f"{key} = Literal[{string}]\n")
                if key == "status_mu" or key == "status_mcu" or key == "status_gen":
                    file.write(f"{key.upper()}: list[{key}] = [{string}]\n")
                else:
                    file.write(f"{key.upper()}: list[str] = [{string}]\n")
            # key array
            string = ", ".join(keys)
            file.write(f"keys = Literal[{string}]\n")
            # all buttons
            string = ", ".join(all)
            file.write(f"all_buttons = Literal[{string}]\n")


if __name__ == "__main__":
    dm = DirectoryManager("/img/")
    # dm.create_json("./img/image_repository.json")
    dm.create_python("ComputerVision/image_repository.py")
    dm.create_types("ComputerVision/cv_types.py")
