from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework import serializers

from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt

from .models import Notice

# Create your views here.

def adds(request):
    return render(request, "add.html")

class NoticeSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Notice
        fields = ['id', 'text']
    
    
class NoticeData(APIView):
    
    def post(self, request):
        
        s = NoticeSerializers(data=request.data)
        
        print(request.data)
        
        if not s.is_valid():
            print("验证失败:",s.errors)
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
    
    def get(self, request, pk):
        # 获取单个Notice数据
        try:
            notice = Notice.objects.get(pk=pk)
            s = NoticeSerializers(notice)
            return Response(s.data, status=200)
        except Notice.DoesNotExist:
            return Response({"error": "找不到数据"}, status=404)
    
    def put(self, request, pk):
        # 更新单个Notice数据
        try:
            notice = Notice.objects.get(pk=pk)
            s = NoticeSerializers(notice, data=request.data)
            if s.is_valid():
                s.save()
                return Response(s.data, status=200)
            else:
                return Response({"errors": s.errors}, status=400)
        except Notice.DoesNotExist:
            return Response({"error": "找不到数据"}, status=404)
    def delete(self, request, pk):
        # 删除单个Notice数据
        try:
            notice = Notice.objects.get(pk=pk)
            notice.delete()
            return Response({"message": "删除成功！"}, status=204)
        except Notice.DoesNotExist:
            return Response({"error": "找不到数据"}, status=404)


