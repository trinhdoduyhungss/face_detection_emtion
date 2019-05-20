from django.shortcuts import render

### Initializing the imports

import dlib
from skimage import io
from math import sqrt
import cv2
from django.views.decorators.csrf import csrf_exempt


from django.http import JsonResponse
# define the path to the face detector which would be an xml file that comes installed with haarcascades
# find it here -> https://github.com/opencv/opencv/tree/master/data/haarcascades
# download and save it in your project repository
# define the face detector now

face_detector = "C:/Users/DELL/PycharmProjects/face-detection-opencv-api-master/haarcascade_frontalface_default.xml"
# start off with defining a function to detect the URL requested which has the image for facial recognition
@csrf_exempt

def requested_url(request):
    #default value set to be false

    hog_face_detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('face_detector/shape_predictor_68_face_landmarks.dat')
    default = {"safely executed": False} #because no detection yet

    ## between GET or POST, we go with Post request and check for https

    if request.method == "POST":
        if request.FILES.get("image", None) is not None:

            image_to_read = read_image(stream = request.FILES["image"])


        else: # URL is provided by the user
            url_provided = request.POST.get("url", None)


            if url_provided is None:
                default["error_value"] = "There is no URL Provided"

                return JsonResponse(default)

            image_to_read = read_image(url=url_provided)


        image_to_read = cv2.cvtColor(image_to_read, cv2.COLOR_BGR2GRAY)
        values =[]
        lines = []
        faces_hog = hog_face_detector(image_to_read, 1)
        landmark = predictor(image_to_read, faces_hog[0])
        for face in faces_hog:
            x = face.left()
            y = face.top()
            w = face.right() - x
            h = face.bottom() - y
            for k, d in enumerate(landmark.parts()):
                if (k >= 60 and k <= 68):
                    lines.append((d.x, d.y))
            # tìm điểm trung bình line
            x_line = round((lines[4][0] + lines[0][0]) / 2)
            y_line = round((lines[4][1] + lines[0][1]) / 2)

            # tính toán khoảng cách
            u_x = (lines[2][0] - x_line) * (lines[2][0] - x_line)
            u_y = (lines[2][1] - y_line) * (lines[2][1] - y_line)

            d_x = (lines[6][0] - x_line) * (lines[6][0] - x_line)
            d_y = (lines[6][1] - y_line) * (lines[6][1] - y_line)
            if sqrt(u_x + u_y) < sqrt(d_x + d_y):
                values.append((x,y,w,h,'Happy'))
            elif sqrt(u_x + u_y) > sqrt(d_x + d_y):
                if sqrt(u_x + u_y) - sqrt( d_x + d_y) >= 1:
                    values.append((x, y, w, h, 'Sad'))
                else:
                    values.append((x, y, w, h, 'Normal'))
        default.update({"#of_faces": len(values),
                        "faces":values,
                        "safely_executed": True })

    return JsonResponse(default)

def read_image(path=None, stream=None, url=None):

    ##### primarily URL but if the path is None
    ## load the image from your local repository

    if path is not None:
        image = cv2.imread(path)

    else:
        if url is not None:

            image = io.imread(url)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif stream is not None:
            #implying image is now streaming
            data_temp = stream.read()


    return image











