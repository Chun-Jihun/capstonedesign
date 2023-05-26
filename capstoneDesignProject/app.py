from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from transformers import pipeline
import os

from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfMerger
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 한글 폰트 등록
pdfmetrics.registerFont(TTFont('malgun', 'malgun.ttf'))

def save_text_to_pdf(text, pdf_file):
    pdf = SimpleDocTemplate("static/uploads/"+pdf_file, pagesizes=letter)
    story = []
    # 커스텀 스타일 생성
    custom_style = ParagraphStyle(
        'CustomStyle', 
        parent=getSampleStyleSheet()['BodyText'], 
        fontName='malgun'
    )
    story.append(Paragraph(text, custom_style))
    pdf.build(story)

# 이미지 데이터를 PDF로 저장하는 함수
def save_img_to_pdf(img_files, pdf_files):
    for i, img_file in enumerate(img_files):
        full_path = 'static/uploads/' + img_file
        c = canvas.Canvas(pdf_files[i], pagesize=letter)
        c.drawImage(full_path, 0, 0, width=200, height=200)
        c.showPage()
        c.save()

# 두 PDF를 합치는 함수
def merge_pdfs(pdf_list, output):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write('static/uploads/'+output)
    merger.close()

app = Flask(__name__)

@app.route('/')
def back_mainPage():
    return render_template('mainPage.html')

@app.route('/send', methods=['POST', 'GET'])
def send():
    if request.method == 'POST':
        title = request.form['title']
        images = request.files.getlist('images')

        #title에 따른 plot 결정
        if(title == '0'):
            f = open('fairyTales/snowWhite.txt', 'r', encoding='UTF8')
            plot = f.read()

        elif(title == '1'):
            f = open('fairyTales/cinderella.txt', 'r', encoding='UTF8')
            plot = f.read()

        elif(title == '2'):
            f = open('fairyTales/kongjuipadjui.txt', 'r', encoding='UTF8')
            plot = f.read()

        elif(title == '#'):
            plot = "오류 : 아무 주제도 고르지 않았습니다."

        #개발한다면 여기 밑에 추가해서 진행하는게 더 좋아보일 듯.
        else:
            generator = pipeline('text-generation', tokenizer='gpt2', model='trained_model')
            plot = generator(title, max_length=800)[0]['generated_text']
            # plot = title 

        #images들을 uploads파일에 저장, outputPage에서 삭제.
        #images값을 아얘 안 넣으면 문제가 생김. 따라서 없을 경우와 아닌 경우를 나눠서 진행
        #images 첫번째 파일 이름 값이 없을 경우를 따져서 파일 유무를 판단함
        if images[0].filename == "":
            images = ""

        else:
            #images로 넘어온 값들을 static/uploads 디렉토리로 하나씩 저장하기 위한 과정
            for i in images:
                i.save('static/uploads/'+ secure_filename(i.filename))

            #해당 static/uploads에 저장된 이미지 데이터들을 list 형식으로 불러옴.
            images = os.listdir('static/uploads')

        files = os.listdir('static/uploads')
        images = [f for f in files if os.path.splitext(f)[1] in ['.png', '.jpg', '.jpeg', '.gif']]

        # 생성된 images와 str들을 pdf로 저장
        save_text_to_pdf(plot,'title.pdf')
        img_pdf=[]
        for i in range(len(images)):
            img_pdf.append('static/uploads/img'+str(i)+'.pdf')
        save_img_to_pdf(images,img_pdf)
        pdf_list = ['static/uploads/title.pdf']+img_pdf
        output = 'result.pdf'
        merge_pdfs(pdf_list,output)

        return render_template("outputPage.html", title=title, images=images, plot= plot)

#outputPage에서 home으로 돌아갈 때, 입력한 이미지를 지우기 위한 과정
@app.route('/delete')
def delete():
    dir = 'static/uploads'
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    return render_template('mainPage.html')

if __name__ == '__main__':
    app.run(debug=True)