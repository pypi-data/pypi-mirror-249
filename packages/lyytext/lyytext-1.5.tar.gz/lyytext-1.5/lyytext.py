import re


def format_replace_text(text, to_replace_dict):
    #输入原文本和替换对，替换对为字典格式，key替换为value
    for key, value in to_replace_dict.items():
        text = text.replace(key, value)
    return text


def format_remove_subtext(text, to_remove_list, debug=False):
    for item in to_remove_list:
        if debug:
            print(item, "是否包含:", bool(item in text))
        text = text.replace(item, "")
    return text


def text_remove_symbol(text):
    """
    去除文本中的符号
    """
    text = re.sub(r"[^\u4e00-\u9fa5a-zA-Z0-9]", "", text)
    return text


def remove_regex_strings(regex_pattern, text):
    # 删除所有符合模式的字符
    pattern = re.compile(regex_pattern)

    # 使用sub方法用空字符串替换所有匹配项
    new_str = re.sub(pattern, '', text)

    return new_str


def batch_remove_regex_strings_by_list(regex_pattern_list, text, debug=True):
    # 删除符合 模式列表 中的任意模式的字符
    for regex in regex_pattern_list:
        if debug:
            matches = re.findall(regex, text)
            print("匹配到的子文本: ", matches)
        if text:
            text = remove_regex_strings(regex, text)
        else:
            break
    return text


def batch_replace_by_regex_dict(regex_new_dict, text):
    # 批量替换指定模式为指定字符，通过使用字典中的值替换键
    for key, value in regex_new_dict.items():
        if text:
            text = re.sub(key, value, text)
        else:
            break
    return text


def batch_strip_text(text, to_remove_words_list):
    #批量删除首尾不要的字符
    for words in to_remove_words_list:
        if text:
            text = text.strip(words)
        else:
            break
    # 删除文本两端的空格
    return text.strip()


def replace_digits_with_chinese(text):
    mapping = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}
    replaced_text = ""
    for char in text:
        if char.isdigit():
            replaced_text += mapping[char]
        else:
            replaced_text += char
    return replaced_text


def extract_regex_strings(regex, text):
    #  正则表达式模式
    pattern = re.compile(regex)

    #  查找所有匹配项并将其添加到列表中
    regex_strings = pattern.findall(text)

    return regex_strings


def clean_text(text):

    # 定义正则表达式模式
    pattern = r'(\d{1,2}:\d{1,2}:\d{1,2}[]) ([\u4e00-\u9fa50-9]+) (.*)'

    # 匹配并删除符合格式的文本
    clean_text = re.sub(pattern, "", text)

    # 查找并替换时间格式
    clean_text = re.sub(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}", "", clean_text)

    print(clean_text)
    return clean_text


def remove_date_time(texting):
    patterns = ['\d{2}:\d{2}:\d{2}[ ]?', '\d{4}-\d{2}-\d{2}[ ]?', '\d{1,2}:\d{2}:\d{2}']

    for pattern in patterns:
        texting = re.sub(pattern, '', str(texting))
    return texting


def get_name_from_code(code):
    import lyystkcode

    stock_code_name_dict = lyystkcode.get_code_name_dict()
    code = str(code).zfill(6)
    if code in stock_code_name_dict.keys():
        return f"[{(code)}:{stock_code_name_dict[code]}]"


def add_stockname_for_stkcode(txt):

    def replace(match):
        num = match.group(0)
        start_digit = num[0]
        if start_digit in ['3', '6', '0']:
            new_num = str(get_name_from_code(int(num)))
            return num.replace(num, new_num)
        else:
            return num

    replaced_text = re.sub(r"\b(?:3|6|0)\d{5}\b", replace, txt)
    #print("toadd_stkname_txt=", txt, "replaced_text=", replaced_text)
    return replaced_text


def num_to_chinese(match):
    num_map = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}
    return ''.join(num_map[digit] for digit in match.group())


def format_to_speak_text(txt):
    """
    文本朗读时候，数字会被读成阿拉伯数字，这里把数字转换成中文，单个读。
    """

    txt = re.sub(r'\d{6}', num_to_chinese, txt)

    txt = remove_date_time(txt)
    txt = clean_text(txt)
    return txt
