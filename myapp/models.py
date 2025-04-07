from django.db import models

# Create your models here.
class LoginTable(models.Model):
    Username = models.CharField(max_length=100, null=True, blank=True)
    Password = models.CharField(max_length=100, null=True, blank=True)
    Type = models.CharField(max_length=100, null=True, blank=True)

class UserTable(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    Phone =models.IntegerField(null=True, blank=True)

class Examiner(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Name = models.CharField(max_length=100, null=True, blank=True)
    Email = models.CharField(max_length=100, null=True, blank=True)
    Phone =models.IntegerField(null=True, blank=True)

class Complaint(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Comp = models.CharField(max_length=100, null=True, blank=True)
    Reply = models.CharField(max_length=100, null=True, blank=True)
    ComplaintDateTime = models.DateTimeField(auto_now_add=True,null=True, blank=True)

class Feedback(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    Feed = models.CharField(max_length=100, null=True, blank=True)
    FeedbackDateTime = models.DateTimeField(auto_now_add=True,null=True, blank=True)


class QuestionPaper(models.Model):
    Question = models.CharField(max_length=100, null=True, blank=True)
    PublishDateTime=models.DateTimeField(null=True,blank=True)


class QuestionPaperCode(models.Model):
    QuestionPaperID=models.ForeignKey(QuestionPaper,on_delete=models.CASCADE,null=True,blank=True)
    ExaminerID=models.ForeignKey(Examiner,on_delete=models.CASCADE,null=True,blank=True)
    Code = models.CharField(max_length=100, null=True, blank=True)

class Log(models.Model):
    LOGINID=models.ForeignKey(LoginTable,on_delete=models.CASCADE,null=True,blank=True)
    LogMessage = models.CharField(max_length=100, null=True, blank=True)
    LogDateTime=models.DateTimeField(auto_now_add=True,null=True, blank=True)