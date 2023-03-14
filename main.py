# This is a sample Python script.
import pdf
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import web
import subprocess
import glob
import markdown
import pdfkit
import os
import dg_test


def get_md_by_time(file_path):
    files = glob.glob(f"*.md", recursive=True)
    if not files:
        return
    else:
        # 格式解释:对files进行排序.x是files的元素,:后面的是排序的依据.   x只是文件名,所以要带上join.
        files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(file_path, x)))
        return files


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    url = input("输入想要添加的父文档链接:")
    layer = input("输入想要下载的文档所在层级:")
    webdriver_path = "edgedriver_win64/msedgedriver.exe"

    # 批量获取文档下载路径
    if url != '':
        layer = int(layer)
        links_list = web.get_links(webdriver_path, url, layer)
        with open("links1.txt", "w") as f:
            for link in links_list:
                f.write(link + '\n')
            f.close()
    else:
        with open('links.txt', 'r') as f:
            links_list = f.read().splitlines()

    # 使用feishu2md批量下载文件
    for link in links_list:
        print("downloading:", link)
        result = subprocess.run(['feishu2md', link], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # 将md文件合并并生成pdf
    # 使用 glob 模块获取所有 Markdown 文件路径
    md_files = get_md_by_time('.')

    # 将所有 Markdown 文件合并为一个文件
    with open('merged.md', 'w', encoding='utf-8') as merged_file:
        for md_file in md_files:
            with open(md_file, 'r', encoding='utf-8') as f:
                merged_file.write(f.read())

    # 将 Markdown 文件转换为 HTML
    with open("merged.md", "r", encoding='utf-8') as f:
        md_html = markdown.markdown(f.read())

    with open("md_html.html", "w", encoding="utf-8") as f:
        f.write(md_html)

    # 将 HTML 转换为 PDF
    htmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    configuration = pdfkit.configuration(wkhtmltopdf=htmltopdf)
    options = {'page-size': 'A4',
               # 'margin-top': '0mm',
               # 'margin-right': '0mm',
               # 'margin-bottom': '0mm',
               # 'margin-left': '0mm',
               'image-quality': 90,
               'encoding': "utf-8",
               'enable-local-file-access': None,
               }
    pdfkit.from_file('md_html.html', 'pdf/output.pdf',  options=options, configuration=configuration)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
