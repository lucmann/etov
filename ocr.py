import easyocr

class Ocr(object):
    def __init__(self):
        self.reader = easyocr.Reader(['en'])

    def read_digit_image(self, image):
        return self.reader.readtext(image, detail=0,
                                    rotation_info=[90],allowlist='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

