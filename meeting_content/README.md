# 회의내용

## 목차
  [1주차](https://github.com/Chun-Jihun/capstonedesign/tree/main/meeting_content#1주차)   
  [2주차](https://github.com/Chun-Jihun/capstonedesign/tree/main/meeting_content#2주차)   
  [3주차](https://github.com/Chun-Jihun/capstonedesign/tree/main/meeting_content#3주차)   
  [4주차](https://github.com/Chun-Jihun/capstonedesign/tree/main/meeting_content#4주차)   
  5주차   

## 1주차
  캡스톤디자인 단체OT진행

### 230302 - 주제 적합성 토의
  > __인물 사진을 기반으로 캐릭터 생성(Stable Defusion모델)__

  > __ChatGPT를 통한 법률상담 챗봇__
    >>  - 부정확성 혹은 남용의 문제가 있을 수 있음

  > __동영상 화질 및 음성품질 개선프로그램__
    >>  - 개발기간이 너무 짧아 현실적으로 개발하기 어려워보임

  > __카메라를 통한 주차 통제 프로그램__
    >>  - 여러 한계성과 접근성의 문제로 실용성이 떨어진다고 판단

  > __음식 사진을 통해 섭취한 열량 계산__
    >>  - 실제 부피를 계산하는 방법에 현재 팀의 수준으로 프로젝트 기간동안 구현하기 힘들다고 판단

  > __ChatGPT를 사용하여 입력한 문서의 내용 요약__

  > __ChatGPT와 이마젠(혹은 Stable Diffusion)을 이용하여 광고영상 제작__

### 230303 - 교수님께 상담할 주제 토의
  > __인물 사진을 기반으로 캐릭터 생성__   
  >>  - 사용자가 원하는 그림체로 캐릭터 생성(독창성)
  >>  - 사진을 통해 배경 학습(DreamBooth모델 사용) + 사진을 캐릭터화(Stable Diffusion)
  >>  1. 사진을 여러장 찍는다.(전신사진도 가능) -> AI에게 학습시켜 배경을 선정한다.(버튼으로 배경 선택) -> 인물과 배경을 캐릭터화한다.(해당 과정에서 그림체 선택 가능)
  >>  2. 얼굴 및 전신을 한 장 찍는다. -> 얼굴 혹은 전신과 배경을 캐릭터화한다.(해당 과정에서 그림체 선택 가능)   
  >>  전자의 경우 구체적이고 사용자가 고를 수 있는 결과물의 양이 다양해진다. 후자의 경우 캐주얼해지면서 간단하게 사용 가능해진다.

  > __저화질 영상 개선 프로그램__

  > __ChatGPT를 사용한 (법률상담) 챗봇__

  >>  - 요점 요약 -> 타이핑한 내용 혹은 이미지를 OCR등의 기술을 사용하여 프롬프트로 변환 후 모델에게 입력

  > __마케팅 및 광고 영상 제작 AI(웹사이트로 진행)__   
  >>  - SE나 BGM은 사람이 직접 추가하는 작업을 거쳐야한다.   
  >>  상품과 관련된 여러 장의 사진과 설명 및 키워드 입력 -> ChatGPT를 사용하여 광고용 시나리오 생성 -> 인공지능 모델(예)[이마젠](https://www.aitimes.com/news/articleView.html?idxno=147178), Stable Diffusion)을 사용하여 마케팅 영상 생성


### 230307 - 팀원 추가 및 주제 회의
  1. 프로젝트 주제 (제안)
  > __인물사진 -> 캐릭터화 (방식은 기존의 방식)__
  >> 간편하게 사진 한장을 찍으면 그것을 바로 AI를 통해 캐릭터화
  >> 인물과 배경을 구분, 배경과 악세서리 등을 AI를 통해 사용자가직접 선택할 수 있게함 (좀 더 구체적)
  >> 차별성 : 캐릭터풍을 다양하게 가능, 배경과 악세서리를 사용자가 직접 선택이 가능 

  > __마케팅 광고 영상 제작 (방식은 기존의 방식)__
  >> 제품에 대한 사진 몇장과 키워드, 제품 설명으로 ChatGPT를 통해 시나리오 작성 기존의 제품 사진과 ChatGPT의 시나리오를 통해 마케팅 광고영상 제작 

  > __수화번역기__
  >> 수화에 잘 모르는 일반인 혹은 수화를 처음 배우는 장애인을 대상. 수화를 인식하여 이를 문장으로 표현, 또한 문장을 입력하여 수화로 표현할 수 있게 함. 
  >> 굳이 수화를 표현해야하는가? 필담보다 나은 점이 있는가?

  > __동화 생성__
  >> ChatGPT를 통해 동화를 생성 (불완전하기에 조정해야함) 사진을 붙여서 하나의 동화로 만들어내거나, 만들어낸 동화를 가지고 동영상으로 만들어서 출력 

  > __옷 착용 검색__
  >> AI로 착용한 옷 및 신발을 구분 이를 구글이미지 검색을 활용하여 결과를 화면에 표시 

  2. 프로젝트 담당 교수님 후보
  * 허종욱 교수님 - 사실상 유력후보 아니신가 생각함. 우리가 하려고 하는 분야와 맞아 떨어지는 교수님
  * 정태경 교수님 - 인공지능융합학부로 우리와 학과가 다르다. 담당하실 수 있을지는 의문. 담당하실 수 없다면 조언을 구하는 쪽으로 생각중   
  아니면 우리 캡스톤 디자인 담당 교수님인 박승용 교수님께 자문을 구하고 교수님을 추천받는 방식이 좋을 것 같다. 

  3. 결론 
  * 3월 9일까지 팀 인원 및 프로젝트 주제 제출 오늘까지
  * 캡스톤 디자인 담당 교수님이신 박승용 교수님께 이메일로 문의를 드려서 현재 나온 5가지 주제를 줄이고 간소화
  * 개발 자문 관련 담당 교수님께 이메일을 드리고 자문을 구하는 형식으로 진행을 할 것

## 2주차

### 230309 - 분반 OT 및 프로젝트 회의
  1. 분반OT내용
  - 종합서류 작성 할 때 해당 서류만 포함해서 올리기(전체서류 올리기 금지)
  - 03분반_ACT_문서이름과 같은 제목으로 서류제출
  - 다음일정: 프로젝트 신청서 및 실행계획서 제출
  - 프로젝트 실행 계획서 작성 요령
  - 참여기업 필수기재 (리스트 17일 보내줄 예정)
  - 프로젝트 실행 계획서에 Git주소 필수기재
  - 오픈소스 사용계획 필수기재
  - 세부인원 현황 - 전자서명 기입(타이핑(X))
  - 활동비 실행 예산서 
    1) 완벽하게 계획대로 집행하지 않아도 됨(예산변경신청서)
    2) 적당히 나눠서작성
  - 개인정보 동의서 작성
  - 총 6장 3/21까지 제출
  - 중간보고서
  - 산업체 참여 신청서 서명은 교수님이 일괄처리 해주실 예정
  - 결과보고서
  - 템플릿 보내주실 예정
    + 추후 추가공지예정
  
### 230313 - 박승용 교수님 면담
추후수정

## 3주차

### 230315 - 허종욱 교수님 면담
1. 교수님 캡스톤 지도방식
- 학생들이 원할 때마다 일정 맞춰서 면담해주심 (오늘과 같이 예약하고 만나면 됨)
- 졸업프로젝트로써 어떤 이력을 남기는가를 중요하게 생각하심
- 취업할 때 자랑할만한 기술 등을 고려하심
- 소스코드 보고 따라하기 보다, 스스로 깊이 있게 할 것을 당부하심
- 본인의 역할에 대해 생각하고, 뭉개지지 않게 할 것! (본인이 맡을 역할에 대한 어필을 중요하게 생각하심)
- 교수님의 의견보다 팀원들과의 조율을 중요시함
- 참신성은 후순위, 기술적인 깊이에 고민, 프로젝트를 다듬을 것
- AI(현재 우리팀 3명)를 한다면 해당 분야에서 역할 담당을 생각할 것

2. 추가적인 내용
- 디테일에 대해서 생각해야함
- 영상생성은 현실적으로 힘들다. 좋은 하드웨어(=서버)를 가져야 한다.
- 프로젝트 진행하는데 어려움이 있으면 의미가 있다고 생각하신다.

3. 교수님께서 골라주신 프로젝트
> 2번 : 마케팅 광고 영상 

> 4번 : 동화 영상 제작

### 230318 - 주제선정회의

- 주제 선정 : 4번 + 1번 : 사진 속의 인물을 캐릭터화 시켜서 동화로 만들어내는 프로그램
- AI 담당 구분 : 1) ChatGPT 담당 1명 / 2) 동화이미지 1명 / 3) 그림체 검수 (앞의 그림과 뒤의 그림이 다르지 않도록 유도) / 4) TTS / 추가로 더 있을 수 있음
- 플랫폼 : 최종적으로는 앱 (현재는 하이브리드 앱을 대상 -> 웹에서 모바일 UI에 맞게 개발, 앱으로 해당 웹 페이지를 띄워 최종적으로는 앱의 형태로 만들어냄) [나중에 기회가 된다면 아얘 크로스플랫폼 앱(플러터 개발)을 노린다.

- 추가 : 2023/03/20(월) 오후 6시 공학관에 모여서 서류 작성할 것.

### 230320 - 제출해야할 서류 작성

## 4주차
