import cv2
import numpy as np

def put_string(frame, text, pt, value, color=(120, 200, 90)):
    """
    프레임에 텍스트를 출력하는 함수. 그림자 효과를 추가합니다.
    """
    if isinstance(value, float):
        text += str(round(value, 2))
    else:
        text += str(value)
        
    shade = (pt[0] + 2, pt[1] + 2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, text, shade, font, 0.7, (0, 0, 0), 2)  # 그림자 효과
    cv2.putText(frame, text, pt, font, 0.7, color, 2)  # 글자 적기

def main():
    """
    메인 함수: 동영상에서 움직이는 객체를 추적하고 원을 그립니다.
    """
    # 동영상 파일 경로를 설정합니다. 이 경로는 사용자의 환경에 맞게 변경해야 합니다.
    video_path = "/root/hong_openCV/data/vtest.avi"
    cap = cv2.VideoCapture(video_path)

    # 동영상이 제대로 열렸는지 확인합니다.
    if not cap.isOpened():
        print("동영상을 열 수 없습니다. 경로를 확인해주세요:", video_path)
        return

    # 배경 차분 모델을 생성합니다.
    # MOG2는 가우시안 혼합 모델 기반의 배경 차분 알고리즘입니다.
    # history: 배경 모델을 학습하는 데 사용되는 프레임 수
    # varThreshold: 픽셀과 배경 모델 간의 마할라노비스 제곱 거리에 대한 임계값
    # detectShadows: 그림자를 감지할지 여부
    bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

    # 비디오 속성을 가져옵니다.
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    
    # 출력 비디오 파일을 설정합니다.
    output_video_path = "data/vtest_output.avi"
    writer = cv2.VideoWriter(output_video_path, fourcc, fps, size)
    
    # 텍스트 오버레이를 위한 변수
    frame_count = 0
    
    print("동영상 처리 시작...")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 모두 읽었습니다. 또는 오류가 발생했습니다.")
            break
        
        frame_count += 1
        
        # 배경 차분 알고리즘을 적용하여 전경 마스크를 생성합니다.
        fg_mask = bg_subtractor.apply(frame)

        # 노이즈 제거를 위한 모폴로지 연산
        # erode(축소): 작은 점 노이즈 제거
        # dilate(확대): 객체의 구멍을 메우고 객체 영역을 확장
        kernel = np.ones((5, 5), np.uint8)
        fg_mask = cv2.erode(fg_mask, kernel, iterations=1)
        fg_mask = cv2.dilate(fg_mask, kernel, iterations=2)
        
        # 전경 마스크에서 윤곽선을 찾습니다.
        # cv2.RETR_EXTERNAL: 가장 바깥쪽 윤곽선만 찾음
        # cv2.CHAIN_APPROX_SIMPLE: 윤곽선의 꼭지점만 저장하여 메모리를 절약
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 감지된 객체 수를 텍스트로 표시합니다.
        put_string(frame, "Detected Objects: ", (10, 30), len(contours), (255, 255, 0))

        # 감지된 각 객체에 대해 원을 그립니다.
        for contour in contours:
            # 윤곽선 영역(면적)이 너무 작으면 무시하여 노이즈를 제거합니다.
            if cv2.contourArea(contour) < 1000:
                continue

            # 윤곽선의 경계 사각형을 구합니다.
            x, y, w, h = cv2.boundingRect(contour)

            # 객체의 무게중심을 계산합니다.
            M = cv2.moments(contour)
            if M["m00"] != 0:
                center_x = int(M["m10"] / M["m00"])
                center_y = int(M["m01"] / M["m00"])

                # 객체 주위에 원을 그립니다.
                cv2.circle(frame, (center_x, center_y), int(w / 2), (0, 255, 0), 2)
                
                # 객체 중심에 작은 원을 표시합니다.
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

        # 처리된 프레임을 화면에 표시하고 파일에 씁니다.
        cv2.imshow("Object Tracking", frame)
        writer.write(frame)
        
        # 'q' 키를 누르면 루프를 종료합니다.
        if cv2.waitKey(int(1000 / fps)) & 0xFF == ord('q'):
            break

    # 자원을 해제합니다.
    cap.release()
    writer.release()
    cv2.destroyAllWindows()
    print("동영상 처리 완료. 출력 파일:", output_video_path)

if __name__ == "__main__":
    main()
