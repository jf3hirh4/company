import os
import random
import shutil

def split_dataset(base_dir, image_folder='ima', label_folder='lab', train_ratio=0.8):
    """
    이미지와 라벨 데이터를 학습용과 검증용으로 분리하는 함수이다.
    base_dir: 전체 데이터가 들어 있는 기본 폴더 경로
    image_folder: 이미지들이 있는 하위 폴더 이름 
    label_folder: 라벨들이 있는 하위 폴더 이름 
    train_ratio: 학습 데이터 비율 
    """
    
    # 이미지 및 라벨 폴더 경로 설정
    image_dir = os.path.join(base_dir, image_folder)
    label_dir = os.path.join(base_dir, label_folder)

    # 학습/검증용 이미지 및 라벨 저장 폴더 경로 생성
    train_img_dir = os.path.join(image_dir, 'train')
    val_img_dir = os.path.join(image_dir, 'val')
    train_label_dir = os.path.join(label_dir, 'train')
    val_label_dir = os.path.join(label_dir, 'val')

    # 위의 경로들이 없으면 생성 (이미 존재하면 건너뜀)
    for d in [train_img_dir, val_img_dir, train_label_dir, val_label_dir]:
        os.makedirs(d, exist_ok=True)

    # 이미지 확장자가 .jpg 또는 .png인 파일 목록 가져오기
    image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png'))]

    # 파일 순서를 무작위로 섞음
    random.shuffle(image_files)

    # 학습용/검증용 파일 개수 기준점 설정
    split_idx = int(len(image_files) * train_ratio)
    train_files = image_files[:split_idx]
    val_files = image_files[split_idx:]

    # 학습 및 검증용 파일을 새로운 폴더로 복사하는 내부 함수 정의
    def move_files(file_list, img_src, lbl_src, img_dst, lbl_dst):
        for img_file in file_list:
            name, _ = os.path.splitext(img_file)  # 확장자 제거한 파일명 추출
            label_file = name + '.txt'  # 라벨 파일명 생성 (.txt)

            # 이미지 파일 복사
            shutil.copy2(os.path.join(img_src, img_file), os.path.join(img_dst, img_file))

            # 라벨 파일도 같은 이름으로 복사 (없으면 에러 발생)
            shutil.copy2(os.path.join(lbl_src, label_file), os.path.join(lbl_dst, label_file))

    # 학습용 이미지 및 라벨 복사
    move_files(train_files, image_dir, label_dir, train_img_dir, train_label_dir)
    # 검증용 이미지 및 라벨 복사
    move_files(val_files, image_dir, label_dir, val_img_dir, val_label_dir)

    # 완료 메시지 출력
    print(f"✅ 분할 완료: {len(train_files)}개는 학습용, {len(val_files)}개는 검증용입니다.")
