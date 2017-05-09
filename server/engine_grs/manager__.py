import preprocessorV2
import gaugedetectorV2
import colorbalance
import gaugeocr
import sys
import cv2

def main(argv):
	if len(argv) > 1:
		path = '/home/pi/GRS/aeye_grs/storage/org_files/'
		outfile = argv[1]
		imgfile = argv[1]
		image = cv2.imread(path+imgfile)
		rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		cb = colorbalance.ColorBalance(image,path+path+'out_files/','out_cb_'+outfile,10)
    	image = cb.simplest_cb()
		detector = gaugedetectorV2.Gaugedetector(image,path+'out_files/','out_d_'+outfile)
		detected_image, retvalue  = detector.gaugedetector()
		if retvalue == False :
        	print "False"
		else :
			pre = preprocessorV2.Preprocessor(detected_image,path+'out_files/','out_p_'+outfile)
			preprocessed_image = pre.preprocessor()
			ocr = gaugeocr.Gaugeocr(path+'out_files/','out_p_'+outfile)
			print ocr.startocr()
		#cv2.imshow("0", preprocessed_image)
		# #cv2.waitKey(0)
	else :
		print "Error : Input image path"

if __name__ == "__main__":
    main(sys.argv)
