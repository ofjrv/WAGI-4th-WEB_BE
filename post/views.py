from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Photo
from .forms import PostForm

@login_required
def post_write(request): # write와 post_create를 하나로 통합
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid(): # 1: 데이터 유효성 검사
            post = form.save(commit=False) 
            post.author = request.user # 2: 작성자 자동 할당
            post.save()
            
            # 다중 이미지 처리 로직
            images = request.FILES.getlist('images')
            for img in images:
                Photo.objects.create(post=post, image=img)
                
            return redirect('post:detail', pk=post.pk)
    else:
        form = PostForm()
    
    return render(request, 'post/write.html', {'form': form})

# 목록 보기
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post/list.html', {'posts': posts})

# 상세보기
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post/detail.html', {'post': post})

@login_required
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 작성자 본인 확인 로직
    if post.author != request.user:
        return HttpResponseForbidden("본인의 글만 수정할 수 있습니다.")

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'post/update.html', {'form': form, 'post': post})