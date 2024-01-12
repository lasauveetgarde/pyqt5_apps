#!/usr/bin/env python3
import rospy
import cv2
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import numpy as np

class image_converter:
    
    def __init__(self) -> None:
        rospy.init_node('video_frame', anonymous=True)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/rs_camera/color/image_raw/compressed",CompressedImage ,self.callback)
        self.image = np.zeros((480, 640, 3), dtype='uint8')
        self.dst_folder = rospy.get_param('~dst_folder','test_folder')
        self.rate = rospy.Rate(15)
        
    def callback(self,data):
        try:
            # print ('received image of type: "%s"' % data.format)
            np_arr = np.fromstring(data.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            cv2.imshow('win',cv_image)
            cv2.waitKey(1)
        except CvBridgeError as e:
            print(e)
        self.image = cv_image

if __name__ == '__main__':
    try:   
        reciev_image = image_converter()
        rate = reciev_image.rate
        while not rospy.is_shutdown():
            frame = reciev_image.image 
    except Exception as e:
      rospy.loginfo(f'EXCEPTION CATCHED:\n {e}')
