from .serializers import UserSerializer, CircleSerializer
from .models import User, Circle
from django.http import Http404

from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from bson.objectid import ObjectId
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import jwt
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
sys.path.insert(0, BASE_DIR)
from server.settings import SECRET_KEY, ALGORITHM


@method_decorator(csrf_exempt, name='dispatch')
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny ,)

    def get_object(self, oid):
        try:
            oid = ObjectId(oid)
            return User.objects.get(_id=oid)
        except:
            raise Http404

    def list(self, request):
        queryset = User.objects.all()
        print(request.META)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def user_auth(self, request):
        auth = request.META['HTTP_AUTHORIZATION']
        json = jwt.decode(auth, SECRET_KEY, ALGORITHM)
        user = User.objects.get(user_id=json['user_id'])
        serializer = UserSerializer(user)
        return Response(serializer.data)


    def create(self, request):
        data = request.data
        user = User(user_id=data['user_id'],
                    user_pw=data['user_pw'],
                    name=data['name'],
                    grade=data['grade'],
                    major=data['major'])
        user.save()
        return Response(request.data)

    def retrieve(self, request, oid):
        user = self.get_object(oid)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, oid):
        user = self.get_object(oid)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, oid):
        user = self.get_object(oid)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # id 조회
    def findId(self, request, oid):
        user = self.get_object(oid)
        serializer = UserSerializer(user)
        return Response(serializer.data['user_id'])

    # pw 변경
    def patchPw(self, request, oid):
        user = self.get_object(oid)
        serializer = UserSerializer(user, data={'user_pw': request.data['user_pw']}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 로그인
    def login(self, request):
        data = request.data
        user = User.objects.get(user_id=data['user_id'])
        if user:
            serializer = UserSerializer(user)
            if data['user_pw'] == serializer.data['user_pw']:
                token = jwt.encode(data, SECRET_KEY, ALGORITHM)
                data = serializer.data
                data['token'] = token
                return Response(data)
        
        return Response({'error':'error'}, status=status.HTTP_400_BAD_REQUEST)


class CircleView(viewsets.ModelViewSet):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self, oid):
        try:
            oid = ObjectId(oid)
            return Circle.objects.get(_id=oid)
        except:
            raise Http404

    def list(self, request):
        queryset = Circle.objects.all()
        serializer = CircleSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        circle = Circle(name=data['name'],
                      leader=data['leader'],
                      member=data['member'])
        circle.save()
        return Response(request.data)

    def retrieve(self, request, oid):
        circle = self.get_object(oid)
        serializer = CircleSerializer(circle)
        return Response(serializer.data)

    def update(self, request, oid):
        circle = self.get_object(oid)
        serializer = CircleSerializer(circle, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, oid):
        circle = self.get_object(oid)
        circle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CircleMemberView(viewsets.ModelViewSet):
    queryset = Circle.objects.all()
    serializer_class = CircleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, oid):
        try:
            oid = ObjectId(oid)
            return Circle.objects.get(_id=oid)
        except:
            raise Http404

    def list(self, request, oid):
        circle = self.get_object(oid)
        serializer = CircleSerializer(circle)
        return Response(serializer.data['member'])

    def add(self, request, oid):
        circle = self.get_object(oid)
        serializer = CircleSerializer(circle)
        circle_member = json.loads(serializer.data['member'])
        circle_member.append(json.loads(request.data['member']))
        serializer = CircleSerializer(circle, data={'member': circle_member}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destory(self, request, circle_oid, member_oid):
        circle = self.get_object(circle_oid)
        serializer = CircleSerializer(circle)
        circle_member = json.loads(serializer.data['member'])
        for member in circle_member:
            if member['_id'] == member_oid:
                circle_member.remove(member)
        serializer = CircleSerializer(circle, data={'member': circle_member}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


