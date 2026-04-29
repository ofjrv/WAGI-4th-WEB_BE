from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post, Photo
from .forms import PostForm
from .forms import CommentForm

@login_required
def write(request): # write와 post_create를 하나로 통합
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
def list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post/list.html', {'posts': posts})

# 상세보기
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    context = {
        'post': post,
        'comment_form': comment_form,
    }
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
            delete_ids = request.POST.getlist('delete_images')
            Photo.objects.filter(id__in=delete_ids, post=post).delete()

            new_images = request.FILES.getlist('new_images')
            for img in new_images:
                Photo.objects.create(post=post, image=img)

            return redirect('post:detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'post/update.html', {'post_form': form, 'post': post})

@login_required
def comment_create(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post       
            comment.author = request.user 
            comment.save()
    return redirect('post:detail', pk=post.pk)

@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user) 
    else:
        post.likes.add(request.user) 
        
    return redirect('post:detail', pk=post.pk)