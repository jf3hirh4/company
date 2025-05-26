import os
import zipfile

def zip_folder(folder_path, zip_path):
    """
    지정된 폴더를 압축시켜주는 함수이다.
    folder_path : 압축시키고 싶은 폴더
    zip_path : 해당폴더의 압축후 이름
    """
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                abs_path = os.path.join(root, file)
                rel_path = os.path.relpath(abs_path, folder_path)
                zipf.write(abs_path, arcname=rel_path)
    print(f"Zipped: {zip_path}")
    
zip_folder("/home/choi/ai_hub/short_labels", "/home/choi/ai_hub/short_labels.zip")
zip_folder("/home/choi/ai_hub/short_images", "/home/choi/ai_hub/short_images.zip")
