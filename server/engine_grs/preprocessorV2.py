import numpy as np
import cv2

class Preprocessor:
    def __init__(self,image,savepath,savefileName):
        self.image = image
        self.savepath = savepath
        self.savefileName = savefileName

        self.minsize = 100
        self.maxsize = 1600

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
        image = cv2.resize(self.image, (340, 104))
        #cv2.imshow("0", image)
        #cv2.waitKey(0)
        rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        lower_blue = np.array([80,80,80])
        upper_blue = np.array([255, 255, 255])
        mask = cv2.inRange(rgb_img, lower_blue, upper_blue)
        #cv2.imshow("0", mask)
        #cv2.waitKey(0)
        #coutput = cv2.Canny(gray,100,200)
        convert_mask = (255-mask)
         #cv2.imshow("0", convert_mask)
        #cv2.waitKey(0)
        #cv2.imshow("0", convert_mask)
        #cv2.waitKey(0)
        contours, hierarchy  = cv2.findContours(convert_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros(convert_mask.shape,np.uint8)
        for i in range(len(contours)):
            cnt = contours[i]
            area = cv2.contourArea(cnt)
            #print area
            if( area >= self.minsize  and area <= self.maxsize):
                #cv2.drawContours(mask,[cnt],0,255,-1)
                #cv2.imshow("0", mask)
                #cv2.waitKey(0)
                box = self.findMax(cnt)
                #print box[3] - box[1]
                #rect = cv2.minAreaRect(cnt)
                #box = cv2.boxPoints(rect)
                #box = np.int0(box)
                #remove noise

                if((box[2] - box[0] < 50 and box[2] - box[0] > 1)  and (box[3] - box[1] < 94 and box[3] - box[1] > 10) ):
                    #print( box[0] )
                    #REMOVE NEAR OBJECT
                    #chooseddnt.append(cnt)
                    #if(box[0] == 53):
                    cv2.drawContours(mask,[cnt],0,255,-1)
                    #cv2.imshow("0", mask)
                    #cv2.waitKey(0)
        output  = cv2.bitwise_and(image,image ,mask = mask)
        ret,output = cv2.threshold(output,100,255,cv2.THRESH_BINARY_INV)
        #cv2.imshow("edge_img1", output)
        #cv2.waitKey(0)



        lower_black = np.array([0,0,0], dtype = "uint16")
        upper_black = np.array([100,100,100], dtype = "uint16")
        output = cv2.inRange(output, lower_black, upper_black)
        ret,output = cv2.threshold(output,100,255,cv2.THRESH_BINARY_INV)
        ret,output = cv2.threshold(output,100,255,cv2.THRESH_BINARY_INV)
        output = cv2.GaussianBlur(output,(3,3),0)
        #cv2.imshow("edge_img2", output)
        #cv2.waitKey(0)
        contours1, hierarchy  = cv2.findContours(output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros(output.shape,np.uint8)
        #cv2.imshow("0", mask)
        #cv2.waitKey(0)
        digt = []
        for i in range(len(contours1)):
            cnt = contours1[i]
            area = cv2.contourArea(cnt)
            #print area
            if( area >= self.minsize  and area <= self.maxsize):
                digt.append(cnt)
                cv2.drawContours(mask,[cnt],0,255,-1)
                #cv2.imshow("0", mask)
                #cv2.waitKey(0)


        rdigt = []
        for i in range(len(digt)):
             mask = np.zeros(output.shape,np.uint8)
             point1 = digt[i]
             #cv2.drawContours(mask,[point1],0,255,-1)
             #cv2.imshow("1", mask)
             #cv2.waitKey(0)
             box1 = self.findMax(point1)
             con = False
             for j in range(len(digt)):
                 if(i != j):
                    point2 = digt[j]
                    box2 = self.findMax(point2)
                    if(abs(box1[0] - box2[0]) <40 ):
                        con = True
                        #if((box1[0] < box2[0] and box1[1] > box2[1]) or (box2[0] < box1[0] and box2[1] > box1[1])):
                            #rdigt.append(point1)
                            #rdigt.append(point2)

                        #print "val"
                        #print abs(box1[0] - box2[0])

                        if(cv2.contourArea(point1) > cv2.contourArea(point2) ):
                            rdigt.append(point1)
                            #print "hi"
             if(con == False):
                 rdigt.append(point1)
                 #print "append"
        mask = np.zeros(output.shape,np.uint8)

        maxhight =0
        for z in range(len(rdigt)):
            cnt = rdigt[z]
            box = self.findMax(cnt)
            if(box[3] - box[1] > maxhight):
                maxhight = box[3] - box[1]
            cv2.drawContours(mask,[cnt],0,255,-1)
            #cv2.imshow("rdigt", mask)
            #cv2.waitKey(0)
        output  = cv2.bitwise_and(image,image ,mask = mask)
        ret,output = cv2.threshold(output,100,255,cv2.THRESH_BINARY_INV)
        lower_black = np.array([0,0,0], dtype = "uint16")
        upper_black = np.array([80,80,80], dtype = "uint16")
        output = cv2.inRange(output, lower_black, upper_black)
        ret,output = cv2.threshold(output,100,255,cv2.THRESH_BINARY_INV)

        if(maxhight <45):
             output = cv2.resize(output, (340, 144))
        #cv2.imshow("output", output)
        #cv2.waitKey(0)
        cv2.imwrite(self.savepath+self.savefileName,output,None)
        return output
