import os
import shutil

def copy_matched_label_image_files(labels_dir, images_dir, result_labels_dir, result_images_dir):
    """
    라벨 파일의 식별자에 해당하는 이미지를 찾아 지정된 결과 폴더에 복사하고 이미지 파일명은 라벨 파일명에 맞춰 변경하는 함수이다.
    
    labels_dir: 원본 라벨(.txt) 파일 경로
    images_dir : 원본 이미지(.jpg) 파일 경로
    result_labels_dir : 복사된 라벨 저장 경로
    result_images_dir : 복사된 이미지 저장 경로
    """
    os.makedirs(result_images_dir, exist_ok=True)
    os.makedirs(result_labels_dir, exist_ok=True)

    matched_count = 0

    for txt_filename in os.listdir(labels_dir):
        if not txt_filename.endswith('.txt'):
            continue

        identifier = txt_filename.split('_')[-1].replace('.txt', '')

        for img_filename in os.listdir(images_dir):
            if identifier in img_filename and img_filename.endswith('.jpg'):
                new_img_filename = txt_filename.replace('.txt', '.jpg')

                shutil.copyfile(
                    os.path.join(images_dir, img_filename),
                    os.path.join(result_images_dir, new_img_filename)
                )

                shutil.copyfile(
                    os.path.join(labels_dir, txt_filename),
                    os.path.join(result_labels_dir, txt_filename)
                )

                matched_count += 1
                break

    print(f"✅ 총 {matched_count}개의 라벨-이미지 쌍이 복사되었습니다.")

# 사용 예시
copy_matched_label_image_files(
    labels_dir='/home/choi/project_doje/ttx',
    images_dir='/home/choi/project_doje/zip1_images',
    result_labels_dir='/home/choi/project_doje/zip2_labels',
    result_images_dir='/home/choi/project_doje/zip2_images'
)
