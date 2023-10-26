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
            keys: list[str] = []
            for key, iterable in self.image_repository.items():
                keys.append(f"'{key}'")
                file.write(key)
                file.write(f" = Literal[")
                temp: list[str] = []
                for index, name_long in enumerate(iterable):
                    name = name_long.split(".")[0]
                    temp.append(name)
                    file.write(f"'{name}'")
                    if index != len(iterable) - 1:
                        file.write(", ")
                file.write("]")
                file.write("\n")
            file.write("keys = Literal[")
            file.write(", ".join(keys))
            file.write("]")
            file.write("\n")


if __name__ == "__main__":
    dm = DirectoryManager("/img/")
    # dm.create_json("./img/image_repository.json")
    dm.create_python("ComputerVision/image_repository.py")
    dm.create_types("ComputerVision/cv_types.py")
