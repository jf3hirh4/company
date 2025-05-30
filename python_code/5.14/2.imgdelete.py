import os

def remove_unmatched_images(folder_path :str):
    """
    txt와 같은 이름을 가지지않은 jpg 삭제하는 함수이다.
    train_folder : 훈련 데이터 디렉토리 경로 ex) obj_Train_data 
    val_folder :  검증 데이터 디렉토리 경로 ex) obj_Validation_data
    """
    # 폴더 내 파일 리스트
    all_files = os.listdir(folder_path)#폴더안에 있는 모든것을 리스트로 

    # .txt 파일과 .jpg 파일 분리
    txt_files = {os.path.splitext(f)[0] for f in all_files if f.endswith('.txt')}
    jpg_files = {os.path.splitext(f)[0] for f in all_files if f.endswith('.jpg')}

    # txt에 없는 jpg 찾기
    unmatched_jpgs = jpg_files - txt_files # txt에 없는게 jpg에 있으면 삭제가 필요하니 저장

    for base_name in unmatched_jpgs:
        img_path = os.path.join(folder_path, base_name + ".jpg") #파일명에 .jpg를 뒤에 붙이고 전체 경로를 만든다. folder_path/123.jpg
        if os.path.exists(img_path):#실제로 경로에 있는지 확인
            os.remove(img_path) #삭제
            print(f"🗑️ 삭제됨: {img_path}")

# 경로 설정
train_folder = "/home/choi/project_doje"


# 실행
remove_unmatched_images(train_folder)

