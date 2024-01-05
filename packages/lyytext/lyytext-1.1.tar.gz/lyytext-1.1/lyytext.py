import re
import lyystkcode


def replace_digits_with_chinese(text):
    mapping = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}
    replaced_text = ""
    for char in text:
        if char.isdigit():
            replaced_text += mapping[char]
        else:
            replaced_text += char
    return replaced_text


def clean_text(text):

    # 定义正则表达式模式
    pattern = r'(\d{1,2}:\d{1,2}:\d{1,2}[]) ([\u4e00-\u9fa50-9]+) (.*)'

    # 匹配并删除符合格式的文本
    clean_text = re.sub(pattern, "", text)

    # 查找并替换时间格式
    clean_text = re.sub(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}", "", clean_text)

    print(clean_text)
    return clean_text


def remove_date_time(input_string):
    patterns = ['\d{2}:\d{2}:\d{2}[ ]?', '\d{4}-\d{2}-\d{2}[ ]?', '\d{1,2}:\d{2}:\d{2}']

    for pattern in patterns:
        input_string = re.sub(pattern, '', str(input_string))
    return input_string


from f1999cfg import stock_code_name_dict


def get_name_from_code(code):
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
    print("toadd_stkname_txt=", txt, "replaced_text=", replaced_text)
    return replaced_text


def num_to_chinese(match):
    num_map = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}
    return ''.join(num_map[digit] for digit in match.group())


def format_to_speak_text(txt):

    txt = re.sub(r'\d{6}', num_to_chinese, txt)

    txt = remove_date_time(txt)
    txt = clean_text(txt)
    return txt
