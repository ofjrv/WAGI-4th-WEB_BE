from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, PostImage, Comment
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# 글 작성
@login_required(login_url='user:login')
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
    posts = Post.objects.all().order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    search_type = request.GET.get('type', 'all')

    if search_query:
        keywords = search_query.replace(',', ' ').split()
        
        query = Q()
        
        for kw in keywords:
            if search_type == 'title':
                query |= Q(title__icontains=kw)
            elif search_type == 'content':
                query |= Q(content__icontains=kw)
            elif search_type == 'all': 
                query |= Q(title__icontains=kw) | Q(content__icontains=kw)
                
        posts = posts.filter(query)

    return render(request, 'list.html', {
        'posts': posts, 
        'search_query': search_query,
        'search_type': search_type
    })


# 글 상세
def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'detail.html', {'post': post})

# 글 수정
@login_required(login_url='user:login')
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


# 글 좋아요
@login_required(login_url='user:login')
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('detail', pk=pk)

# 댓글
@login_required(login_url='user:login')
def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('detail', pk=pk)

# 대댓글
@login_required(login_url='user:login')
def add_comment(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id') # 대댓글용 부모 ID
        
        if content:
            if parent_id:
                parent_obj = get_object_or_404(Comment, pk=parent_id)
                Comment.objects.create(post=post, author=request.user, content=content, parent_comment=parent_obj)
            else:
                Comment.objects.create(post=post, author=request.user, content=content)
    return redirect('detail', pk=pk)

# 댓글 좋아요
@login_required(login_url='user:login')
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('detail', pk=comment.post.pk)