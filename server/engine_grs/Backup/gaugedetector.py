
import numpy as np
import cv2

class Gaugedetector:
    def __init__(self,image,savepath,savefileName):
        #self.m_image = Gaugedetector(image,savepath,savefileName)
        self.image = image
        self.savepath = savepath
        self.savefileName = savefileName

    def getoutput(self):
        if self.m_image == 0 :
            return False
        else :
            return True, self.m_image

    def gaugedetector(self):
        #print self.savepath+self.savefileName
        rgb_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        lower_blue = np.array([100,8,20])
        upper_blue = np.array([227, 100, 125])
        mask = cv2.inRange(rgb_img, lower_blue, upper_blue)
        #cv2.imshow("0", mask)
        #cv2.waitKey(0)
        contours, hierarchy  = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        mask2 = np.zeros(self.image.shape,np.uint8)
        max_area = 0
        max_area_cnt = 0
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if area > max_area :
                max_area = area
                max_area_cnt = cnt
        cv2.drawContours(mask2,[max_area_cnt],0,(255,255,255),-1)
        #cv2.imshow("1", mask2)
        #cv2.waitKey(0)
        point_x = 1000000
        point_y = 1000000
        mask_width = 0
        mask_hight = 0
        for ho in max_area_cnt:
            for p in ho:
                # set X, Y
                if p[0] < point_x :
                    point_x = p[0]
                if p[1] < point_y :
                    point_y = p[1]
                if p[0] > mask_width :
                    mask_width = p[0]
                if p[1] > mask_hight :
                    mask_hight = p[1]
        mask_width = mask_width - point_x
        mask_hight = mask_hight - point_y
        #mask_width_w = (mask_width * 5/3)-22 + mask_width
        #point_x = point_x - (mask_width * 5/3)+22
	mask_width_w = (mask_width * 2)-22 + mask_width
        point_x = point_x - (mask_width * 2)+22
	if (point_x < 0 ):
            point_x = 0
        crop_img = self.image[point_y:point_y+mask_hight-40, point_x:point_x+mask_width_w]
        cv2.imwrite(self.savepath+self.savefileName,crop_img,None)
        #cv2.imshow("0", image)
        #cv2.waitKey(0)
        #cv2.imshow("0", crop_img)
        #cv2.waitKey(0)
        return crop_img

    def Gaugedetector(path,filname):
        image = cv2.imread(path+filname)
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #cv2.imshow("0", rgb_img)
        #cv2.waitKey(0)
        lower_blue = np.array([100,8,20])
        upper_blue = np.array([227, 112, 125])
        mask = cv2.inRange(rgb_img, lower_blue, upper_blue)
        #cv2.imshow("0", mask)
        #cv2.waitKey(0)
        contours, hierarchy  = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        mask2 = np.zeros(image.shape,np.uint8)
        max_area = 0
        max_area_cnt = 0
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if area > max_area :
                max_area = area
                max_area_cnt = cnt

        cv2.drawContours(mask2,[max_area_cnt],0,(255,255,255),-1)
        #cv2.imshow("1", mask2)
        #cv2.waitKey(0)
        point_x = 1000000
        point_y = 1000000
        mask_width = 0
        mask_hight = 0
        for ho in max_area_cnt:
            for p in ho:
                # set X, Y
                if p[0] < point_x :
                    point_x = p[0]
                if p[1] < point_y :
                    point_y = p[1]
                if p[0] > mask_width :
                    mask_width = p[0]
                if p[1] > mask_hight :
                    mask_hight = p[1]
        mask_width = mask_width - point_x
        mask_hight = mask_hight - point_y
        mask_width_w = mask_width * 5/3 + mask_width
        point_x = point_x - (mask_width * 5/3)
        crop_img = image[point_y:point_y+mask_hight-40, point_x:point_x+mask_width_w]
        cv2.imwrite(path+'crop'+'out_'+filname,crop_img,None)
        #cv2.imshow("0", image)
        #cv2.waitKey(0)
        #cv2.imshow("0", crop_img)
        #cv2.waitKey(0)
        return crop_img
