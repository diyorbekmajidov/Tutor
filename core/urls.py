from django.contrib import admin
from django.urls import path, include
from user.views import *
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Pdp Online dars uchun API Documentation",
      default_version='v1',
      description="API Documentation",
      contact=openapi.Contact(email="dosumbetov19983010@gmail.com"),
   ),
   public=True,
   permission_classes=(AllowAny,),
)

router = DefaultRouter()
router.register('tutors', TutorViewSet, 'tutor')
router.register('users', UsersViewSet, 'users')
router.register('allTutors', AllTutorsViewSet, 'all_tutors')
router.register('folders', FolderViewSet, 'folders')
router.register('uplodedFiles', UploadedFiledViewSet, 'files')
router.register('allfiles', AllFilesViewSet, 'allfiles')
router.register('messages', MessageViewSet, 'messages')
router.register('receiverfortutor', ReceiverForTutorViewSet, 'receiverfortutor')

router.register('xabar', XabarViewSet, 'xabar')
router.register('studentislocation', StudentIsLocationViewSet, 'studentislocation')
router.register('studentisnotlocation', StudentIsNotLocationViewSet, 'studentisnotlocation')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', views.obtain_auth_token),
    path('send_otp/', send_otp),
    path('verify_otp/', verify_otp),
    path('send_sms/', send_sms),
    path('verify_sms/', verify_sms),
    path('admin/', admin.site.urls),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
