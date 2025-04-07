from django.urls import path
from .views import *
urlpatterns = [
    path('',indexview.as_view(),name='index'),
    path('loginview',loginview.as_view(),name='login'),
    path('logout',logout.as_view(),name='logout'),
    path('viewfeedback',viewfeedback.as_view(),name='viewfeedback'),
    path('admindashboard',admindashboard.as_view(),name='admindashboard'),
    path('examinerdashboard',examinerdashboard.as_view(),name='examinerdashboard'),
    path('viewusers',viewusers.as_view(),name='viewusers'),
    path('viewexaminer',viewexaminer.as_view(),name='viewexaminer'),
    path('addexaminer',addexaminer.as_view(),name='addexaminer'),
    path('editexaminer/<int:id>',editexaminer.as_view(),name='editexaminer'),
    path('delete_examiner/<int:id>/', delete_examiner.as_view(), name='delete_examiner'),
    path('viewcomplaint',viewcomplaint.as_view(),name='viewcomplaint'),
    path('sendreply',sendreply.as_view(),name='sendreply'),
    # path('viewquestionpaper',viewquestionpaper.as_view(),name='viewquestionpaper'),
    path('examinerviewusers',examinerviewusers.as_view(),name='examinerviewusers'),
    path('examinerviewcomplaint',examinerviewcomplaint.as_view(),name='examinerviewcomplaint'),
    path('examinersendcomplaint',examinersendcomplaint.as_view(),name='examinersendcomplaint'),


    

]