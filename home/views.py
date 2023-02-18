from django.shortcuts import render,HttpResponse,redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from blog.models import Post



# password for testcase in admin user---> dipdas123

# Create your views here.
def index(request):
    # return HttpResponse('This is home page.')
    # messages.success(request, "this is a test message.")
    if request.user.is_anonymous:
        return render(request, 'home/index.html')
    return render(request, 'home/index.html')

def signupUser(request):
    
    if request.method=="POST":
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']

        #Check for errorneous inputs
        if (len(username)>10):
            messages.error(request, "Username should be under 10 characters and more than 5 characters!")
            return redirect('/signup')

        if not username.isalnum():
            messages.error(request, "Username should only contain letters and numbers!")
            return redirect('/signup')
        
        if len(password)<8:
            messages.error(request, "Your password should contain minimum 8 characters!")
            return redirect('/signup')

        if (password!=password2):
            messages.error(request, "Enter same password!")
            return redirect('/signup')

        #creating user
        myuser= User.objects.create_user(username=username, email=email, password=password)
        myuser.first_name= firstname
        myuser.last_name= lastname

        myuser.save()
        messages.success(request, "Your account has been successfully created.")
        return redirect('/login')
    
    # else:
    #     return HttpResponse("404- Not found")

    return render(request, 'home/signup.html')
    

def loginUser(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        # check if the user has entered corrected credentials
        user=authenticate(username=username , password=password)
        if user is not None:
            # A backend authenticated the credentials
            login(request, user)
            # messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            # No backend authenticated the credentials
            messages.error(request, "Invalid credentials")
            return redirect('/')

    return render(request, 'home/login.html')

    # return HttpResponse("404- Not found")

def logoutUser(request):
    logout(request)
    # messages.success(request, "Successfully Logged Out")
    return redirect("/")

def about(request):
    # return HttpResponse('This is about page.')
    return render(request, 'home/about.html')
        


def contact(request):
    # return HttpResponse('This is contact page.')
    if request.method=="POST":
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        desc=request.POST.get('desc')
        feedback=request.POST.get('feedback')
        contact= Contact(firstname=firstname, lastname=lastname, email= email, phone=phone, desc=desc, feedback=feedback, date=datetime.today())
        contact.save()
        messages.success(request, 'Your form has been submitted!')

    return render(request, 'home/contact.html')


def search(request):
    # return HttpResponse('This is search page.')
    query= request.GET['query']
    if len(query)>80:
        allposts= Post.objects.none()
    else:
        # allposts= Post.objects.all()
        allpostsTitle= Post.objects.filter(title__icontains=query)
        allpostsContent= Post.objects.filter(content__icontains=query)
        allpostsAuthor= Post.objects.filter(author__icontains=query)
        allposts= allpostsTitle.union(allpostsContent).union(allpostsAuthor)

    if allposts.count()==0:
        messages.warning(request, "No search result found. Please refine your query.")
    params={'allposts':allposts, 'query':query}
    return render(request, 'home/search.html', params)


def kolkata(request):
    # return HttpResponse('This is kolkata page.')
    return render(request, 'home/kolkata.html')



def payment(request):
    return render(request, 'home/payment.html')