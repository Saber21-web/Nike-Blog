from django.shortcuts import render, redirect
from .models import Post, Category, Like, Comment
import re
from .forms import PostForm
from django.db.models import Q
from datetime import datetime


def home(request):
    year, month = datetime.now().year, datetime.now().strftime('%m')
    q = request.GET.get('q', '')
    category = request.GET.get('category', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    date_from_year, date_from_month = None, None
    date_to_year, date_to_month = None, None

    if date_from:
        date_from_year, date_from_month = map(int, date_from.split('-'))
    if date_to:
        date_to_year, date_to_month = map(int, date_to.split('-'))

    print('Информация:', date_from, date_to, category)

    if q:
        posts = Post.objects.filter(title__icontains=q).order_by('-id')
    elif date_from or date_to or category:
        filter_conditions = Q()
        if date_from_year and date_from_month:
            filter_conditions &= Q(date__year__gte=date_from_year) & Q(date__month__gte=date_from_month)
        if date_to_year and date_to_month:
            filter_conditions &= Q(date__year__lte=date_to_year) & Q(date__month__lte=date_to_month)
        if category:
            filter_conditions &= Q(category__name__icontains=category)
        
        posts = Post.objects.filter(filter_conditions).order_by('-id')
    else:
        posts = Post.objects.all().order_by('-id')

    categories = Category.objects.all()

    context = {
        'q': q,
        'posts': posts,
        'categories': categories,
        'year': year,
        'month': month
    }

    return render(request, 'app/home.html', context)

def post_detail(request, pk):
    post = Post.objects.get(id=pk)


    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, post=post).exists()
    else:
        is_liked = False


    if request.method == 'POST':
 
        if 'like' in request.POST:

            if is_liked:
                Like.objects.filter(user=request.user, post=post).delete()
                return redirect('post_detail', pk=post.id)
            else:
                Like.objects.create(user=request.user, post=post)
                return redirect('post_detail', pk=post.id)
        if 'comment' in request.POST:
            comment = request.POST.get('comment')
            Comment.objects.create(user=request.user, post=post, text=comment)
            return redirect('post_detail', pk=post.id)
 
    context = {
        'post': post,
        'is_liked': is_liked
    }

    return render(request, 'app/post_detail.html', context)

def post_create(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False)
            title = form.cleaned_data['title']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            
            post = Post.objects.create(user=request.user, title=title, image=image, description=description)
            post.category.set(category)

            post.save()
            return redirect('post_detail', pk=post.id)

    context = {
        'form': form
    }

    return render(request, 'app/post_create.html', context)

def post_update(request, pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.id)
    context = {
        'form': form
    }

    return render(request, 'app/post_update.html', context)

def post_delete(request, pk):

    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'app/post_delete.html', {'post': post})

def myposts(request):
       post = Post.objects.filter(user=request.user)
       return render(request, 'app/myposts.html', {'post': post})

def comment_delete(request, pk):
    comment = Comment.objects.get(id=pk)
    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=comment.post.id)

    return render(request, 'app/comment_delete.html', {'comment': comment})
