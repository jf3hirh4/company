import os
import shutil
from collections import defaultdict

def get_class_to_files_map(source_dir):
    class_to_files = defaultdict(set)

    label_files = sorted([f for f in os.listdir(source_dir) if f.endswith(".txt")])

    for label_file in label_files:
        path = os.path.join(source_dir, label_file)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        classes_in_file = set()
        for line in lines:
            parts = line.strip().split()
            if not parts:
                continue
            try:
                cls = int(parts[0])
                if cls in range(4):
                    classes_in_file.add(cls)
            except ValueError:
                continue

        for cls in classes_in_file:
            class_to_files[cls].add(label_file)

    return class_to_files

def copy_files_per_class(class_to_files, source_dir, target_dir, max_per_class=1000):
    os.makedirs(target_dir, exist_ok=True)
    total_copied_files = set()

    for cls, files in class_to_files.items():
        selected_files = sorted(list(files))[:max_per_class]
        for file in selected_files:
            if file not in total_copied_files:
                src = os.path.join(source_dir, file)
                dst = os.path.join(target_dir, file)
                shutil.copyfile(src, dst)
                total_copied_files.add(file)

    return len(total_copied_files)


# 복사된 클래스 분포 확인
def count_labels_per_class(labels_dir):
    counts = {cls: 0 for cls in range(4)}
    label_files = [f for f in os.listdir(labels_dir) if f.endswith(".txt")]

    for label_file in label_files:
        path = os.path.join(labels_dir, label_file)
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                try:
                    cls = int(parts[0])
                    if cls in counts:
                        counts[cls] += 1
                except ValueError:
                    continue
    return counts
# 경로 설정
source_labels_folder = "/home/choi/project_doje/zip_labels" #원본
target_labels_folder = "/home/choi/project_doje/limited_labels"

# 클래스별 파일 리스트 만들기
class_to_files = get_class_to_files_map(source_labels_folder)

# 각 클래스별로 최대 1000개 파일 복사
copied_file_count = copy_files_per_class(class_to_files, source_labels_folder, target_labels_folder, max_per_class=1000)
print(f"총 {copied_file_count}개의 라벨 파일 복사 완료.")

counts = count_labels_per_class(target_labels_folder)
print("복사된 라벨 클래스별 객체 수:", counts)
