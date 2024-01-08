from endustry.edge_post import EdgePost
import cv2

img = cv2.imread("apitest.jpg")

url = "http://172.27.254.2:57306"
EPOD = EdgePost(img, url, mode="OD")
output = EPOD.post()

print(output)