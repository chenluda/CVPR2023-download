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
    # 获取目录下所有文件夹
    folders = [os.path.join(directory, folder) for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    # 检查保存路径是否存在，如果不存在，则创建
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    for i in tqdm(range(0, len(folders), batch_size)):
        # 定义zip文件名
        zip_filename = f"no{i+1}to{i+batch_size}.zip"
        zip_filepath = os.path.join(save_directory, zip_filename)

        # 创建zip文件并添加文件
        with zipfile.ZipFile(zip_filepath, 'w') as myzip:
            for folder in folders[i:i+batch_size]:
                for dirpath, dirnames, filenames in os.walk(folder):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        arcname = os.path.join(os.path.basename(dirpath), filename)
                        myzip.write(filepath, arcname=arcname)  # arcname为压缩文件中的名称

if __name__ == "__main__":
    batch_zip_files('./cvpr_papers', './cvpr_papers_zip')
