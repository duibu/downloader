from bs4 import BeautifulSoup
import re


def get_html_tag_content(html, tag_name, content_start_with):
    soup = BeautifulSoup(html, 'html.parser')

    # 找到所有的<script>标签
    script_tags = soup.find_all(tag_name)

    result = ''

    # 遍历每个<script>标签并打印脚本内容
    for script_tag in script_tags:
        script_content = script_tag.get_text()

        if script_content.startswith(content_start_with):
            result = script_content[len(content_start_with):]
            break

    return result