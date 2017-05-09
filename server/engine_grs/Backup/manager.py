import preprocessor
import gaugedetector
import gaugeocr
import sys
import cv2

def main(argv):
    # My code here
    path ='/home/aeye_grs/storage/org_files/'
    opath = '/home/aeye_grs/storage/org_files/out_files/'
    fileName ='test.jpg'
    image = cv2.imread(path+fileName)
    if (image is not None):
    	detector = gaugedetector.Gaugedetector(image,opath,'out_d_'+fileName)
    	detected_image  = detector.gaugedetector()
    	pre = preprocessor.Preprocessor(detected_image,opath,'out_p_'+fileName)
    	preprocessed_image = pre.preprocessor()
    	ocr = gaugeocr.Gaugeocr(opath,'out_p_'+fileName)
    	print ocr.startocr()
    #cv2.imshow("0", preprocessed_image)
    #cv2.waitKey(0)
    pass

if __name__ == "__main__":
    main(sys.argv)
