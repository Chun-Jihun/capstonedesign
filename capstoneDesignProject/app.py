from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from transformers import pipeline
import os
import sys
import urllib.request
import json

from PIL import Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 한글 폰트 등록
pdfmetrics.registerFont(TTFont('malgun', 'malgun.ttf'))

# 개발자센터에서 발급받은 Client ID 값
client_id = "8sg4VSnc_BjMjlFTLqY8" 
# 개발자센터에서 발급받은 Client Secret 값
client_secret = "9lFaUkZXdm" 

def save_story_to_pdf(text_list, img_files, pdf_file):
    #저장할 pdf지정
    pdf = SimpleDocTemplate("static/uploads/"+pdf_file, pagesizes=letter)
    story = []
    custom_style = ParagraphStyle(
        'CustomStyle', 
        parent=getSampleStyleSheet()['BodyText'], 
        #사용할 폰트
        fontName='malgun',
        #글자 크기
        fontSize=30,
        #줄 간격
        leading=38
    )

    #이미지와 텍스트파일 병합
    for i in range(min(len(text_list), len(img_files))):
        full_path = 'static/uploads/' + img_files[i]
        img = Image(full_path, width=200, height=200)
        story.append(img)
        text = Paragraph(text_list[i], custom_style)
        story.append(text)
        story.append(PageBreak())

    #지정한 pdf에 저장
    pdf.build(story)

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

        #title을 주제로 받으면 fairytalemaker실행
        else:
            #title이 한국어면 영어로 변환
            # if title.isalpha():
                # encText = urllib.parse.quote(title)
                # data = "source=ko&target=en&text=" + encText
                # url = "https://openapi.naver.com/v1/papago/n2mt"
                # api_request = urllib.request.Request(url)
                # api_request.add_header("X-Naver-Client-Id",client_id)
                # api_request.add_header("X-Naver-Client-Secret",client_secret)
                # api_response = urllib.request.urlopen(api_request, data=data.encode("utf-8"))
                # api_rescode = api_response.getcode()
                # if(api_rescode==200):
                #     response_body = api_response.read()
                #     title = json.loads(response_body.decode('utf-8'))['message']['result']['translatedText']

            generator = pipeline('text-generation', tokenizer='gpt2', model='trained_model')
            plot = generator(title, max_length=800)[0]['generated_text']
            
            # encText = urllib.parse.quote(plot)
            # data = "source=en&target=ko&text=" + encText
            # url = "https://openapi.naver.com/v1/papago/n2mt"
            # api_request = urllib.request.Request(url)
            # api_request.add_header("X-Naver-Client-Id",client_id)
            # api_request.add_header("X-Naver-Client-Secret",client_secret)
            # api_response = urllib.request.urlopen(api_request, data=data.encode("utf-8"))
            # api_rescode = api_response.getcode()
            # if(api_rescode==200):
            #     response_body = api_response.read()
            #     plot = json.loads(response_body.decode('utf-8'))['message']['result']['translatedText']

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

        if len(title) == 1:
            files = os.listdir('static/uploads')
            images = [f for f in files if os.path.splitext(f)[1] in ['.png', '.jpg', '.jpeg', '.gif']]

            # plot을 문단으로 분리
            plot_paragraphs = [p for p in plot.split('\n') if p.strip() != '']

            # 생성된 images와 plot_paragraphs를 pdf로 저장
            save_story_to_pdf(plot_paragraphs, images, 'result.pdf')
        else:
            pdf = SimpleDocTemplate("static/uploads/result.pdf", pagesizes=A4)
            story = []
            custom_style = ParagraphStyle(
            'CustomStyle', 
            parent=getSampleStyleSheet()['BodyText'], 
            #사용할 폰트
            fontName='malgun',
            #글자 크기
            fontSize=30,
            #줄 간격
            leading=38
            )
            story.append(Paragraph(plot, custom_style))
            pdf.build(story)

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