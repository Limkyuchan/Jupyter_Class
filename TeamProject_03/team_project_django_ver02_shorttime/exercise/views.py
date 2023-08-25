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
        
        if form.is_valid():
            form.save()
            
            img_url = 'media/' + str(form.cleaned_data['file'])
            print("업로드한 img_url : ", img_url)
            
            result_data = inference.deep_inference(img_url)
            
            result = ImgModel()
            result.img_data = result_data['img_data']
            result.ex_class = result_data['ex_class']
            result.ex_name = result_data['ex_name']
            result.save()
            
            return redirect(reverse('exercise:image'))



def image(request):

    # 라벨링 된 사진
    img = ImgModel.objects.last()
    img_data = img.img_data
    ex_class = img.ex_class
    ex_name = img.ex_name
    print("라벨링 예측 값 :" , ex_class, ex_name )
    
    # 운동 순서(클래스)에 따른 운동 부위, 기구 이름름
    ex_part_list = ['팔', '허리', '등', '가슴', '가슴', '가슴', '엉덩이', '등', 
                    '허벅지', '허벅지', '허벅지', '어깨', '허벅지']  
    ex_name_list = ['암컬', '백 익스텐션', '케이블머신', '펙덱 플라이 머신', '체스트 프레스 머신', 
                    '어시스트 치닝 앤 디핑 머신', '힙 어브덕션', '랫 풀 다운', '레그 익스텐션', '레그 프레스',
                    '레그 컬 - 라잉', '숄더 프레스 - 머신', '스쿼트 - 스미스 머신']
    
    ex_pred_part = ex_part_list[ex_class]
    ex_pred_name = ex_name_list[ex_class]
        
    print('ex_pred_part 예측 값: ', ex_pred_part)
    print('ex_pred_name 예측 값: ', ex_pred_name)
        
    # 예측한 이미지 객체와 객체의 이름, id값
    predict_name = Exercise.objects.get(ex_name = ex_pred_name)
    pre_index = predict_name.id
    pre_name = predict_name.ex_name

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
        'img_data' : img_data,
        'predict_name' : predict_name,
        'zip_data' : zip_data,
    }
    
    return render(request, 'exercise/image.html', context)


def machine_model(request, id):

    ex_detail = Exercise.objects.get(id=id)
    ex_method = ex_detail.ex_method
    ex_method = ex_method.replace(". ",".<br>")
    context = {
        'ex_detail' : ex_detail,
        'ex_method' : ex_method,
    }

    return render(request, 'exercise/machine.html', context)



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

