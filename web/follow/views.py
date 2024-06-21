# from follow.models import Follow

from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Follow, User
#from .models import Profile
from django.http import JsonResponse
from accounts.models import CustomUser
from django.views.decorators.http import require_POST
#from .models import UserProfile  # 사용자 프로필 모델 임포트








# User = get_user_model()  # Django 프로젝트에서 사용 중인 사용자 모델을 가져옴

# @login_required
# def user_profile(request, user_id):
#     user = get_object_or_404(User, pk=user_id)
#     return render(request, 'follow/profile.html', {'user': user})


# follow 앱의 views.py 파일

import json

@login_required
@require_POST
def follow_user(request):
    # 현재 로그인한 사용자의 user_id 가져오기
    current_user = request.user
    
    # 요청에서 seller_email 가져오기
    data = json.loads(request.body)
    seller_email = data.get('following_id')
    
    # seller_email로부터 user_id 조회
    seller = get_object_or_404(User, email=seller_email)
    
    try:
        # follow_follow 테이블에 follower_id와 following_id 값 삽입
        follow, created = Follow.objects.get_or_create(follower=current_user, following=seller)
        
        if created:
            return JsonResponse({"message": "Follow successful"}, status=200)
        else:
            return JsonResponse({"message": "Already following"}, status=200)
    except Exception as e:
        return JsonResponse({"message": f"An error occurred: {e}"}, status=500)











    # current_user_profile = request.user.profile  # 현재 로그인한 사용자의 프로필 가져오기
    
    # if profile_to_follow == current_user_profile:
    #     return JsonResponse({'status': 'error', 'message': '자기 자신을 팔로우할 수 없습니다.'}, status=400)
    
    # if profile_to_follow in current_user_profile.following.all():
    #     current_user_profile.following.remove(profile_to_follow)
    #     status = 'unfollowed'
    # else:
    #     current_user_profile.following.add(profile_to_follow)
    #     status = 'followed'
    
    # return JsonResponse({'status': status})


