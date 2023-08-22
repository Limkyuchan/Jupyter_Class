from PIL import Image
import torch
import base64
import io
import joblib


# 딥 러닝 모델 
def inference(img):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='exercise/deep_learning/best.pt', force_reload=True)
    img = Image.open(img)
    
    results = model(img, size=640)
    result = results.pandas().xyxy[0].to_numpy()
    
    if len(result) != 0:
        ex_class = result[0][5]    # 운동 클래스 번호
        ex_name = result[0][6]     # 예측한 운동 이름
        
        results.ims        # 추론을 위해 모델에 전달된 원본 이미지 배열
        results.render()   # 결과 업데이트
        
        for img in results.ims:
            buffered = io.BytesIO()
            img_base64 = Image.fromarray(img)
            img_base64.save(buffered, format='JPEG')
            encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')   # base64 인코딩된 이미지
            
        data = {
            'ex_class' : ex_class,
            'ex_name' : ex_name,
            'img_data' : encoded_img,
        }
        
        return data
    
    else:
        return 1
    

# 머신 러닝 모델 (운동 이름으로 예측)
def find_exercise_name(exercise, name):
    
    exercise_weight = joblib.load('exercise/machine_learning/exercise_weight.pkl')
    exercise_sorted_ind = exercise_weight.argsort()[:, ::-1]
    
    name_title = exercise[exercise['운동 이름'] == name]
    name_index = name_title.index.values
    similar_indexes = exercise_sorted_ind[name_index, :6]
    similar_indexes = similar_indexes.reshape(-1)
    
    return exercise.iloc[similar_indexes][:6]