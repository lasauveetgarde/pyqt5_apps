import cv2
import datetime
import os 
capture = cv2.VideoCapture(0)
 
fourcc = cv2.VideoWriter_fourcc('X','V','I','D')
video_timestamp = datetime.datetime.now().strftime("%Y%m%d")
folder_name = ('Результаты' + '/' + 'Видео' + '/' + video_timestamp)
os.makedirs(folder_name, exist_ok=True)
videoWriter = cv2.VideoWriter(folder_name + '/video.mp4', fourcc, 30.0, (640,480)) 
while (True):
 
	ret, frame = capture.read()
	 
	if ret:
		cv2.imshow('video', frame)
		videoWriter.write(frame)
 
	if cv2.waitKey(1) == 27:
		break
 
capture.release()
videoWriter.release()
 
cv2.destroyAllWindows()