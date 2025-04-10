from django.urls import path
from .views import *
urlpatterns = [
    path('',indexview.as_view(),name='index'),
    path('loginview',loginview.as_view(),name='login'),
    path('logout/',logout.as_view(),name='logout'),
    path('viewfeedback',viewfeedback.as_view(),name='viewfeedback'),
    path('admindashboard',admindashboard.as_view(),name='admindashboard'),
    path('examinerdashboard',examinerdashboard.as_view(),name='examinerdashboard'),
    path('viewusers',viewusers.as_view(),name='viewusers'),
    path('viewexaminer',viewexaminer.as_view(),name='viewexaminer'),
    path('addexaminer',addexaminer.as_view(),name='addexaminer'),
    path('editexaminer/<int:id>',editexaminer.as_view(),name='editexaminer'),
    path('deleteexaminer/<int:id>/', deleteexaminer.as_view(), name='deleteexaminer'),
    path('viewcomplaint',viewcomplaint.as_view(),name='viewcomplaint'),
    path('sendreply/<int:id>/',sendreply.as_view(),name='sendreply'),
    # path('viewquestionpaper',viewquestionpaper.as_view(),name='viewquestionpaper'),
    path('examinerviewusers',examinerviewusers.as_view(),name='examinerviewusers'),
    path('examinerviewcomplaint',examinerviewcomplaint.as_view(),name='examinerviewcomplaint'),
    path('examinersendcomplaint',examinersendcomplaint.as_view(),name='examinersendcomplaint'),

    path('view_blockchain', ViewBlockchainView.as_view(), name='view_blockchain'),
    path('add_question_paper', AddQuestionPaperView.as_view(), name='add_question_paper'),
    path('view_question_paper', ViewQuestionPaperView.as_view(), name='view_question_paper'),
    path('update_question_paper/<int:id>', UpdateQuestionPaperView.as_view(), name='update_question_paper'),
    path('delete_question_paper/<int:id>', DeleteQuestionPaperView.as_view(), name='delete_question_paper'),
    path('download_question_paper/<str:hash>', DownloadQuestionPaperView.as_view(), name='download_question_paper'),




    

]