'''
Description: 
Version: 1.0
Author: 陈路达
Email: chenluda01@outlook.com
Date: 2023-06-17 08:50:04
FilePath: \21-CVPR_download\app.py
Copyright (c) 2023 by Kust-BME, All Rights Reserved. 
'''
from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_args
import mysql.connector

app = Flask(__name__)

def get_CVPR_papers(search=None, highlights=False, candidates=False):
    """
    从数据库获取CVPR论文相关信息
    """
    papers = []
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='cvpr2023'
        )

        cursor = connection.cursor()
        query = 'SELECT * FROM papers WHERE 1=1'
        
        query_params = []

        if search:
            query += " AND (paper_title LIKE %s OR paper_abstract LIKE %s)"
            query_params.append('%'+search+'%')
            query_params.append('%'+search+'%')
            
        if highlights:
            query += " AND is_highlight = 1"

        if candidates:
            query += " AND is_candidate = 1"

        cursor.execute(query, query_params)
        
        papers = cursor.fetchall()

        connection.commit()

    except mysql.connector.Error as error:
        print(f"Failed to select paper: {error}")
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()

    return papers


@app.template_filter('truncate_words')
def truncate_words_filter(s, num):
    words = s.split()
    if len(words) > num:
        words = words[:num]
    return ' '.join(words)

@app.route('/', methods=['GET'])
def index():
    search = request.args.get('search', '')
    highlights = 'highlights' in request.args
    candidates = 'candidates' in request.args
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(get_CVPR_papers(search, highlights, candidates))
    pagination_papers = get_CVPR_papers(search, highlights, candidates)[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('index.html', papers=pagination_papers, page=page, per_page=per_page, pagination=pagination, search=search, highlights=highlights, candidates=candidates, total=total)


if __name__ == "__main__":
    app.run(debug=True)
