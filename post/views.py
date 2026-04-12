from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostImage
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

# 글 작성
def write(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        images = request.FILES.getlist('images')

        post = Post.objects.create(
            author=request.user,
            title=title,
            content=content
        )

        for img in images:
            PostImage.objects.create(post=post, image=img)

        return redirect('home')

    return render(request, 'write.html')



# 글 목록
def home(request):
    posts = Post.objects.all()
    return render(request, 'list.html', {'posts': posts})


# 글 상세
def detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'detail.html', {'post': post})

#글 수정
def update(request, pk):
    post = Post.objects.get(pk=pk)

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('detail', id=post.id)

    return render(request, 'update.html', {'post': post})

# 회원가입
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')


# 로그인
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


# 로그아웃
def user_logout(request):
    logout(request)
    return redirect('home')


# 글 작성
def write(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        images = request.FILES.getlist('images')

        post = Post.objects.create(
            author=request.user,
            title=title,
            content=content
        )

        for img in images:
            PostImage.objects.create(post=post, image=img)

        return redirect('home')

    return render(request, 'write.html')


# 글 목록
def home(request):
    posts = Post.objects.all()
    return render(request, 'list.html', {'posts': posts})


# 글 상세
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'detail.html', {'post': post})


# 글 수정
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 작성자만 수정 가능
    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('detail', pk=post.pk)

    return render(request, 'update.html', {'post': post})