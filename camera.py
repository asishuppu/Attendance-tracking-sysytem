import cv2
class VideoCamera(object):
    def __init__(self):
        #self.video = cv2.VideoCapture(0)
        self.video = cv2.VideoCapture(0)

        if not self.video.isOpened():
            raise Exception("Could not open video device")
        ret, frame = self.video.read()


    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
    def get_image(self):
       retval, im = self.video.read()
       return im
    def delete(self):
        self.video.release()
