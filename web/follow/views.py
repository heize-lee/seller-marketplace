from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Follow
# from follow.models import Follow



User = get_user_model()  # Django 프로젝트에서 사용 중인 사용자 모델을 가져옴

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'follow/profile.html', {'user': user})

@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('user_profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('user_profile', user_id=user_id)
