#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import datetime
import numpy as np
import os

font = cv2.FONT_HERSHEY_SIMPLEX
gb = 1073741824
desired_size = 0.25 * gb


class image_converter:
    
    def __init__(self) -> None:
        rospy.init_node('video_frame', anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/rs_camera/color/image_raw/compressed",CompressedImage ,self.callback)
        self.image = np.zeros((480, 640, 3), dtype='uint8')
        self.dst_folder = rospy.get_param('~dst_folder','test_folder') # the name of the base frame of the robot
        self.rate = rospy.Rate(15)
        
    def callback(self,data):
        try:
            # cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
            # newimg = self.bridge.compressed_imgmsg_to_cv2(data)
            print ('received image of type: "%s"' % data.format)
            np_arr = np.fromstring(data.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            cv2.imshow('win',cv_image)
            cv2.waitKey(1)
        except CvBridgeError as e:
            print(e)
        # cv_image = cv2.resize(cv_image,(640,480),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        self.image = cv_image

if __name__ == '__main__':
    try:
        
        reciev_image = image_converter()
        rate = reciev_image.rate
        
        current_date = datetime.datetime.now()
        current_date = current_date.strftime('%d-%m-%y_%H-%M-%S')
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        directory = f'/home/work/{reciev_image.dst_folder}/'

        path = os.path.join(directory, current_date)
        os.mkdir(path)

        out = cv2.VideoWriter(path +'/agv_video.mp4',
                            fourcc, 15.0, (640, 480))
        rospy.loginfo(f'\n\trecord started to {path} directory\n')    

        while not rospy.is_shutdown():
                
            frame = reciev_image.image 
            current_date = datetime.datetime.now()
            current_date_string = current_date.strftime('%d-%m-%y %H:%M:%S')

            storage_size = os.path.getsize(path +'/agv_video.mp4')
            # print(storage_size)
            
            frame = cv2.putText(frame,current_date_string,(50, 50),font, 1 ,(255,255,255), 4) 

            if storage_size <= desired_size:
                out.write(frame)
            else:
                print('Trigerred new file')
                out.release()
                current_date = datetime.datetime.now()
                current_date = current_date.strftime('%d-%m-%y_%H-%M-%S')
                fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

                directory = f'/home/hp-pc/{reciev_image.dst_folder}/'

                path = os.path.join(directory, current_date)
                os.mkdir(path)

                out = cv2.VideoWriter(path +'/agv_video.mp4',
                    fourcc, 15.0, (640, 480))

            rate.sleep()

        out.release() 
        rospy.loginfo(f'\n\tvideo saved to {path} directory\n')


    except Exception as e:
      rospy.loginfo(f'EXCEPTION CATCHED:\n {e}')
        # cv2.destroyAllWindows()