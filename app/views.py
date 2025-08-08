from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Notice, LoginData, EmailCode
from django.core.mail import send_mail
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

import string
import random
import uuid
# Create your views here.

def adds(request):
    return render(request, "add.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

class Myauthentication(BaseAuthentication):

    def authenticate(self, request):
       
        token = request.GET.get('token')
       
        if not token:
           raise AuthenticationFailed({"error": "未提供令牌"})
       
        try:
            CheckToken = LoginData.objects.filter(token=token).first()
            if CheckToken:
                return (CheckToken, token)    # request.user = CheckToken, request.auth = token
            else:
                raise AuthenticationFailed({"error": "令牌错误"})
        except Exception as e:
            raise AuthenticationFailed({"error": "令牌错误"})

class NoticeSerializers(serializers.ModelSerializer):
    
    # text = serializers.CharField()
    
    # user_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = Notice
        fields='__all__'
        
class RegisterSerializers(serializers.ModelSerializer):
    
    emailCode = serializers.CharField(max_length=6, required=True, help_text="验证码", write_only=True)
    
    class Meta:
        model = LoginData
        fields = '__all__'
        
class EmailCodeSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = EmailCode
        fields = '__all__'
        
class LoginSerializers(serializers.Serializer):
    
    id = serializers.IntegerField(read_only=True)
    
    username = serializers.CharField(max_length=30)
    
    password = serializers.CharField(max_length=128)
    
    # updated_at = serializers.DateTimeField(read_only=True)
    
class RegisterDataView(APIView):
    
    def get(self, request):

        # 获取所有的LoginData数据
        registers = LoginData.objects.all()
        s = RegisterSerializers(registers, many=True)
        return Response({"user_info": s.data}, status=200)
    
    def post(self, request):
        
        s = RegisterSerializers(data=request.data)
        
        if not s.is_valid():
            print(s.errors)
            if s.errors['username'][0] == "具有 用户名 的 login data 已存在。":
                return Response({"error": "用户名已存在"}, status=400)
            elif s.errors['email'][0] == "具有 邮箱 的 login data 已存在。":
                return Response({"error": "邮箱号已存在"}, status=400)
            return Response({"errors": s.errors}, status=400)
        else:
            if not EmailCode.objects.filter(email=s.validated_data.get('email'), code=s.validated_data.get('emailCode')).exists():
                return Response({"error": "验证码错误"}, status=400)
            else:
                k = s.validated_data.copy()
                k.pop('emailCode', None)
                user_info = LoginData.objects.create(**k)
                return Response({"注册成功": RegisterSerializers(user_info).data}, status=201)
            
class LoginDataView(APIView):
    
    def get(self, request):
        
        logins = LoginData.objects.all()
        ls = LoginSerializers(logins, many=True)
        
        return Response({"Login_Data": ls.data}, status=200)
        
        
    def post(self, request):
        
        ls = LoginSerializers(data=request.data)
        
        if not ls.is_valid():
            print(ls.validated_data)
            print(ls.errors)
            return Response({"error": ls.errors}, status=400)
        else:
            if not LoginData.objects.filter(username=ls.validated_data.get('username')).exists():
                return Response({"error":"用户名不存在"}, status=400) 
                      
            elif LoginData.objects.get(username=ls.validated_data.get('username')).password != ls.validated_data.get('password'):    # 修改一下密码检验的方法
                return Response({"error":"密码输入不正确"}, status=400)
            
            else:
                token = str(uuid.uuid4())
                UpdateData = LoginData.objects.get(username=ls.validated_data.get('username'))
                UpdateData.token = token
                UpdateData.save()
                # print("UpdateData:", UpdateData)
                return Response({"message": "登陆成功", "token": token, "id": UpdateData.id}, status=201)
            
class NoticeData(APIView):
    
    authentication_classes = [Myauthentication]
    
    def post(self, request):
        
        s = NoticeSerializers(data=request.data)
        
        if not s.is_valid():
            # print("验证失败:",s.errors)
            return Response({"errors": s.errors}, status=400)
        else:
            ns = Notice.objects.create(**s.validated_data)
            s = NoticeSerializers(ns)
            return Response({"notices": s.data}, status=201)
    
    def get(self, request):
        # 获取所有的Notice数据
        
        notices = Notice.objects.all()
        s = NoticeSerializers(notices, many=True)
        # return Response(s.data, status=200)
        return Response({"notices": s.data}, status=200)

class NoticeDataDerail(APIView):
    
    authentication_classes = [Myauthentication]
    
    def post(self, request):

        s = NoticeSerializers(data=request.data)
        
        if not s.is_valid():
            # print("验证失败:",s.errors)
            return Response({"errors": s.errors}, status=400)
        else:
            ns = Notice.objects.create(**s.validated_data)
            s = NoticeSerializers(ns)
            return Response({"notices": s.data}, status=201)
    
    def get(self, request):
        # 获取单个Notice数据
        # print(userID)   
        userID = request.GET.get('id')
        
        # print("token:", token)
        # print("userID:", userID)

        # print("authentication_classes:", self.authentication_classes)
        # print("request.user:", request.user)
        # print("request.auth:", request.auth)
        
        if userID:
            try:
                notice = Notice.objects.filter(user=userID)
                s = NoticeSerializers(notice, many=True)
                return Response(s.data, status=200)
            except Notice.DoesNotExist:  
                return Response({"error": "找不到数据"}, status=404)
            
        else:
            try:
                notice = Notice.objects.all()
                s = NoticeSerializers(notice, many=True)
                return Response(s.data, status=200)
            except Notice.DoesNotExist:
                return Response({"error": "找不到数据"}, status=404)
    
    def put(self, request):
        # 更新单个Notice数据
        
        dataID = request.GET.get('dataid')
        if not dataID:
            return Response({"error": "未提供数据ID"}, status=400)
        
        try:
            notice = Notice.objects.get(pk=dataID)
            s = NoticeSerializers(notice, data=request.data)
            if s.is_valid():
                s.save()
                return Response(s.data, status=200)
            else:
                return Response({"errors": s.errors}, status=400)
        except Notice.DoesNotExist:
            return Response({"error": "找不到数据"}, status=404)
    def delete(self, request):
        # 删除单个Notice数据
        dataID = request.GET.get('dataid')
        if not dataID:
            return Response({"error": "未提供数据ID"}, status=400)
        try:
            notice = Notice.objects.get(pk=dataID)
            notice.delete()
            return Response({"message": "删除成功！"}, status=204)
        except Notice.DoesNotExist:
            return Response({"error": "找不到数据"}, status=404)
    
class sendEmail(APIView):
    
    def post(self, request):
        
        username = request.data.get('username')

        email = request.data.get('email')

        code = ''.join(random.sample(string.digits, k=6))
        
        try:
            send_mail(
                'Notice发来了验证码!!!',
                f'您的验证码是：{code}',
                from_email=None,
                recipient_list=[email]
            )
            
            emailData = {
                'username': username,
                'email': email,
                'code': code
            }
            EmailCode.objects.create(**emailData)
            
            return Response({"message": "验证码已发送"}, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=500)