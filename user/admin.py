from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . models import NewUser, Codes, TutorPage, UploadedFiles, Folders, receivers, message, xabar, Talaba


fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info', {'fields' :('first_name', 'last_name', 'email', 'is_phone_verified', 'otp', 'hemis_id', 'user_type')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(NewUser, UserAdmin)
admin.site.register(Codes)
admin.site.register(TutorPage)
admin.site.register(Folders)
admin.site.register(UploadedFiles)
admin.site.register(receivers)
admin.site.register(message)
admin.site.register(xabar)
admin.site.register(Talaba)