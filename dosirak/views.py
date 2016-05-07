#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from django.shortcuts import get_object_or_404,render
from django.core.urlresolvers import reverse
# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from dosirak.models import Question,Reply
from django.template import RequestContext, loader
from django.utils import timezone

def index(request):
    question_list=Question.objects.order_by('-pub_date')[:]
    #template = loader.get_template('dosirak/index.html')
    #context = RequestContext(request, {
    #    'question_list': question_list,
    #})
    context={'question_list':question_list}
    #return HttpResponse(output+template.render(context))
    return render(request, 'dosirak/index.html', context)

def detail(request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    reply_list=Reply.objects.order_by('question')[:]
    return render(request, 'dosirak/detail.html', {'question':question,'reply_list':reply_list})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'dosirak/taken.html', {'question': question})

def again(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'dosirak/error.html', {'question': question})

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    taste=request.POST.get('taste')
    service=request.POST.get('service')
    price=request.POST.get('price')
    air=request.POST.get('air')
    cleanness=request.POST.get('cleanness')
    replier=request.POST.get('replier')
    review=request.POST.get('review')
    star_set=[taste,service,price,air,cleanness]
    if star_set.__contains__('0') or (replier is None or review is None):
        return HttpResponseRedirect(reverse('again', args=(p.id,)))
    else:
        add_reply=Reply(question=p,name=replier,count_taste=taste,count_price=price,count_service=service,count_air=air,count_cleanness=cleanness,reple=review,rep_date=timezone.now())
        add_reply.save()
        add_reply.update_Question()
        return HttpResponseRedirect(reverse('results', args=(p.id,)))