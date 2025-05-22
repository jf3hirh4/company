import os
import cv2
from ultralytics import YOLO

def annotate_videos(model_path: str, input_dir: str, output_dir: str, conf:int, frame_rate:int): # 0.4  30
    """
    model_path에 해당하는 모델을 이용해 input_dir안에 있는 모든 .mp4영상을 객체 탐지후  output_dir 안에 저장하는 함수이다.
    model_path : yolo모델의 절대경로
    input_dir :  mp4영상이 있는 폴더의 절대경로
    output_dir : 탐지한 영상을 저장할 위치
    conf : 신뢰도 ex) 0.4이상인것만 
    frame_rate: 초당프레임수 ex)30

    """
    # 모델 로드
    model = YOLO(model_path)

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True) #output_dir 폴더를 만든다.만약 있어도 그냥 넘어감

    # 입력 디렉토리에서 모든 .mp4 파일 탐색
    for filename in os.listdir(input_dir): # input_dir 에 있는 것 하나씩
        if filename.endswith('.mp4'): # .mp4로 끝나면
            input_path = os.path.join(input_dir, filename) # 해당 mp4의 전체 경로
            output_path = os.path.join(output_dir, f'annotated_{filename}') # 처리된 영상의 저장 경로 , 이름을 annotated_123.mp4로 저장

            cap = cv2.VideoCapture(input_path) # 비디오 열기위한 객체를 만든다.
            fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
            out = cv2.VideoWriter(# 비디오 저장을 위한 객체를 만든다.
                output_path, #저장할 경로
                fourcc, # 비디오 코덱 즉 mp4v
                frame_rate,  #초당 프레임수
                (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) # 원본비디오의 가로 세로 해상도
            )

            while cap.isOpened(): # 영상이 끝날때까지 계속
                ret, frame = cap.read() # 한프레임을 읽는다.
                if not ret: #영상이 끝나면 종료
                    break

                results = model.predict(source=frame, conf=conf, save=False) #yolo로 탐지 
                annotated_frame = results[0].plot() #결과를 박스나 라벨로 그려서 주석 처리된 이미지를 만든다
                out.write(annotated_frame) # 한 프레임씩 저장

            cap.release() #읽기 자원 해제,메모리누수나 파일 손상 방지
            out.release() #쓰기 자원 해제
            print(f"✔️ 처리 완료: {filename}")

    print("✅ 모든 영상 처리 완료!")

# 사용 예시
annotate_videos(
    model_path='/home/choi/road_robot/runs/detect/train1/weights/best.pt',
    input_dir='/home/choi/road_robot/result',
    output_dir='road_robot/annotated',
    conf = 0.4, 
    frame_rate=30.0
)
