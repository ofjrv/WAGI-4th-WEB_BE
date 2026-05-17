from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Image, Comment, CommentLike
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
# Create your views here.
@login_required
def write(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        post = Post.objects.create(
            author = request.user,
            title = title, 
            content = content
        )
        images = request.FILES.getlist('images')

        for img in images:
            Image.objects.create(
                post = post,
                image = img
            )
        
        return redirect('home')
    
    return render(request, 'write.html')

def home(request):
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')

    posts = Post.objects.all().order_by('-id')

    if query:
        words = query.replace(',', ' ').split()

        q_objects = Q()

        for word in words:

            if search_type == 'title':
                q_objects |= Q(title__icontains=word)

            elif search_type == 'content':
                q_objects |= Q(content__icontains=word)

            else:
                q_objects |= (
                    Q(title__icontains=word) |
                    Q(content__icontains=word)
                )

        posts = Post.objects.filter(q_objects).distinct().order_by('-id')

    return render(request, 'list.html', {
        'posts': posts,
        'query': query,
        'search_type': search_type
    })

def detail(request, post_id):
    post = Post.objects.get(id = post_id)

    comments = post.comment_set.filter(parent=None)

    return render(request, 'detail.html', {
        'post' : post,
        'comments' : comments,
    })
    

@login_required
def update(request, id):
    post = Post.objects.get(id = id)

    if post.author != request.user:
        return HttpResponseForbidden("수정 권한 없음")

    if request.method == "POST":
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        delete_images = request.POST.getlist('delete_images')

        for image_id in delete_images:
            image = Image.objects.get(id=image_id)
            image.delete()

        new_images = request.FILES.getlist('new_images')

        for img in new_images:
            Image.objects.create(
                post=post,
                image=img
            )

        return redirect(f'/detail/{post.id}/')
    
    return render(request, 'update.html', {'post' : post})

@login_required
def create_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)

        parent_id = request.POST.get('parent_id')

        parent = None
        if parent_id:
            parent = Comment.objects.get(id=parent_id)

        Comment.objects.create(
            post=post,
            author=request.user,
            content=request.POST.get('content'),
            parent=parent
        )

    return redirect(f'/detail/{post_id}/')


@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)

    else:
        post.likes.add(request.user)

    return redirect(f'/detail/{post_id}/')

@login_required
def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(
        user=request.user,
        comment=comment
    )

    if not created:
        like.delete()

    return redirect('detail', post_id=comment.post.id)