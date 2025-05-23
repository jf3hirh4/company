import os
import json
import shutil

def convert_coco_to_yolo(base_path):
    """
    json에서 도로이정표(34)가 있는 것만 yolo 라벨 파일로 바꾸고 해당하는 이미지도 저장
    """
    # 결과를 저장할 폴더 설정
    labels_output_dir = os.path.join(base_path, "result_labels")  # YOLO 라벨 파일 저장 위치
    images_output_dir = os.path.join(base_path, "result_images")  # 대응 이미지 저장 위치
    images_input_dir = os.path.join(base_path, "images")          # 원본 이미지 위치
    json_input_dir = os.path.join(base_path, "labels")            # COCO 형식 JSON 파일 위치

    # 출력 디렉토리 생성 (없을 경우)
    os.makedirs(labels_output_dir, exist_ok=True)
    os.makedirs(images_output_dir, exist_ok=True)

    # 관심 있는 COCO category_id (예: 도로이정표는 34)
    target_category_id = 34

    # JSON 파일 반복 처리
    for filename in os.listdir(json_input_dir):
        if not filename.endswith(".json"): # .json이 아니면 무시
            continue  

        json_path = os.path.join(json_input_dir, filename)

        # COCO JSON 파일 열기
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 이미지에 대한 정보 저장
        image_id_to_info = {img["id"]: img for img in data["images"]}
        result_annotations = {}  # 파일별 YOLO 라인 저장용

        # 반복 처리
        for ann in data["annotations"]:
            if ann["category_id"] != target_category_id:
                continue  # target_category_id가 아니면 무시

            image_id = ann["image_id"]
            bbox = ann["bbox"]  # COCO 형식: [x, y, width, height]
            image_info = image_id_to_info.get(image_id)

            if not image_info:
                continue  # 이미지 정보가 없으면 건너뜀

            width = image_info["width"]
            height = image_info["height"]
            file_name = image_info["file_name"]

            # 바운딩 박스가 유효하지 않으면 무시
            x, y, w, h = bbox
            if w <= 0 or h <= 0 or width == 0 or height == 0:
                continue

            # YOLO 형식으로 변환 (정규화된 중심 좌표와 크기)
            x_center = (x + w / 2) / width
            y_center = (y + h / 2) / height
            w_norm = w / width
            h_norm = h / height

            # YOLO 라벨 라인: class x_center y_center width height
            yolo_line = f"0 {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}"

            # 이미지 파일명 기준으로 라인 저장
            if file_name not in result_annotations:
                result_annotations[file_name] = []
            result_annotations[file_name].append(yolo_line)

        # YOLO 라벨 저장 및 이미지 복사
        for file_name, yolo_lines in result_annotations.items():
            txt_name = os.path.splitext(file_name)[0] + ".txt"
            txt_path = os.path.join(labels_output_dir, txt_name)

            # YOLO 라벨 파일 저장
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write("\n".join(yolo_lines))
            print(f"✅ YOLO saved: {txt_path}")

            # 이미지 파일 복사
            src_img_path = os.path.join(images_input_dir, file_name)
            dst_img_path = os.path.join(images_output_dir, file_name)

            if os.path.exists(src_img_path):
                shutil.copy2(src_img_path, dst_img_path)
                print(f"📷 Image copied: {src_img_path} -> {dst_img_path}")
            else:
                print(f"⚠️ Warning: Image file not found: {src_img_path}")

    # 대응하는 이미지가 없는 .txt 파일 삭제
    print("\n🧹 Removing orphan .txt files (no matching image)...")
    for txt_file in os.listdir(labels_output_dir):
        if not txt_file.endswith(".txt"):
            continue

        base_name = os.path.splitext(txt_file)[0]
        possible_extensions = [".jpg", ".jpeg", ".png"]
        image_found = False

        # 여러 이미지 확장자 중 하나라도 존재하면 유효
        for ext in possible_extensions:
            if os.path.exists(os.path.join(images_output_dir, base_name + ext)):
                image_found = True
                break

        if not image_found:
            txt_path = os.path.join(labels_output_dir, txt_file)
            os.remove(txt_path)
            print(f"🗑️ Removed orphan txt: {txt_path}")
            
convert_coco_to_yolo("/home/choi/ai_hub") 