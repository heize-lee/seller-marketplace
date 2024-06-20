from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Follow
# from follow.models import Follow
from django.shortcuts import render, get_object_or_404
from .models import Profile
from django.shortcuts import get_object_or_404, redirect

from django.http import JsonResponse

from accounts.models import CustomUser
from django.views.decorators.http import require_POST

from .models import UserProfile  # 사용자 프로필 모델 임포트





User = get_user_model()  # Django 프로젝트에서 사용 중인 사용자 모델을 가져옴

@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    return render(request, 'follow/profile.html', {'user': user})


# follow 앱의 views.py 파일

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
#@require_POST
def follow_user(request):
    user_id = request.POST.get('user_id')
    
    try:
        profile_to_follow = UserProfile.objects.get(id=user_id)  # 팔로우할 사용자 프로필 가져오기
    except UserProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '사용자를 찾을 수 없습니다.'}, status=404)
    
    current_user_profile = request.user.profile  # 현재 로그인한 사용자의 프로필 가져오기
    
    if profile_to_follow == current_user_profile:
        return JsonResponse({'status': 'error', 'message': '자기 자신을 팔로우할 수 없습니다.'}, status=400)
    
    if profile_to_follow in current_user_profile.following.all():
        current_user_profile.following.remove(profile_to_follow)
        status = 'unfollowed'
    else:
        current_user_profile.following.add(profile_to_follow)
        status = 'followed'
    
    return JsonResponse({'status': status})



@require_POST
@login_required
def follow_user(request):
    user_id = request.POST.get('user_id')
    try:
        profile_to_follow = UserProfile.objects.get(id=user_id)  # 팔로우할 사용자 프로필 가져오기
    except UserProfile.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': '사용자를 찾을 수 없습니다.'}, status=404)
    
    current_user_profile = request.user.profile  # 현재 로그인한 사용자의 프로필 가져오기
    
    if profile_to_follow == current_user_profile:
        return JsonResponse({'status': 'error', 'message': '자기 자신을 팔로우할 수 없습니다.'}, status=400)
    
    if profile_to_follow in current_user_profile.following.all():
        current_user_profile.following.remove(profile_to_follow)
        status = 'unfollowed'
    else:
        current_user_profile.following.add(profile_to_follow)
        status = 'followed'
    
    return JsonResponse({'status': status})

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('user_profile', user_id=user_id)


def profile_view(request, id):
    profile = get_object_or_404(Profile, id=id)
    return render(request, 'profile.html', {'profile': profile})