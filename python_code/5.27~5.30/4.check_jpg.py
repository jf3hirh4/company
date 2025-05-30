import os

def delete_unlabeled_images(images_dir, labels_dir):
    """
    해당 이미지 파일에 대응되는 라벨이 없으면 해당 이미지를 삭제하는 함수이다.

    images_dir: 이미지 파일들이 저장된 디렉터리 
    labels_dir: 라벨 파일들이 저장된 디렉터리 
    """

    deleted_count = 0  # 삭제된 이미지 수를 카운트

    # 이미지 디렉터리의 모든 파일 확인
    for filename in os.listdir(images_dir):
        # 이미지 확장자인 경우만 처리
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            name, _ = os.path.splitext(filename)  # 확장자 제거한 파일명 추출
            txt_path = os.path.join(labels_dir, name + ".txt")  # 라벨 파일 경로 구성

            # 해당 이미지에 대응하는 라벨 파일이 없으면 이미지 삭제
            if not os.path.exists(txt_path):
                img_path = os.path.join(images_dir, filename)
                os.remove(img_path)
                print(f"🗑️ 삭제됨: {img_path}")
                deleted_count += 1

    # 삭제 요약 출력
    print(f"\n✅ 삭제 완료: 총 {deleted_count}개의 이미지가 삭제됨.")

# 사용 예시
delete_unlabeled_images(
    images_dir="/home/choi/project_doje/data/images/train",     # 이미지 폴더 경로
    labels_dir="/home/choi/project_doje/data/labels/train"      # 라벨(.txt) 폴더 경로
)
