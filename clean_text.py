import re
import num2words


def text_num2words(text):
    return re.sub(r"(\d+)", lambda x : num2words.num2words(int(x.group(0))), text)
