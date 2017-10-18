import cv2


'''
Params:
    frame - np.array
    height - int
    scale - array fx, fy
'''
def downscale(frame, height=None, scale=[]):
    if height is not None:
        width = frame.shape[1] * height / frame.shape[0]
        return cv2.resize(frame, (width, height))
    if len(scale):
        return cv2.resize(frame, (0, 0), fx=scale[0], fy=scale[1])
    else:
        return frame

def frame_generator(filename='', feed=None):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        frame = cv2.imread(filename)
        yield filename, frame
    else:
        frame_number = 0

        if filename.startswith('/dev/video'):
            video = cv2.VideoCapture(int(filename[10:]))
        elif len(filename) > 0:
            video = cv2.VideoCapture(filename)
        elif feed is not None:
            video = cv2.VideoCapture(feed)
        else:
            yield '{}#{:06d}'.format("Can't process filename", frame_number), None

        while True:
            _, frame = video.read()

            if frame is None:
                break

            yield '{}#{:06d}'.format(filename, frame_number), frame
            frame_number += 1

        video.release()


if __name__ == '__main__':
    frames = frame_generator(feed=1)

    for frame_number, frame in frames:
        if frame is None:
            print frame_number
            break

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

