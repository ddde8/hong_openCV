import cv2
import numpy as np

# 전역 변수 설정
is_drawing = False
canvas = None
logo_image = None
last_point = None

# 트랙바 콜백 함수 (아무 작업도 하지 않음)
def on_trackbar_change(pos):
    pass

def on_mouse_event(event, x, y, flags, param):
    """
    마우스 이벤트 콜백 함수.
    마우스 왼쪽 버튼을 누른 상태에서 선을 그립니다.
    """
    global is_drawing, last_point, canvas

    if event == cv2.EVENT_LBUTTONDOWN:
        is_drawing = True
        last_point = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        is_drawing = False
        last_point = None
    elif event == cv2.EVENT_MOUSEMOVE:
        if is_drawing:
            if last_point is not None:
                # 트랙바에서 현재 두께 값을 가져옵니다.
                thickness = cv2.getTrackbarPos('Thickness', 'Draw to Reveal the Logo')
                # 두께가 0일 경우 1로 설정하여 선이 그려지도록 합니다.
                if thickness == 0:
                    thickness = 1
                
                cv2.line(canvas, last_point, (x, y), (0, 0, 0), thickness)
                last_point = (x, y)

def main():
    """
    메인 함수: 트랙바와 마우스 그리기 기능을 결합하여 로고를 비춰 보여줍니다.
    """
    global canvas, logo_image

    # 1. 배경이 될 캔디 이미지와 비출 로고 이미지를 불러옵니다.
    background_image = cv2.imread("/root/hong_openCV/data/candies.png", cv2.IMREAD_COLOR)
    logo_image = cv2.imread("/root/hong_openCV/data/cow.png", cv2.IMREAD_COLOR)

    if background_image is None or logo_image is None:
        raise Exception("이미지 파일을 읽을 수 없습니다. 파일 경로를 확인하세요.")

    # 2. 로고 이미지를 배경 이미지의 크기에 맞게 조절합니다.
    logo_resized = cv2.resize(logo_image, (background_image.shape[1], background_image.shape[0]))

    # 3. 캔버스를 초기화합니다.
    canvas = background_image.copy()

    # 4. 윈도우를 생성하고 마우스 콜백 함수를 연결합니다.
    window_name = 'Draw to Reveal the Logo'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, on_mouse_event)
    
    # 5. 트랙바를 생성하고 윈도우에 추가합니다.
    # 'Thickness'라는 이름의 트랙바를 생성하고, 초기값은 5, 최대값은 20으로 설정합니다.
    cv2.createTrackbar('Thickness', window_name, 5, 20, on_trackbar_change)
    
    print("마우스를 드래그하여 로고를 비춰보세요. 트랙바를 이용하여 선의 두께를 조절할 수 있습니다.")
    print("'r'을 누르면 초기화, 'q'를 누르면 종료됩니다.")

    while True:
        # 그리기 캔버스에서 검은색(0,0,0) 픽셀의 위치를 찾습니다.
        black_pixels = np.where(np.all(canvas == [0, 0, 0], axis=-1))

        # 로고를 배경 위에 복사합니다.
        revealed_image = background_image.copy()
        
        # 검은색 픽셀 위치에 로고 이미지 픽셀을 복사하여 "비춰보이는" 효과를 만듭니다.
        revealed_image[black_pixels] = logo_resized[black_pixels]

        # 최종 이미지를 화면에 표시합니다.
        cv2.imshow(window_name, revealed_image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            # 'r' 키를 누르면 캔버스를 초기화합니다.
            canvas = background_image.copy()
        elif key == ord('q'):
            # 'q' 키를 누르면 루프를 종료합니다.
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
