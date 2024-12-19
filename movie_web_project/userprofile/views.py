from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile

# Create your views here.
# @login_required
# def profile_view(request):
#     user = request.user
#     edit_mode = False

#     if request.method == 'POST':
#         if 'username' in request.POST:
#             user.username = request.POST['username']
#             user.email = request.POST['email']
#             user.first_name = request.POST['first_name']
#             user.last_name = request.POST['last_name']
#             user.save()
#             edit_mode = False
#         elif 'edit_profile' in request.POST:
#             edit_mode = True

#     return render(request, 'userprofile/profile.html', {'user': user, 'edit_mode': edit_mode})
# def profile_view(request):
#     user = request.user
#     edit_mode = False

#     if request.method == 'POST':
#         if 'edit_profile' in request.POST:
#             user.username = request.POST['username']
#             user.email = request.POST['email']
#             user.first_name = request.POST['first_name']
#             user.last_name = request.POST['last_name']
#             user.save()
#         return redirect('profile')
#     return render(request, 'userprofile/profile.html', {'user':user, 'edit_mode': edit_mode})

@login_required
def profile_view(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST['new_email']
        user.userprofile.birth_date = request.POST['new_birth_date']
        # Xử lý các trường chỉnh sửa khác
        user.save()
        return redirect('profile')  # Chuyển hướng người dùng sau khi cập nhật
    return render(request, 'userprofile/profile.html')

