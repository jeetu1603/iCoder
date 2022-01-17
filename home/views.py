from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import Post
from django.db.models import Count

# Create your views here.
# HTML Pages 
def home(request):
    posts= Post.objects.all().order_by('-views')[0:4]
    params = {"posts": posts}
    return render(request, 'home/index.html', params)

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        desc = request.POST['desc']
        if len(name)<2 or len(phone)<10 or len(email)<3 or len(desc)<4:
            messages.error(request, 'Plz fill the form correctly.')
        else:
            contact = Contact(name=name, phone=phone, email=email, content=desc)
            contact.save()
            messages.success(request, "Your message has been sent successfully.")
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if(len(query) > 78):
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsAuthor, allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, "No Search Results found. Plz refine your query.")
    params = {"allPosts": allPosts, "query": query}
    return render(request, 'home/search.html', params)

# Authentication APIs 
def handleSignUp(request):
    if request.method == "POST":
        uname = request.POST['uname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        cPassword = request.POST['cPassword']
        
        # check for errorneous input 
        if len(uname) < 6:
            messages.error(request, "Your username must be at least under 6 characters.")
            return redirect('home')
        if not uname.isalnum():
            messages.error(request, "Username should only contain letters and numbers.")
            return redirect('home')
        if password != cPassword:
            messages.error(request, "Your Passwords do not match.")
            return redirect('home')

        # create the user 
        myuser = User.objects.create_user(uname, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your iCoder account has been created successfully.")
        return redirect('home')

    else:
        return HttpResponse("Error - 404 Page Not Found")

def handleLogin(request):
    if request.method == "POST":
        # get the post parameters 
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In.")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials. Plz try again.")
            return redirect('home')

    return HttpResponse("Error - 404 Page Not Found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect("home")