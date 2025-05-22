import os
import shutil
import re #복잡한 문자열 처리 도와주는 라이브러리
import zipfile

def setup_directories(base_dir):
    """
    필요한 폴더 경로를 설정하고 폴더( images, labels, anotated )를 생성하는 코드이다.

    base_dir : result가 생성되는 위치의 경로

    """
    src_anotated = os.path.join(base_dir, "model_n_cvat", "anotated")
    src_non_annotated = os.path.join(base_dir, "model_n_cvat", "non_annotated")
    dst_base = os.path.join(base_dir, "model_n_cvat_result")

    dst_images = os.path.join(dst_base, "images")
    dst_labels = os.path.join(dst_base, "labels")
    dst_anotated = os.path.join(dst_base, "anotated")

    os.makedirs(dst_images, exist_ok=True)
    os.makedirs(dst_labels, exist_ok=True)
    os.makedirs(dst_anotated, exist_ok=True)

    return src_anotated, src_non_annotated, dst_base, dst_images, dst_labels, dst_anotated


def copy_labeled_images_and_labels(src_anotated, dst_images, dst_labels):
    """
    라벨이 있는 이미지만 dst_images로 복사하고 해당 라벨 파일은 dst_labels로 복사하는 함수이다.

    src_anotated : 원본 anotated 경로
    dst_images : images 폴더 경로
    dst_labels : labels 폴더 경로

    """
    for file in os.listdir(src_anotated):
        if file.lower().endswith((".jpg", ".png")):
            label_name = os.path.splitext(file)[0] + ".txt"
            label_path = os.path.join(src_anotated, label_name)
            if os.path.exists(label_path):  # 라벨 파일 존재 시에만 복사
                shutil.copy(os.path.join(src_anotated, file), dst_images)
                shutil.copy(label_path, dst_labels)


def copy_unlabeled_images(src_non_annotated, dst_images):
    """
    라벨이 없는 이미지들을 dst_images로 복사하는 함수이다.

    src_non_annotated : 원본 non_anotated 경로
    dst_images : images 폴더 경로
    """
    for file in os.listdir(src_non_annotated):
        if file.lower().endswith((".jpg", ".png")):
            shutil.copy(os.path.join(src_non_annotated, file), dst_images)


def copy_only_labeled_images(src_anotated, dst_anotated):
    """
    anotated 폴더 내에서 라벨 파일이 있는 이미지 파일만 dst_anotated로 복사하는 함수이다.

    src_anotated : 원본 anotated 경로
    dst_anotated : anotated 경로
    """
    for file in os.listdir(src_anotated):
        if file.lower().endswith((".jpg", ".png")):
            label_name = os.path.splitext(file)[0] + ".txt"
            label_path = os.path.join(src_anotated, label_name)
            if os.path.exists(label_path):
                shutil.copy(os.path.join(src_anotated, file), dst_anotated)
    print("✅ 라벨링된 이미지(라벨 파일 제외)만 anotated 폴더에 복사 완료되었습니다.")


def extract_frame_number(filename):
    """
    파일에서 frame숫자를 추출하여 정렬하는 함수이다.
    """
    match = re.search(r'frame(\d+)', filename)
    return int(match.group(1)) if match else -1


def create_metadata_files(dst_labels, dst_images, class_names):
    """
    모델 학습에 필요한 metadata 파일들을 생성하는 함수이다.( obj.names,train.txt,obj.data )
    """
    # 1. obj.names 생성
    with open(os.path.join(dst_labels, "obj.names"), "w") as f_names:
        for c in class_names:
            f_names.write(c + "\n")

    # 2. train.txt 생성 (프레임 숫자 기준 정렬)
    image_files = [f for f in os.listdir(dst_images) if f.lower().endswith((".jpg", ".png"))]
    image_files_sorted = sorted(image_files, key=extract_frame_number)
    with open(os.path.join(dst_labels, "train.txt"), "w") as f_train:
        for img_file in image_files_sorted:
            f_train.write(f"{img_file}\n")

    # 3. obj.data 생성
    with open(os.path.join(dst_labels, "obj.data"), "w") as f_data:
        f_data.write(f"classes= {len(class_names)}\n")
        f_data.write(f"train  = train.txt\n")
        f_data.write(f"names = obj.names\n")

    print("✅ obj.names, train.txt, obj.data 파일 생성 완료")


def zip_folder(folder_path, zip_path):
    """
    지정된 폴더를 ZIP 형식으로 압축합하는 함수이다.
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, arcname=rel_path)


def run_pipeline():
    """
    전체 파이프라인을 실행하는 함수이다
    """
    base_dir = os.path.abspath(os.path.dirname(__file__))  # 현재 파일 위치 기준
    class_names = ["label"]  # 실제 프로젝트에 맞는 클래스 이름으로 수정

    # 경로 설정 및 디렉토리 생성
    src_anotated, src_non_annotated, dst_base, dst_images, dst_labels, dst_anotated = setup_directories(base_dir)

    # 이미지 및 라벨 분류 복사
    copy_labeled_images_and_labels(src_anotated, dst_images, dst_labels)
    copy_unlabeled_images(src_non_annotated, dst_images)
    copy_only_labeled_images(src_anotated, dst_anotated)

    # 학습용 메타데이터 파일 생성
    create_metadata_files(dst_labels, dst_images, class_names)

    # 결과 압축 파일 생성
    zip_folder(dst_anotated, os.path.join(dst_base, "anotated.zip"))
    zip_folder(dst_images, os.path.join(dst_base, "images.zip"))
    zip_folder(dst_labels, os.path.join(dst_base, "labels.zip"))

    print("✅ 모든 작업이 완료되었습니다.")


if __name__ == "__main__": # 어디에 result를 만들지(py파일이 있는 위치를 경로로)
    run_pipeline()
