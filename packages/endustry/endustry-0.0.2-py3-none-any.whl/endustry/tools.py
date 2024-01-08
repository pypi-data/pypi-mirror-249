import cv2
import base64


def im_to_base64(img):
    """transform image to base64 style"""
    _, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = base64.b64encode(buffer)

    return jpg_as_text.decode('utf-8')
