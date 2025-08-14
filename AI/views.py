from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import ChatTable
from rest_framework import status
from app.models import LoginData
from lessonTable.models import LessonTable
from openai import OpenAI
from dotenv import load_dotenv
from django.http import StreamingHttpResponse

# Create your views here.

def chat(request):
    
    return render(request, "chat.html")

class ChatSerializer(serializers.Serializer):
    
    class Meta:
        model = ChatTable
        fields = '__all__'
        
class LessonSerializer(serializers.ModelSerializer):   
    
    class Meta:
        model = LessonTable
        fields = '__all__'

class chat_ai(APIView):
    
    def generate(self, prompt):
        client = OpenAI(api_key= "sk-fvincrhushambjtzxemtssjzqkgvqobctfjvvjlhcuvstyrm", base_url="https://api.siliconflow.cn/v1")
        response = client.chat.completions.create(  
            model="Pro/Qwen/Qwen2-7B-Instruct",  
            messages=[
                {"role": "system", "content": "你是我的智能学生助手这个系统的ai助手"},
                {"role": "user",  "content": prompt},
                
            ],  
            temperature=0.7,  
            max_tokens=4096,
            stream = True,
            extra_body={
                "thinking_budget": 1024
            },
        ) 

        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
                
    
    def post(self, request):
        
        userID = request.GET.get('id')
        
        try:
            user_instance = LoginData.objects.get(id=userID)
            print("user_instance:\n", user_instance)
        except LoginData.DoesNotExist:
            return StreamingHttpResponse({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        prompt = request.data.get('prompt')
        
        if not prompt:
            return Response({"status": "error", "error": "没有输入"}, status=400)
        
        # prompt = serializer.validated_data.question
        
        try:
        
            return StreamingHttpResponse(self.generate(prompt), content_type="text/event-stream")
            
            # ChatTable.objects.create(
                
            #     user = userID
            # )
            
            # res = response.choices[0].message.content
            
            # res = ' '.join(res.split())
            
            # print("response:", res)
            
            # return Response({
            #     "status": "success",
            #     "response": res
            # })
        except Exception as e:
            
            return Response({"error": str(e)}, status=500)
        
    def get(self, request):
        
        userID = request.GET.get('id')
        
        if userID:
            try:  
                d = ChatTable.objects.filter(user=userID)
                
                serializer = ChatSerializer(instance=d, many=True)
                
                return Response(serializer.data,status=200)

            except ChatTable.DoesNotExist:
                return Response({"error": "找不到数据"}, status=404)
            
            