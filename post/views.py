from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, PostImage

# [추가] 회원가입에 필요한 임포트
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

# 1. 목록 (누구나)
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'list.html', {'posts': posts})

# 2. 글 쓰기 (로그인 필수)
@login_required(login_url='login')
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        images = request.FILES.getlist('images') 
        
        # 현재 로그인한 유저를 author로 저장
        post = Post.objects.create(author=request.user, title=title, content=content)
        
        for img in images:
            PostImage.objects.create(post=post, image=img)
            
        return redirect('home')
    return render(request, 'write.html')

# 3. 상세 보기 (누구나)
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'detail.html', {'post': post})

# 4. 수정 (로그인 필수 + 본인 확인)
@login_required(login_url='login')
def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    # 작성자가 아니면 튕겨내기
    if post.author != request.user:
        messages.error(request, "본인의 글만 수정할 수 있습니다.")
        return redirect('detail', post_id=post.id)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save() 
        return redirect('detail', post_id=post.pk)
    
    return render(request, 'update.html', {'post': post})

# 5. 삭제 (로그인 필수 + 본인 확인)
@login_required(login_url='login')
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.author != request.user:
        messages.error(request, "본인의 글만 삭제할 수 있습니다.")
        return redirect('detail', post_id=post.id)

    post.delete()
    return redirect('home')

# [추가] 6. 회원가입 (signup)
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # 가입 즉시 로그인 처리
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})