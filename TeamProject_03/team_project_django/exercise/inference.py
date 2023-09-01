from PIL import Image
import torch
import base64
import io
import joblib
import pandas as pd
import sqlite3


# 딥 러닝 모델 
def deep_inference(img):
    
    try:
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='exercise/deep_learning/best.pt', force_reload=True)
        img = Image.open(img)
        
        results = model(img, size=640)
        result = results.pandas().xyxy[0].to_numpy()
        
        if len(result) != 0:
            ex_per = result[0][4]      # 기구 예측 확률 결과
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
                'ex_per' : ex_per,
                'ex_class' : ex_class,
                'ex_name' : ex_name,
                'img_data' : encoded_img,
            }
            return data
        else:
            return 1
        
    except:
        print("딥 러닝 모델 학습 중 오류발생!")
    

# 머신 러닝 모델
def machine_inference(part):
    
    # db에 저장된 csv 내용 가져오기
    con = sqlite3.connect("db.sqlite3")
    df = pd.read_sql("SELECT * FROM exercise_exercise", con, index_col="id")
    pd.set_option('display.max_colwidth', None)
    
    # 파일로 저장된 머신러닝 모델 활용
    exercise_weight = joblib.load('exercise/machine_learning/exercise_weight.pkl')
    sorted_ind = exercise_weight.argsort()[:, ::-1]
    
    name_title = df[df['ex_part'] == part]
    name_index = name_title.index.values
    index = sorted_ind[name_index]
    index = index.reshape(-1)

    return df.iloc[index][:6]

        
    # try:
    #     # db에 저장된 csv 내용 가져오기
    #     con = sqlite3.connect("db.sqlite3")
    #     df = pd.read_sql("SELECT * FROM exercise_exercise", con, index_col="id")
    #     pd.set_option('display.max_colwidth', None)
        
    #     # 파일로 저장된 머신러닝 모델 활용
    #     exercise_weight = joblib.load('exercise/machine_learning/exercise_weight.pkl')
    #     sorted_ind = exercise_weight.argsort()[:, ::-1]
        
    #     name_title = df[df['ex_part'] == part]
    #     name_index = name_title.index.values
    #     index = sorted_ind[name_index]
    #     index = index.reshape(-1)
    #     print("111111", df.iloc[id][:6])
    #     print("222222", df.iloc[index][:6])
        
    #     return df.iloc[index][:6]
    
    # except:
    #     print("머신 러닝 모델 학습 중 오류발생!")