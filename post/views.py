from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from .models import Post, Photo, Comment, Reply
from .forms import PostForm, CommentForm, ReplyForm

@login_required
def write(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            images = request.FILES.getlist('images')
            for img in images:
                Photo.objects.create(post=post, image=img)
            return redirect('post:detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'post/write.html', {'form': form})

def list(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', '전체')

    if query:
        keywords = [k.strip() for k in query.replace(',', ' ').split() if k.strip()]
        q_obj = Q()
        for keyword in keywords:
            if search_type == '제목':
                q_obj |= Q(title__icontains=keyword)
            elif search_type == '내용':
                q_obj |= Q(content__icontains=keyword)
            else:
                q_obj |= Q(title__icontains=keyword) | Q(content__icontains=keyword)

        posts = Post.objects.filter(q_obj).distinct().order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')
    return render(request, 'post/list.html', {'posts': posts, 'query': query, 'search_type' : search_type})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    reply_form = ReplyForm()
    context = {
        'post': post,
        'comment_form': comment_form,
        'reply_form': reply_form,
    }
    return render(request, 'post/detail.html', context)

@login_required
def update(request, pk):
    post = get_object_or_404(Post, pk=pk)
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

# 대댓글 작성
@login_required
def reply_create(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.comment = comment
            reply.author = request.user
            reply.save()
    return redirect('post:detail', pk=comment.post.pk)

# 댓글 좋아요 
@login_required
def comment_like(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)
    return redirect('post:detail', pk=comment.post.pk)