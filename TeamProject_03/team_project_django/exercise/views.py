from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UploadFileForm
from .models import ImgModel, Exercise
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
            print("업로드한 img_url (Upload): ", img_url)
            
            result_data = inference.deep_inference(img_url)
            
            # 운동기구 사진이 아닐 때
            if result_data == 1:
                form = UploadFileForm()
                context = {
                    'form' : form,
                    'alert_message' : "운동 사진 업로드바람",
                }
                return render(request, 'exercise/upload.html', context)
            
            # 운동기구 사진일 때
            else:
                result = ImgModel()
                result.img_data = result_data['img_data']
                result.ex_class = result_data['ex_class']
                result.ex_name = result_data['ex_name']
                result.ex_per = result_data['ex_per']
                result.save()
                
                return redirect(reverse('exercise:predict'))


def predict(request):

    # 라벨링 된 사진
    img = ImgModel.objects.last()
    img_data = img.img_data
    ex_class = img.ex_class
    ex_name = img.ex_name
    ex_per = int(round(img.ex_per, 2) * 100)
    print("라벨링 예측 값 (Predict): " , ex_class, ex_name, ex_per )
    
    # 운동 순서(클래스)에 따른 운동 부위, 기구 이름름
    ex_part_list = ['팔', '허리', '등', '가슴', '가슴', '가슴', '엉덩이', '등', 
                    '허벅지', '허벅지', '허벅지', '어깨', '허벅지']  
    ex_name_list = ['암컬', '백 익스텐션', '케이블머신', '펙덱 플라이 머신', '체스트 프레스 머신', 
                    '어시스트 치닝 앤 디핑 머신', '힙 어브덕션', '랫 풀 다운', '레그 익스텐션', '레그 프레스',
                    '레그 컬 - 라잉', '숄더 프레스 - 머신', '스쿼트 - 스미스 머신']
    
    ex_pred_part = ex_part_list[ex_class]
    ex_pred_name = ex_name_list[ex_class]
        
    print('이름 예측 값 (Predict): ', ex_pred_name)
    print('부위 예측 값 (Predict): ', ex_pred_part)
        
    # 예측한 이미지 객체의 값들
    predict_result = Exercise.objects.get(ex_name = ex_pred_name)
    pre_index = predict_result.id
    pre_name = predict_result.ex_name
    pre_video1 = predict_result.ex_video1
    pre_video2 = predict_result.ex_video2
    pre_text = predict_result.ex_method
    pre_text = pre_text.replace(". ", ".<br>")

    # 머신러닝 모델 학습
    mac_predict = inference.machine_inference(ex_pred_part)

    name_predict = mac_predict.ex_name.tolist()
    index_predict = mac_predict.index.tolist()
    
    name = []
    index = []
    
    for i, j in zip(name_predict, index_predict):
        if i == pre_name or j == pre_index:
            continue
        else:
            name.append(i)
            index.append(j)
                
    zip_data = zip(name, index)
    
    context = {
        'ex_per' : ex_per, 
        'img_data' : img_data,
        'predict_result' : predict_result,
        'zip_data' : zip_data,
        'pre_video1' : pre_video1,
        'pre_video2' : pre_video2,
        'pre_text' : pre_text,
    }
    
    return render(request, 'exercise/predict.html', context)


def recommend(request, id):

    # 추천 운동 객체의 값들
    ex_detail = Exercise.objects.get(id=id)
    ex_video1 = ex_detail.ex_video1
    ex_video2 = ex_detail.ex_video2
    ex_text = ex_detail.ex_method
    ex_text = ex_text.replace(". ",".<br>")
    
    context = {
        'ex_detail' : ex_detail,
        'ex_text' : ex_text,
        'ex_video1' : ex_video1,
        'ex_video2' : ex_video2,
    }

    return render(request, 'exercise/recommend.html', context)