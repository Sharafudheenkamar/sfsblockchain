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
    path('viewlogdetails',viewlogdetails.as_view(),name='viewlogdetails'),
    # path('viewquestionpaper',viewquestionpaper.as_view(),name='viewquestionpaper'),
    path('examinerviewusers',examinerviewusers.as_view(),name='examinerviewusers'),
    path('examinerviewcomplaint',examinerviewcomplaint.as_view(),name='examinerviewcomplaint'),
    path('examinersendcomplaint',examinersendcomplaint.as_view(),name='examinersendcomplaint'),
    path('publishquestionpaper/<int:id>',publishquestionpaper.as_view(),name='publishquestionpaper'),
    path('unpublishquestionpaper/<int:id>',unpublishquestionpaper.as_view(),name='unpublishquestionpaper'),
    path('view_blockchain', ViewBlockchainView.as_view(), name='view_blockchain'),
    path('add_question_paper', AddQuestionPaperView.as_view(), name='add_question_paper'),
    path('view_question_paper', ViewQuestionPaperView.as_view(), name='view_question_paper'),
    path('ex_view_question_paper', ExViewQuestionPaperView.as_view(), name='ex_view_question_paper'),
    path('update_question_paper/<int:id>', UpdateQuestionPaperView.as_view(), name='update_question_paper'),
    path('delete_question_paper/<int:id>', DeleteQuestionPaperView.as_view(), name='delete_question_paper'),
    path('download_question_paper/<str:hash>', DownloadQuestionPaperView.as_view(), name='download_question_paper'),
    path('exdownload_question_paper/<str:hash>', ExDownloadQuestionPaperView.as_view(), name='exdownload_question_paper'),
    path('ex_show_alert_and_redirect/', ex_show_alert_and_redirect.as_view(), name='ex_show_alert_and_redirect'),


    path('verify-code/<int:qpid>/', ExaminerCodeVerificationView.as_view(), name='verify_examiner_code'),
    path('download/<str:hash>/', DownloadQuestionPaperView.as_view(), name='download_question'),
    path('api/active-question-papers/', ActiveQuestionPaperAPIView.as_view(), name='active-question-papers'),

    path('api-question-paper-access/<int:qpid>/', QuestionPaperAccessAPIView.as_view(), name='question_paper_access'),


    

]