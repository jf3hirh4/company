import os

def delete_orphan_txt_files(labels_dir, images_dir):
    """
    라벨 파일 중 같은 이름의 이미지가 존재하지 않으면 해당 .txt 파일을 삭제하는 함수이다.

    labels_dir: 라벨 파일들이 있는 디렉터리
    images_dir: 이미지 파일들이 있는 디렉터리
    """

    deleted_count = 0  # 삭제된 파일 수 카운트용
    image_extensions = [".jpg", ".jpeg", ".png"]  # 비교할 이미지 확장자 목록

    # 라벨 디렉터리의 모든 파일 확인
    for filename in os.listdir(labels_dir):
        if filename.endswith(".txt"):
            name = os.path.splitext(filename)[0]  # 확장자를 제외한 파일 이름

            # 해당 이름의 이미지가 있는지 확인
            image_exists = any(
                os.path.exists(os.path.join(images_dir, name + ext))
                for ext in image_extensions
            )

            # 이미지가 존재하지 않으면 .txt 삭제
            if not image_exists:
                txt_path = os.path.join(labels_dir, filename)
                os.remove(txt_path)
                print(f"🗑️ 삭제됨: {txt_path}")
                deleted_count += 1

    # 최종 결과 출력
    print(f"\n✅ 삭제 완료: 총 {deleted_count}개의 .txt 파일이 삭제됨.")

# 사용 예시
delete_orphan_txt_files(
    images_dir="/home/choi/project_doje/data/images/val",     # 이미지 폴더
    labels_dir="/home/choi/project_doje/data/labels/val"      # 라벨(.txt) 폴더
)
