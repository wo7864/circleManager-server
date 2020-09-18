from rest_framework import serializers
from .models import User, Circle, TextPost


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_id', 'user_pw', 'name', 'grade', 'major',)

class CircleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Circle
        fields = ('name', 'leader', 'member')

class TextPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextPost
        fields = ('author', 'title', 'contents')
