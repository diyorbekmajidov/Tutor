from rest_framework import serializers
from .models import TutorPage, UploadedFiles, Folders, NewUser, message, receivers, xabar, Talaba

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id', 'username', 'hemis_id')

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TutorPage
        fields = ("role", "hemis_id", )

class FolderSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model = Folders
        fields = '__all__'

class UploadedFilesSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    folder=FolderSerializer()
    class Meta:
        
        model = UploadedFiles
        
        fields = '__all__'

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = message
        fields = ('id', 'xabar', 'img', 'fullname', 'tutorlar', "created_at")
    
class ReceiversSerializer(serializers.ModelSerializer):
    xabar_id = MessagesSerializer()
    tutors = UserSerializer()
    class Meta:
        model = receivers
        fields = ('xabar_id', 'tutors', 'is_readed', "created_at")

class XabarSerializer(serializers.ModelSerializer):
    class Meta:
        model = xabar
        fields = ('id', 'matn', 'student_massiv', 'img_manaviy', 'fullname_manaviy', "tutor_fullname", "tutor_hemis_id", "group_id", "group", "created_at")
    
class StudentSerializer(serializers.ModelSerializer):
    xabar_id = XabarSerializer()
    class Meta:
        model = Talaba
        fields = "__all__"