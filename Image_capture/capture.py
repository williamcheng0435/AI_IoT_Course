# Import opencv
import cv2 
# Import uuid
import uuid
# Import Operating System
import os
# Import time
import time


labels = ['shape']
IMAGES_PATH = os.path.join('shape')
number_imgs = 4

    
for label in labels:
    for imgnum in range(number_imgs):
        
        print('Collecting images for {}, no {}'.format(label, imgnum))
        time.sleep(1)
        print('3')
        time.sleep(1)
        print('2')
        time.sleep(1)
        print('1')
        time.sleep(1)

        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        ret, frame = cap.read()           
        #cv2.imshow('frame', frame)
        imgname = os.path.join(IMAGES_PATH,label+'.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imgname, frame)
        time.sleep(5)
        cv2.destroyAllWindows()
        cap.release()
        

        if cv2.waitKey(1) & 0xFF == ord('q'):
                break

                
cap.release()
cv2.destroyAllWindows()