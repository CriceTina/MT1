import pytesseract
from PIL import Image

# 指定 Tesseract 的路径（如果未在环境变量中设置）
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# 测试图像（使用你的图像路径）
image_path = 'img.png'
image = Image.open(image_path)

# 进行 OCR 处理
text = pytesseract.image_to_string(image)

print(text)