from django.urls import reverse
from django.shortcuts import render#render HTMP templates
from django.http import HttpResponse,HttpResponseRedirect#return HTTP response
from .models import Candidate #Candidate model from the current application
from OTSapp.models import *#importing all models in this app
import random# used for generating random numbers or making random selections


def welcome(request):
    return render(request, 'welcome.html')

def candidateRegistrationForm(request):
    return render(request, 'registration_form.html')
    
def candidateRegistration(request):
    userStatus = 3  # Initialize userStatus and context
    context = {}
    
    if request.method == "POST":
        username = request.POST['username']
        # Check if the user already exists
        if(len( Candidate.objects.filter(username=username))):
            userStatus = 1
        else:
            candidate = Candidate()
            candidate.username = username
            candidate.password = request.POST['password']
            candidate.name = request.POST['name']
            candidate.save()
            userStatus = 2
    else:
        userStatus=3
    context={
            'userStatus':userStatus
    }
    
    res=render(request,'registration.html',context)
    return res
    
  
def loginView(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        candidate=Candidate.objects.filter(username=username,password=password)
        if len(candidate)==0:
            loginError='Invalid username or password '
            res=render(request, 'login.html',{'loginError':loginError})
        else:
            #login success
            request.session['username']=candidate[0].username
            request.session['name']=candidate[0].name 
            res = HttpResponseRedirect(reverse('OTSapp:home')) 
    else:        
       res=render(request, 'login.html')
    return res
def candidateHome(request):#getting error   for return request home.html ,will be fix  on next lecture
    if 'username' not in request.session.keys():
        res=render(request,"login.html")
    else:
        res=render(request,"home.html")
    return res
      
  
def testPaper(request):
    if 'name' not in request.session.keys():
        res=render(request,"login.html")
    #fetch question from database table
    n=int(request.GET['n'])
    question_pool=list(Questions.objects.all()) 
    random.shuffle(question_pool)
    questions_list=question_pool[:n]
    context={'questions':questions_list}
    res=render( request,'test_paper.html',context)
    return res
    
def calculateTestResult(request):
    if "name" not in request.session.keys():
        res= HttpResponseRedirect(reverse('OTSapp:login'))
        
    total_attempt=0
    total_right=0
    total_wrong=0
    qid_list=[]
    for k in request.POST:
        if k.startswith('qno'):
            qid_list.append(request.POST[k])

    
    for n in qid_list:
        question=Questions.objects.get(qid=n)
        try:
            if question.ans==request.POST['q'+str(n)]:
                total_right+=1
            else:
                total_wrong+=1
            total_attempt+=1
        except:
            pass
        else:
            points=(total_attempt-total_wrong)/len(qid_list)*10
    #store result in DB table
    result=Result()
    result.username=Candidate.objects.get(username=request.session['username'])
    result.attempt=total_attempt
    result.right=total_right
    result.wrong=total_wrong
    result.point=points
    result.save()
    #update Candidate table
    candidate=Candidate.objects.get(username=request.session['username'])
    candidate.test_attempted=1
    candidate.points=(candidate.points*(candidate.test_attempted-1)+points)/candidate.test_attempted
    candidate.save()
    return HttpResponseRedirect(reverse('OTSapp:result'))
def TestResultHistory(request): 
    if "name" not in request.session.keys():
        res= HttpResponseRedirect(reverse('OTSapp:login'))
    candidate=Candidate.objects.filter(username=request.session['username'])
    results=Result.objects.filter(username_id=candidate[0].username)
    context={'candidate_info':candidate[0],'result':results}
    res=render(request,'candidate_history.html',context)
    return res
    
    
def showTestResult(request):
    if "name" not in request.session.keys():
        res= HttpResponseRedirect(reverse('OTSapp:login'))
    #fetch latest result from result table
    result=Result.objects.filter(resultid=Result.objects.latest('date','time').resultid,  username_id=request.session['username'])
    context={'result':result}
    res=render(request,'show_result.html',context)
    return res
def logoutView(request):
    if 'name'  in request.session.keys():
        del request.session['username']
        del request.session['name']
    res=render(request,"login.html")
    return res