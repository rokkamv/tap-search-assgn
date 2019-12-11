from flask import Flask, render_template, redirect, request, session, url_for
import PyPDF2 #For PDF parsing
from nltk import word_tokenize #For tokenizing words
import pickle #For saving the indexed dictionary and using the saved .pickle in another function

app=Flask(__name__)

@app.route('/',methods=['GET', 'POST'])
def main(): #Takes input for choice of entering text and redirects accordingly
    if request.method=='POST':
        fileortxt=request.form['fileortxt']
        if fileortxt==str(0):
            return render_template('input.html',txt="Enter the text: ")
        else:
            return render_template('ipdf.html',file="Choose the file: ")

    return render_template('index.html')

@app.route("/handletxt", methods=['GET','POST'])
def handletxt(): #If directly text is entered then it is handled by this function
    if request.method=='POST':
        text=request.form['txtstr']
        doc_arr=[]
        lowtext=text.lower()
        doc_arr=lowtext.split('\r\n\r\n\r')
        docs,c={},1
        for doc in doc_arr:
            docs["Paragraph_"+str(c)]=word_tokenize(doc)
            c+=1
        with open('filename.pickle', 'wb') as handle: 
            pickle.dump(docs, handle, protocol=pickle.HIGHEST_PROTOCOL) #Saving the dictionary
        return render_template('search.html',indxt="Indexed content:",indexdisp=str(docs))
    
    return render_template('index.html')

@app.route("/handlePDF", methods=['GET','POST'])
def handlePDF(): #If a .pdf file is uploaded then it is handled by this function
    if 'pdf' in request.files:
        pdf = request.files['pdf']
        if pdf.filename != '':            
            pdf.save(pdf.filename)
            pdfFileObj = open(pdf.filename, 'rb') 
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
            text=""
            pdfnumpg=pdfReader.numPages
            for i in range(1,pdfnumpg):
                pageObj = pdfReader.getPage(i) 
                text+=pageObj.extractText() 
            pdfFileObj.close()
            doc_arr=[]
            lowtext=text.lower()
            doc_arr=lowtext.split('\n\n')
            docs,c={},1
            for doc in doc_arr:
                docs["Paragraph_"+str(c)]=word_tokenize(doc)
                c+=1
            with open('filename.pickle', 'wb') as handle:
                pickle.dump(docs, handle, protocol=pickle.HIGHEST_PROTOCOL) #Saving the dictionary
            return render_template('search.html',indxt="Indexed content:",indexdisp=str(docs))

    return render_template('index.html')

@app.route("/search",methods=['POST'])
def search(): #The word to be searched for is handled here and returns the locations where word is found
    if request.method=='POST':
        with open('filename.pickle', 'rb') as handle:
            docs = pickle.load(handle) #Retrieving the dictionary
        word=request.form['word']
        locs=[]
        for d_id,d_val in docs.items():
            if word.lower() in d_val:
                locs.append(d_id)
        res="'"+word+"' found in -"
        return render_template('result.html',res=res,locs=str(locs[:10]))
    
    return render_template('search.html')

if __name__ == '__main__':
    app.run(threaded=True,port=5000)
