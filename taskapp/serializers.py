from rest_framework import serializers
from taskapp.models import User,Task

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields="__all__"
        
class TaskSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Task
        fields="__all__"