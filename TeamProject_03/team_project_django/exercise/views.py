from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UploadFileForm
from .models import ImgModel, UploadFile
import torch
import numpy as np
import pandas as pd
from io import BytesIO
from PIL import Image
import base64
from . import inference

# Create your views here.

def index(request):
    return render(request, 'exercise/index.html')

def upload(request):
      
    if request.method == 'GET':
        form = UploadFileForm() 
        return render(request, 'exercise/upload.html', {'form':form})
        
    elif request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            
            img_url = 'media/' + str(form.cleaned_data['file'])
            print("img_url : ", img_url)
            
            result_data = inference.inference(img_url)
            
            result = ImgModel()
            result.img_data = result_data['img_data']
            result.ex_class = result_data['ex_class']
            result.ex_name = result_data['ex_name']
            result.save()

            return redirect(reverse('exercise:image'))
    

def image(request):
    
    # 올린 원본 사진
    form = UploadFile.objects.last()
    print("파일 이름 :", form.file)

    # 라벨링 된 사진
    img = ImgModel.objects.last()
    img_data = img.img_data
    ex_class = img.ex_class
    ex_name = img.ex_name
    
    data_info = {
        'form' : form,
        'img_data' : img_data,
        'ex_class' : ex_class,
        'ex_name' : ex_name,
    }

    return render(request, 'exercise/image.html', data_info)



# def image(request):
    
#     form = UploadFile.objects.last()
#     print("파일 이름 :", form.file)
    
#     model = torch.hub.load('ultralytics/yolov5', 'custom', path='./exercise/deep_learning/best.pt', force_reload=True)
#     img = f"./media/{form.file}"
#     result = model(img)
    
#     result.save()
#     print("result : ", result)

#     result_name = result.pandas().xyxy[0].to_dict()
#     print("예측 결과 :", result_name)
#     name = result_name['name'][0]

#     context = {
#         'form' : form,
#         'name' : name,
#         'result' : result,
#     }
    
#     return render(request, 'exercise/image.html', context)





# def image(request):
  
#     # 모델 불러오기
#     model = torch.load("C:/Users/denni/Jupyter_Class/TeamProject_03/team_project_django/exercise/model/best.pt")
    
#     # 모델 추론 모드 설정
#     model.eval()
    
#     # 이미지 불러오기 (이미지 경로 / 이미지 이름.jpg)
#     image = cv2.imread("C:/Users/denni/OneDrive/바탕 화면/TeamProject_03/운동기구 사진/팀 수집 운동기구 자료 라벨링 진행/lat_pulldown/zdown_028.jpg")
    
#     # 이미지 사이즈 조정
#     resized_image = cv2.resize(image, (640, 640))
    
#     # 이미지 배열 초기화
#     image_tensor = np.zeros((1, 3, 640, 640), dtype=np.float32)
#     image_tensor[0] = torch.from_numpy(resized_image.transpose(2, 0, 1))
    
#     # 모델 입력 값 설정
#     model_input = (image_tensor.cuda(),)
    
#     # 모델 추론 실행
#     output = model(*model_input)
#     """
#     이제 모델을 추론한 결과인 output에서 추출하려는 객체를 찾을 수 있습니다.
#     출력값을 파싱하는 것은 자세한 모델 구조와 파라미터 등에 따라 다릅니다. 
#     YOLOv5에서는 output 변수의 형태를 (N, 6)로 가정합니다. 여기서 N은 이미지에서 추출한 객체의 수입니다. 
#     6개의 값은 [x, y, w, h, cls, conf]의 형태로, 이미지에서 추출한 객체의 좌표와 클래스 정보 등을 나타냅니다.
#     이제 이러한 값에서 본인이 원하는 객체의 정보를 추출하면 됩니다.
#     """
#     return render(request, 'exercise/image.html', {'output':output})