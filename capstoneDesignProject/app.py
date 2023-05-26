from flask import Flask, render_template, request, url_for
from werkzeug.utils import secure_filename
import os

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
            plot = title 

        #images들을 uploads파일에 저장, outputPage에서 삭제.
        #images값을 아얘 안 넣으면 문제가 생김. 따라서 없을 경우와 아닌 경우를 나눠서 진행
        #images 첫번째 파일 이름 값이 없을 경우를 따져서 파일 유무를 판단함
        if images[0].filename == "":
            images = ""
        else:
            #images로 넘어온 값들을 static/uploads 디렉토리로 하나씩 저장하기 위한 과정
            for i in images:
                i.save('static/uploads/'+ secure_filename(i.filename))
            #이미지 관련 AI 프로그래밍을 굴린다면###########################################################################
            #############################################################################################################
            # [이 공간을 활용해서 AI실행 python을 실행하고 다시 uploads파일에서 불러오고 생성 이미지를 저장하여 진행하도록 할 것]
            #############################################################################################################
            #############################################################################################################
            #해당 static/uploads에 저장된 이미지 데이터들을 배열 형식으로 불러옴. (정확히는 리스트인가?)
            images = os.listdir('static/uploads')

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