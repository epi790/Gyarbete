from qreader import QReader
from imutils.video import VideoStream
import imutils
import zxing
from pyzbar import pyzbar
from PIL import Image as im 
import time
from cv2 import imread, VideoCapture, imshow, waitKey, destroyAllWindows, cvtColor, COLOR_BGR2RGB, rectangle, putText, FONT_HERSHEY_SIMPLEX

#vid = VideoCapture(0)

def init():
    vs = VideoStream(src=0).start()
    #qreader = zxing.BarCodeReader()
    return vs


if __name__ == "__main__":


    while True:
        #print("taking image")
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        #aztec_data = qreader.decode(im.fromarray(frame))
        #print(aztec_data)
        
        #ret, frame = vid.read()

        #imshow('frame', frame)

        #frame = cvtColor(frame, COLOR_BGR2RGB)

        #image = im.fromarray(frame)

        #image.save("testimage.png")

        barcodes = pyzbar.decode(frame)
        for barcode in barcodes:
            # extract the bounding box location of the barcode and draw
            # the bounding box surrounding the barcode on the image
            #(x, y, w, h) = barcode.rect
            #rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # the barcode data is a bytes object so if we want to draw it
            # on our output image we need to convert it to a string first
            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type
            # draw the barcode data and barcode type on the image
            text = "{} ({})".format(barcodeData, barcodeType)

            print(barcodeData)
            # putText(frame, text, (x, y - 10),
            #     FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            # imshow("frame", frame)
        else:
            imshow("frame", frame)
        #print(decodedtext)
        #print(ret, frame)

        if waitKey(1) & 0xFF == ord('q'): 
            break

#print( qreader.decode("az.png", try_harder=True, possible_formats="AZTEC"))

#foo
# vid.release() 
# destroyAllWindows() 

# qreader = QReader()

# qreader_reader, cv2_reader, pyzbar_reader = QReader(), QRCodeDetector(), decode

# for img_path in ('test_mobile.jpeg', 'test_draw64x64.jpeg'):
#     qreaderout = qreader_reader.detect_and_decode(image=img)



def get_qr_data(vs):
    frame = vs.read()
    frame = imutils.resize(frame, width=400)
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        #text = "{} ({})".format(barcodeData, barcodeType)
        return barcodeData