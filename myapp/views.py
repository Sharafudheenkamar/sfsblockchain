from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
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
                return HttpResponse('''<script>alert("Welcome to Examiner page");window.location="/examinerdashboard"</script>''')

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
        publishDate = request.POST.get('publishDate')
        publishTime = request.POST.get('publishTime')


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
            publishDate=publishDate,
            publishTIme=publishTime,
            
        )
        # Generate Random Code and Map to All Examiners
        examiners = Examiner.objects.all()
        print(examiners)

        for examiner in examiners:
            random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            print(random_code)  # 8 char code
            QuestionPaperCode.objects.create(
                QuestionPaperID=question_paper,
                ExaminerID=examiner,
                Code=random_code
            )
            # subject = 'Secure Question Paper Access Code'
            # message = f'''
            #     Hello {examiner.Name},

            #     A new Question Paper has been assigned to you.

            #     Question: {question}

            #     Your Unique Code to Access it: {random_code}

            #     Please keep this code confidential.

            #     Regards,
            #     Admin Team
            #                 '''
            # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [examiner.Email])


        return HttpResponse('''<script>alert("Question Paper Added to Blockchain");window.location="/view_question_paper"</script>''')
# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import QuestionPaper, BlockData
from .serializers import QuestionPaperSerializer

class ActiveQuestionPaperAPIView(APIView):
    """
    API to return all active question papers.
    """

    def get(self, request):
        active_questions = []

        for qp in QuestionPaper.objects.all():
            try:
                block = BlockData.objects.get(current_hash=qp.blockchain_hash)
                block_data = block.data

                if block_data.get('status') == 'Active':
                    active_questions.append(qp)
            except BlockData.DoesNotExist:
                continue

        serializer = QuestionPaperSerializer(active_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
class ExViewQuestionPaperView(View):
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

        return render(request, 'ex_view_question_paper.html', {'questions': active_questions})
   
from django.utils.timezone import localtime, make_aware   
class UpdateQuestionPaperView(View):
    def get(self, request, id):
        qp = get_object_or_404(QuestionPaper, id=id)

        return render(request, 'update_question_paper.html', {'qp':qp})
    def post(self, request, id):
        from django.utils import timezone
        import base64
        import json
        import hashlib

        qp = get_object_or_404(QuestionPaper, id=id)
        question = request.POST.get('question')
        pdf = request.FILES.get('pdf')
        publishDate = request.POST.get('publishDate')
        publishTime = request.POST.get('publishTime')
        print(publishTime)





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
        qp.publishDate=publishDate
        qp.publishTime=publishTime
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
            print(response)
            return response

        except BlockData.DoesNotExist:
            return HttpResponse("File not found in Blockchain")

from django.http import HttpResponse
import base64
class ExDownloadQuestionPaperView(View):
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
            print(response)
            return response

        except BlockData.DoesNotExist:
            return HttpResponse("File not found in Blockchain")


from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
import base64
from django.utils import timezone
import pytz
from django.utils.timezone import localtime
from datetime import datetime
from django.utils.timezone import make_aware



class ExaminerCodeVerificationView(View):
    def get(self, request, qpid):
        return render(request, 'examiner_code_entry.html')

    def post(self, request, qpid):
        question_paper = get_object_or_404(QuestionPaper, id=qpid)
        all_codes = QuestionPaperCode.objects.filter(QuestionPaperID=question_paper)

        log_msgs = []
        valid_count = 0
        attempted_examiners = []
        print(log_msgs)

        for i in range(1, 4):
            code = request.POST.get(f'code{i}')
            examiner_name = request.POST.get(f'examiner{i}')
            attempted_examiners.append(examiner_name or '')  # Avoid None

                    # Get the examiner by name
            
            examiner = Examiner.objects.filter(LOGINID__Username=examiner_name).first()


            if examiner:
            # Match code for this examiner and this question paper
                matching_code = all_codes.filter(Code=code, ExaminerID=examiner).first()

                # matching_code = all_codes.filter(Code=code).first()


                if matching_code:
                    valid_count += 1
                    # Inside your view
                    publish_str = f"{question_paper.publishDate} {question_paper.publishTime}"
                    try:
                        publish_datetime = make_aware(datetime.strptime(publish_str, "%Y-%m-%d %H:%M:%S"))
                    except ValueError:
                        publish_datetime = None

                    if publish_datetime and timezone.now() < publish_datetime:
                        log_msgs.append(
                            f"Early access attempt by Examiner '{examiner_name}' (ID: {matching_code.ExaminerID.id})"
                        )
                else:
                        log_msgs.append(f"Wrong code '{code}' entered by Examiner: {examiner_name}")
        print(valid_count)
        if valid_count < 3:
            log_msgs.append(
                f"Failed Access Attempt with only ({valid_count}/3) valid codes by Examiners: {', '.join(attempted_examiners)} for QuestionPaperID: {qpid}"
            )
        # local_time = timezone.now().astimezone(pytz.timezone("Asia/Kolkata"))
        local_time=localtime()
        

# Get current local datetime
        current_local_datetime = localtime()

        # Get local date and time separately
        local_date = current_local_datetime.date()   # e.g., 2025-04-12
        local_time = current_local_datetime.time()   # e.g., 18:04:23

        # Print them
        print("Local Date:", local_date)
        print("Local Time:", local_time)
        publish_date=question_paper.publishDate
        publish_time=question_paper.publishTime
        print(publish_date,publish_time)
        try:
            publish_date = datetime.strptime(question_paper.publishDate, "%Y-%m-%d").date()
            publish_time = datetime.strptime(question_paper.publishTime, "%H:%M").time()
        except (ValueError, TypeError):
            publish_date = None
            publish_time = None

        print(publish_date,publish_time)
        local_datetime = datetime.combine(local_date, local_time)
        publish_datetime = datetime.combine(publish_date, publish_time)

        # Now safely compare
        if valid_count == 3 and publish_datetime <= local_datetime:
            print("Valid access after publish date and time")
            print("Valid access after publish date and time")



            print("wwwwwwwwwwwwwww#")
            log_msgs.append(
                f"Successful Question Paper Download by Examiners: {', '.join(attempted_examiners)} for QuestionPaperID: {qpid}"
            )
            for msg in log_msgs:
                c=LoginTable.objects.get(id=request.session['userid'])
                print(c)
                Log.objects.create(LOGINID=c, LogMessage=msg)

            print("hhhhhh")
            # return redirect('exdownload_question_paper', hash=question_paper.blockchain_hash)
            return render(request, 'trigger_download_and_redirect.html', {
        'download_url': reverse('exdownload_question_paper', kwargs={'hash': question_paper.blockchain_hash}),
        'redirect_url': reverse('ex_view_question_paper')  # <- change to your actual redirect view name
    })
        else:
            log_msgs.append(
                f"All codes correct but early access attempt by Examiners: {', '.join(attempted_examiners)} for QuestionPaperID: {qpid}"
            )

        for msg in log_msgs:
            c=LoginTable.objects.get(id=request.session['userid'])
            print(c)
            Log.objects.create(LOGINID=c, LogMessage=msg)

        request.session['log_alerts'] = log_msgs

        return redirect('ex_show_alert_and_redirect')



    
class ex_show_alert_and_redirect(View):
    def get(self,request):
        print("show alert and redirect")
        messages = request.session.pop('log_alerts', [])
        return render(request, 'show_alert_and_redirect.html', {'messages': messages})
    


import base64
from django.http import FileResponse, Http404
from django.utils.timezone import make_aware, localtime
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from io import BytesIO
from .models import QuestionPaper, BlockData

class QuestionPaperAccessAPIView(APIView):
    """
    Allows access to a question paper only if the current time is X minutes after publish time.
    Sends the file (decoded from base64) as a downloadable response.
    """

    def get(self, request, qpid):
        question_paper = get_object_or_404(QuestionPaper, id=qpid)
        allowed_delay_minutes = 5
        current_local_datetime = localtime()

        # Parse and localize the publish datetime
        try:
            publish_date = datetime.strptime(question_paper.publishDate, "%Y-%m-%d").date()
            publish_time = datetime.strptime(question_paper.publishTime, "%H:%M").time()
            publish_datetime_naive = datetime.combine(publish_date, publish_time)
            publish_datetime = make_aware(publish_datetime_naive, timezone=current_local_datetime.tzinfo)
        except (ValueError, TypeError):
            return Response({"error": "Invalid publish date or time format."}, status=status.HTTP_400_BAD_REQUEST)

        allowed_access_time = publish_datetime + timedelta(minutes=allowed_delay_minutes)

        if current_local_datetime < allowed_access_time:
            return Response({
                "message": "Question paper cannot be downloaded yet.",
                "wait_until": allowed_access_time.strftime("%Y-%m-%d %H:%M:%S"),
                "current_time": current_local_datetime.strftime("%Y-%m-%d %H:%M:%S")
            }, status=status.HTTP_403_FORBIDDEN)

        # Fetch file data from BlockData
        try:
            block = BlockData.objects.get(current_hash=question_paper.blockchain_hash)
            file_data_base64 = block.data.get('file_data')
            filename = block.data.get('filename', f"question_{qpid}.pdf")
            
            if not file_data_base64:
                return Response({"error": "File data not found in block."}, status=status.HTTP_404_NOT_FOUND)

            # Decode base64 and serve as file
            file_bytes = base64.b64decode(file_data_base64)
            file_stream = BytesIO(file_bytes)

            return FileResponse(file_stream, as_attachment=True, filename=filename)

        except BlockData.DoesNotExist:
            return Response({"error": "Blockchain data not found for this question paper."}, status=status.HTTP_404_NOT_FOUND)