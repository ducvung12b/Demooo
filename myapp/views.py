from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render,redirect
import os
from django.http import HttpResponse,JsonResponse
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
# @login_required
# def page(request):
#     page = Pages.objects.all()
#     return render(request,'myapp/listpage.html',{'page': page})

def home(request):
    pages = Pages.objects.all()
    return render(request,'myapp/home.html',{'pages': pages})



def loginPage(request):
    if request.user.is_authenticated:
        return redirect('page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username ,password = password)
        if user is not None:
            login(request,user)
            return redirect('page')
        else:  messages.info(request,'Tài Khoản Đăng Nhập Chưa Đúng..!')
    context={}
    return render(request,'myapp/loginpage.html',context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            login(request, user)
            return redirect('page')
        else:
            return render(request, 'register.html', {'Lỗi': 'Mật Khẩu Không Trùng Khớp'})
    return render(request,'myapp/register.html')


@login_required

# def postpage(request):
#     if request.method == "POST":
#         title = request.POST.get("title")
#         description = request.POST.get("description")
#         author = request.user  # Lấy người dùng hiện tại

#         # Lưu bài viết vào cơ sở dữ liệu
#         Pages.objects.create(title=title, description=description, author=author)

#         return redirect('page')  # Chuyển hướng đến trang danh sách bài viết

#     return render(request, 'myapp/postpage.html')

@login_required
def page(request):
    # Lấy tất cả bài viếtp
    pages = Pages.objects.all().order_by('-created_at')
    return render(request, 'myapp/page.html', {'pages': pages})



@login_required
def detail(request,page_id):
    page = get_object_or_404(Pages, id=page_id)
    return render(request,'myapp/detail.html', {'page': page,})


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        checks = Pages.objects.filter(title__contains = searched)
    page = Pages.objects.all()
    return render(request, 'myapp/search.html', {'page':page,'searched': searched, 'checks': checks})


@login_required 
def follow_user(request, user_id): 
    user_to_follow = get_object_or_404(User, id=user_id) 
    follow, created = Follow.objects.get_or_create(follower=request.user, followed=user_to_follow) 
    if created: 
        messages.success(request, f'Bạn đã theo dõi {user_to_follow.username} thành công.') 
    else: 
        messages.info(request, f'Bạn đã theo dõi {user_to_follow.username} trước đó rồi.') 
    return redirect('user') # Thay 'home' bằng tên URL của trang bạn muốn chuyển hướng tới

@login_required 
def unfollow_user(request, user_id): 
    user_to_unfollow = get_object_or_404(User, id=user_id) 
    follow = Follow.objects.filter(follower=request.user, followed=user_to_unfollow).first() 
    if follow: 
        follow.delete() 
        messages.success(request, f'Bạn đã hủy theo dõi {user_to_unfollow.username}.') 
    else: 
        messages.info(request, f'Bạn chưa theo dõi {user_to_unfollow.username}.') 
    return redirect('user') # Thay 'home' bằng tên URL của trang bạn muốn chuyển hướng tới

@login_required
def postpage(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        page = Pages.objects.create(title=title, description=description, author=request.user)
        followers = Follow.objects.filter(followed=request.user)
        for follow in followers:
            Notification.objects.create(
                recipient=follow.follower,
                sender=request.user,
                page=page,
                message=f'{request.user.username} đã đăng một nội dung mới.'
            )
            print(f'Notification created for {follow.follower.username}')
        messages.success(request, 'Nội dung của bạn đã được đăng thành công.')
        return redirect('page')  # Thay 'home' bằng URL bạn muốn chuyển hướng tới
    return render(request, 'myapp/postpage.html')

        
@login_required 
def notifications(request): 
    notifications = request.user.notifications.all().order_by('-timestamp') 
    return render(request, 'myapp/notifications.html', {'notifications': notifications})


@login_required
def user_list(request): 
    users = User.objects.exclude(id=request.user.id) # Loại bỏ người dùng hiện tại khỏi danh sách 
    following = Follow.objects.filter(follower=request.user).values_list('followed_id', flat=True) 
    return render(request, 'myapp/user.html', {'users': users, 'following': following})