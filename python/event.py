import cv2
import numpy as np
#sourch from chat gpt

# 초기값 설정
drawing = False       # 마우스 클릭 여부
last_point = (-1, -1) # 마지막 마우스 위치
color = (0, 0, 255)   # 초기 색상 (빨강)

# 마우스 콜백 함수
def draw(event, x, y, flags, param):
    global drawing, last_point, color, image

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            cv2.line(image, last_point, (x, y), color, thickness=3)
            last_point = (x, y)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.line(image, last_point, (x, y), color, thickness=3)

def main():
    global image, color
    width, height = 800, 600
    image = np.ones((height, width, 3), np.uint8) * 255  # 흰색 배경

    cv2.namedWindow("Paint")
    cv2.setMouseCallback("Paint", draw)

    while True:
        cv2.imshow("Paint", image)
        key = cv2.waitKey(1) & 0xFF

        if key == 27:  # ESC 종료
            break
        elif key == ord('r'):
            color = (0, 0, 255)   # 빨강 (BGR)
        elif key == ord('g'):
            color = (0, 255, 0)   # 초록
        elif key == ord('b'):
            color = (255, 0, 0)   # 파랑

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
