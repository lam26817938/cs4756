import os
import shutil
import pandas as pd

# 設定主目錄
base_dir = 'airsim_data'
record_dir = os.path.join(base_dir, 'record')

# 確保record資料夾存在
if not os.path.exists(record_dir):
    os.makedirs(record_dir)

# 在record資料夾內創建一個存放所有圖片的子資料夾
target_image_dir = os.path.join(record_dir, 'images')
if not os.path.exists(target_image_dir):
    os.makedirs(target_image_dir)

# 設定合併後的airsim_rec.txt文件的儲存路徑
target_rec_file = os.path.join(record_dir, 'airsim_rec.txt')

# 用於存儲所有 DataFrame 的列表
all_data = []

# 遍歷主目錄下的每個子資料夾
for folder_name in os.listdir(base_dir):
    folder_path = os.path.join(base_dir, folder_name)
    
    if folder_name != 'record' and os.path.isdir(folder_path):  # 確保它是一個資料夾且不是record資料夾
        # 處理圖片
        image_folder_path = os.path.join(folder_path, 'images')
        if os.path.exists(image_folder_path):
            for image_name in os.listdir(image_folder_path):
                source_image_path = os.path.join(image_folder_path, image_name)
                target_image_path = os.path.join(target_image_dir, image_name)
                # 檢查目標路徑是否已存在文件，避免覆蓋
                if not os.path.exists(target_image_path):
                    shutil.copy(source_image_path, target_image_path)
                else:
                    print(f"File {target_image_path} already exists. Skipping.")

        # 處理 airsim_rec.txt
        rec_file_path = os.path.join(folder_path, 'airsim_rec.txt')
        if os.path.exists(rec_file_path):
            df = pd.read_csv(rec_file_path, sep='\t')  # 讀取每個文件
            all_data.append(df)

# 合併所有 DataFrame
if all_data:
    combined_data = pd.concat(all_data)
    # 保存合併後的數據到record資料夾
    combined_data.to_csv(target_rec_file, sep='\t', index=False)