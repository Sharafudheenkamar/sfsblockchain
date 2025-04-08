from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import *

# Create your views here.
class indexview(View):
    def get(self, request):
        return render(request, 'index.html')

class logout(View):
    def get(self, request):
        if 'userid' in request.session:
            del request.session['userid']
        return HttpResponse('''<script>alert("You have been logged out successfully");window.location="/"</script>''')

    def post(self, request):
        if 'userid' in request.session:
            del request.session['userid']
        return HttpResponse('''<script>alert("You have been logged out successfully");window.location="/"</script>''')



class loginview(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self, request):
        username = request.POST.get('Username')
        password = request.POST.get('Password')
        print(username,password)


        try:
            login_obj = LoginTable.objects.get(Username=username, Password=password)
            request.session['userid'] = login_obj.id

            if login_obj.Type == "admin":
                return HttpResponse('''<script>alert("Welcome to Admin page");window.location="/admindashboard"</script>''')
            elif login_obj.Type == "examiner":
                return HttpResponse('''<script>alert("Welcome to Park Assistant page");window.location="/examinerdashboard"</script>''')

        except LoginTable.DoesNotExist:
            return HttpResponse('''<script>alert("Invalid password");window.location="/"</script>''')    


    
class admindashboard(View):
    def get(self, request):
        return render(request, 'admindashboard.html')
    
class examinerdashboard(View):
    def get(self, request):
        return render(request, 'examinerdashboard.html')
class viewusers(View):
    def get(self,request):
        return render(request, 'viewusers.html')
    
class viewexaminer(View):
    def get(self,request):
        examiners=Examiner.objects.all()
        return render(request, 'viewexaminer.html',{'examiners':examiners})
class viewfeedback(View):
    def get(self,request):
        users=Feedback.objects.all()
        return render(request, 'viewfeedback.html',{'users':users})
class addexaminer(View):
    def get(self,request):
        return render(request, 'addexaminer.html')
    def post(self,request):
        Name=request.POST.get('Name')
        Email=request.POST.get('Email')
        Password=request.POST.get('Password')
        Phone=request.POST.get('Phone')
        Type='examiner'
        try:
        # Create login entry
            lo = LoginTable.objects.create(Username=Email, Password=Password, Type=Type)

            # Create examiner entry with foreign key to LoginTable
            user = Examiner.objects.create(Name=Name, Email=Email, Phone=Phone, LOGINID=lo)

            return HttpResponse('''<script>alert("Examiner Added Successfully");window.location="/viewexaminer"</script>''')

        except Exception as e:
            return HttpResponse(f'''<script>alert("Error: {str(e)}");window.location="/addexaminer"</script>''')
class editexaminer(View):
    def get(self,request,id):
        examiner=Examiner.objects.get(id=id)
        return render(request, 'editexaminer.html',{'examiner':examiner})
    def post(self,request,id):
        Name=request.POST.get('Name')
        Email=request.POST.get('Email')
        Password=request.POST.get('Password')
        Username=request.POST.get('Username')
        Phone=request.POST.get('Phone')
        examiner = Examiner.objects.get(id=id)  # Fetch examiner
        examiner.Name = Name
        examiner.Email = Email
        examiner.Phone = Phone
        examiner.save()

        login = LoginTable.objects.get(id=examiner.LOGINID.id)  # Fetch related Login
        login.Username = Username
        login.Password = Password
        login.save()

        return HttpResponse('''<script>alert("Examiner Updated Successfully");window.location="/viewexaminer"</script>''')
class deleteexaminer(View):
    def get(self,request,id):
        examiner=Examiner.objects.get(id=id)
        log=LoginTable.objects.get(id=examiner.LOGINID.id) 
        log.delete()
        return HttpResponse('''<script>alert("Examiner Deleted Successfully");window.location="/viewexaminer"</script>''')



    
class viewcomplaint(View):
    def get(self,request):
        comp=Complaint.objects.all()
        return render(request, 'viewcomplaint.html',{'comp':comp})
    
class sendreply(View):
    def get(self,request,id):
        return render(request, 'sendreply.html',{'compid':id})
    def post(self,request,id):
        print(id)
        reply=request.POST.get('reply')
        comp=Complaint.objects.get(id=id)
        comp.Reply=reply
        comp.save()
        return redirect('viewcomplaint')
    
class examinerviewusers(View):
    def get(self,request):
        return render(request, 'examinerviewusers.html')
    

class examinerviewcomplaint(View):
    def get(self,request):
        return render(request, 'examinerviewcomplaint.html')

class examinersendcomplaint(View):
    def get(self,request):
        return render(request, 'examinersendcomplaint.html')
    
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from .models import QuestionPaper, Examiner, QuestionPaperCode
import hashlib
import json


import base64

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.timestamp = str(timezone.now())
        self.data = data  # Contains base64 PDF
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = str(self.index) + self.timestamp + json.dumps(self.data) + self.previous_hash
        return hashlib.sha256(block_string.encode()).hexdigest()

# Blockchain Structure
from .models import BlockData

class Blockchain:
    def create_genesis_block(self):
        return Block(0, {"info": "Genesis Block"}, "0")

    def latest_block(self):
        return BlockData.objects.latest('index')

    def add_block(self, new_data):
        latest_block = self.latest_block()

        new_index = latest_block.index + 1
        new_timestamp = timezone.now()
        previous_hash = latest_block.current_hash

        block_string = str(new_index) + str(new_timestamp) + json.dumps(new_data) + previous_hash
        current_hash = hashlib.sha256(block_string.encode()).hexdigest()

        BlockData.objects.create(
            index=new_index,
            timestamp=new_timestamp,
            data=new_data,
            previous_hash=previous_hash,
            current_hash=current_hash
        )


# Blockchain Instance
blockchain = Blockchain()

import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.utils.dateparse import parse_datetime
# Add Question Paper View
class AddQuestionPaperView(View):
    def get(self, request):
        return render(request, 'add_question_paper.html')

    def post(self, request):
        question = request.POST.get('question')
        pdf = request.FILES['pdf']
        publish_datetime = request.POST.get('publish_datetime')
        publish_datetime = parse_datetime(publish_datetime)

        pdf_content = base64.b64encode(pdf.read()).decode('utf-8')  # File stored in Blockchain

        block_data = {
            "question": question,
            "file_data": pdf_content,
            "status": "Active"
        }

        blockchain.add_block(block_data)

        latest_block = BlockData.objects.latest('index')

        question_paper=QuestionPaper.objects.create(
            Question=question,
            blockchain_hash=latest_block.current_hash,
            PublishDateTime=publish_datetime,
        )
                # Generate Random Code and Map to All Examiners
        examiners = Examiner.objects.all()

        for examiner in examiners:
            random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))  # 8 char code
            QuestionPaperCode.objects.create(
                QuestionPaperID=question_paper,
                ExaminerID=examiner,
                Code=random_code
            )
            subject = 'Secure Question Paper Access Code'
            message = f'''
                Hello {examiner.Name},

                A new Question Paper has been assigned to you.

                Question: {question}

                Your Unique Code to Access it: {random_code}

                Please keep this code confidential.

                Regards,
                Admin Team
                            '''
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [examiner.Email])


        return HttpResponse('''<script>alert("Question Paper Added to Blockchain");window.location="/view_question_paper"</script>''')
# View Question Paper
class ViewQuestionPaperView(View):
    def get(self, request):
        active_questions = []

        for qp in QuestionPaper.objects.all():
            try:
                block = BlockData.objects.get(current_hash=qp.blockchain_hash)
               
                block_data = block.data  
                
                if block_data.get('status') == 'Active':
                    active_questions.append(qp)
            except BlockData.DoesNotExist:
                pass  # Ignore if block not found

        return render(request, 'view_question_paper.html', {'questions': active_questions})
    
class UpdateQuestionPaperView(View):
    def get(self, request, id):
        qp = get_object_or_404(QuestionPaper, id=id)
        return render(request, 'update_question_paper.html', {'qp': qp})

    def post(self, request, id):
        from django.utils import timezone
        import base64
        import json
        import hashlib

        qp = get_object_or_404(QuestionPaper, id=id)
        question = request.POST.get('question')
        pdf = request.FILES.get('pdf')
        publish_datetime = request.POST.get('publish_datetime')
        publish_datetime = parse_datetime(publish_datetime)

        # Handle file (New or Old)
        if pdf:
            pdf_content = base64.b64encode(pdf.read()).decode('utf-8')
        else:
            # Get old file_data from BlockData DB
            try:
                old_block = BlockData.objects.get(current_hash=qp.blockchain_hash)
                old_data = old_block.data
                pdf_content = old_data.get('file_data')
            except BlockData.DoesNotExist:
                return HttpResponse(f'''<script>alert("Old File Not Found in Blockchain!");window.location="/update_question_paper/{id}"</script>''')

        # Prepare new block data
        block_data = {
            "question": question,
            "file_data": pdf_content,
            "status": "Active"
        }

        latest_block = BlockData.objects.latest('index')

        new_index = latest_block.index + 1
        new_timestamp = timezone.now()
        new_previous_hash = latest_block.current_hash
        new_current_hash = hashlib.sha256(
            (str(new_index) + str(new_timestamp) + json.dumps(block_data) + new_previous_hash).encode()
        ).hexdigest()

        # Save New Block in DB
        BlockData.objects.create(
            index=new_index,
            timestamp=new_timestamp,
            data=block_data,
            previous_hash=new_previous_hash,
            current_hash=new_current_hash,
        )

        # Update Question Paper Table
        qp.Question = question
        qp.blockchain_hash = new_current_hash
        qp.PublishDateTime = publish_datetime
        qp.save()

        return HttpResponse('''<script>alert("Question Paper Updated in Blockchain");window.location="/view_question_paper"</script>''')
class DeleteQuestionPaperView(View):
    def get(self, request, id):
        qp = get_object_or_404(QuestionPaper, id=id)

        block_data = {
            "question": qp.Question,
            "file_data": "Deleted",   # Indicating file deleted
            "status": "Inactive"
        }

        blockchain.add_block(block_data)

        latest_block = BlockData.objects.latest('index')

        qp.status = 'Inactive'
        qp.blockchain_hash = latest_block.current_hash
        qp.save()

        return HttpResponse('''<script>alert("Question Paper Deleted in Blockchain");window.location="/view_question_paper"</script>''')

# View Blockchain Database
class ViewBlockchainView(View):
    def get(self, request):

        active_blocks = BlockData.objects.all().order_by('index')
        return render(request, 'view_blockchain.html', {'blockchain': active_blocks})
from django.http import HttpResponse
import base64
class DownloadQuestionPaperView(View):
    def get(self, request, hash):
        import base64
        import json
        from django.http import HttpResponse
        from django.shortcuts import get_object_or_404

        # Search in BlockData Table
        try:
            block = BlockData.objects.get(current_hash=hash)
            block_data = block.data
            file_data = block_data.get('file_data')

            if not file_data:
                return HttpResponse("File data missing in Blockchain")

            file_content = base64.b64decode(file_data)

            response = HttpResponse(file_content, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="question_paper.pdf"'
            return response

        except BlockData.DoesNotExist:
            return HttpResponse("File not found in Blockchain")
