from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openpyxl
import pandas as pd
import io

# Create your views here.

def adds(request):
    return render(request, "lessonTable.html")

class UploadExcelView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        excel_file = request.FILES.get('file')
        if not excel_file:
            return Response({"error": "请上传文件"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if excel_file.name.endswith('.xls'):
                engine = 'xlrd'
            else:
                engine = 'openpyxl'
        try:
            df = pd.read_excel(excel_file, engine=engine, dtype=str, na_filter=True)
            df = df.where(pd.notnull(df), None)  # 将 NaN 替换为 None
            
            data = df.to_dict('records')  # 转换为字典列表
            
            return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "请上传文件"}, status=status.HTTP_400_BAD_REQUEST)

        print("request.FILES:", request.data)
        try:
            print("!")
            excel_file = request.FILES.get('file')
            print("excel_file.name:", excel_file.name)
            # 使用 pandas 读取 Excel
            
            if excel_file.name.endswith('.xls'):
                engine = 'xlrd'
            elif excel_file.name.endswith('.xlsx'):
                engine = 'openpyxl'
            df = pd.read_excel(excel_file, engine=engine, dtype=str, na_filter=True)
            
            df = df.where(pd.notnull(df), None)
            
            print("df:", df)
            
            data = df.to_dict('records')  # [{'列名1': 值1, '列名2': 值2}, ...]
            
            return Response({"status": "success","data": data,}, status=status.HTTP_200_OK)
        except Exception as e:
            
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)