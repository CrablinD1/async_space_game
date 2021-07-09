import os


def get_garbage_frames():
    garbage_frames = []
    filesnames = os.listdir("./space_garbage")
    for filename in filesnames:
        path = os.path.join("./space_garbage", filename)
        with open(path, "r") as file:
            garbage_frames.append(file.read())
    return garbage_frames
