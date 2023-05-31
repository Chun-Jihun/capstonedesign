from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
from transformers import pipeline
import os
import sys
import urllib.request
import json
import subprocess
from time import sleep

from PIL import Image
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 한글 폰트 등록
pdfmetrics.registerFont(TTFont('Binggrae', 'Binggrae.ttf'))

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
        fontName='Binggrae',
        #글자 크기
        fontSize=30,
        #줄 간격
        leading=38
    )

    #이미지와 텍스트파일 병합
    for i in range(len(text_list)):
            if i < len(img_files):
                if i == 0:
                    full_path = 'static/uploads/' + img_files[i]
                else:
                    full_path = 'static/uploads/txt2img/' + img_files[i]
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
            plot_ill = open('fairyTales/snowWhite_eng.txt', 'r', encoding='UTF8').read()


        elif(title == '1'):
            f = open('fairyTales/cinderella.txt', 'r', encoding='UTF8')
            plot = f.read()
            plot_ill = open('fairyTales/cinderella_eng.txt', 'r', encoding='UTF8').read()


        elif(title == '2'):
            f = open('fairyTales/kongjuipadjui.txt', 'r', encoding='UTF8')
            plot = f.read()
            plot_ill = open('fairyTales/kongjuipadjui_eng.txt', 'r', encoding='UTF8').read()

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
            #img2img프롬프트
            #prompt = "masterpiece, (detailed), by disney, worst quality:-1.4, low quality:-1.4, greyscale:-1.1, monochrome:-1.1, 3D face:-1.0, Easynegative:-1.0"
            prompt = "masterpiece, (detailed), by disney, worst quality:-1.4, low quality:-1.4, greyscale:-1.1, monochrome:-1.1, 3D face:-1.0, Easynegative:-1.0"
            #이미지 이름 불러와야함
            # init_img = "static/uploads/test.jpg"
            init_img = 'static/uploads/'+[f for f in os.listdir('static/uploads') if os.path.splitext(f)[1] in ['.png', '.jpg', '.jpeg', '.gif']][0]


            command = f'python scripts/img2img.py --prompt "{prompt}" --init-img "{init_img}"'
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                stdout, stderr = process.communicate()
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
            process.terminate()

            if process.returncode != 0:
                print(f'Error occurred: {stderr.decode()}')
            else:
                print(stdout.decode())
                
            #txt2img프롬프트
            plot_paragraphs = [p for p in plot_ill.split('\n') if p.strip() != '']
            for i in plot_paragraphs:
                command_ill = f'python scripts/txt2img.py --prompt "{i}"'
                process_ill = subprocess.Popen(command_ill, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    stdout_ill, stderr_ill = process_ill.communicate(timeout=30)
                except subprocess.TimeoutExpired:
                    process_ill.kill()
                    stdout_ill, stderr_ill = process_ill.communicate()
                process_ill.terminate()


            if process_ill.returncode != 0:
                print(f'Error occurred: {stderr_ill.decode()}')
            else:
                print(stdout_ill.decode())
            files = os.listdir('static/uploads')
            images_0 = [f for f in files if os.path.splitext(f)[1] in ['.png', '.jpg', '.jpeg', '.gif']][0]
            print('**************************************************************************')
            print('images : ', images)
            print('txt2img : ',[f for f in os.listdir('static/uploads/txt2img') if os.path.splitext(f)[1] in ['.png', '.jpg', '.jpeg', '.gif']])
            print('**************************************************************************')
            images = [f for f in os.listdir('static/uploads/txt2img') if os.path.splitext(f)[1] in ['.png', '.jpg', '.jpeg', '.gif']]
            images.insert(0,images_0)
            # plot을 문단으로 분리
            plot_paragraphs = [p for p in plot.split('\n') if p.strip() != '']

            # 생성된 images와 plot_paragraphs를 pdf로 저장
            save_story_to_pdf(plot_paragraphs, images, 'result.pdf')
            process.kill()
            process_ill.kill()
        else:
            pdf = SimpleDocTemplate("static/uploads/result.pdf", pagesizes=A4)
            story = []
            custom_style = ParagraphStyle(
            'CustomStyle', 
            parent=getSampleStyleSheet()['BodyText'], 
            #사용할 폰트
            fontName='Binggrae',
            #글자 크기
            fontSize=30,
            #줄 간격
            leading=38
            )
            files = os.listdir('static/uploads')
            images = [f for f in files if os.path.splitext(f)[1] in ['.png', '.jpg', '.jpeg', '.gif']]

            #이미지와 텍스트파일 병합
            full_path = 'static/uploads/' + images[0]
            img = Image(full_path, width=200, height=200)
            story.append(img)
            story.append(Paragraph(plot, custom_style))
            story.append(Paragraph(plot, custom_style))
            pdf.build(story)

        process.kill()
        process_ill.kill()
        return render_template("outputPage.html", title=title, images=images, plot= plot)

#outputPage에서 home으로 돌아갈 때, 입력한 이미지를 지우기 위한 과정
@app.route('/delete')
def delete():
    dir = 'static/uploads'
    dir_1 = 'static/uploads/txt2img'
    dir_2 = 'static/uploads/txt2img/samples'
    for f in os.listdir(dir_2):
        os.remove(os.path.join(dir_2, f))
    os.rmdir(dir_2)
    for f in os.listdir(dir_1):
        os.remove(os.path.join(dir_1, f))
    os.rmdir(dir_1)
    for f in os.listdir(dir):
        os.remove(os.path.join(dir, f))
    
    return render_template('mainPage.html')

if __name__ == '__main__':
    app.run(debug=True)