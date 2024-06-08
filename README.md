# LoveBox!

### 1. 개요

---

#### 1.1. 소개

머뭇거리는 당신을 위한 **연인 선물 추천 서비스** - [바로가기](https://djdongjae.pythonanywhere.com/)

#### 1.2. 기술 스택

<img src="https://img.shields.io/badge/python-3776AB?style=flat-square&logo=Python&logoColor=white" />&nbsp;<img src="https://img.shields.io/badge/django-092E20?style=flat-square&logo=django&logoColor=white" />&nbsp;<img src="https://img.shields.io/badge/OpenAi-412991?style=flat-square&logo=openai&logoColor=white" />&nbsp;<img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white" />&nbsp;<img src="https://img.shields.io/badge/Apache Echarts-AA344D?style=flat-square&logo=apacheecharts&logoColor=white" />
<img src="https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white" />&nbsp;<img src="https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white" />&nbsp;<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=white" />

### 2. 실행방법

---

#### 2.1. `secrets.json`

* 프로젝트 최상위 디렉토리에 위치

![alt text](<./image/Screenshot 2024-06-08 at 1.59.14 PM.png>)


#### 2.2. 가상환경 설치 및 실행

* Windows
```shell
 python -m venv venv
 source venv/Scripts/activate
```
* Mac
```shell
 python3 -m venv venv
 source venv/bin/activate
```

#### 2.3. 패키지 설치

```shell
 pip install -r requirements.txt
```

#### 2.4. DB 마이그레이션

* Windows
```shell
 python manage.py makemigrations
 python manage.py migrate
```
* Mac
```shell
 python3 manage.py makemigrations
 python3 manage.py migrate
```

#### 2.5. 서버 실행

* Windows
```shell
 python manage.py runserver
```
* Mac
```shell
 python3 manage.py runserver
```

### 3. 구현 기능 및 실행 이미지

---

#### 3.1. 선물 추천 기능

17가지의 질문 답변 후 폼 제출시 ChatGPT를 통한 선물 추천

<br>

![alt text](<./image/Screenshot 2024-06-08 at 2.34.55 PM.png>)

<br>

![alt text](<./image/Screenshot 2024-06-08 at 2.35.39 PM.png>)

<br>

![alt text](<./image/Screenshot 2024-06-08 at 2.36.01 PM.png>)

<br>

#### 3.2. 상품 목록 조회 기능

네이버 쇼핑 API를 통한 추천 선물 상위 10개 항목 리스트업

<br>

![alt text](<./image/Screenshot 2024-06-08 at 2.36.28 PM.png>)

<br>

#### 3.3. 통계 그래프

질문 폼을 통해 쌓인 데이터로 유의미한 통계 자료 제공

<br>

![alt text](<./image/Screenshot 2024-06-08 at 2.45.37 PM.png>)

<br>

![alt text](<./image/Screenshot 2024-06-08 at 2.45.46 PM.png>)

<br>

![alt text](<./image/Screenshot 2024-06-08 at 2.45.53 PM.png>)

<br>

![alt text](<./image/Screenshot 2024-06-08 at 2.46.00 PM.png>)