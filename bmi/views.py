from django.shortcuts import render
from django.http import HttpResponse
from .forms import BmiForm
import random

def bmi(request):
    params = {
    'title' : 'BMI値測定',
    'form' : BmiForm()
    }

    if (request.method == 'POST'):
        height = int(request.POST['height'])
        weight = int(request.POST['weight'])
        
        bmi = round(weight / ((height/100) * (height/100)), 1)
        standard = round((height/100) * (height/100) * 22, 1)

        difference = round(abs(weight - standard), 1)
        if bmi < 18.5:
            result = f'痩せ型です。標準体重まで、{difference}kgです。がんばりましょう。'
        elif 18.5 <= bmi < 25.0:
            result = f'標準体重です。その状態を維持しましょう。'
        elif 25.0 <= bmi < 30.0:
            result = f'肥満(1度)です。標準体重より、{difference}kg多いです。がんばりましょう。'
        elif 30.0 <= bmi < 35.0:
            result = f'肥満(2度)です。標準体重より、{difference}kg多いです。がんばりましょう。'
        elif 35.0 <= bmi <40.0:
            result = f'肥満(3度)です。標準体重より、{difference}kg多いです。がんばりましょう。'
        elif 40 <= bmi:
            result = f'肥満(4度)です。標準体重より、{difference}kg多いです。もっとがんばりましょう。'

        if weight < 0:
            result = f'測定できません!  もう一度入力してください。'
        if height < 0:
            result = f'測定できません!  もう一度入力してください。'

        menu = ["松坂牛のステーキ", "アメリカ産牛肉の牛丼", "鶏の唐揚げ", "アブラカレイのムニエル", "腐ったみかん", "あさりのパスタ", "ペスカトーレ", "かき揚げ丼", "カレーライス", "ハヤシライス", "青汁", "ふやけたラーメン", "カキフライ", "刺身の5点盛り", "しなびた漬物", "シェフの気まぐれすぎるサラダ", "麻婆豆腐", "タバスコ特盛りタコス", "カニすき", "オムレツ", "カツ丼"]
        lunch = f'今日の献立ては、{random.choice(menu)}です。残さず、食べましょう。'

 
        params['bmi'] =bmi
        params['standard'] = standard
        params['result'] = result
        params['lunch'] = lunch

    return render(request, 'bmi/bmi.html', params)
