import re


def extract_links(text):
    pattern = r'https?://\S+'
    links = re.findall(pattern, text)

    return links


def identify_content(text):
    """
    分析并返回类型和提取的网址。

    Args:
        text (_type_): _description_

    Returns:
        类型: img file 或者text
        文本: 提取的网址。如果不是网址，则返回全部文本。
    """
    # 匹配图片的正则表达式模式
    img_pattern = r"https://gchat\.qpic.+|http.+?\.(?:png|jpg|gif)"

    # 匹配文件的正则表达式模式
    file_pattern = r"http.+?\.(?:doc|pdf|docx)"

    # 判断是否为图片
    img_match = re.search(img_pattern, text)
    if img_match:
        return "img", img_match.group()

    # 判断是否为文件
    file_match = re.search(file_pattern, text)
    if file_match:
        return "file", file_match.group()

    # 若不匹配图片或文件的模式，返回其他内容
    return "text", text


def 提取网址(full_text, debug=False):
    pattern = re.compile(r'http[s]?://[\w-]+(?:\.[\w-]+)+[\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-]')

    #pattern = re.compile(r'http://[^s]*\.pdf')
    result = re.findall(pattern, full_text)
    url = result[0]

    # 去除前后的标点符号
    url = url.strip('\'"<>')
    if debug: print("提取网址结果=" + result[0])
    return result[0]


if __name__ == '__main__':
    t = '"http://43.132.151.196:9993/down.php/f846e67d6ef725ec2a087405abde6b62.pdf"'

    print(提取网址(t))
