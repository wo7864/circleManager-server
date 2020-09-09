from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserView,  CircleView, CircleMemberView
#from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

user_auth = UserView.as_view({
    'get': 'user_auth'
})
user_list = UserView.as_view({
    'post': 'create',
    'get': 'list'
})

user_detail = UserView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

find_id = UserView.as_view({
    'get': 'findId',
})

patch_pw = UserView.as_view({
    'put': 'patchPw',
})

login = UserView.as_view({
    'post': 'login'
})

circle_list = CircleView.as_view({
    'get': 'list',
    'post': 'create'
})

circle_detail = CircleView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

circle_member_list = CircleMemberView.as_view({
    'get':'list',
    'put':'add',
})

circle_member_update = CircleMemberView.as_view({
    'delete': 'destory'
})
urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('api-token-auth/', obtain_jwt_token),
    #path('api-token-ver/', verify_jwt_token),
    path('user/', user_auth, name='user_auth'),
    path('users/', user_list, name='user_list'),
    path('users/login/', login, name='login'),

    path('users/<str:oid>/', user_detail, name='user_detail'),
    path('users/id/<str:oid>/', find_id, name='find_id'),
    path('users/pw/<str:oid>/', patch_pw, name='patch_pw'),

    path('circles/', circle_list, name='circle_list'),
    path('circles/<str:oid>/', circle_detail, name='circle_detail'),
    path('circles/member/<str:oid>/', circle_member_list, name='circle_member_list'),
    path('circles/member/<str:circle_oid>/<str:member_oid>', circle_member_update, name='circle_member_list'),



])