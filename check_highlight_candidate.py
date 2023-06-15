'''
Description: 
Version: 1.0
Author: 陈路达
Email: chenluda01@outlook.com
Date: 2023-06-15 18:03:33
FilePath: \21-CVPR_download\check_highlight_candidate.py
Copyright (c) 2023 by Kust-BME, All Rights Reserved. 
'''

import mysql.connector

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
            SELECT * from papers
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


def check_highlight_candidate(papers):
    """
    检查 highlight 和 candidate 的数量是否符合（highlight_num = 235, candidate_num = 12）
    """
    highlight_num = 0
    candidate_num = 0
    for paper in papers:
        if paper[7]:
            highlight_num += 1
        if paper[8]:
            candidate_num += 1
    print(f'highlight_num: {highlight_num}')
    print(f'candidate_num: {candidate_num}')



if __name__ == "__main__":
    papers = get_CVPR_papers()
    check_highlight_candidate(papers)