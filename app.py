from fastapi import FastAPI, UploadFile, File
import uvicorn
import numpy as np
import cv2
import shutil

app = FastAPI()

@app.get("/")
def index():
    return{"Welcome to PAKPLANTS"}

@app.post("/percent")
def mask(file: UploadFile =File(...)):
    with open(f'{file.filename}' , "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    img= cv2.imread(file.filename) 
    grid_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV)
    lower_green = np.array([36 ,0 , 0])
    upper_green = np.array([102,255,255])
    mask= cv2.inRange(grid_HSV, lower_green, upper_green)
    green_perc = (np.sum(mask) / np.size(mask))/255
    green_perc = green_perc*100
    return{round(green_perc,3)}

if __name__ == "__main__":
    uvicorn.run(app, debug=True)


#        curl -X 'POST' \
#       'http://localhost:8000/percent' \
#      -H 'accept: application/json' \
#     -H 'Content-Type: multipart/form-data' \
#    -F 'file=@wh0051.jpg;type=image/jpeg'