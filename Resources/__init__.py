import os
import glob
import random
from pathlib import Path

__videos_path = Path(__file__).parent.joinpath("videos")


def get_batches():
    files = glob.glob(str(__videos_path.joinpath('*')))
    dirs = list(filter(os.path.isdir, files))
    return dirs


def get_videos():
    from Settings import Settings
    if Settings.order_of_videos != "two batches, random":
        videos = [os.path.abspath(path) for path in glob.glob(str(__videos_path.joinpath('**')))] # TODO: Fixme pathing
        if videos == []:
            raise ValueError("No videos found in " + str(__videos_path))  # TODO: Fixme pathing
        return videos
    else:
        dirs = get_batches()
        if len(dirs) != 2:
            if len(dirs) > 2:
                raise ValueError(f"Found more than two film batches ({len(dirs)}), don't know what to do :<")
            else:
                raise ValueError(f"Found less than 2 batches ({len(dirs)}), don't know what to do :<")

        dirs.remove(Settings._starting_batch)
        first = Settings._starting_batch
        second = dirs[0]
        first = [os.path.abspath(path) for path in glob.glob(os.path.join(first, '*'))]
        second = [os.path.abspath(path) for path in glob.glob(os.path.join(second, '*'))]
        random.shuffle(first)
        random.shuffle(second)
        output = []
        for x in zip(first, second):
            output.append(x[0])
            output.append(x[1])
        return output

images = [os.path.abspath(path) for path in glob.glob('./Resources/images/*')]
if images == []:
    raise ValueError("No matrices found in " + os.path.abspath("./Resources"))  # TODO: Fixme pathing
languages = []
for language_file in glob.glob('./Resources/text/*'):
    name = os.path.basename(language_file.strip('.py'))
    if name not in ['__init__', '__pycache__']:
        languages.append(name)
if languages == []:
    raise ValueError("No language files found in " + os.path.abspath("./Resources/text"))


def import_text():
    global text
    from Resources.text import text
