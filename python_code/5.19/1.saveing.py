import os
import cv2
from ultralytics import YOLO
from pathlib import Path

def process_videos_with_yolo(model_path, video_dirs, annotated_dir, non_annotated_dir, conf=0.25, iou=0.45):
    """
	video_dirs에 있는 영상을 model_path에 있는 모델로 검출하고 검출된 frame을 
	라벨링 있게 만든 사진은 annotated_dir경로에 저장하고
	없게 만든 사진을 non_annotated_dir에 저장한다.
	
	model_path : 모델의 경로
	video_dirs : 검출할 영상의 폴더 경로
	annotated_dir : 라벨링 있는 사진 저장 경로 폴더
	non_annotated_dir : 라벨링 없는 사진 저장 경로 폴더
	"""
    # 출력 디렉토리 생성
    os.makedirs(annotated_dir, exist_ok=True)
    os.makedirs(non_annotated_dir, exist_ok=True)

    # 모델 로드
    model = YOLO(model_path)

    for video_dir in video_dirs:
        for file in os.listdir(video_dir): #video_dir 폴더 안에 있는 모든 파일 하나씩
            if not file.endswith('.mp4'): #뒤가 mp4로 끝나지 않으면
                continue #건너뜀

            video_path = os.path.join(video_dir, file) #경로를 만들어준다.
            cap = cv2.VideoCapture(video_path) #cv로 영상을 불러온다.
            frame_count = 0 #프레임 번호 세는것

            while cap.isOpened(): #비디오가 열려있는 동안
                ret, frame = cap.read() #프레임을 한장씩 읽는다
                if not ret: #영상이 끝나면
                    break # 끝
                frame_count += 1 

                # 객체 탐지 수행 (YOLOv8, 로그 출력 활성화)
                results = model.predict(
                    source=frame,
                    conf=conf,
                    iou=iou,
                    verbose=True
                )

                if results and len(results[0].boxes) > 0: #바운딩 박스 정보가 하나라도 있으면
                    frame_name = f"{Path(file).stem}_frame{frame_count}.jpg" # 이미지의 파일 이름 만드는것
                    annotated_path = os.path.join(annotated_dir, frame_name) # 라벨있는 사진 저장 경로
                    non_annotated_path = os.path.join(non_annotated_dir, frame_name)# 라벨없는 사진 저장 경로

                    # 라벨 없는 원본 저장
                    cv2.imwrite(non_annotated_path, frame)

                    # 라벨이 포함된 이미지 저장
                    annotated_img = results[0].plot()  # 박스 및 라벨 그려진 이미지
                    cv2.imwrite(annotated_path, annotated_img) #이미지를 디스크에 저장하는 함수 

            cap.release()

# 사용 예시
model_path = '/home/choi/road_robot/runs/detect/train1/weights/best_choi.pt'
video_dirs = ['/home/choi/road_robot/vvideo/am', '/home/choi/road_robot/vvideo/pm']
annotated_dir = '/home/choi/road_robot/model_n/anotated'
non_annotated_dir = '/home/choi/road_robot/model_n/non_anotated'

process_videos_with_yolo(model_path, video_dirs, annotated_dir, non_annotated_dir)
