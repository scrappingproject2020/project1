
import json
import unicodedata
import pandas as pd
import re

#read json
with open('../Data/article_text.json',encoding='utf-8') as json_file:
    data = json.load(json_file)

#create dataframe
df = pd.DataFrame.from_dict(data)
df.head()

#remove all the na
df = df.dropna()

#transform from list to values/text
df['article_title'] = df['article_title'].str[0]
df['blurp']=df['blurp'].str[0]

#clean text function
def clean_text(text):
    text = ''.join(text)
    text = text.strip()
    text = " ".join(text.split())
    text = text.replace('[','')
    text = text.replace(']','')
    return text
#rename article body column to text
df.rename(columns={'article_body': "text"},inplace= True)

#apply clean text function
df['text'] =df['text'].apply(lambda x: clean_text(x))

#output to csv
df.to_csv('../Output/article_text.csv')
