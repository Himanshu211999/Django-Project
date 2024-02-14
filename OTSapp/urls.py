
from django.urls import path
from OTSapp.views import *
app_name = 'OTSapp'
urlpatterns = [
    path('', welcome),
    path('new-candidate',candidateRegistrationForm,name='Registration'),
    path('store-candidate',candidateRegistration,name='storeCandidate'),
    path('login',loginView,name='login'),
    path('home',candidateHome,name='home'),
    path('test-paper',testPaper,name='testPaper'),
    path('calculate-result',calculateTestResult,name='calculateTest'),
    path('test-history',TestResultHistory,name='testHistory'),
    path('result',showTestResult,name='result'),
    path('logout',logoutView,name='logout'),
]
