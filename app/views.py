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
                can = Candidate.objects.get(user_id=user)
                request.session['id'] = user.id
                request.session['role'] = user.role
                request.session['firstname'] = can.firstname
                request.session['lastName'] = can.lastName
                request.session['email'] = user.email
                return redirect('index')
            else:
                message ="Password doesn't match"
                return render(request,"app/login.html",{'msg':message})
        else:
            message = "User doesn't exist"
            return render(request,"app/login.html",{'msg':message})

def ProfilePage(request,pk):
    if pk:
        user = UserMaster.objects.get(pk=pk)
        can = Candidate.objects.get(user_id=user)
        return render(request,"app/profile.html",{'user':user,'can':can})
                
def UpdateProfile(request,pk):
    user = UserMaster.objects.get(pk=pk)
    if user.role == "Candidate":
        can = Candidate.objects.get(user_id=user)
        can.state          = request.POST['state']# fristcountry belong to database and secondcountry belog to html field
        can.city           = request.POST['city']
        can.jobtype        = request.POST['jobtype']
        can.jobcategory    = request.POST['jobcategory']
        can.highestedu     = request.POST['highestedu']
        can.experience     = request.POST['experience']
        can.website        = request.POST['website']
        can.shift          = request.POST['shift']
        can.jobdescription = request.POST['jobdescription']
        can.min_salary     = request.POST['min_salary']
        can.max_salary     = request.POST['max_salary']
        can.contact        = request.POST['contact']
        can.gender         = request.POST['gender']
        can.profile_pic    = request.POST['profile_pic']
        can.save()
        url = f'/profile/{pk}' # Formatting URL
        return redirect(url)
