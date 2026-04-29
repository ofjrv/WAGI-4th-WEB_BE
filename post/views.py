from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, PostImage, Comment  # Comment 추가

# 계정 관련 필수 임포트
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
        
        post = Post.objects.create(author=request.user, title=title, content=content)
        
        for img in images:
            PostImage.objects.create(post=post, image=img)
            
        return redirect('home')
    return render(request, 'write.html')

# 3. 상세 보기 (누구나)
def detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'detail.html', {'post': post})

# 4. 수정 (사진 삭제 + 추가 기능 구현)
@login_required(login_url='login')
def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    if post.author != request.user:
        messages.error(request, "본인의 글만 수정할 수 있습니다.")
        return redirect('detail', post_id=post.id)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        
        # [5주차 핵심] 기존 사진 삭제 (체크박스 선택된 것들)
        delete_image_ids = request.POST.getlist('delete_images')
        for img_id in delete_image_ids:
            img = get_object_or_404(PostImage, id=img_id)
            img.delete() # 모델 삭제 시 지우님이 만든 시그널이 파일도 지워줍니다.

        # [5주차 핵심] 새로운 사진 추가
        new_images = request.FILES.getlist('images')
        for img in new_images:
            PostImage.objects.create(post=post, image=img)
            
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

# --- 5주차 추가 기능 (좋아요 / 댓글) ---

# 6. 좋아요 토글 (M:N 관계 활용)
@login_required(login_url='login')
def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user) # 이미 눌렀다면 취소
    else:
        post.likes.add(request.user)    # 안 눌렀다면 추가
    return redirect('detail', post_id=post_id)

# 7. 댓글 작성 (1:N 관계 활용)
@login_required(login_url='login')
def comment_write(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=post_id)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id') # 대댓글일 경우 부모 ID가 넘어옴

        if content:
            comment = Comment(post=post, author=request.user, content=content)
            if parent_id: # 부모 ID가 있다면 대댓글로 저장
                comment.parent_id = parent_id
            comment.save()
            
    return redirect('detail', post_id=post_id)

# 8. 댓글 삭제 (본인 확인)
@login_required(login_url='login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post_id = comment.post.id
    if comment.author == request.user:
        comment.delete()
    else:
        messages.error(request, "본인 댓글만 삭제 가능합니다.")
    return redirect('detail', post_id=post_id)

# --- 기존 계정 관리 함수 ---
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')