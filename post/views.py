from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostImage, Comment
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


# 글 작성
@login_required(login_url='login')
def write(request):
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

#글 수정
@login_required(login_url='login')
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect('home')

    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        # 기존 이미지 삭제
        delete_image_ids = request.POST.getlist('delete_images')
        for img_id in delete_image_ids:
            image = get_object_or_404(PostImage, pk=img_id)
            image.delete()

        # 새로운 이미지 추가
        images = request.FILES.getlist('images')
        for img in images:
            PostImage.objects.create(post=post, image=img)

        return redirect('detail', pk=post.pk)

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


# 좋아요
@login_required(login_url='login')
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('detail', pk=pk)

# 댓글
@login_required(login_url='login')
def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('detail', pk=pk)