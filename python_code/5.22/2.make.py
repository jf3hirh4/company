import os

def create_yolo_config_files(base_path):
    """
    label 폴더안에 obj.anmes , train.txt , obj.data 생성
    """
    
    labels_dir = os.path.join(base_path, "short_labels") # 저장 폴더이름 설정(라벨)
    images_dir = os.path.join(base_path, "short_images") # 저장 폴더이름 설정(이미지)

    # 출력 디렉토리 생성 (존재하지 않으면 생성)
    os.makedirs(labels_dir, exist_ok=True)

    # 1. obj.names 파일 생성 (클래스 이름 정의)
    names_path = os.path.join(labels_dir, "obj.names")
    with open(names_path, "w", encoding="utf-8") as f:
        f.write("label\n")  # 하나의 클래스: label
    print(f"Created: {names_path}")

    # 2. train.txt 파일 생성 (labels_dir 폴더 안에)
    train_txt_path = os.path.join(labels_dir, "train.txt")
    with open(train_txt_path, "w", encoding="utf-8") as f:
        # 이미지 디렉토리 내의 파일명만 기록
        for img_file in sorted(os.listdir(images_dir)):
            if img_file.lower().endswith((".jpg", ".png", ".jpeg")):
                f.write(img_file + "\n")
    print(f"Created: {train_txt_path}")

    # 3. obj.data 파일 생성 (YOLO 학습 설정 파일)
    obj_data_path = os.path.join(labels_dir, "obj.data")
    with open(obj_data_path, "w", encoding="utf-8") as f:
        f.write("classes = 1\n")             # 클래스 수
        f.write(f"train = train.txt\n")      # 학습 이미지 목록 경로
        f.write(f"names = obj.names\n")      # 클래스 이름 파일 경로
    print(f"Created: {obj_data_path}")

create_yolo_config_files("/home/choi/ai_hub") 