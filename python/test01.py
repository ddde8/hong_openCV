import cv2

def main():
    print("hello, opencv!")
    print(cv2.__version__)
    imgfile = '/root/hong_openCV/data/lenna.bmp'
    img = cv2.imread(imgfile)
    cv2.imshow("lenna ing", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

    