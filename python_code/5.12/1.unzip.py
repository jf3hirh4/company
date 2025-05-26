import os
import zipfile

def unzip_all_in_folder(folder_path : str):
    """

    주어진 폴더 내의 모든 zip을 압축 해제한다.
    folder_path: zip 파일들이 있는 파일 경로

    """

    for filename in os.listdir(folder_path): # foler_path 안에 있는 파일이랑 파일이름들을 리스트로 반환한다. 
        filepath = os.path.join(folder_path, filename) # 전체 파일 경로 만드는 거다. ~/RS/val/123.zip , 전체 경로가 만들어진것
        if filename.endswith(".zip") and os.path.isfile(filepath): # 만약 파일의 마지막이 .zip 즉 zip파일 이고 filepath에 있으면 실행
            extract_folder = os.path.join(folder_path, filename[:-4]) #뒤에 확장자뺀 경로 ~/RS/val/123  ,이게 폴더이름이 됨
            os.makedirs(extract_folder, exist_ok=True) # 폴더생성 폴더이름이 123인 , 이미 폴더 있어도 에러 발생하지 말고 넘어가라는것

            try: # 되면 하고 안되도 프로그램이 멈추지 않도록
                with zipfile.ZipFile(filepath, 'r') as zip_ref: #with: 작업끝나면 자동으로 닫음 안쓰면 zip_ref.close()를 해야한다. filepath를 읽기모드로 연다는뜻
                    zip_ref.extractall(extract_folder) #extract_folder에 zip_ref를 압축해제 하라는것
                print(f"✅ Extracted: {filename} → {extract_folder}")# 압축해제가 잘 되면 완료 메시지를 출력
            except zipfile.BadZipFile: #오류 즉 손상된 zip파일이거나 zip파일이 아니면 
                print(f"❌ Bad ZIP file: {filename}") #오류 메시지를 출력

# 메인 경로 기준으로 압축 해제
base_dir = os.path.expanduser("~/RS/val")
label_dir = os.path.join(base_dir, "label") # ~/RS/val/label

unzip_all_in_folder(base_dir)
unzip_all_in_folder(label_dir)
