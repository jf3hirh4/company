import os
import cv2
from ultralytics import YOLO
from pathlib import Path

def process_single_video_with_yolo(video_path, model_path, annotated_dir, non_annotated_dir, fps_to_process,conf=0.25, iou=0.45):
    """
	video_path영상을 model_path에 있는 모델로 검출하고 검출된 frame을 1초당 fps_to_process만큼
	라벨링 있게 만든 사진은 annotated_dir경로에 저장하고
	없게 만든 사진을 non_annotated_dir에 저장한다.
	
	model_path : 모델의 경로
	video_path : 검출할 영상경로
	annotated_dir : 라벨링 있는 사진 저장 경로 폴더
	non_annotated_dir : 라벨링 없는 사진 저장 경로 폴더
    fps_to_process : 1초당 몇 프레임을 저장할지
	"""
      
    # 출력 디렉토리 생성
    os.makedirs(annotated_dir, exist_ok=True)
    os.makedirs(non_annotated_dir, exist_ok=True)

    # 모델 로드
    model = YOLO(model_path)

    cap = cv2.VideoCapture(video_path) #cv로 영상을 불러온다.
    original_fps = cap.get(cv2.CAP_PROP_FPS) # 비디오의 프레임수 가져온다.
    frame_interval = int(original_fps // fps_to_process) if original_fps >= fps_to_process else 1
    #몇 프레임마다 처리할지 간격을 계산하는 코드
    #만약 original_fps가 fps_to_process보다 작으면 모든프레임 처리(else 1)

    frame_count = 0
    saved_count = 0
    file = os.path.basename(video_path) #파일명만 추출

    while cap.isOpened(): #비디오가 열려있는 동안
        ret, frame = cap.read() #프레임을 한장씩 읽는다
        if not ret: #영상이 끝나면
            break # 끝

        frame_count += 1

        # 프레임 스킵
        if frame_count % frame_interval != 0:
            continue

        results = model.predict(
            source=frame,
            conf=conf,
            iou=iou,
            verbose=True
        )

        if results and len(results[0].boxes) > 0: #바운딩 박스 정보가 하나라도 있으면
            saved_count += 1
            frame_name = f"{Path(file).stem}_frame{saved_count}.jpg" # 이미지의 파일 이름 만드는것
            annotated_path = os.path.join(annotated_dir, frame_name) # 라벨있는 사진 저장 경로
            non_annotated_path = os.path.join(non_annotated_dir, frame_name) # 라벨없는 사진 저장 경로

            # 라벨 없는 원본 저장
            cv2.imwrite(non_annotated_path, frame)

            # 라벨 포함된 이미지 저장
            annotated_img = results[0].plot() # 박스 및 라벨 그려진 이미지
            cv2.imwrite(annotated_path, annotated_img) #이미지를 디스크에 저장하는 함수

    cap.release()
model_path = '/home/choi/road_robot/runs/detect/train1/weights/buser_best.pt'
video_path = '/home/choi/road_robot/vvideo/am/2025-05-13_10-59-19.mp4'
annotated_dir = '/home/choi/road_robot/model_l/anotated'
non_annotated_dir = '/home/choi/road_robot/model_l/non_anotated'
fps_to_process = 5

process_single_video_with_yolo(video_path, model_path, annotated_dir, non_annotated_dir,fps_to_process)
