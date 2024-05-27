from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .helpers import send_otp_tp_phone, send_sms_to_tutors_phone
from .models import NewUser, Codes, TutorPage, UploadedFiles, Folders, message, receivers, Talaba, xabar
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.viewsets import ModelViewSet
from .serializer import TutorSerializer, UploadedFilesSerializer, FolderSerializer, UserSerializer, ReceiversSerializer, MessagesSerializer, XabarSerializer, StudentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.pagination import PageNumberPagination

from django_filters import rest_framework as filters
import requests
from rest_framework import filters
import json
from rest_framework import status
token = "UNlW_aD5UZZytL6G24Tq2jylV9yENZ--"
headers = {'Authorization': "Bearer {}".format(token)}


@api_view(['POST'])
def send_otp(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status':400,
            'message':"key phone_number is required"
        })
    
    if data.get('password') is None:
        return Response({
            'status':400,
            'message':"password is required"
        })
    
    if data.get('hemis_id') is None:
        return Response({
            'status':400,
            'message':"key hemis_id is required"
        })
    if NewUser.objects.filter(username=data.get('phone_number')).exists():
        return Response({
            'status':400,
            'message':"Bunaqa telefon raqam mavjud"
        })
    
    if NewUser.objects.filter(hemis_id=data.get('hemis_id')).exists():
        return Response({
            'status':400,
            'message':"Bunaqa hemis id mavjud"
        })
    
    BASE_URL = 'https://student.uzfi.uz/rest/v1/data/employee-list?type=employee&_staff_position=34&limit=100'
    auth_response = requests.get(BASE_URL, headers=headers).json()
    n=auth_response["data"]['items']
    tutors_id = []
    for i in n:
        tutors_id.append(i['employee_id_number'])

    if data.get('hemis_id') in tutors_id:
        if Codes.objects.filter(tel=data.get('phone_number')).exists():
            cod = Codes.objects.get(tel=data.get('phone_number'))
            cod.tel = data.get('phone_number')
            cod.code=send_otp_tp_phone(data.get('phone_number'))
            cod.hemis_id = data.get('hemis_id')
            cod.save()
        else:
            cod = Codes.objects.create(tel=data.get('phone_number'), code=send_otp_tp_phone(data.get('phone_number')), hemis_id=data.get('hemis_id'))
            cod.save()
        

        return Response({
            'status': 200, 
            'message': 'Otp Sent',
            "hemisId": data.get('hemis_id'),
            "password": data.get('password'),
            "phoneNumber": data.get('phone_number'),
        })
    else:
        return Response({
            'status':400,
            'message':"Bunaqa id tutorlar bazasida yoq tekshirib boshqatdan kirgizing"
        })
    

@api_view(['POST'])
def verify_otp(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status':400,
            'message':"Telefon raqam kiritilmagan"
        })
    
    if data.get('password') is None:
        return Response({
            'status':400,
            'message':"Parol kiritilmagan"
        })
    
    
    if data.get('otp') is None:
        return Response({
            'status':400,
            'message':"Tasdiqlash kodi kiritilmagan"
        })
    
    if NewUser.objects.filter(username=data.get('phone_number')).exists():
        return Response({
            'status':400,
            'message':"Bunaqa telefon raqam mavjud"
        })
    cod_obj = Codes.objects.get(tel=data.get('phone_number'))
    if NewUser.objects.filter(hemis_id=cod_obj.hemis_id).exists():
        return Response({
            'status':400,
            'message':"Bunaqa telefon raqam mavjud"
        })
    
    try:
        cod_obj = Codes.objects.get(tel=data.get('phone_number'))
        
    except Exception as e:
        return Response({
            'status':400,
            'message':"Invalid phone"
        })
    
    if cod_obj.code == data.get('otp'):
        user = NewUser.objects.create(hemis_id=cod_obj.hemis_id, username = data.get('phone_number'))
        user.set_password(data.get('password'))
        user.is_phone_verified = True
        user.user_type="Tutor"
        user.save()
        tutor_page = TutorPage.objects.create(user=user, hemis_id=user.hemis_id)
        tutor_page.save()
        return Response({
            'status':200,
            'message':"otp matched"
        })
    
    return Response({
            'status':400,
            'message':"Invalid Otp"
        })


@api_view(['POST'])
def send_sms(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status':400,
            'message':"key phone_number is required"
        })
    
    if data.get('password') is None:
        return Response({
            'status':400,
            'message':"password is required"
        })
    user = authenticate(username=data.get('phone_number'), password=data.get('password'))
    print(user)
    if user is not None:
        user_model = get_object_or_404(NewUser, username=data.get('phone_number'))
        user_model.otp = send_otp_tp_phone(data.get('phone_number'))
        user_model.save()
        return Response({
            'status': 200, 
            'message': "Sms xabar jo'natildi",
            "password": data.get('password'),
            "phoneNumber": data.get('phone_number'),
        })
    else:
        return Response({
            'status': 401, 
            'message': "Login yoki parol xato",
        })


@api_view(['POST'])
def verify_sms(request):
    data = request.data

    if data.get('phone_number') is None:
        return Response({
            'status':400,
            'message':"Telefon raqam kiritilmagan"
        })
    
    if data.get('password') is None:
        return Response({
            'status':400,
            'message':"Parol kiritilmagan"
        })
    
    if data.get('sms_code') is None:
        return Response({
            'status':400,
            'message':"Tasdiqlash kodi kiritilmagan"
        })
    
    user_model  = get_object_or_404(NewUser, username=data.get('phone_number'))
    if user_model.otp == data.get('sms_code'):
            
        
        user = authenticate(username=data.get('phone_number'), password=data.get('password'))
        token = Token.objects.get_or_create(user=user)
        token=token[0]
        return Response({
            'status': 200, 
            'message': "Sms tasdiqlandi",
            'Token':str(token),
	    'hemis_token':'UNlW_aD5UZZytL6G24Tq2jylV9yENZ--',
            'user_type':user.user_type,
            'phone_number':user.username,
        })


class TutorViewSet(ModelViewSet):
    serializer_class = TutorSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    queryset = TutorPage.objects.all()

    def get_queryset(self):
        result = []

        tutor_model = TutorPage.objects.filter(user=self.request.user)
        if self.request.user.user_type == "Tutor":
            BASE_URL = 'https://student.uzfi.uz/rest/v1/data/employee-list?type=employee&_staff_position=34&limit=100'
            auth_response = requests.get(BASE_URL, headers=headers).json()
            n=auth_response["data"]['items']
            
            for i in n:
                i['phone_number']=self.request.user.username
                if tutor_model.values_list("hemis_id", flat=True)[0] == i['employee_id_number']:
                    for k in i['tutorGroups']:
                        BASE_URL_gurux = 'https://student.uzfi.uz/rest/v1/data/student-list?_group={}&limit=100'.format(k['id'])
                        auth_response = requests.get(BASE_URL_gurux, headers=headers).json()
                        gurux=auth_response["data"]['items']
                        k['id']=gurux
                    q={"hemis_id":json.dumps(i), "role":self.request.user.user_type}
                    result.append(q)
                    break
        if self.request.user.user_type == "Manaviyat":
            manaviyat_info = {
            'full_name': 'Muminova Zarifa Odilovna',
            'hemis_token':'UNlW_aD5UZZytL6G24Tq2jylV9yENZ--',
            'short_name': 'Muminova Z. O.',
            'first_name': 'Zarifa',
            'second_name': 'Muminova',
            'third_name': 'Odilovna',
            'employee_id_number': '123456789',
            'phone_number':self.request.user.username,
            'gender': {'code': '12', 'name': 'Ayol'},
            'birth_date': '',
            'image': 'https://uzfi.uz/frontend/web/arguments/rek_img/64a3aa82737f0.jpg',
            'year_of_enter': 2021,
            'academicDegree': {'code': '10', 'name': ''},
            'academicRank': {'code': '10', 'name': ''},
            'department': {'id': 1, 'name': 'Yoshlar masalalari va manaviy-marifiy ishlar boyicha birinchi prorektor'}
        }
            q={"hemis_id":json.dumps(manaviyat_info), "role":self.request.user.user_type}
            result.append(q)


        return result
    
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 24
    page_size_query_param = 'page_size'
    max_page_size = 10000


class FolderViewSet(ModelViewSet):
    queryset = Folders.objects.all()
    serializer_class = FolderSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

class UploadedFiledViewSet(ModelViewSet):
    queryset = UploadedFiles.objects.all()
    serializer_class = UploadedFilesSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = LargeResultsSetPagination
    search_fields = ['name', 'folder__name']
    ordering_fields = ['name']
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        name = request.data['name']
        user = self.request.user
        files = request.data['files']
        description = request.data['description']
        folder_model = Folders.objects.get(name=request.data['folder'])

        UploadedFiles.objects.create(user = user, name = name, files = files, description = description, folder=folder_model)
        return Response("Files muvaffaqiyatli qoshildi", status=status.HTTP_200_OK)
    
    def get_queryset(self):
        tutor_model = UploadedFiles.objects.filter(user=self.request.user).order_by("-created_at")
        return tutor_model


class AllFilesViewSet(ModelViewSet):
    queryset = UploadedFiles.objects.all().order_by("-created_at")
    serializer_class = UploadedFilesSerializer
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filter_backends = [DjangoFilterBackend]
    pagination_class = LargeResultsSetPagination
    # search_fields = ['name', 'folder__name', "user__hemis_id"]
    filterset_fields = ['user__hemis_id', 'folder__name']
    # ordering_fields = ['name']
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    parser_classes = (MultiPartParser, FormParser)


class UsersViewSet(ModelViewSet):
    serializer_class = UserSerializer
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        tutor_model = NewUser.objects.filter(user_type="Tutor")
        return tutor_model

class AllTutorsViewSet(ModelViewSet):
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        tutor_model = NewUser.objects.filter(user_type="Tutor")
        return tutor_model
    

class MessageViewSet(ModelViewSet):
    queryset = message.objects.all()
    serializer_class = MessagesSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        xabar = request.data['xabar']
        img = request.data['img']
        tutorlar = request.data['tutorlar']
        fullname = request.data['fullname']
        my_object = message(xabar=xabar, img=img, tutorlar=tutorlar, fullname=fullname)
        my_object.save()
        my_object_id = my_object.id
        for i in my_object.tutorlar:
            user_model = NewUser.objects.get(hemis_id=int(i))
            send_sms_to_tutors_phone(user_model.username, xabar)
            receivers.objects.create(xabar_id=my_object, tutors=user_model)

        return Response("Xabar muvaffaqiyatli yuborildi", status=status.HTTP_200_OK)

    def get_queryset(self):
        tutorlar_model = message.objects.all().order_by('-id')
        
        for i in tutorlar_model:
            tutor_dict = {}
            tutor_m = receivers.objects.filter(xabar_id=i.id)
            for j in tutor_m:
                print(j.tutors.username)
                tutor_dict[j.id]={'hemis_id':j.tutors.hemis_id, 'is_readed':j.is_readed}
            i.tutorlar = json.dumps(tutor_dict)
        return tutorlar_model

class ReceiverForTutorViewSet(ModelViewSet):
    queryset = receivers.objects.all()
    serializer_class = ReceiversSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            tutor_model = receivers.objects.filter(tutors=self.request.user, id=pk).order_by('-id')
            return tutor_model
        else:
            tutor_model = receivers.objects.filter(tutors=self.request.user).order_by('-id')
            return tutor_model
    
    
class XabarViewSet(ModelViewSet):
    queryset = xabar.objects.all()
    serializer_class = XabarSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        matn = request.data['matn']
        img_manaviy = request.data['img_manaviy']
        student_massiv = request.data['student_massiv']
        fullname_manaviy = request.data['fullname_manaviy']
        tutor_fullname = request.data['tutor_fullname']
        tutor_hemis_id = request.data['tutor_hemis_id']
        group_id = request.data['group_id']
        group = request.data['group']
        my_object = xabar(matn=matn,
            img_manaviy=img_manaviy,
            student_massiv=student_massiv,
            fullname_manaviy=fullname_manaviy,
            tutor_fullname=tutor_fullname,
            tutor_hemis_id=tutor_hemis_id,
            group_id=group_id,
            group=group)
        my_object.save()
        my_object_id = my_object.id
        tutor_id = NewUser.objects.get(hemis_id=tutor_hemis_id)
        for i in my_object.student_massiv:
            Talaba.objects.create(tutor=tutor_id,
                xabar_id=my_object,
                img_manaviy=img_manaviy,
                fullname_manaviy=fullname_manaviy,
                tutor_fullname=tutor_fullname,
                tutor_hemis_id=tutor_hemis_id,
                group_id=group_id,
                group=group,
                student_hemis_id=i)

        return Response("Xabar muvaffaqiyatli yuborildi", status=status.HTTP_200_OK)
    
class StudentIsLocationViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    # filter_backends = [DjangoFilterBackend]
    pagination_class = LargeResultsSetPagination
    filterset_fields = ['student_hemis_id',]
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            if self.request.user.user_type == "Manaviyat":
                tutor_model = Talaba.objects.filter(status=True, id=pk).order_by('-id')
                return tutor_model
            else:
                tutor_model = Talaba.objects.filter(status=True, tutor=self.request.user, id=pk).order_by('-id')
                return tutor_model
        else:
            if self.request.user.user_type == "Manaviyat":
                tutor_model = Talaba.objects.filter(status=True).order_by('-id')
                return tutor_model
            else:
                tutor_model = Talaba.objects.filter(status=True, tutor=self.request.user).order_by('-id')
                return tutor_model
            
        
class StudentIsNotLocationViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    # filter_backends = [DjangoFilterBackend]
    pagination_class = LargeResultsSetPagination
    filterset_fields = ['student_hemis_id',]
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            if self.request.user.user_type == "Manaviyat":
                tutor_model = Talaba.objects.filter(status=False, id=pk).order_by('-id')
                return tutor_model
            else:
                tutor_model = Talaba.objects.filter(status=False, tutor=self.request.user, id=pk).order_by('-id')
                return tutor_model
        else:
            if self.request.user.user_type == "Manaviyat":
                tutor_model = Talaba.objects.filter(status=False).order_by('-id')
                return tutor_model
            else:
                tutor_model = Talaba.objects.filter(status=False, tutor=self.request.user).order_by('-id')
                return tutor_model