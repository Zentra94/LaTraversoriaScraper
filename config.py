import os
from pathlib import Path

Path.cwd()
PATH_MAIN = Path(os.path.dirname(__file__))
PATH_STATICS = PATH_MAIN / "statics"
PATH_STATICS_IMAGES = PATH_STATICS / "images"

if __name__ == '__main__':
    print("the main path is: {}".format(PATH_MAIN))
    vars = locals().copy()
    paths = {}
    for k, v in vars.items():
        if k.startswith("PATH_"):
            path = Path(v)
            if path.is_dir():
                print("directory {} already exists".format(v))
            else:
                os.mkdir(path)
                print("directory {} created".format(v))
