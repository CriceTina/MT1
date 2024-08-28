from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
# device = 'cpu' #or 'cpu' for translate on cpu

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_name = 'zh-en-ru'
model = T5ForConditionalGeneration.from_pretrained(model_name)
model.to(device)
tokenizer = T5Tokenizer.from_pretrained(model_name)

prefix = 'translate to zh: '
src_text = prefix + "Extract text"

# translate Russian to Chinese en ru zh
input_ids = tokenizer(src_text, return_tensors="pt")

generated_tokens = model.generate(**input_ids.to(device))

result = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)

print(result)