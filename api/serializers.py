from rest_framework import serializers
from .models import Patient,Record,CustomUser,Post,Comment
from taggit.serializers import (TagListSerializerField,TaggitSerializer)

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        fields='__all__'

class RecordSerializer(serializers.ModelSerializer):
    tags = TagListSerializerField()
    class Meta:
        model=Record
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    class Meta:
        model=Comment
        fields=['author','comment','date']




class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    doctors_related = UserSerializer(many=True)
    comments= CommentSerializer(many=True,read_only=True)
    tags = TagListSerializerField()
    
    class Meta:
        model=Post
        fields=['id','author','title','desc','date','tags','comments','doctors_related']
