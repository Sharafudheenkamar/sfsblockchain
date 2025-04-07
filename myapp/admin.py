from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(LoginTable)
admin.site.register(UserTable)
admin.site.register(Examiner)
admin.site.register(Complaint)
admin.site.register(Feedback)
admin.site.register(QuestionPaper)
admin.site.register(QuestionPaperCode)
admin.site.register(Log)