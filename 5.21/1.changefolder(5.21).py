import os
import cv2
from ultralytics import YOLO
from pathlib import Path

def process_single_video_with_yolo(video_path, model_path, annotated_dir, non_annotated_dir, fps_to_process, conf=0.25, iou=0.45):
    os.makedirs(annotated_dir, exist_ok=True)
    os.makedirs(non_annotated_dir, exist_ok=True)

    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)
    original_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(original_fps // fps_to_process) if original_fps >= fps_to_process else 1

    frame_count = 0
    saved_count = 0
    file = os.path.basename(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % frame_interval != 0:
            continue

        results = model.predict(
            source=frame,
            conf=conf,
            iou=iou,
            verbose=True
        )

        if results and len(results[0].boxes) > 0:
            saved_count += 1
            frame_name = f"{Path(file).stem}_frame{saved_count}.jpg"
            annotated_path = os.path.join(annotated_dir, frame_name)
            non_annotated_path = os.path.join(non_annotated_dir, frame_name)

            # 라벨 없는 원본 저장
            cv2.imwrite(non_annotated_path, frame)

            # 라벨 포함된 이미지 저장
            annotated_img = results[0].plot()
            cv2.imwrite(annotated_path, annotated_img)

            # YOLO txt 라벨 저장 추가
            label_txt_path = os.path.splitext(annotated_path)[0] + ".txt"
            img_h, img_w = frame.shape[:2]

            with open(label_txt_path, "w") as f:
                for box in results[0].boxes:
                    cls = int(box.cls.cpu().numpy())  # 클래스 id
                    # xyxy 좌표 가져오기 (x1,y1,x2,y2)
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    # 정규화 (0~1 범위로)
                    x_center = ((x1 + x2) / 2) / img_w
                    y_center = ((y1 + y2) / 2) / img_h
                    width = (x2 - x1) / img_w
                    height = (y2 - y1) / img_h
                    # 한 줄에 class_id x_center y_center width height
                    f.write(f"{cls} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    cap.release()

# 변수 설정 및 함수 호출은 동일하게
model_path = '/home/choi/road_robot/runs/detect/train1/weights/best_choi.pt'
video_path = '/home/choi/road_robot/vvideo/am/2025-05-13_10-59-19.mp4'
annotated_dir = '/home/choi/road_robot/model_n_cvat/anotated'
non_annotated_dir = '/home/choi/road_robot/model_n_cvat/non_annotated'
fps_to_process = 5

process_single_video_with_yolo(video_path, model_path, annotated_dir, non_annotated_dir, fps_to_process)
