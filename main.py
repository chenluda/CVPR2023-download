'''
Description: 
Version: 1.0
Author: 陈路达
Email: chenluda01@outlook.com
Date: 2023-06-13 21:19:32
FilePath: \21-CVPR_download\main.py
Copyright (c) 2023 by Kust-BME, All Rights Reserved. 
'''
import os
import re
from urllib.parse import urljoin
import numpy as np

import mysql.connector
import requests
from tqdm import tqdm

from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def requests_retry_session(
    retries=5,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    """
    重试请求
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_CVPR_links(url, filename):
    """
    将 CVPR2023 的论文页面链接保存到文本文件中
    """
    url = urljoin(base_url, url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    html_links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith(
        '.html') and a['href'].startswith('/content/CVPR2023/')]

    with open(filename, 'w') as f:
        for link in html_links:
            f.write(link + '\n')


def get_papers_information(filename, batch_size):
    """
    获取论文的标题、作者、摘要、链接、补充材料链接、bibtex
    """
    paper_list = []

    with open(filename, 'r') as f:
        html_links = [link.strip() for link in f.readlines()]

        # 中断重启
        checkpoint = np.load('checkpoint.npy') if os.path.exists('checkpoint.npy') else 0
        html_links = html_links[checkpoint:]

    for idx, link in enumerate(tqdm(html_links), start=checkpoint):

        full_link = urljoin(base_url, link)

        response = requests_retry_session().get(full_link)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取文章标题
        paper_title = soup.select_one("div#papertitle").text.strip()
        # 获取文章作者
        paper_authors = soup.select_one("div#authors").find('i').text.strip()
        # 获取文章摘要
        paper_abstract = soup.select_one("div#abstract").text.strip()
        # 获取文章链接
        for a in soup.find_all('a', href=True):
            if a['href'].endswith('.pdf') and a['href'].startswith('/content/CVPR2023/papers/'):
                paper_link = a['href']

            if a['href'].endswith('.pdf') and a['href'].startswith('/content/CVPR2023/supplemental/'):
                paper_supplemental_link = a['href']
        # 获取 bibtex
        paper_bibtex = soup.select_one("div.bibref").text.strip()

        paper_list.append({
            'paper_title': paper_title,
            'paper_authors': paper_authors,
            'paper_abstract': paper_abstract,
            'paper_link': paper_link,
            'paper_supplemental_link': paper_supplemental_link,
            'paper_bibtex': paper_bibtex,
        })

        # 每 batch_size 条数据插入一次数据库
        if len(paper_list) == batch_size:
            insert_papers_to_db(paper_list)
            paper_list.clear()

        # 更新断点
        np.save('checkpoint.npy', idx+1)

    # 插入剩余的数据
    if paper_list:
        insert_papers_to_db(paper_list)


def insert_papers_to_db(papers):
    """
    将获取的论文信息保存至数据库
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
        for paper in papers:
            query = '''
                INSERT INTO papers (paper_title, paper_authors, paper_abstract, paper_link, paper_supplemental_link, paper_bibtex)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, (
                paper['paper_title'],
                paper['paper_authors'],
                paper['paper_abstract'],
                paper['paper_link'],
                paper['paper_supplemental_link'],
                paper['paper_bibtex'],
            ))
        connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to insert paper: {error}")
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()


def download_CVPR_papers():
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
            SELECT paper_title, paper_link, paper_supplemental_link from papers
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

    # 中断重启
    checkpoint_pdf = np.load('checkpoint_pdf.npy') if os.path.exists('checkpoint_pdf.npy') else 0
    papers = papers[checkpoint_pdf:]

    for idx, paper in enumerate(tqdm(papers), start=checkpoint_pdf):
        paper_title = paper[0]
        paper_link = paper[1]
        paper_supplemental_link = paper[2]

        paper_title = re.sub(r'[\\/:*?"<>|]', '', paper_title)

        paper_link = urljoin(base_url, paper_link)
        paper_supplemental_link = urljoin(base_url, paper_supplemental_link)

        # 下载论文
        paper_response = requests_retry_session().get(paper_link)

        if not os.path.exists(f'./cvpr_papers/{paper_title}'):
            os.mkdir(f'./cvpr_papers/{paper_title}')

        with open(f'./cvpr_papers/{paper_title}/paper.pdf', 'wb') as f:
            f.write(paper_response.content)

        # 下载补充材料
        paper_supplemental_response = requests_retry_session().get(paper_supplemental_link)
        with open(f'./cvpr_papers/{paper_title}/supplemental.pdf', 'wb') as f:
            f.write(paper_supplemental_response.content)

        # 更新断点
        np.save('checkpoint_pdf.npy', idx+1)


if __name__ == '__main__':
    base_url = 'https://openaccess.thecvf.com/'

    if not os.path.exists(f'./cvpr_links.txt'):
        # 获取链接并保存到文本文件中
        get_CVPR_links('CVPR2023?day=all', 'cvpr_links.txt')

    # 获取论文的标题、作者、摘要、链接、补充材料链接、bibtex
    paper_list = get_papers_information('cvpr_links.txt', 50)

    # 通过链接下载 CVPR2023 论文和补充材料
    download_CVPR_papers()
