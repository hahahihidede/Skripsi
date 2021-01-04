import cv2

vid = cv2.VideoCapture("./vp.mp4")
d = 0
ret, frame = vid.read()

while ret:
    ret, frame = vid.read()
    filename = "bukti/file_%d.png"%d
    cv2.imwrite(filename, frame)
    d+=1
