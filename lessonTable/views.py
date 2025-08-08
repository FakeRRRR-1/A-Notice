from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime #获取本地时间
from rest_framework import serializers
from .models import LessonTable
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from app.models import LoginData
import openpyxl
import pandas as pd
import io
import re #导入正则表达式

# Create your views here.
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

def adds(request):
    return render(request, "lessonTable.html")

class LessonSerializer(serializers.ModelSerializer):   
    
    class Meta:
        model = LessonTable
        fields = '__all__'
    
class UploadExcelView(APIView):
    
    authentication_classes = [Myauthentication]
    
    def post(self, request, *args, **kwargs):
        
        userID = request.GET.get('id')
        
        try:
            user_instance = LoginData.objects.get(id=userID)
        except LoginData.DoesNotExist:
            return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        if 'file' not in request.FILES:
            return Response({"error": "请上传文件"}, status=status.HTTP_400_BAD_REQUEST)
        
        # print("request", request.data)
        
        try:
            weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
            Month = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
            MonthDay = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
            start_time = ['8:00','10:00','13:00','14:50','16:40','18:30']
            
            excel_file = request.FILES.get('file')
            time = request.data.get('start_date')
            currentTime = datetime.now()
            
            time = time.split(' ')
            time[1] = Month[time[1]];time[2] = int(time[2]);time[3] = int(time[3])
            startTime = datetime(time[3], time[1], time[2])                             # 学期开始的时间
            
            nowweek = 1  # 周次
            
            print("nowweek:", nowweek)
            
            if excel_file.name.endswith('.xls'):
                engine = 'xlrd'
            elif excel_file.name.endswith('.xlsx'):
                engine = 'openpyxl'
            df = pd.read_excel(excel_file, engine=engine, dtype=str, na_filter=True, header=None)
            
            df = df.where(pd.notnull(df), None)
            
            print("df:\n", df)
            
            print("df.iloc:\n", df.iloc[2, 2])
            
            lesson = []
            for col in range(2,9):                                  # 获取excel表格中课程数据
                daily_lesson = {}
                for row in range(2,8):
                    if weekdays[col-2] not in daily_lesson:
                        daily_lesson[weekdays[col-2]] = []
                    daily_lesson[weekdays[col-2]].append(df.iloc[row, col])
                
                lesson.append(daily_lesson)
                
            print("lesson:\n", lesson[0][weekdays[0]])   
                 
            for week in range(1,21):                                # 遍历课程数据 将数据存储进数据库中
                
                for day_idx in range(7):
                    time_slots = lesson[day_idx][weekdays[day_idx]]            # 获取周一的所有课程
                    for slot_idx in range(6):                                  # 一天有六节课，遍历六节课
                        slot_data = time_slots[slot_idx]
                        
                        if not slot_data:
                            continue
                        
                        for course_entry in slot_data.split('\r\n'):
                            
                            course_entry = course_entry.strip()       #去掉首位字符串的空字符
                            
                            week_time = re.findall(r'(\d+(?:-\d+)?周)',course_entry)
                            
                            # print("week_time", week_time)
                            
                            for week_str in week_time:
                                
                                week_range = week_str[:-1]
                                
                                if self._is_week_in_range(week, week_range):
                                    
                                    # print(f"匹配成功: 周次 {nowweek} ∈ {week_range}")
                                    
                                    # course_entry示例：示例：计算机网络/(1-2节)5周/ LXA202/李芳
                                    try:
                                        course_name = course_entry.split('/')[0]                    
                                        location = course_entry.split('/')[2].strip()
                                        teacher = course_entry.split('/')[3].split(',')[0].strip()
                                        if slot_idx <=2:
                                            day_time = 1
                                            
                                        elif slot_idx <=4:
                                            day_time = 2
                                            
                                        else:
                                            day_time = 3
                                            
                                        LessonTable.objects.create(
                                            week=week,
                                            day=weekdays[day_idx],
                                            lesson=course_name,
                                            start_time=start_time[slot_idx],
                                            day_time=day_time,
                                            startime=startTime,
                                            user=user_instance,
                                            location=location,
                                            teacher=teacher,
                                        )
                                    except Exception as e:
                                        print(f"解析课程失败: {course_entry}, 错误: {e}")
            return Response({"success": "课程数据已处理"},status=status.HTTP_200_OK)                                                   
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request, *args, **kwargs):
        
        d = LessonTable.objects.all()
        
        serializer = LessonSerializer(instance=d, many=True)
        
        return Response(serializer.data)
    
    def _is_week_in_range(self, current_week, week_range_str):
        """检查当前周是否在指定的周范围内（如'1-2'、'5'）"""
        if '-' in week_range_str:
            start, end = map(int, week_range_str.split('-'))
            return start <= current_week <= end
        else:
            return current_week == int(week_range_str)
            