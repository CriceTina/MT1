from sqlalchemy.dialects import mysql
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import chardet
import codecs
import os



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
path = 'translate_3'  # 确保路径正确
model = T5ForConditionalGeneration.from_pretrained(path)
model.to(device)

tokenizer = T5Tokenizer.from_pretrained(path)

task_prefixes = {
    "en": "translate to en: ",
    "zh": "translate to zh: ",
    "ru": "translate to ru: "
}

def process_text(text,targetlanguage = "zh"):

    prefix = task_prefixes[targetlanguage]

    src_text = prefix + text
    input_ids = tokenizer(src_text, return_tensors="pt")
    generated_tokens = model.generate(**input_ids.to(device))
    result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

    result = ''.join(map(str, result))
    print(result)
    return result





def read_text_file(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']

    # 读取文件内容并使用检测到的编码格式解码
    with codecs.open(file_path, 'r', encoding=detected_encoding, errors='ignore') as file:
        text = file.read()

    return text


def change_file_extension(file_path, new_extension):
    root, _ = os.path.splitext(file_path)
    new_file_path = root + new_extension

    try:
        os.rename(file_path, new_file_path)
        print(f"File extension changed to {new_extension} successfully.")
    except OSError as e:
        print(f"Error: {e}")