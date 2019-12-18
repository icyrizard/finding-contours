import cv2

import camera

filename = '/top/receipts/729510.jpg'
filename = '/top/receipts/736814.jpg'

'''
Returns:
    np array
'''
def to_grayscale(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

'''
Returns:
    np array
'''
def blur(frame, blur_x=5, blur_y=5):
    return cv2.GaussianBlur(frame, (blur_x, blur_y), 0)

'''
Returns:
    ret, thres
'''
def threshold(frame, low_threshold=127, high_threshold=255):
    return cv2.threshold(frame, low_threshold, high_threshold, 0)

'''
Returns:
    ret, thres
'''
def canny_edge(frame, threshold_1, threshold_2):
    return cv2.Canny(frame, threshold_1, threshold_2)

'''
show frame
Returns:
    None
'''
def show(frame):
    cv2.imshow('frame', frame)
    cv2.waitKey(0)

'''
Returns:
    contours, hierarchy
'''
def find_contours(frame):
    return cv2.findContours(
        frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )


def draw_contours(frame, contours, hierarchy):
    if hierarchy is None:
        return

    hierarchy = hierarchy[0]

    # For each contour, find the bounding rectangle and draw it
    for component in zip(contours, hierarchy):
        current_contour = component[0]
        current_hierarchy = component[1]

        x,y,w,h = cv2.boundingRect(current_contour)
        hull = cv2.convexHull(current_contour, returnPoints=False)

        if len(hull) < 4:
            continue

        #if current_hierarchy[2] < 0:
            # these are the innermost child components
            # cv2.rectangle(frame, (x, y), (x+w, y+h),(0, 0, 255), 3)
        if current_hierarchy[3] < 0:
            # these are the outermost parent components
            # cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            defects = cv2.convexityDefects(current_contour, hull)

            try:
                for i in range(defects.shape[0]):
                    s, e, f, d = defects[i, 0]

                    start = tuple(current_contour[s][0])
                    end = tuple(current_contour[e][0])
                    far = tuple(current_contour[f][0])

                    cv2.line(frame,start, end, [0, 255, 0], 2)
                    cv2.circle(frame, far, 2, [0, 0, 255], -1)
            except Exception as e:
                continue


def get_contours(frame, draw=True, canny_threshold_1=75, canny_threshold_2=200,
        blur_x=5, blur_y=5):
    gray = to_grayscale(frame)
    blurred = blur(gray, blur_x=blur_x, blur_y=blur_y)

    thres = canny_edge(blurred, canny_threshold_1, canny_threshold_2)
    contours, hierarchy = find_contours(thres)

    if draw:
        draw_contours(blurred, contours, hierarchy)

    return thres, blurred


if __name__ == '__main__':
    frames = camera.frame_generator(feed=0)

    canny_threshold_1 = 75
    canny_threshold_2 = 200

    blur_x = 5
    blur_y = 5

    for frame_number, frame in frames:
        if frame is None:
            break


        frame = camera.downscale(frame, scale=[0.8, 0.8])
        thres, blurred = get_contours(frame,
                canny_threshold_1=canny_threshold_1,
                canny_threshold_2=canny_threshold_2,
                blur_x=blur_x,
                blur_y=blur_y
                )

        cv2.imshow('frame', blurred)
        cv2.imshow('gray', thres)

        k = cv2.waitKey(1) & 0xFF

        if k == ord('B'):
            blur_x -= 2
            blur_y -= 2
            print 'blur', blur_x, blur_y
        if k == ord('b'):
            blur_x += 2
            blur_y += 2
            print 'blur', blur_x, blur_y
        if k == ord('n'):
            print 'canny_threshold_1', canny_threshold_1
        if k == ord('j'):
            canny_threshold_1 -= 10
            print 'canny_threshold_1', canny_threshold_1
        elif k == ord('k'):
            canny_threshold_1 += 10
            print 'canny_threshold_1', canny_threshold_1
        elif k == ord('h'):
            canny_threshold_2 -= 10
            print 'canny_threshold_2', canny_threshold_2
        elif k == ord('l'):
            canny_threshold_2 += 10
            print 'canny_threshold_2', canny_threshold_2
        elif k == ord('q'):
            break


