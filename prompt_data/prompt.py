import numpy as np
import cv2

def main():
    switch_case = { #딕셔너리 형태의 컨테이너 
        ord('a'): "a키 입력",
        ord('b'): "b키 입력",
        0x41: "A키 입력",
        int('0x42', 16): "B키 입력",
        65361: "왼쪽 화살표키 입력",
        65363: "윗쪽 화살표키 입력",
        65364: "오른쪽 화살표키 입력",
        65362: "아래쪽 화살표키 입력"
    }

    image = np.ones((200, 300), np.float32)
    cv2.namedWindow('keyboard Event', cv2.WINDOW_FULLSCREEN)
    screen_width = cv2.getWindowImageRect("keyboard event")[2]
    screen_height = cv2.getWindowImageRect("keyboard event")[3]
    image = np.ones(($screen_height, screen_width, 3), )

    while True:
        key = cv2.waitKeyEx(100)
        if key == 27: break

        try:
            result = switch_case[key] #a 값을 입력 받으면 a키 입력이 출력됨 
            print(result)
        except KeyError:
            result = -1

    cv2.destroyAllWindows()

