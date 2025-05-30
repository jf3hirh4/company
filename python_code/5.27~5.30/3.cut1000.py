import os
import shutil
from collections import defaultdict

def get_class_to_files_map(source_dir):
    """
    source_dir 내부의 모든 .txt 라벨 파일을 읽어서 각 클래스가 등장한 파일명을 클래스별로 복사하는 함수이다.

    반환: { 클래스 번호: set(해당 클래스가 등장하는 파일명) }
    """
    class_to_files = defaultdict(set)

    # 라벨 파일 목록 수집
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
                if cls in range(4):  # 클래스 수가 4개 (0 ~ 3)인 경우
                    classes_in_file.add(cls)
            except ValueError:
                continue

        # 해당 클래스에 이 파일 추가
        for cls in classes_in_file:
            class_to_files[cls].add(label_file)

    return class_to_files

def copy_files_per_class(class_to_files, source_dir, target_dir, max_per_class=1000):
    """
    클래스별로 최대 max_per_class개까지 파일을 복사하고 중복 없이 복사되도록 처리하는 함수이다.
    """
    os.makedirs(target_dir, exist_ok=True)
    total_copied_files = set()

    for cls, files in class_to_files.items():
        selected_files = sorted(list(files))[:max_per_class]  # 최대 max_per_class개 선택
        for file in selected_files:
            if file not in total_copied_files:
                src = os.path.join(source_dir, file)
                dst = os.path.join(target_dir, file)
                shutil.copyfile(src, dst)
                total_copied_files.add(file)

    return len(total_copied_files)

# 경로 설정
source_labels_folder = "/home/choi/project_doje/zip_labels"  # 원본 라벨 경로
target_labels_folder = "/home/choi/project_doje/limited_labels"  # 복사할 대상 폴더

# 클래스별 파일 리스트 만들기
class_to_files = get_class_to_files_map(source_labels_folder)

# 클래스별 최대 1000개까지 복사
copied_file_count = copy_files_per_class(
    class_to_files, source_labels_folder, target_labels_folder, max_per_class=1000
)
print(f"총 {copied_file_count}개의 라벨 파일 복사 완료.")

# ✅ 복사된 폴더에서 클래스별 실제 객체 수를 확인
def count_labels_per_class(labels_dir):
    """
    라벨 파일에서 각 클래스 번호가 몇 번 등장했는지를 카운트합니다.
    """
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

# 결과 출력
counts = count_labels_per_class(target_labels_folder)
print("복사된 라벨 클래스별 객체 수:", counts)
