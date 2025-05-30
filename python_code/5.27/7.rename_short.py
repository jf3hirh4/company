import os

def split_dataset(folder):
    """
    파일이름이 너무 길어 마지막 언더스코어 뒤에 있는 날짜로 이름을 바꾼다. 
    folder: 해당 파일이 있는 폴더의 경로
    back: 바꿀폴더의 뒷 확장자
    """
    for filename in os.listdir(folder,back):
        if filename.endswith(back):
            # 파일명에서 마지막 언더스코어(_) 이후 문자열 추출
            new_name = filename.split('_')[-1]
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")

folder = '/home/choi/project_doje/data/labels/train'
back = '.txt'
split_dataset(folder,back)