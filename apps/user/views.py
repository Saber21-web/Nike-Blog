from django.shortcuts import render, redirect
from .forms import LoginForm, CreateUserForm, UserForm
from .models import User, Subscription
from django.contrib.auth import login, authenticate, logout
# Create your views here.


def login_page(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'user/login.html', context)

def sign_up(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.instance
            form.save()

            login(request, user)
            return redirect('home')

    context  ={
        'form': form
    }

    return render(request, 'user/sign_up.html', context)

def logout_page(request):
    logout(request)
    return redirect('home')

def profile(request, pk):
    user = User.objects.get(id=pk)

    subscribers= Subscription.objects.filter(author=user)
    subscribes = Subscription.objects.filter(user=user)

    subscrbers_count = subscribers.count()
    subscrbions_count = subscribes.count()


    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(user=request.user, author=user).exists()
    else:
        is_subscribed = False

    form = UserForm(instance=user)
    if request.method == 'POST':
        if 'update_user' in request.POST:
            form = UserForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect('profile', pk=pk)
        if 'subscribe' in request.POST:
            if is_subscribed:
                Subscription.objects.filter(user=request.user, author=user).delete()
                return redirect('profile', pk=pk)
            else:
                Subscription.objects.create(user=request.user, author=user)
                return redirect('profile', pk=pk)

    context = {
        'form': form,
        'user': user,
        'is_subscribed': is_subscribed,
        'subscrbers_count': subscrbers_count,
        'subscrbions_count': subscrbions_count,
        'subscribers': subscribers,
        'subscribes': subscribes

    }
    return render(request, 'user/profile.html', context)

