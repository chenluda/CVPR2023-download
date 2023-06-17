# CVPR2023 论文下载

![image](https://github.com/chenluda/CVPR2023-download/assets/45784833/77251c0f-5e69-4e37-9352-0805fe66261f)

### 背景

* CVPR 2023 收到了 9155 份投稿，相比上一年度的 CVPR 2022 的 8161 份投稿增加了 12%。
* 在所有投稿中，共有 2359 篇论文被接受，接受率为 25.8%。
* 在被接受的 2359 篇论文中，235 篇被选为 highlights，占比 10%，另有 12 篇（占比 0.5%）入围最佳论文奖候选。

---

### 功能

1. 获取 CVPR2023 所有接收论文的标题、作者、摘要、链接、补充材料链接、bibtex、是否为 Highlight、是否为获奖候选，并保存至本地数据库；
2. 从本地数据库读取论文的链接和补充材料链接，下载 PDF 文件；

---

### 代码说明

* main.py（中国香港节点稳定）：1）将 CVPR2023 的论文页面链接保存到文本文件中；2）获取论文的标题、作者、摘要、链接、补充材料链接、bibtex；3）将获取的论文信息保存至数据库；4）通过链接下载 CVPR2023 论文和补充材料。；
```
python main.py
```
* paper_classification.py：字符串匹配简单筛选论文；
* check_highlight_candidate.py：检查 highlight 和 candidate 的数量是否符合（highlight_num = 235, candidate_num = 12）；
* batch_zip_files.py：自动打包指定目录下的文件，每 batch_size 个文件打包成一个 zip 文件。
* app.py：一个简单的展示论文相关信息的网站。
```
python app.py
```

---

### 文件说明

* cvpr_links.txt：所有论文的网址，网站内包含论文标题、作者、摘要、链接、补充材料链接、bibtex 等信息；
![image](https://github.com/chenluda/CVPR2023-download/assets/45784833/6c5b9d30-2b8d-4b7a-a8cb-a23d2ed23514)

* cvpr2023.sql：数据库文件，包含 2359 篇论文的标题、作者、摘要、链接、补充材料链接、bibtex、是否为 Highlight、是否为获奖候选等字段；
![961c3ff1b19579253c8fc9bf4d5e841a](https://github.com/chenluda/CVPR2023-download/assets/45784833/67c0e7c3-e20d-496d-8c80-66c3f6aadd18)

* relevant_papers.md：从 2359 篇论文中筛选出的 58 篇医学影像相关论文，按论文标题、作者、摘要的顺序排列。
![image](https://github.com/chenluda/CVPR2023-download/assets/45784833/58a24a63-9850-4c71-8d28-ba62c80508f3)
