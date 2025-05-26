import os
import shutil

def create_yolo_v5_structure(base_path='.'):
    """
    Yolov8 학습용 폴더 구조 및 data.yaml파일을 생성하는 함수이다.
    base_path: 기본경로다
    base_path아래에 data/obj_Train_data,data/obj_Validation_data,obj.names가 있어야한다.
    
    """
    train_src = os.path.join(base_path, 'data', 'obj_Train_data') #절대 경로 만들어주는것 base_path/data/obj_Train_data
    val_src = os.path.join(base_path, 'data', 'obj_Validation_data')
    names_path = os.path.join(base_path, 'obj.names') 

    # 새 구조 경로 정의
    image_train_path = os.path.join(base_path, 'images', 'train') # base_path/images/train
    image_val_path = os.path.join(base_path, 'images', 'val') # base_path/images/val
    label_train_path = os.path.join(base_path, 'labels', 'train') # base_path/labels/train
    label_val_path = os.path.join(base_path, 'labels', 'val') # base_path/labels/val
    
    # 디렉토리 생성
    os.makedirs(image_train_path, exist_ok=True) #경로에 해당하는 폴더를 만든다. 중간에 필요한 폴더도 같이 만든다, 이미 해당 폴더있어도 오류를 발생시키지 않는다.
    os.makedirs(image_val_path, exist_ok=True)
    os.makedirs(label_train_path, exist_ok=True)
    os.makedirs(label_val_path, exist_ok=True)

    # 클래스 이름 불러오기
    if not os.path.exists(names_path): # obj.names 폴더 없으면
        print(f"[✗] obj.names 파일이 존재하지 않습니다: {names_path}")
        return
    
    with open(names_path, 'r', encoding='utf-8') as f: # 읽기 모드로 obj.names 열기
        class_names = [line.strip() for line in f.readlines()] #모든줄을 리스트로 읽고 앞뒤 공백 제거 ex) ['car','road']
    num_classes = len(class_names) #리스트 길이를 세어서 클래수 수 를 구함 즉 2

    # 이미지/라벨 복사 함수
    def copy_data(src_folder:str, image_dst:str, label_dst:str):
        """
        구조에 맞게 이미지 파일와 txt파일을 폴더로 복사하는 함수이다.
        src_folder: 훈련 txt파일과 이미지 파일이 있는 경로 ex) obj_Train_data의 절대경로
        image_dst : 훈련이미지 폴더 경로 ex) base_path/images/train
        label_dst : 훈련 txt파일 저장할 경로 ex: base_path/labels/train
        만약 검증데이터면 train말고 val
        """
        for file in os.listdir(src_folder): #src_folder안에 있는것 하나씩
            file_path = os.path.join(src_folder, file)
            if file.lower().endswith(('.jpg', '.png', '.jpeg')): # 이미지면
                shutil.copy(file_path, os.path.join(image_dst, file)) #image_dst경로에 복사
            elif file.endswith('.txt'): # 텍스트면
                shutil.copy(file_path, os.path.join(label_dst, file)) #label_dst경로에 복사

    # 데이터 복사
    copy_data(train_src, image_train_path, label_train_path) # 훈련 복사
    copy_data(val_src, image_val_path, label_val_path) # 검증 복사 

    # data.yaml 생성
    yaml_path = os.path.join(base_path, 'data.yaml') # data.yaml의 절대경로를 만든다.
    with open(yaml_path, 'w', encoding='utf-8') as f: #쓰기모드로 연다. 안에 내용 초기화
        f.write(f"train: {os.path.abspath(image_train_path)}\n") #내용쓰기 
        f.write(f"val: {os.path.abspath(image_val_path)}\n\n")
        f.write(f"nc: {num_classes}\n")
        f.write(f"names: {class_names}\n")

    print("[✓] YOLOv8용 폴더 및 파일 생성 완료!")
    print(f"[✓] 클래스 수: {num_classes}")
    print(f"[✓] 클래스 이름: {class_names}")
    print(f"[✓] data.yaml 위치: {yaml_path}")

# 실행
create_yolo_v5_structure()
