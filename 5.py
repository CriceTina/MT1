import numpy as np
import torch
import json
from transformers import T5ForConditionalGeneration, T5Tokenizer, Trainer, TrainingArguments
from torch.utils.data import Dataset
from torch.optim import AdamW
from datasets import load_metric
from evaluate import load

# 定义一个数据集类

task_prefixes = {
    "en":"translate to en: ",
    "zh":"translate to zh: ",
    "ru":"translate to ru: "
}
# 定义一个数据集类
class TranslationDataset(Dataset):
    def __init__(self, tokenizer, file_path, max_length=512):
        self.tokenizer = tokenizer
        self.data = []
        self.max_length = max_length

        # 读取并处理数据
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                item = json.loads(line)
                self.data.append(item)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        item = self.data[idx]
        input_text = item['input']
        target_text = item['output']

        # 获取相应的任务前缀
        target_language = 'en'  # 假设每个item都有'language'字段，用于标识目标语言
        task_prefix = task_prefixes[target_language]

        # 准备输入数据，添加任务标识符
        input_text_with_prefix = task_prefix + input_text

        # 编码输入和目标
        encoding = self.tokenizer(input_text_with_prefix, return_tensors='pt', max_length=self.max_length,
                                  truncation=True, padding='max_length')
        input_ids = encoding['input_ids'].squeeze()
        attention_mask = encoding['attention_mask'].squeeze()

        # 编码目标文本并确保与输入长度一致
        labels = self.tokenizer(target_text, return_tensors='pt', max_length=self.max_length, truncation=True,
                                padding='max_length')['input_ids'].squeeze()

        # 返回一个字典，包含模型训练所需的数据
        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }


# 加载预训练的T5模型和分词器
model_name = 'zh-en-ru'
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# 创建数据集实例
train_dataset = TranslationDataset(tokenizer=tokenizer, file_path='data/train.json')
eval_dataset = TranslationDataset(tokenizer=tokenizer, file_path='data/test.json')
# 定义训练参数
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    metric_for_best_model="bleu",
)

# 初始化模型和优化器
model = T5ForConditionalGeneration.from_pretrained('zh-en-ru')
optimizer = AdamW(model.parameters(), lr=5e-5)

# 加载BLEU评分指标
bleu_metric = load_metric

# 定义计算BLEU分数的函数
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    decoded_preds = tokenizer.batch_decode(predictions, skip_special_tokens=True)
    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # 计算BLEU分数
    result = bleu_metric.compute(predictions=decoded_preds, references=decoded_labels)
    print(result)
    return result["bleu"]



# 初始化Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    optimizers=(optimizer, None),
    compute_metrics=compute_metrics,  # 添加BLEU分数计算
)

# 开始训练
trainer.train()

# 评估模型
trainer.evaluate()

# 保存训练后的模型
trainer.save_model('./my_trained_t5_model')