import os
import shutil
import re

base_dir = os.path.abspath(os.path.dirname(__file__))

src_anotated = os.path.join(base_dir, "model_n_cvat", "anotated")
src_non_annotated = os.path.join(base_dir, "model_n_cvat", "non_annotated")
dst_base = os.path.join(base_dir, "model_n_cvat_result")

dst_images = os.path.join(dst_base, "images")
dst_labels = os.path.join(dst_base, "labels")
dst_anotated = os.path.join(dst_base, "anotated")  # 추가 폴더

os.makedirs(dst_images, exist_ok=True)
os.makedirs(dst_labels, exist_ok=True)
os.makedirs(dst_anotated, exist_ok=True)

# 1. anotated 폴더에서 이미지 및 라벨 복사 (images, labels 용)
for file in os.listdir(src_anotated):
    if file.lower().endswith((".jpg", ".png")):
        label_name = os.path.splitext(file)[0] + ".txt"
        label_path = os.path.join(src_anotated, label_name)
        if os.path.exists(label_path):  # 라벨 파일이 있을 때만 복사
            shutil.copy(os.path.join(src_anotated, file), dst_images)
            shutil.copy(label_path, dst_labels)

# 2. non_anotated 폴더의 이미지 복사 (라벨 없음)
for file in os.listdir(src_non_annotated):
    if file.lower().endswith((".jpg", ".png")):
        shutil.copy(os.path.join(src_non_annotated, file), dst_images)

# 3. anotated 폴더에서 라벨링된 이미지(라벨 파일이 있는)만 dst_anotated에 복사 (txt는 복사하지 않음)
for file in os.listdir(src_anotated):
    if file.lower().endswith((".jpg", ".png")):
        label_name = os.path.splitext(file)[0] + ".txt"
        label_path = os.path.join(src_anotated, label_name)
        if os.path.exists(label_path):  # 라벨 파일이 있을 때만 이미지 복사
            shutil.copy(os.path.join(src_anotated, file), dst_anotated)

print("✅ 라벨링된 이미지(라벨 파일 제외)만 anotated 폴더에 복사 완료되었습니다.")

# 클래스 리스트 직접 작성 또는 읽기 (예시는 직접 작성)
class_names = ["label"]  # 실제 클래스명으로 바꾸세요

# 숫자 추출 함수
def extract_frame_number(filename):
    match = re.search(r'frame(\d+)', filename)
    if match:
        return int(match.group(1))
    else:
        return -1

# 1) obj.names 생성
with open(os.path.join(dst_labels, "obj.names"), "w") as f_names:  # 변경: dst_base -> dst_labels
    for c in class_names:
        f_names.write(c + "\n")

# 2) train.txt 생성 (dst_images 폴더 내 모든 이미지 경로 숫자 기준 정렬 후 상대 경로로)
with open(os.path.join(dst_labels, "train.txt"), "w") as f_train:  # 변경: dst_base -> dst_labels
    image_files = [f for f in os.listdir(dst_images) if f.lower().endswith((".jpg", ".png"))]
    image_files_sorted = sorted(image_files, key=extract_frame_number)
    for img_file in image_files_sorted:
        f_train.write(f"{img_file}\n")

# 3) obj.data 생성
num_classes = len(class_names)
with open(os.path.join(dst_labels, "obj.data"), "w") as f_data:  # 변경: dst_base -> dst_labels
    f_data.write(f"classes= {num_classes}\n")
    f_data.write(f"train  = train.txt\n")
    f_data.write(f"names = obj.names\n")

print("✅ obj.names, train.txt, obj.data 파일 생성 완료") 


import zipfile

def zip_folder(folder_path, zip_path):
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                # zip 안에 들어갈 상대 경로 (폴더명 포함)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, arcname=rel_path)

# anotated 폴더 압축
zip_folder(dst_anotated, os.path.join(dst_base, "anotated.zip"))

# images 폴더 압축
zip_folder(dst_images, os.path.join(dst_base, "images.zip"))

# labels 폴더 압축
zip_folder(dst_labels, os.path.join(dst_base, "labels.zip"))

print("✅ anotated, images, labels 폴더 각각 zip 파일로 압축 완료")
