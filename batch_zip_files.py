'''
Description: 
Version: 1.0
Author: 陈路达
Email: chenluda01@outlook.com
Date: 2023-06-15 20:06:47
FilePath: \21-CVPR_download\batch_zip_files.py
Copyright (c) 2023 by Kust-BME, All Rights Reserved. 
'''
import os
import zipfile
from tqdm import tqdm

def batch_zip_files(directory, save_directory, batch_size=100):
    """
    自动打包目录下的文件，每 batch_size 个文件打包成一个 zip 文件
    """
    # 获取目录下所有文件
    files = os.listdir(directory)
    files = [os.path.join(directory, file) for file in files]

    # 检查保存路径是否存在，如果不存在，则创建
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for i in tqdm(range(0, len(files), batch_size)):
        # 定义zip文件名
        zip_filename = f"no{i+1}to{i+batch_size}.zip"
        zip_filepath = os.path.join(save_directory, zip_filename)

        # 创建zip文件并添加文件
        with zipfile.ZipFile(zip_filepath, 'w') as myzip:
            for filepath in files[i:i+batch_size]:
                myzip.write(filepath, arcname=os.path.basename(filepath)) # arcname为压缩文件中的名称

if __name__ == "__main__":
    batch_zip_files('./cvpr_papers', './cvpr_papers_zip')