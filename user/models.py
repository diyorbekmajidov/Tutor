from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class NewUser(AbstractUser):
    user_type_data = (
        ("Admin", 'Admin'),
        ("Manaviyat", 'Manaviyat'),
        ("Tutor", 'Tutor')
        )
    user_type = models.CharField(default="Admin", choices=user_type_data, max_length=50)
    hemis_id = models.CharField(max_length=100, unique=True)
    is_phone_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)

class Codes(models.Model):
    code = models.CharField(max_length=112)
    tel = models.CharField(max_length=255)
    hemis_id = models.CharField(max_length=255)

class TutorPage(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='tutor')
    hemis_id = models.CharField(max_length=255)
    role = models.CharField(max_length=50)


class Folders(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    files_number = models.IntegerField(default=0)
    files_size = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class UploadedFiles(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE, related_name='files')
    folder = models.ForeignKey(Folders, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    files = models.FileField(upload_to="uploads/%Y/%m/%d/")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_filesize(self):
        return self.files.size

@receiver(post_save, sender=UploadedFiles)
def count_files_inside_folder(sender, instance, created, **kwargs):
    upload_files_count = UploadedFiles.objects.filter(folder=instance.folder).count()
    file_size = 0
    for i in UploadedFiles.objects.filter(folder=instance.folder):
        file_size = file_size + (i.get_filesize())//1024
    folder_model = Folders.objects.get(name=instance.folder)
    folder_model.files_number=upload_files_count
    folder_model.files_size = file_size
    folder_model.save()

@receiver(post_delete, sender=UploadedFiles)
def delete_after_count_files_inside_folder(sender, instance, **kwargs):
    upload_files_count = UploadedFiles.objects.filter(folder=instance.folder).count()
    file_size = 0
    for i in UploadedFiles.objects.filter(folder=instance.folder):
        file_size = file_size + (i.get_filesize())//1024
    folder_model = Folders.objects.get(name=instance.folder)
    folder_model.files_number=upload_files_count
    folder_model.files_size = file_size
    folder_model.save()
    
class message(models.Model):
    xabar = models.TextField()
    img = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    tutorlar = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class receivers(models.Model):
    xabar_id = models.ForeignKey(message, on_delete=models.CASCADE)
    tutors = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    is_readed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Topshiriq(models.Model):
    user = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    img = models.CharField(max_length=255)
    fullname = models.CharField(max_length=255)
    talabalar = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

class xabar(models.Model):
    matn = models.TextField()
    student_massiv = models.CharField(max_length=255)
    img_manaviy = models.CharField(max_length=255)
    fullname_manaviy = models.CharField(max_length=255)
    tutor_fullname = models.CharField(max_length=255)
    tutor_hemis_id = models.CharField(max_length=255)
    group_id = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.matn

class Talaba(models.Model):
    tutor = models.ForeignKey(NewUser, on_delete=models.CASCADE)
    xabar_id = models.ForeignKey(xabar, on_delete=models.CASCADE)
    img_manaviy = models.CharField(max_length=255)
    fullname_manaviy = models.CharField(max_length=255)
    tutor_fullname = models.CharField(max_length=255)
    tutor_hemis_id = models.CharField(max_length=255)
    group_id = models.CharField(max_length=255)
    group = models.CharField(max_length=255)
    student_hemis_id = models.CharField(max_length=255)
    img = models.CharField(max_length=255, blank=True)
    student_phone_number_1 = models.CharField(max_length=255, null=True, blank=True)
    student_phone_number_2 = models.CharField(max_length=255, null=True, blank=True)
    student_telegram = models.CharField(max_length=255, null=True, blank=True)
    location_url = models.CharField(max_length=255, null=True, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.tutor_fullname


