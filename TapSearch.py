#!/usr/bin/env python
# coding: utf-8

# In[1]:


from nltk import word_tokenize


# In[ ]:


def clear(text,doc_arr,docs):
    text,doc_arr,docs="",[],{}
    return text,doc_arr,docs
    
def preprocess(text):
    doc_arr=[]
    lowtext=text.lower()
    doc_arr=lowtext.split('\n\n')
    return doc_arr
    
def index(doc_arr):
    docs,c={},1
    for doc in doc_arr:
        docs["Paragraph_"+str(c)]=word_tokenize(doc)
        c+=1
    return docs

def search(word,docs):
    locs=[]
    for d_id,d_val in docs.items():
        if word.lower() in d_val:
            locs.append(d_id)
    print("'"+word+"' found in-")
    print(str(locs[:10]))
       

inp=input("Enter 0 to to upload a text file or 1 to input text: ")
if inp==str(0):    
    filename=input("Enter file name: ")
    text=open(filename).read()
else:
    text=input("Enter the text:")
doc_arr=preprocess(text)
docs=index(doc_arr)
# print('abc'+str(docs))
choice=1
while choice==1:
    word=input("Enter a word to search for: ")
    search(word,docs)
    choice=input("Enter 0 to exit or 1 to search again: ")
text,doc_arr,docs=clear(text,doc_arr,docs)


# In[ ]:




