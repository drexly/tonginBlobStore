#-*- coding: utf-8 -*-
import sys
import cgi
reload(sys)
sys.setdefaultencoding("utf-8")
from django.shortcuts import get_object_or_404,render
from django.core.urlresolvers import reverse
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from dosirak.models import Question,Reply
from django.utils import timezone
from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.api import images
from django import http
from google.appengine.ext.webapp import blobstore_handlers
import webapp2
from dosirak.baseView import BaseView
from dosirak.blobstore import get_uploads
from google.appengine.ext.webapp import template
from django.contrib.staticfiles.templatetags.staticfiles import static


# This datastore model keeps track of which users uploaded which photos.
# <form action="{% url 'vote' question.id %}" method="POST" enctype="multipart/form-data">

class ImageInfo(ndb.Model):

    serving_url = ndb.StringProperty(indexed=False)

    blob_key = ndb.BlobKeyProperty(indexed=False)

    content_type = ndb.StringProperty(indexed=False)

    original_filename = ndb.StringProperty(indexed=False)

    created = ndb.DateTimeProperty(auto_now_add=True)

class PhotoUploadFormHandler(BaseView):

    #def __init__(self,*args,**kwargs):
     #   array=str(kwargs).split("'")
      #  self.question_id=int(array[len(array)-2])
       # self.question=get_object_or_404(Question,pk=self.question_id)
        #self.reply_list=Reply.objects.order_by('question')[:]

    def get(self,question_id):
        question=get_object_or_404(Question,pk=question_id)
        gpsarray=question.gps.split(",")
        gpsx=gpsarray[0]
        gpsy=gpsarray[1]
        reply_list=question.reply_set.order_by('question')[:]#Reply.objects.order_by('question')[:]
        update_taste=update_price=update_service=update_cleanness=update_air=0
        if(len(reply_list)>0):
            for rep in reply_list:
                update_taste+=rep.count_taste
                update_price+=rep.count_price
                update_air+=rep.count_air
                update_cleanness+=rep.count_cleanness
                update_service+=rep.count_service
            question.taste=float(float(update_taste)/len(reply_list))
            question.price=float(float(update_price)/len(reply_list))
            question.air=float(float(update_air)/len(reply_list))
            question.cleanness=float(float(update_cleanness)/len(reply_list))
            question.service=float(float(update_service)/len(reply_list))
        else:
            question.taste=question.price=question.air=question.cleanness=question.service=float(0.0)
        question.save()
        upload_url = blobstore.create_upload_url('/dosirak/upload_photo/')
        return self.render_to_response('dosirak/detail.html',{'question':question,'reply_length':len(reply_list) ,'reply_list':reply_list, 'upload_url':upload_url,'question_id':question_id,'gpsx':gpsx,'gpsy':gpsy})
        #self.response.out.write(template.render('dosirak/detail.html',{'question':self.question, 'reply_list':self.reply_list, 'upload_url':upload_url,'question_iid':self.question_id}))
        #return render(self.request,'dosirak/detail.html', {'upload_url':upload_url})
        #return render_to_response('dosirak/detail.html', context={'question':self.question, 'reply_list':self.reply_list, 'upload_url':upload_url,'question_iid':self.question_id})
        #return render('dosirak/detail.html', {'question':question,'reply_list':reply_list})
#class PhotoUploadFormHandler(webapp2.RequestHandle,BaseView):

 #    def __init__(self,*args,**kwargs):
  #      array=str(kwargs).split("'")
   #     self.question_id=int(array[len(array)-2])
    #    self.question=get_object_or_404(Question,pk=self.question_id)
     #   self.reply_list=Reply.objects.order_by('question')[:]

    #def get(self,*arg):
        #question=get_object_or_404(Question,pk=question_id)
        #reply_list=Reply.objects.order_by('question')[:]
     #   upload_url = blobstore.create_upload_url('/dosirak/upload_photo/')

        #self.response.out.write(template.render('dosirak/detail.html',{'question':self.question, 'reply_list':self.reply_list, 'upload_url':upload_url,'question_iid':self.question_id}))
        #return render(self.request,'dosirak/detail.html', {'upload_url':upload_url})
        #return render_to_response('dosirak/detail.html', context={'question':self.question, 'reply_list':self.reply_list, 'upload_url':upload_url,'question_iid':self.question_id})
        #return render('dosirak/detail.html', {'question':question,'reply_list':reply_list})



#class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
class PhotoUploadHandler(BaseView):
    def post(self):
        qid=self.request.POST.get('qid')
        p = get_object_or_404(Question, pk=qid)
        taste=self.request.POST.get('taste')
        service=self.request.POST.get('service')
        price=self.request.POST.get('price')
        air=self.request.POST.get('air')
        cleanness=self.request.POST.get('cleanness')
        replier=self.request.POST.get('replier')
        review=self.request.POST.get('review')
        phone=self.request.POST.get('phone')
        path="/dosirak/"+qid
        star_set=[taste,service,price,air,cleanness]
        if star_set.__contains__('0') or (replier=='' or review==''):
            return HttpResponseRedirect(reverse('again', args=(p.id,)))
        else:
            add_reply=Reply(question=p,name=replier,count_taste=taste,count_price=price,count_service=service,count_air=air,count_cleanness=cleanness,reple=review,rep_date=timezone.now(),phonen=phone,imageR=path)
            add_reply.save()
            add_reply.update_Question()
            upload = get_uploads(self.request,field_name="image")
            if len(upload)is not 0:
                blobkey=upload[0].key()
                bkarray=str(blobkey).split("'")
                bkstr=str(bkarray[len(bkarray)-2])
                try:
                    user_photo = ImageInfo(
                        serving_url=images.get_serving_url(blobkey),
                        blob_key=blobkey,
                        content_type=upload[0].content_type,
                        original_filename=upload[0].filename
                    )
                    user_photo.put()
                    path=images.get_serving_url(blobkey)
                    revise=Reply.objects.filter(reple=review).order_by('-id')[0]
                    revise.imageR=path
                    revise.save()
                    return HttpResponseRedirect(reverse('results', args=(p.id,)))
                except:
                    revise=Reply.objects.filter(reple=review).order_by('-id')[0]
                    revise.imageR=path
                    revise.save()
                    #Reply.objects.select_for_update().filter(reple=review).update(imageR=path)
                    return HttpResponseRedirect(reverse('results', args=(p.id,)))
            else:
                return HttpResponseRedirect(reverse('results', args=(p.id,)))

class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)

def index(request):
    question_list=Question.objects.order_by('-pub_date')[:]
    question_list_t=Question.objects.order_by('-taste')[:]
    question_list_p=Question.objects.order_by('-price')[:]
    question_list_s=Question.objects.order_by('-service')[:]
    question_list_c=Question.objects.order_by('-cleanness')[:]
    question_list_a=Question.objects.order_by('-air')[:]
    question_list_r=Question.objects.order_by('-replier')[:]
    question_list_x=Question.objects.order_by('id')[:]
    replies=Reply.objects.order_by('-id')[:]
    total=[]
    star=[0.4,1.4,2.4,3.4,4.4]
    repimg={}
    for y in question_list_x:
        f=True
        for rimg in replies:
            if y.id == rimg.question_id and rimg.imageR != '/':
                    repimg[y.id]=rimg.imageR
                    f=False
                    break
        if f:
           repimg[y.id]=static('noimg.png')
    #총점순+리플정렬
    for x in question_list_x:
        all=float(x.taste+x.price+x.service+x.cleanness+x.air)
        say=""
        for rp in replies:
            if x.id==rp.question_id:
                say+=(rp.reple+", ")
        total.append([x.id,all,say,x.question_text])
    totalsorted=sorted(total,key=lambda total:-total[1] )
    #template = loader.get_template('dosirak/index.html')
    #context = RequestContext(request, {
    #    'question_list': question_list,
    #})
    context={'question_list':question_list,'taste':question_list_t,'price':question_list_p,'service':question_list_s,'clean':question_list_c,'air':question_list_a,'replier':question_list_r,'rep':replies,'sum':totalsorted,'rimg':repimg,'counter':star}
    #return HttpResponse(output+template.render(context))
    return render(request, 'dosirak/index.html', context)

#def detail(request, question_id):
#    question=get_object_or_404(Question,pk=question_id)
#    reply_list=Reply.objects.order_by('question')[:]
#    url=PhotoUploadFormHandler()
#    return render_to_response('dosirak/detail.html', context={'question':question, 'reply_list':reply_list, 'upload_url':url.get()})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'dosirak/taken.html', {'question': question})

def again(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'dosirak/error.html', {'question': question})

#def vote(request, question_id):
 #       return HttpResponseRedirect(reverse('results', args=(p.id,)))

app = webapp2.WSGIApplication([
    ('/dosirak/([^/]+)?', PhotoUploadFormHandler),
    ('/dosirak/upload_photo/', PhotoUploadHandler),
    ('/dosirak/view_photo/([^/]+)?', ViewPhotoHandler),
], debug=True)