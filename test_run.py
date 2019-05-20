import cv2, requests
url = " http://apifacedetecemotion.herokuapp.com/face_detection/detect/"
##### image 1 #####
image_to_read = cv2.imread("nguyen.jpg") #dowload hình ảnh test về máy, lưu vào thư mục face-detection-opencv-api-master
tracker = {"url": "https://scontent.fdad4-1.fna.fbcdn.net/v/t1.0-9/57387308_414195376035110_5106852200982773760_n.jpg?_nc_cat=109&_nc_oc=AQk9uoRKmcPbbaN1OUxkmAXfIN72SciFrbwv7dIo29v3dunVVyczaiEaiqmN-24fqzY&_nc_ht=scontent.fdad4-1.fna&oh=ea04d6de303f5bf622292da7127010ca&oe=5D633F52"}
req = requests.post(url, data=tracker).json()
print
"image3.png: {}".format(req)


for (x,y,w,h,txt) in req["faces"]:
    print(x)
    print(y)
    print(w)
    print(h)
    cv2.rectangle(image_to_read,(x,y), (x+w,y+h), (0, 255, 0), 2)
    cv2.putText(image_to_read, txt, (x, y), fontFace=cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, fontScale=0.8, color=(0, 0, 255))
cv2.imshow("image1.jpg", image_to_read)
cv2.waitKey(0)
