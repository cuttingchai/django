from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from .models import Post,Comment
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

def posts(request):
    posts = Post.objects.order_by('created_date')
    return render(request, 'post_list.html', {'posts':posts,})

def post_detail(request, postid):
    post = Post.objects.get(id=postid)
    comments = Comment.objects.filter(post=post)

    return render(request, 'post_detail.html', {'post': post,'comments':comments,'user':request.user})

def logout_blog(request):
    if request.user.is_authenticated():
        logout(request)
        return redirect('/posts/')
    else:
        return HttpResponseRedirect('/login')

def new_post(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            author = request.user
            text = request.POST.get('text')
            title = request.POST.get('title')
            post = Post.objects.create(author=author,text=text,title=title)
            post.save()
            return redirect('/posts/')
        else:
            return render(request, 'post_add.html')
    else:
        return HttpResponseRedirect('/login')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        user = User.objects.create(
            first_name = name,
            username = username,
            )
        user.set_password(password)
        user.save()

        user = authenticate(username = username, password = password)
        login(request, user)
        return redirect('/posts/')
    else:
        return render(request,'register.html')   

def login_blog(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user :
            if user.is_active:
                login(request,user)
                return redirect('/posts/')
            else:
                return HttpResponse('Disabled Account')
        else:
            return HttpResponse("Invalid Login details.Are you trying to Sign up?")
    else:
        return render(request,'login.html')


def add_comment(request, pid):
    if request.user.is_authenticated():
        if request.method == 'POST':
            post = Post.objects.get(id=pid) 
            text = request.POST.get('text')
            comment = Comment.objects.create(post=post,author=request.user,text=text)
            comment.save()
            return HttpResponseRedirect('/post_detail/'+str(pid))
    else:
        return HttpResponseRedirect('/login')

'''
if request.method == "POST":
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        author = Author.objects.create(name=request.user.username, email=request.user.email)
        author.save()
        comment.author = author
        comment.post = post
        comment.post_date = timezone.now()
        comment.save()
        return redirect('/posts/'+pk+'/')
    
else:
    form = CommentForm()
if not request.user.is_authenticated():
    form = ''
comments = Comment.objects.order_by('post_date')    
'''
'''
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            author = Author.objects.create()
            author.name = request.user
            author.email = ""
            post.author = author
            post.published_date = timezone.now()
            post.save()
            return redirect('/posts/')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_edit.html', {'form': form})
'''
