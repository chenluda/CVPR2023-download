'''
Description: 
Version: 1.0
Author: 陈路达
Email: chenluda01@outlook.com
Date: 2023-06-14 21:05:00
FilePath: \21-CVPR_download\paper_classification.py
Copyright (c) 2023 by Kust-BME, All Rights Reserved. 
'''
import re

import mysql.connector
from tqdm import tqdm

def get_CVPR_papers():
    """
    通过链接下载 CVPR2023 论文和补充材料
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='cvpr2023'
        )

        cursor = connection.cursor()
        query = '''
            SELECT paper_title, paper_authors, paper_abstract from papers
        '''
        cursor.execute(query)

        papers = cursor.fetchall()

        connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to select paper: {error}")
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()
    
    return papers

def get_medical_papers(target_text, papers):
    """
    通过关键词从论文的标题和摘要中筛选出主题相关的论文
    """
    relevant_papers = []

    for paper in tqdm(papers):
        for target in target_text.split(','):
            if (re.search(target, paper[0], re.IGNORECASE) or 
                re.search(target, paper[2], re.IGNORECASE)):
                relevant_papers.append(paper)
                break

    return relevant_papers

def write_to_md(relevant_papers):
    """
    将筛选出的论文按照论文标题、作者、摘要的格式写入到 relevant_papers.md 文件中
    """
    with open('relevant_papers.md', 'w', encoding='utf-8') as f:
        for paper in relevant_papers:
            f.write('## ' + paper[0] + '\n')  
            f.write('**Authors:** ' + paper[1] + '\n')  
            f.write('**Abstract:** ' + paper[2] + '\n\n')  


if __name__ == "__main__":

    papers = get_CVPR_papers()

    target_text = "medical, CT, MRI, radiology, ultrasound, X-ray, PET, Fluoroscopy, Nuclear medicine, Interventional radiology"

    relevant_papers = get_medical_papers(target_text, papers)

    write_to_md(relevant_papers)
