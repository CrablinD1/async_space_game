def get_rocket_frames():
    with open("./rocket_frames/rocket_frame_1.txt", "r") as f:
        frame_1 = f.read()
    with open("./rocket_frames/rocket_frame_2.txt", "r") as f:
        frame_2 = f.read()

    rocket_frames = [frame_1, frame_1, frame_2, frame_2]

    return rocket_frames
