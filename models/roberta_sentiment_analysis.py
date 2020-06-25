from collections import defaultdict
import numpy as np
import pandas as pd
import torch
import transformers
from sklearn.model_selection import train_test_split
from transformers import RobertaModel, RobertaTokenizer

# Creating a dataset
class OURDataset(torch.utils.data.Dataset):
    
    def __init__(self, text, target, tokenizer, max_len):
        self.text = text
        self.target = target
        self.tokenizer = tokenizer 
        self.max_len = max_len
        
    def __len__(self):
        return len(self.text)
    
    def __getitem__(self, item):
        text = str(self.text[item])
        encoding = tokenizer.encode_plus(
            text,
            max_length = self.max_len,
            add_special_tokens = True,
            pad_to_max_length = True,
            return_attention_mask = True,
            return_token_type_ids = False,
            return_tensors = 'pt'
        )
        return {
            'input_ids': encoding['input_ids'].reshape(MAX_LEN) ,
            'attention_mask': encoding['attention_mask'].reshape(MAX_LEN),
            'targets': torch.tensor(self.target[item], dtype=torch.long),
            'text': text
            
        }

def create_data_loader(df, tokenizer, max_len, batch_size):
    ds = OURDataset(
        text = df.Text.to_numpy(),
        target = df.Sentiment.to_numpy(),
        tokenizer = tokenizer,
        max_len = max_len
    )
    return torch.utils.data.DataLoader(
        ds,
        batch_size = batch_size,
        num_workers = 4
    )

class SentimentClassifier(torch.nn.Module):
    def __init__(self, n_cls):
        super(SentimentClassifier, self).__init__()
        self.bert = RobertaModel.from_pretrained('roberta-base')
        self.drop = torch.nn.Dropout(p=0.3)
        self.l1 = torch.nn.Linear(self.bert.config.hidden_size, 700)
        self.l2 = torch.nn.Linear(700, 500)
        self.l3 = torch.nn.Linear(500, 200)
        self.out = torch.nn.Linear(200, n_cls)
        self.softmax = torch.nn.Softmax(dim=1)
        
    def forward(self, input_ids, attention_mask):
        _, pooled_output = self.bert(
        input_ids = input_ids,
        attention_mask = attention_mask
        )
        output = self.drop(pooled_output)
        output = self.l1(output)
        output = self.drop(output)
        output = self.l2(output)
        output = self.drop(output)
        output = self.l3(output)
        output = self.drop(output)
        output = self.out(output)
        return self.softmax(output)


def train_epoch(model, data_loader, loss_fn, optimizer, device, scheduler, n_ex):
    model = model.train()
    losses = []
    correct = 0
    for d in data_loader:
        input_ids = d['input_ids'].to(1)
        attention_mask = d['attention_mask'].to(1)
        targets = d['targets'].to(1)        
        
        outputs = model(
                  input_ids=input_ids,
                  attention_mask=attention_mask
        )
        _, preds = torch.max(outputs, dim=1)
        loss = loss_fn(outputs, targets)
        
        correct += torch.sum(preds == targets)
        losses.append(loss.item())
        
        loss.backward()
        torch.nn.utils.clip_grad_norm(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad()
        
    return correct.double() / n_ex, np.mean(losses)

def eval_model(model, data_loader, loss_fn, device, n_ex):
    model = model.eval()
    losses = []
    correct = 0
    
    with torch.no_grad():
        for d in data_loader:
            input_ids = d['input_ids'].to(1)
            attemtion_mask_d = d['attention_mask'].to(1)
            targets = d['targets'].to(1)        

            outputs = model(
                      input_ids=input_ids,
                      attention_mask=attemtion_mask_d
            )
            _, preds = torch.max(outputs, dim=1)
            loss = loss_fn(outputs, targets)

            correct += torch.sum(preds == targets)
            losses.append(loss.item())
            
    return correct.double() / n_ex, np.mean(losses)    
# Read the data
sentiment_data = pd.read_csv('../DATA/twitter_sentiment_analysis.csv')
sentiment_data.Sentiment = sentiment_data.Sentiment.apply(lambda x: 0 if x == -1  else 1)
print(sentiment_data.head())

tokenizer = RobertaTokenizer.from_pretrained('roberta-base')

# Main params
MAX_LEN = 50
BATCH_SIZE = 16
EPOCHS = 50

df_train, df_test = train_test_split(sentiment_data, test_size=0.2)
df_val, df_test = train_test_split(df_test, test_size=14/29)

train_data_loader = create_data_loader(df_train, tokenizer,  MAX_LEN, BATCH_SIZE)
val_data_loader = create_data_loader(df_val, tokenizer,  MAX_LEN, BATCH_SIZE)
test_data_loader = create_data_loader(df_test, tokenizer,  MAX_LEN, BATCH_SIZE)

model = SentimentClassifier(2)
model = model.to(1)

optimizer = transformers.AdamW(model.parameters(), lr=2e-5, correct_bias=False)

total_steps = len(train_data_loader) * EPOCHS

scheduler = transformers.get_linear_schedule_with_warmup(
            optimizer,
            num_warmup_steps=0,
            num_training_steps=total_steps
)

loss_fn = torch.nn.CrossEntropyLoss().to(1)

# Training

history = defaultdict(list)
best_acc = 0

for epoch in range(EPOCHS):
    print(f"Epoch {epoch + 1}/{EPOCHS}")
    print("-"*10)
    
    train_acc, train_loss = train_epoch(
        model,
        train_data_loader,
        loss_fn,
        optimizer,
        0,
        scheduler,
        len(df_train))
    
    print(f"Train: loss => {train_loss} accuracy => {train_acc}")
    
    val_acc, val_loss = eval_model(
        model,
        val_data_loader,
        loss_fn,
        0,
        len(df_val))
    
    print(f"Validation: loss => {val_loss} accuracy => {val_acc}")
    print()
    
    history['train_acc'].append(train_acc)
    history['train_loss'].append(train_loss)   
    
    history['val_acc'].append(val_acc)        
    history['val_loss'].append(val_loss)    
    
    if val_acc > best_acc:
        torch.save(model.state_dict(), 'roberta_sentiment_twitter.bin')
        best_acc = val_acc