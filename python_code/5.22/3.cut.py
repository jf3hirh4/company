import os
import shutil


def copy_first_1000_files(src_images_dir, src_labels_dir, dst_images_dir, dst_labels_dir, limit):
    """
    이미지 및 라벨 파일을 limit개수로만 복사하는 함수
    src_images_dir : 원본 이미지 폴더
    src_labels_dir : 원본 라벨 폴더
    dst_images_dir : 복사할 이미지 목적지
    dst_labels_dir : 복사할 라벨 목적지
    limit : 복사할 개수
)
    """
    # 대상 디렉토리 생성 (존재하지 않으면 생성)
    os.makedirs(dst_images_dir, exist_ok=True)
    os.makedirs(dst_labels_dir, exist_ok=True)

    # 소스 이미지 디렉토리에서 이미지 파일 목록 가져오기 (.jpg, .jpeg, .png 확장자)만
    image_files = sorted([
        f for f in os.listdir(src_images_dir)
        if f.lower().endswith(('.jpg', '.jpeg', '.png'))
    ])

    # 소스 라벨 디렉토리에서 라벨 파일 목록 가져오기 (.txt 확장자)만
    label_files = sorted([
        f for f in os.listdir(src_labels_dir)
        if f.lower().endswith('.txt')
    ])

    # 이미지 파일 복사 (앞 limit개)
    for f in image_files[:limit]:
        shutil.copy2(os.path.join(src_images_dir, f), os.path.join(dst_images_dir, f))
    print(f"Copied {min(len(image_files), limit)} images to {dst_images_dir}")

    # 라벨 파일 복사 (앞 limit개)
    for f in label_files[:limit]:
        shutil.copy2(os.path.join(src_labels_dir, f), os.path.join(dst_labels_dir, f))
    print(f"Copied {min(len(label_files), limit)} label files to {dst_labels_dir}")

# 함수 호출 예시
copy_first_1000_files(
    '/home/choi/ai_hub/result_images',  
    '/home/choi/ai_hub/result_labels',   
    '/home/choi/ai_hub/short_images',    
    '/home/choi/ai_hub/short_labels',
    limit=1000                           
)