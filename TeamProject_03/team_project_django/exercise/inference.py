from PIL import Image
import torch
import base64
import io

def inference(img):
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='exercise/deep_learning/best.pt', force_reload=True)
    img = Image.open(img)
    
    results = model(img, size=640)
    result = results.pandas().xyxy[0].to_numpy()
    
    if len(result) != 0:
        ex_class = result[0][5]
        ex_name = result[0][6]
        
        results.ims
        results.render()
        
        for img in results.ims:
            buffered = io.BytesIO()
            img_base64 = Image.fromarray(img)
            img_base64.save(buffered, format='JPEG')
            encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
        data = {
            'ex_class' : ex_class,
            'ex_name' : ex_name,
            'img_data' : encoded_img,
        }
        
        return data
    
    else:
        return 1