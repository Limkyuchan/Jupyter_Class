from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UploadFileForm
from .models import ImgModel, UploadFile, Exercise
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
        form.save()
        form_image = UploadFile.objects.last()
        return render(request, 'exercise/upload.html', {'form_image':form_image})
 
 
def predict(request):

    form = UploadFile.objects.last()    
    img_url = 'media/' + str(form.file)
    print("업로드한 img_url : ", img_url)
    
    result_data = inference.deep_inference(img_url)
    
    result = ImgModel()
    result.img_data = result_data['img_data']
    result.ex_class = result_data['ex_class']
    result.ex_name = result_data['ex_name']
    result.save()
    
    img = ImgModel.objects.last()
    img_data = img.img_data
    ex_class = img.ex_class
    ex_name = img.ex_name
    print("라벨링 예측 값 :" , ex_class, ex_name )
    
    ex_part_list = ['팔', '허리', '등', '가슴', '가슴', '가슴', '엉덩이', '등', '허벅지', '허벅지', '허벅지', 
                    '어깨', '허벅지']   # 운동 순서(클래스)에 따른 운동 부위
    ex_name_list = ['암컬', '백 익스텐션', '케이블머신', '체스트 프레스 머신', '어시스트 치닝 앤 디핑 머신', 
                '힙 어브덕션', '랫 풀 다운', '레그 익스텐션', '레그 컬 - 라잉', '펙덱 플라이 머신', 
                '레그 프레스', '숄더 프레스 - 머신', '스쿼트 - 스미스 머신']
    
    ex_pred_part = ex_part_list[ex_class]
    ex_pred_name = ex_name_list[ex_class]
    
    print('ex_pred_part 예측 값: ', ex_pred_part)
    print('ex_pred_name 예측 값: ', ex_pred_name)
    
    predict_name = Exercise.objects.get(ex_name = ex_pred_name)

    mac_predict = inference.machine_inference(ex_pred_part)
    
    name = mac_predict.ex_name.tolist()
    index = mac_predict.index.tolist()
    zip_data = zip(name, index)
    
    context = {
        'img_data' : img_data,
        'predict_name' : predict_name,
        'mac_predict' : mac_predict,
        'zip_data' : zip_data,
        'index' : index,
    }
    return render(request, 'exercise/predict.html', context)
        

def detail(request, id):
    
    ex_detail = Exercise.objects.get(id=id)
    context = {
        'ex_detail' : ex_detail
    }

    return render(request, 'exercise/detail.html', context)



def image(request):
    
    # 올린 원본 사진
    form = UploadFile.objects.last()
    print("파일 이름 :", form.file)

    # 라벨링 된 사진
    img = ImgModel.objects.last()
    img_data = img.img_data
    ex_class = img.ex_class
    ex_name = img.ex_name
    print("라벨링 예측 값 :" , ex_class, ex_name )
    
    ex_list = ['팔', '허리', '등', '가슴', '가슴', '가슴', '엉덩이', '등', '허벅지', '허벅지', '허벅지', 
               '어깨', '허벅지']   # 운동 순서(클래스)에 따른 운동 부위
    
    ex_pred = ex_list[ex_class]
    print('ex_pred 예측 값: ', ex_pred)
    
    predict = inference.machine_inference(ex_pred)
    
    name = predict['ex_name'].tolist()
    part = predict['ex_part'].tolist()
    method = predict['ex_method'].tolist()
    
    zip_data = zip(name, part, method)
    
    context = {
        'form' : form,
        'img_data' : img_data,
        'ex_class' : ex_class,
        'ex_name' : ex_name,
        'zip_data' : zip_data,
    }
    
    return render(request, 'exercise/image.html', context)


def machine_model(request):

    predict = inference.machine_inference("등")
    
    name = predict['ex_name'].tolist()
    part = predict['ex_part'].tolist()
    method = predict['ex_method'].tolist()
    zip_data = zip(name, part, method)
    
    context = {
        'zip_data' : zip_data,
    }

    return render(request, 'exercise/machine.html', context)








# def upload(request):
      
#     if request.method == 'GET':
#         form = UploadFileForm() 
#         return render(request, 'exercise/upload.html', {'form':form})
        
#     elif request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
        
#         if form.is_valid():
#             form.save()
            
#             img_url = 'media/' + str(form.cleaned_data['file'])
#             print("업로드한 img_url : ", img_url)
            
#             result_data = inference.deep_inference(img_url)
            
#             result = ImgModel()
#             result.img_data = result_data['img_data']
#             result.ex_class = result_data['ex_class']
#             result.ex_name = result_data['ex_name']
#             result.save()
            
#             form_image = UploadFile.objects.last()

#             return render(request, 'exercise/upload.html', {'form_image':form_image})
#             # return redirect(reverse('exercise:image'))


# def image(request):
    
#     # 올린 원본 사진
#     form = UploadFile.objects.last()
#     print("파일 이름 :", form.file)

#     # 라벨링 된 사진
#     img = ImgModel.objects.last()
#     img_data = img.img_data
#     ex_class = img.ex_class
#     ex_name = img.ex_name
#     print("라벨링 예측 값 :" , ex_class, ex_name )
    
#     ex_list = ['팔', '허리', '등', '가슴', '가슴', '가슴', '엉덩이', '등', '허벅지', '허벅지', '허벅지', 
#                '어깨', '허벅지']   # 운동 순서(클래스)에 따른 운동 부위
    
#     ex_pred = ex_list[ex_class]
#     print('ex_pred 예측 값: ', ex_pred)
    
#     predict = inference.machine_inference(ex_pred)
    
#     name = predict['ex_name'].tolist()
#     part = predict['ex_part'].tolist()
#     method = predict['ex_method'].tolist()
    
#     zip_data = zip(name, part, method)
    
#     context = {
#         'form' : form,
#         'img_data' : img_data,
#         'ex_class' : ex_class,
#         'ex_name' : ex_name,
#         'zip_data' : zip_data,
#     }
    
#     return render(request, 'exercise/image.html', context)


# def machine_model(request):

#     predict = inference.machine_inference("등")
    
#     name = predict['ex_name'].tolist()
#     part = predict['ex_part'].tolist()
#     method = predict['ex_method'].tolist()
#     zip_data = zip(name, part, method)
    
#     context = {
#         'zip_data' : zip_data,
#     }

#     return render(request, 'exercise/machine.html', context)
















# def image(request):
    
#     form = UploadFile.objects.last()
#     print("업로드 파일 이름 :", form.file)
    
#     model = torch.hub.load('ultralytics/yolov5', 'custom', path='./exercise/deep_learning/best.pt', force_reload=True)
#     img = f"./media/{form.file}"
#     result = model(img)
    
#     result.save()
#     print("딥러닝 학습 결과 : ", result)

#     result_name = result.pandas().xyxy[0].to_dict()
#     print("운동기구 예측 결과 :", result_name)
#     name = result_name['name'][0]   # 예측한 운동기구 이름

#     context = {
#         'form' : form,        # 파일 이름
#         'name' : name,        # 운동기구 이름
#         'result' : result,    # 학습 결과
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