# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from django.contrib import admin
from dosirak.models import Question, Reply
# Register your models here.
class QuestionAdmin(admin.ModelAdmin):
   fieldsets =[('도시락점 이름',{'fields':['question_text']}),('Location',{'fields':['location']}),('Contacts',{'fields':['telephone']}),('Replier',{'fields':['replier']}),('Date information',{'fields':['pub_date'],'classes':['collapse']}),('맛',{'fields':['taste']}),('가격',{'fields':['price']}),('서비스',{'fields':['service']}),('분위기',{'fields':['air']}),('청결도',{'fields':['cleanness']}),('100자평',{'fields':['review']})]
   #fieldsets=[('Questionaire',{'fields':['question_text']}),('Date Info',{'fields':['pub_date']}),]
   # fields = ['pub_date','question_text']
   list_display = ('question_text','location','telephone','pub_date','replier','was_published_recently','taste','price','service','cleanness','air','review')
   list_filter = ['pub_date','question_text']
   #search_fields = ['question_text']
   #search_fields = ['foreign_key__related_fieldname']
   search_fields = ['question_text','location','telephone']

class ReplyAdmin(admin.ModelAdmin):
     fieldsets =[('도시락점 이름',{'fields':['question']}),('등록자',{'fields':['name']}),('Replied Date',{'fields':['rep_date'],'classes':['collapse']}),('맛',{'fields':['count_taste']}),('가격',{'fields':['count_price']}),('서비스',{'fields':['count_service']}),('분위기',{'fields':['count_air']}),('청결도',{'fields':['count_cleanness']}),('100자평',{'fields':['reple']})]
     list_display = ('question','name','rep_date','count_taste','count_price','count_service','count_cleanness','count_air','reple')
     list_filter = ['rep_date','question']
     list_filter = ['question']

admin.site.register(Question,QuestionAdmin)#상점 등록
admin.site.register(Reply,ReplyAdmin)#평 등록



