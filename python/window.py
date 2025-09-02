import numpy as np
import cv2

def main():
    image = np.zeros((200, 400), np.uint8)
    image[:] = 20

    title, title2 = "Position", "Position2"
    cv2.namedWindow(title, cv2.WINDOW_AUTOSIZE)
    cv2.namedWindow(title2)
    cv2.moveWindow(title, 150, 150)
    cv2.moveWindow(title2, 400, 50)

    cv2.imshow(title, image)
    cv2.imshow(title2, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()    