import cv2
import numpy as np 

def main():
    olive, violet, brown = (128, 128, 0), (128, 0, 128), (42, 42, 165)
    pt1, pt2 = (50, 230), (50, 310)

    image = np.zeros((350, 500, 3), np.uint8)
    image.fill(255)

    cv2.putText(image, "simplex", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, brown)
    
    cv2.imshow("putText", image)
    cv2.waitKey(0)
    cv2.destroyALLWindows()

    

if __name__ == "__main__":
    main()