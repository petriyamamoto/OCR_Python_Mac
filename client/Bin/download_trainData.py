from paddleocr import PPStructure
import cv2

table_engine = PPStructure(recovery=True)
image = cv2.imread('resource/fileicon.png')
result = table_engine(image)
