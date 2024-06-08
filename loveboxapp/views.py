from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Form
from pyecharts.charts import Bar
from pyecharts import options as opts
from pyecharts.charts import Pie
import openai
from django.conf import settings
import requests
import pandas as pd
import os

openai.api_key = settings.OPENAI_API_KEY
naver_shopping_api_URL = settings.NAVER_SHOPPING_API_URL
naver_shopping_api_client_id = settings.NAVER_SHOPPING_API_CLIENT_ID
naver_shopping_api_client_secret = settings.NAVER_SHOPPING_API_CLIENT_SECRET

# Create your views here.
def index(request):
    return render(request, 'index.html')

def new(request):
    return render(request, 'new.html')

def create(request):
    form = Form()
    form.sex = request.POST['sex']
    form.mbti = request.POST['mbti']
    form.price = request.POST['price']
    form.fashion_style = request.POST['fashion_style']
    form.hobby = request.POST['hobby']
    form.color = request.POST['color']
    form.food = request.POST['food']
    form.character = request.POST['character']
    form.laugh_cause = request.POST['laugh_cause']
    form.reaction_to_new_experience = request.POST['reaction_to_new_experience']
    form.music_style = request.POST['music_style']
    form.weather = request.POST['weather']
    form.sns_style = request.POST['sns_style']
    form.travel = request.POST['travel']
    form.movie_genre = request.POST['movie_genre']
    form.cat_or_dog = request.POST['cat_or_dog']
    form.value = request.POST['value']
    form.save()
    return redirect(f'/result?form_id={form.id}')

def result(request):
    id = request.GET.get('form_id')
    form = get_object_or_404(Form, id = id)
    reqText = '''너는 사용자가 제공한 연인의 정보들로 가장 확률이 높은 상위 1개 연인의 선물을 추천한다. 
        정확한 근거 없는 내용은 피한다.
        소개와 설명을 다음과 같은 형식으로 제공한다.
        item: 자동차, description: 자동차는 참 좋은 선물입니다.'''
    
    questionList = [
        "연인의 성별은 어떻게 되나요?",
        "연인의 MBTI가 무엇인가요?",
        "예상 선물 가격대는?(단위: 달러)",
        "연인이 선호하는 패션 스타일은?",
        "연인의 취미는 어떤 부류인가요?",
        "연인이 좋아하는 색깔은?",
        "연인이 좋아하는 음식은?",
        "연인의 정치 성향은?",
        "연인의 행복 모먼트는?",
        "새로운 경험을 할 때 보이는 반응",
        "좋아하는 음악 스타일은 무엇인가요?",
        "연인이 좋아하는 날씨는 어떤가요?",
        "연인의 SNS 사용 빈도는?",
        "연인은 어떤 여행을 선호하나요?",
        "선호하는 장르는 무엇인가요?",
        "강아지 vs 고양이",
        "연인의 중요한 가치관은 무엇인가요?"
    ]
    
    reqText += "\ninput: " + questionList[0] + "\noutput: " + form.sex
    reqText += "\ninput: " + questionList[1] + "\noutput: " + form.mbti
    reqText += "\ninput: " + questionList[2] + "\noutput: " + form.price
    reqText += "\ninput: " + questionList[3] + "\noutput: " + form.fashion_style
    reqText += "\ninput: " + questionList[4] + "\noutput: " + form.hobby
    reqText += "\ninput: " + questionList[5] + "\noutput: " + form.color
    reqText += "\ninput: " + questionList[6] + "\noutput: " + form.food
    reqText += "\ninput: " + questionList[7] + "\noutput: " + form.character
    reqText += "\ninput: " + questionList[8] + "\noutput: " + form.laugh_cause
    reqText += "\ninput: " + questionList[9] + "\noutput: " + form.reaction_to_new_experience
    reqText += "\ninput: " + questionList[10] + "\noutput: " + form.music_style
    reqText += "\ninput: " + questionList[11] + "\noutput: " + form.weather
    reqText += "\ninput: " + questionList[12] + "\noutput: " + form.sns_style
    reqText += "\ninput: " + questionList[13] + "\noutput: " + form.travel
    reqText += "\ninput: " + questionList[14] + "\noutput: " + form.movie_genre
    reqText += "\ninput: " + questionList[15] + "\noutput: " + form.cat_or_dog
    reqText += "\ninput: " + questionList[16] + "\noutput: " + form.value

        
    reqText += "\n\ninput: 연인에게 선물할 물건명 한가지와 추천한 선물에 대한 설명을 제공한다.\n" + "output:\n"
    
    query = openai.ChatCompletion.create( 
		model="gpt-3.5-turbo",
		messages=[
        	{'role':'user','content': reqText}
    	], 
		max_tokens=1024, 
		n=1, 
		stop=None, 
		temperature=0.5, 
	)
    response = query.choices[0].message["content"]
    
    lines = response.strip().split('\n')

    item = None
    description = None

    for line in lines:
        if line.startswith('item: '):
            item = line[len('item: '):].strip()
        elif line.startswith('description: '):
            description = line[len('description: '):].strip()
    
    return render(request, 'result.html', {'item': item, 'description': description})

def shopping(request):
    query = request.GET.get("item")
    url = naver_shopping_api_URL + "?query=" + query
    response = requests.get(url, headers={
        "X-Naver-Client-Id": naver_shopping_api_client_id, 
        "X-Naver-Client-Secret": naver_shopping_api_client_secret
    })
    items = response.json().get('items', [])
    return render(request, 'shopping.html', {'items': items})

def chooseStat(request):
    return render(request, 'chooseStat.html')

def statistics(request):
    forms = Form.objects.all().values()
    df = pd.DataFrame(forms)
    
    question = request.GET.get("question")
    
    if (question == 'sex-x-fashion-style') :
        gender_fashion = df.groupby(['sex', 'fashion_style']).size().unstack().fillna(0)
        graph = (
            Bar(init_opts=opts.InitOpts(width="100%", height="500px", chart_id="chart"))
            .add_xaxis(gender_fashion.columns.tolist())
            .add_yaxis("여성", gender_fashion.loc['여성'].tolist())
            .add_yaxis("남성", gender_fashion.loc['남성'].tolist())
        )
        title = "성별에 따른 패션스타일 분포"
    elif (question == 'mbti'):
        mbti_counts = df['mbti'].value_counts().reset_index()
        mbti_counts.columns = ['mbti', 'count']
        graph = (
            Pie(init_opts=opts.InitOpts(width="100%", height="500px", chart_id="mbti_chart"))
            .add("", [list(z) for z in zip(mbti_counts['mbti'], mbti_counts['count'])], radius=["20%", "60%"],)
            .set_global_opts(title_opts=opts.TitleOpts(title="MBTI Distribution", subtitle="MBTI 유형별 분포도"),
                    legend_opts=opts.LegendOpts(pos_bottom="0%",orient="horizontal",))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        )
        title = "MBTI 분포도"
    elif (question == 'sns-x-travel'):
        sns_travel = df.groupby(['sns_style', 'travel']).size().unstack().fillna(0)
        graph = (
            Bar(init_opts=opts.InitOpts(width="100%", height="500px", chart_id="sns_travel_chart"))
            .add_xaxis(['관광 추구형', '휴양 추구형'])
            .add_yaxis("SNS 자주함", sns_travel.loc['새로운 트렌드를 따라가는 것을 즐김'].to_list())
            .add_yaxis("SNS 안함", sns_travel.loc['SNS를 하지 않거나 정량적으로 사용함'].to_list())
        )
        title = "SNS 사용빈도에 따른 여행 스타일"
    
    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)

    graph_path = os.path.join(settings.MEDIA_ROOT, 'fashion_style_distribution.html')
    graph.render(graph_path)
    
    with open(graph_path, 'r', encoding='utf-8') as file:
        graph_html = file.read()

    context = {
        'title': title,
        'graph_html': graph_html
    }

    return render(request, 'statistics.html', context)