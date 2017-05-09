import preprocessorV2
import gaugedetectorV2
import colorbalance
import gaugeocr
import sys
import cv2

def main(argv):
	
	path = '/home/pi/GRS/aeye_grs/storage/org_files/'
	outfile = ""
	imgfile = ""
	
	if len(argv) > 1:
		outfile = argv[1]
		imgfile = argv[1]
		image = cv2.imread(path+imgfile)
		cb = colorbalance.ColorBalance(image,path+'out_files/','out_cb_'+outfile,10)
		image = cb.simplest_cb()
		detector = gaugedetectorV2.Gaugedetector(image,path+'out_files/','out_d_'+outfile)
		detected_image,retvalue = detector.gaugedetector()
		if retvalue == True :
			pre = preprocessorV2.Preprocessor(detected_image,path+'out_files/','out_p_'+outfile)
			preprocessed_image = pre.preprocessor()
			ocr = gaugeocr.Gaugeocr(path+'out_files/','out_p_'+outfile)
			print ocr.startocr()
		else :
			print "error(02) : object detect"
			
	else:
		print "error(01) : imgfile not found "
	
    

if __name__ == "__main__":
    main(sys.argv)
