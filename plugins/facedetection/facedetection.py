#!/usr/bin/python3

import waggle.logging
import waggle.pipeline
import sys
import time
import os

# openCV3 check
try:
    import cv2
except ImportError:
    print("openCV for Python3 does not exist")
    logger = waggle.logging.getLogger("face_detection")
    logger.error("openCV for Python3 does not exist")
    exit(1)

def get_cam_index(path, default=0):
    idx = default
    if os.isfile(path):
        try:
            with open(path, 'r') as f:
                data = f.read()
                if data != '':
                    idx = int(data)
        except:
            pass
    return idx

top_cam_idx = get_cam_index('/etc/waggle/waggle_cam_idx_top', default=0)
bottom_cam_idx = get_cam_index('/etc/waggle/waggle_cam_idx_top', default=1)

class FaceDetectionPlugin(waggle.pipeline.Plugin):

    plugin_name = 'face_detection'
    plugin_version = '1'

    def run(self):
        if len(sys.argv) == 2:
            cascPath = sys.argv[1]
        else:
            cascPath = 'haarcascade_frontalface_default.xml'

        faceCascade = cv2.CascadeClassifier(cascPath)

        debugging = False
        viewing = False

        t = 0
        period = 10  # sec

        # index 0 for the first camera (normally internal)
        # index 1 for the second camera (normally external)
        #video_capture = cv2.VideoCapture(1)
        video_capture = cv2.VideoCapture(top_cam_idx)

        while True:
            num_of_faces = avg_faces = 0
            max_faces = 0
            min_faces = 10000
            # start timer
            t = time.time()
            last_frame = None

            while True:
                # Capture frame-by-frame
                ret, frame = video_capture.read()
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.1,
                    minNeighbors=5,
                    minSize=(30, 30),
                    # flags=cv2.cv.CV_HAAR_SCALE_IMAGE # python
                    flags=0)

                if debugging:
                    # Draw a rectangle around the faces
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    # Display the resulting frame
                    if viewing:
                        cv2.imshow('Video', frame)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                elasped = time.time() - t
                num_of_faces = len(faces)
                if num_of_faces >= max_faces:
                    max_faces = num_of_faces
                if num_of_faces <= min_faces:
                    min_faces = num_of_faces

                cv2.imwrite('test.png', frame)
                if debugging:
                    print("number of faces %d" % (num_of_faces))
                if elasped > period:
                    break
            # calculate agv
            if max_faces >= min_faces:
                avg_faces = (max_faces + min_faces) / 2.0
                data = []
                data.append('min:%d' % (min_faces))
                data.append('max:%d' % (max_faces))
                data.append('avg:%.2f' % (avg_faces))
                if debugging:
                    print(data)
                self.send(sensor='camera', data=data)
                ret = self.send_file(sensor='camera_raw', filepath='/usr/lib/waggle/plugin_manager/plugins/facedetection/test.png')
            else:
                self.send(sensor='camera', data=['nodata:error'])

        # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()


register = FaceDetectionPlugin.register

if __name__ == '__main__':
    #plugin = FaceDetectionPlugin.fileTransferConfig()
    plugin = FaceDetectionPlugin()
    plugin.add_handler(waggle.pipeline.RabbitMQHandler('amqp://localhost'))
    plugin.add_file_handler(waggle.pipeline.RabbitMQHandler('amqp://localhost', dest_queue='images'))
    plugin.run()
