import os


def remove_empty_txt_and_related_image(train_txt_path :str, validation_txt_path:str, train_data_dir:str, validation_data_dir:str):
    """
    빈 txt와 jpg 삭제를 삭제한다. 삭제할때 jpg의 경로를 담고있는 train.txt와 validation.txt에 jpg의 경로 줄도 같이 삭제하는 함수이다.
    train_txt_pat: 훈련 파일 경로 ex) train.txt
    validation_txt_path: 검증 파일 경로 ex) validation.txt
    train_data_dir: 훈련 데이터 디렉토리 경로 ex) obj_Train_data 
    validation_data_dir: 검증 데이터 디렉토리 경로 ex) obj_Validation_data

    """

    # 1. obj_Train_data와 obj_Validation_data 디렉토리 내의 .txt 파일 확인
    # 2번 반복한다 1.directory = train_data_dir, txt_path = train_txt_path 2. directory = validation_data_dir, txt_path = validation_txt_path
    for directory, txt_path in [(train_data_dir, train_txt_path), (validation_data_dir, validation_txt_path)]:
       
        for filename in os.listdir(directory): #지정한 디렉토리(directory) 내의 모든 파일과 디렉토리의 리스트 가져온다 반복으로
            if filename.endswith('.txt'): # 파일이름이 .txt로 끝나면
                file_path = os.path.join(directory, filename) #경로 만드는거
                if os.path.getsize(file_path) == 0:  # 파일이 비어 있는 경우
                    # 2. 비어있는 텍스트 파일 삭제
                    print(f"Deleting empty file: {file_path}") #어떤 파일을 삭제하는지 해당 파일의 경로를 말해준다.
                    os.remove(file_path) #해당 파일 삭제
                    
                    # 3. 해당 이미지 파일을 Train.txt 또는 Validation.txt에서 삭제
                    image_filename = filename.replace('.txt', '.jpg')  # 텍스트 파일명에서 jpg로 변환   왜냐하면 같은 이름으로 txt와 jpg가 있어서
                    image_path = f"data/{os.path.basename(directory)}/{image_filename}"  # 이러면 이미지 경로가 만들어진다.
                    # ex) data/direcotory안의 내용/image_filename
                    # 4. 해당 이미지를 Train.txt와 Validation.txt에서 삭제
                    remove_line_from_file(train_txt_path, image_path) # 해당 txt삭제
                    remove_line_from_file(validation_txt_path, image_path) #해당 jsp삭제


# 해당 경로에 있는 파일을 삭제하는 함수
def remove_line_from_file(file_path, line_to_remove):
    with open(file_path, 'r') as file: #파일을 읽기모드('r')로 연다.
        lines = file.readlines()# 파일의 모든 줄을 한번에 읽어와서 리스트 형태로 저장
    with open(file_path, 'w') as file: #파일을 쓰기모드('w')로 연다. 이때 기존 내용은 모두 지워지고 새로 씀
        for line in lines:
            if line.strip() != line_to_remove: #공백/개행 제거후 line_to_remove와 비교 같지 않으면 
                file.write(line)#다시 파일에 쓴다.

# 경로 설정 (실제 디렉토리 경로로 수정)
train_txt_path = '/home/choi/road_robot/Train.txt'  # Train.txt 파일 경로
validation_txt_path = '/home/choi/road_robot/Validation.txt'  # Validation.txt 파일 경로
train_data_dir = '/home/choi/road_robot/obj_Train_data'  # obj_Train_data 디렉토리 경로
validation_data_dir = '/home/choi/road_robot/obj_Validation_data'  # obj_Validation_data 디렉토리 경로

# 빈 파일과 관련 이미지를 삭제
remove_empty_txt_and_related_image(train_txt_path, validation_txt_path, train_data_dir, validation_data_dir)
