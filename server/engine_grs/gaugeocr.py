try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract


class Gaugeocr:
    def __init__(self,path,fileName):
        self.file =path+fileName

    def startocr(self):
        return pytesseract.image_to_string(Image.open(self.file),lang='gasf')


