from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Form
import openai
from django.conf import settings

openai.api_key = settings.OPEN_AI_KEY

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
    form.save()
    return redirect(f'/result/?form_id={form.id}')

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
        "예상 선물 가격대는?",
        "연인이 선호하는 패션 스타일은?"
    ]
    
    reqText += "\ninput: " + questionList[0] + "\noutput: " + form.sex
    reqText += "\ninput: " + questionList[1] + "\noutput: " + form.mbti
    reqText += "\ninput: " + questionList[2] + "\noutput: " + str(form.price)
    reqText += "\ninput: " + questionList[3] + "\noutput: " + form.fashion_style
        
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

    # item과 description 초기화
    item = None
    description = None

    # 각 줄을 검사하여 item과 description을 추출
    for line in lines:
        if line.startswith('item: '):
            item = line[len('item: '):].strip()
        elif line.startswith('description: '):
            description = line[len('description: '):].strip()
    
    return render(request, 'result.html', {'item': item, 'description': description})
