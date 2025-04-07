from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import LoginTable
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
        return render(request, 'viewexaminer.html')
class viewfeedback(View):
    def get(self,request):
        return render(request, 'viewfeedback.html')
class addexaminer(View):
    def get(self,request):
        return render(request, 'addexaminer.html')
    
class editexaminer(View):
    def get(self,request,id):
        return render(request, 'editexaminer.html')
    
class viewcomplaint(View):
    def get(self,request):
        return render(request, 'viewcomplaint.html')
    
class sendreply(View):
    def get(self,request):
        return render(request, 'sendreply.html')
    
class examinerviewusers(View):
    def get(self,request):
        return render(request, 'examinerviewusers.html')
    

class examinerviewcomplaint(View):
    def get(self,request):
        return render(request, 'examinerviewcomplaint.html')

class examinersendcomplaint(View):
    def get(self,request):
        return render(request, 'examinersendcomplaint.html')