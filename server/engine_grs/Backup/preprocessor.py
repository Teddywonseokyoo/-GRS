import numpy as np
import cv2

class Preprocessor:
    def __init__(self,image,savepath,savefileName):
        self.image = image
        self.savepath = savepath
        self.savefileName = savefileName

    def getoutput(self):

        if self.m_image == 0 :
            return False
        else :
            return True, self.m_image

    def findMax(self,cnt):
        maxvalue_x = 0
        maxvalue_y = 0
        #get x max value
        for i in range(len(cnt)):
            if(cnt[i][0][0] > maxvalue_x ):
                maxvalue_x = cnt[i][0][0]
            if(cnt[i][0][1] > maxvalue_y ):
                maxvalue_y = cnt[i][0][1]
        minvalue_x = maxvalue_x
        minvalue_y = maxvalue_y
        for i in range(len(cnt)):
            if(cnt[i][0][0] < minvalue_x ):
                minvalue_x = cnt[i][0][0]
            if(cnt[i][0][1] < minvalue_y ):
                minvalue_y = cnt[i][0][1]
        #print("findMax")
        #print(maxvalue_x)
        #print(maxvalue_y)
        return minvalue_x,minvalue_y,maxvalue_x,maxvalue_y


    def preprocessor(self):
        image = cv2.resize(self.image, (247, 42))
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        lower_blue = np.array([100,100,100])
        upper_blue = np.array([255, 255, 255])
        mask = cv2.inRange(rgb_img, lower_blue, upper_blue)
        convert_mask = (255-mask)
        contours, hierarchy  = cv2.findContours(convert_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros(convert_mask.shape,np.uint8)
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if( area >= 30  and area <= 280):
		box = self.findMax(cnt)
                if((box[2] - box[0] < 16 and box[2] - box[0] > 2)  and (box[3] - box[1] < 27 and box[3] - box[1] > 15) ):
                    cv2.drawContours(mask,[cnt],0,255,-1)
        output  = cv2.bitwise_and(image,image ,mask = mask)
        ret,output = cv2.threshold(output,120,255,cv2.THRESH_BINARY_INV)
        cv2.imwrite(self.savepath+self.savefileName,output,None)
        return output

    """
    def preprocessor(path,fileName) :
        image = cv2.imread(path+fileName)
        image = cv2.resize(image, (247, 42))
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        lower_blue = np.array([120,120,120])
        upper_blue = np.array([250, 250, 250])
        mask = cv2.inRange(rgb_img, lower_blue, upper_blue)
        convert_mask = (255-mask)
        contours, hierarchy  = cv2.findContours(convert_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours_ = []
        mask = np.zeros(convert_mask.shape,np.uint8)
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            if( area >= 30  and area <= 250):
                cv2.drawContours(mask,[cnt],0,255,-1)
                contours_.append(cnt)
        output  = cv2.bitwise_and(image,image ,mask = mask)
        ret,output = cv2.threshold(output,120,255,cv2.THRESH_BINARY_INV)
        cv2.imwrite(path+'preprocess_'+fileName,output,None)
        return output

    """
