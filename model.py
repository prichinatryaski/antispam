import torch
import re
from transformers import AutoModelForSequenceClassification, AutoTokenizer

class Model:
    def __init__(self, model_name):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=1).to(self.device).eval()
        
    async def check(self, message) -> float:
        async def clean_text(text) -> str:
            text = re.sub(r'http\S+', '', text)
            text = re.sub(r'[^А-Яа-я0-9 ]+', ' ', text)
            text = text.lower().strip()
            return text
        
        message = await clean_text(message)
        encoding = AutoTokenizer.from_pretrained(self.model_name)(message, padding='max_length', truncation=True, max_length=128, return_tensors='pt')
        input_ids = encoding['input_ids'].to(self.device)
        attention_mask = encoding['attention_mask'].to(self.device)
        
        with torch.no_grad():
            outputs = self.model(input_ids, attention_mask=attention_mask).logits
            pred = torch.sigmoid(outputs).cpu().numpy()[0][0]
            
        return pred