import os

def filter_class4_labels(base_dir: str, lbl_prefix: str, img_prefix: str, class_id : str , foldernum: int):

    """

    base_dir폴더 안에서 txt에서 클래스가 class_id인 줄만 빼고 삭제하고 해당하는 이미지도 삭제한다.
    base_dir: 사용할 경로
    lbl_prefix: 라벨 폴더의 앞 이름 , 예) lbl_va001
    img_prefix: 이미지 폴더의 앞 이름 ,예) img_va001
    class_id : 무슨 클래스만 남길지
    foldernum : 폴더 뒤에 숫자가 몇개 있는지 ex) lbl_va001

    """

    base_dir = os.path.expanduser(base_dir) # ~/RS/val 이걸 /home/choi/RS/val 이렇게 절대경로로 바꿔준다.(lbl_,img_ 폴더들이 들어있는 경로)

    # 라벨 폴더들 찾기                                       
    lbl_folders = [os.path.join(base_dir, d) for d in os.listdir(base_dir)
                   # base_dir 안에 있는 모든 파일과 폴더 이름을 리스트로 가져와서, 그 이름들을 base_dir 경로와 합쳐서 전체 경로 리스트를 만드는 코드
                   # ex) base_dir 안에 1.txt 2.jpg 3 이란 파일들이 있으면
                   # [ base_dir/1.txt   ,   base_dir/2.jpg    , base_dir/3 ] 을 lbl_folders  라는 리스트로 저장
                   if os.path.isdir(os.path.join(base_dir, d)) and d.startswith(lbl_prefix)]
                    # 폴더이고 이름이 lbl_prefix(라벨폴더)로 시작하는지  lbl_prefix로 시작하면 저장
                    # 여기서 d는  base_dir/1.txt  이거 하나 말하는것


    # 라벨 폴더에 맞는 이미지 폴더 경로 만들기 
    # lbl_v003이라는 라벨 폴더를 찾으면
    # img_v003이라는 걸 img_folders에 저장하는것
    img_folders = {}

    for d in os.listdir(base_dir):  # base_dir 안에  모든 걸 d에 대입
        if d.startswith(lbl_prefix):  # d가 lbl_prefix로 시작하면
            # d에서 뒤를 foldernum 만큼 저장 ex) 003
            folder_num = d[-foldernum:]  
            # img_prefix와 합쳐서 이미지 폴더 이름을 만든다. ex) img_v003
            img_folder_name = f'{img_prefix}{folder_num}'
            # 이미지 폴더 전체 경로 만든다 base_dir/img_folder_name
            img_folder_path = os.path.join(base_dir, img_folder_name)
            # img_folders에 저장
            img_folders[img_folder_name] = img_folder_path


    for lbl_folder in lbl_folders: #라벨 폴더 경로들을 하나씩 대입
        txt_files = [f for f in os.listdir(lbl_folder) if f.endswith('.txt')] # 라벨 폴더안의 파일이 .txt로 끝나면 저장
        folder_num = os.path.basename(lbl_folder)[-foldernum:] #폴더의 맨 마지막 3숫자만 저장 ex) 001
        img_folder = img_folders.get(f'{img_prefix}{folder_num}', None) #img_001에 해당하는게 img_folders에 있으면 img_folder에 저장 없으면 none을 저장

        if not img_folder:
            print(f"⚠️ 대응하는 이미지 폴더 없음: {folder_num}")
            continue

        for txt_file in txt_files: #  123.txt
            txt_path = os.path.join(lbl_folder, txt_file) # 전체 경로 만드는것 txt의

            with open(txt_path, 'r') as f: #읽기 모드로 열기 
                lines = f.readlines()# 모든줄을 한꺼번에 읽어서 리스트로 저장 한줄씩

            # 특정 클래스만 유지
            target_lines = [line for line in lines if line.strip().startswith(f'{class_id} ')] 
            #class_id로 시작하는 줄만 고르고 그걸 target_lines라는 리스트로 새로 저장

            if target_lines:
                with open(txt_path, 'w') as f: #덮어쓰기로 열기
                    f.writelines(target_lines) # 파일에 target_lines의 내용을 써준다
                print(f"✅ 유지: {txt_file} → 클래스 {class_id} 줄 {len(target_lines)}개")
            else:
                os.remove(txt_path)
                print(f"🗑️ 클래스 {class_id} 없음 → TXT 삭제: {txt_file}")

                # 이미지도 삭제
                img_name = txt_file.replace('.txt', '.jpg')
                img_path = os.path.join(img_folder, img_name) #경로 만들어 주는것
                if os.path.exists(img_path):
                    os.remove(img_path)
                    print(f"🗑️ 이미지 삭제: {img_path}")
                else:
                    print(f"❌ 이미지 없음: {img_path}")



filter_class4_labels(
    base_dir='~/RS/val',             # 사용할 경로
    lbl_prefix='label_',            # 라벨 폴더 접두사
    img_prefix='image_',            # 이미지 폴더 접두사
    class_id='4',                    # 필터링할 클래스 ID
    foldernum=3                     #폴더 뒤에 숫자가 몇개 있는지 ex) lbl_va001
)