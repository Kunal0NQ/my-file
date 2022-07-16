from email import message
from django.shortcuts import redirect, render
from app.models import Candidate, UserMaster
from random import randint


# Create your views here.
def IndexPage(request):
    return render(request,"app/index.html")

def SgPage(request):
    return render(request,"app/signup.html")

def RegisterUser(request):
    if request.POST['role']=="Candidate":
        role = request.POST['role']
        fname = request.POST['firstname']
        lname = request.POST['lastName']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

# Registration
        user = UserMaster.objects.filter(email=email)
# server side validation
        if user:
            message = "User already Exist"
            return render (request,"app/signup.html",{'msg':message})
        else:
            if password == cpassword:
                otp = randint(100000,999999)
                newuser = UserMaster.objects.create(role=role,otp=otp,email=email,password=password)
                newcand = Candidate.objects.create(user_id=newuser,firstname=fname,lastName=lname)
                return render(request,"app/otp.html",{'email':email})
            else:   
                 print("Company Registration")    

def OTPPage(request):
    return render(request,"app/otp.html")


def OtpVerify(request):
    email = request.POST['email']
    otp = int(request.POST['otp'])

    user = UserMaster.objects.get(email=email)

    if user:
        if user.otp == otp:
            message = "OTP Verify Successfully"
            return render(request,"app/login.html",{'msg':message})
        else:
            message = "Otp is incorrect"
            return render(request,"app/otp.html",{'msg':message})
    else:
        return render(request,"app/signup.html")

def LoginPage(request):
    return render(request,"app/login.html")

def LoginUser(request):
    if request.POST['role']=="Candidate":
        email = request.POST['email']
        password = request.POST['password']

        user = UserMaster.objects.get(email=email)
        if user:
            if user.password==password and user.role=="Candidate":
                can = Candidate.object.get(user_id=user)
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['firstname'] = user.firstname
                request.session['lastName'] = user.lastName
                request.session['email'] = user.email
                return redirect('index')
            else:
                message ="Password doesnot match"
                return render(request,"app/login.html",{'msg':message})
        else:
            message = "User not found"

