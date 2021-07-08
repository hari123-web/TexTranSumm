from flask import Flask,render_template,request,send_file
import os
import PyPDF2
from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords

from textblob import TextBlob
import os
from gtts import gTTS         #text to audio conversion

import pyttsx3                # use to access system speaker
speaker=pyttsx3.init()

name=" "




demo = Flask(__name__)
picfolder = os.path.join('static','pics')
demo.config['UPLOAD_FOLDER']=picfolder


@demo.route('/')
@demo.route('/home')
def home():
    pic1=os.path.join(demo.config['UPLOAD_FOLDER'],'logo.png')
    return render_template('home.html',user_image=pic1)

@demo.route('/about')
def about():
    pic1 = os.path.join(demo.config['UPLOAD_FOLDER'], 'logo.png')
    return render_template('about.html', user_image=pic1)

@demo.route('/summary', methods=["GET","POST"])
def summary():
    if request.method=="POST":
        try:
            file = request.files["file"]
            file.save(os.path.join("uploads", file.filename))
            name = file.filename
            if (name.find(".pdf") != -1):
                name = pdf(name)
            res=summarization(name)

            return render_template("summary.html", message="Successfully Uploaded !!!",text=res)
        except:
            return render_template("summary.html", message="Opps !!! Please Select proper option and check file is uploaded or not")



    return render_template('summary.html', message="Upload a .txt or .pdf file")



@demo.route('/txtTranslation', methods=["GET","POST"])
def txtTranslation():

    if request.method=="POST":
        try:
            file = request.files["file"]
            file.save(os.path.join("uploads", file.filename))
            name = file.filename
            if(name.find(".pdf")!=-1):
                name=pdf(name)
            option = request.form.getlist('options')
            res=txtTrans(name, option)

            return render_template("txtTranslation.html", message="Successfully Uploaded !!!",text=res)
        except:
            return render_template("txtTranslation.html", message="Opps !!! Please Select proper option and check file is uploaded or not")

    return render_template('txtTranslation.html', message="Upload a .txt or .pdf file")


@demo.route('/transSummay', methods=["GET","POST"])
def transSummay():

    if request.method=="POST":
        try:
            file = request.files["file"]
            file.save(os.path.join("uploads", file.filename))
            name = file.filename
            if (name.find(".pdf") != -1):
                name = pdf(name)
            option = request.form.getlist('options')
            res=transmarry(name, option)

            return render_template("transSummay.html", message="Successfully Uploaded !!!",text=res)
        except:
            return render_template("transSummay.html", message="Opps !!! Please Select proper option and check file is uploaded or not")



    return render_template('transSummay.html', message="Upload a .txt or .pdf file")



def txtTrans(name,option):
    name="A:\\project\\text summerizer\\website\\uploads\\"+name
    FileObject = open(name, 'r',encoding="utf8")  # open file
    an = FileObject.read()  # read file and store it in variable an
    FileObject.close()  # close file

    if option[0]=="Marathi":
        lan='mr'
    if option[0]=="Hindi":
        lan='hi'
    if option[0]=="English":
        lan='en'

    hi_blob = TextBlob(an)
    result = hi_blob.translate(to=lan)

    return result

def summarization(name):
    name = "A:\\project\\text summerizer\\website\\uploads\\" + name
    FileObject = open(name, 'r', encoding="utf8")  # open file
    an = FileObject.read()  # read file and store it in variable an
    FileObject.close()  # close file

    res = summarize(an, split=True, ratio=0.5)
    str1 = " "
    resFinal = str1.join(res)
    return resFinal

def transmarry(name,option):
    name = "A:\\project\\text summerizer\\website\\uploads\\" + name
    FileObject = open(name, 'r', encoding="utf8")  # open file
    an = FileObject.read()  # read file and store it in variable an
    FileObject.close()  # close file

    res = summarize(an, split=True, ratio=0.5)
    str1 = " "
    resFinal = str1.join(res)

    if option[0]=="Marathi":
        lan='mr'
    if option[0]=="Hindi":
        lan='hi'
    if option[0]=="English":
        lan='en'

    hi_blob = TextBlob(resFinal)
    result = hi_blob.translate(to=lan)
    return result


def pdf(name):
    name = "A:\\project\\text summerizer\\website\\uploads\\" + name
    pdffileobj=open(name,'rb')
    pdfreader=PyPDF2.PdfFileReader(pdffileobj)
    x=pdfreader.numPages
    txt=" "
    for i in range(0,x):
        pageobj = pdfreader.getPage(i)
        txt = txt + pageobj.extractText()
    file1=open(r"A:\\project\\text summerizer\\website\\uploads\\demoTXT2.txt","a",encoding='utf8')
    file1.truncate(0)
    file1.writelines(txt)
    name="demoTXT2.txt"
    return name

if __name__ == "__main__":
    demo.run(debug=True)