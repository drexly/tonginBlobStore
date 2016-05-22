# -*- coding: utf-8 -*-
import datetime#여기서임포트
from django.db import models
from django.utils import timezone



# Create your models here.
class Question(models.Model):
    question_text=models.CharField(max_length=100,default='통인시장 도시락집 이름')#식당 이름
    location=models.CharField(max_length=200,default='어디 와 어디 사이')#식당 위치
    telephone=models.CharField(max_length=200,default='02-')#식당 연락처
    replier=models.IntegerField(default=0)#평 남긴 방문자수
    gps=models.CharField(max_length=100,default='37.580718,126.969985')
    pub_date=models.DateTimeField('Published Date' ,default=timezone.now())#등록날짜

    def was_published_recently(self):#최근에 등록됬냐
        return self.pub_date >= timezone.now()-datetime.timedelta(days=7)#출판날짜가 더 크면 트루리턴
    was_published_recently.admin_order_field='pub_date'
    was_published_recently.boolean=True
    was_published_recently.short_description='최근 한 주 평 등록 여부'

    taste = models.FloatField(default=0.00)
    price = models.FloatField(default=0.00)
    service = models.FloatField(default=0.00)
    air = models.FloatField(default=0.00)
    cleanness = models.FloatField(default=0.00)
    review=models.CharField(max_length=2000,default='리뷰')#질문지2000
    def __str__(self):
        return self.question_text

class Reply(models.Model):
    question=models.ForeignKey(Question)
    name= models.CharField(max_length=100,default='사용자')
    count_taste = models.IntegerField(default=0)
    count_price = models.IntegerField(default=0)
    count_service = models.IntegerField(default=0)
    count_air = models.IntegerField(default=0)
    count_cleanness = models.IntegerField(default=0)
    rep_date=models.DateTimeField('Replied Date', default=timezone.now())#등록날짜
    reple=models.CharField(max_length=2000,default='리뷰')#질문지2000
    phonen=models.CharField(max_length=20,default=0)
    imageR=models.CharField(max_length=200)
    def update_Question(self):#별점 계산
        tastenew=(self.question.taste*(self.question.replier)+float(self.count_taste))/(self.question.replier+1)
        pricenew=(self.question.price*(self.question.replier)+float(self.count_price))/(self.question.replier+1)
        servicenew=(self.question.service*(self.question.replier)+float(self.count_service))/(self.question.replier+1)
        airnew=(self.question.air*(self.question.replier)+float(self.count_air))/(self.question.replier+1)
        cleannessnew=(self.question.cleanness*(self.question.replier)+float(self.count_cleanness))/(self.question.replier+1)#여기까지평점 재합산
        repliernew=self.question.replier
        Question.objects.filter(question_text=self.question.question_text).update(taste=tastenew,price=pricenew,service=servicenew,air=airnew,cleanness=cleannessnew,pub_date=self.rep_date,replier=repliernew+1)

    def __str__(self):
        return self.reple



