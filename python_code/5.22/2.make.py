import os

def create_yolo_config_files(base_path):
    """
    label 폴더안에 obj.names , train.txt , obj.data 생성
    클래스 4개일 때 적용
    """
    
    labels_dir = os.path.join(base_path, "zip2_labels") # 저장 폴더이름 설정(라벨)
    images_dir = os.path.join(base_path, "zip2_images") # 저장 폴더이름 설정(이미지)

    # 출력 디렉토리 생성 (존재하지 않으면 생성)
    os.makedirs(labels_dir, exist_ok=True)
    # 클래스 이름 리스트 (4개)
    class_names = ["happy", "angry", "sad", "neutrality"]

    # 1. obj.names 파일 생성 (클래스 이름 정의)
    names_path = os.path.join(labels_dir, "obj.names")
    with open(names_path, "w", encoding="utf-8") as f:
        for name in class_names:
            f.write(name + "\n")  # 클래스 이름 한 줄씩 쓰기
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
        f.write(f"classes = {len(class_names)}\n")  # 클래스 수 4로 설정
        f.write(f"train = train.txt\n")              # 학습 이미지 목록 경로
        f.write(f"names = obj.names\n")              # 클래스 이름 파일 경로
    print(f"Created: {obj_data_path}")

# 함수 호출 (경로는 필요에 맞게 변경)
create_yolo_config_files("/home/choi/project_doje")
