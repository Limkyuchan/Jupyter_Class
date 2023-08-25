import torch
import pandas as pd
from PIL import Image

model = torch.hub.load('ultralytics/yolov5', 'custom', path='./exercise/deep_learning/best.pt')
img = "media/zback_extension_05.jpg"
result = model(img)

result.print()
result.show()
