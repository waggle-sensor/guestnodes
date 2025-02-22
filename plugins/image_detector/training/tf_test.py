import numpy as np
# ANL:waggle-license
#  This file is part of the Waggle Platform.  Please see the file
#  LICENSE.waggle.txt for the legal details of the copyright and software
#  license.  For more details on the Waggle project, visit:
#           http://www.wa8.gl
# ANL:waggle-license
import tensorflow as tf
import cv2 as cv

classes = {}
with open('../models/ssd_mobilenet_coco.classes', 'r') as file:
    for line in file:
        sp = line.strip().split(' ')
        classes[int(sp[0])] = sp[1]

# Read the graph.
with tf.gfile.FastGFile('faster_rcnn_resnet101_pet.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())

with tf.Session() as sess:
    # Restore session
    sess.graph.as_default()
    tf.import_graph_def(graph_def, name='')

    # Read and preprocess an image.
    img = cv.imread('../example.jpg')
    rows = img.shape[0]
    cols = img.shape[1]
    inp = cv.resize(img, (300, 300))
    inp = inp[:, :, [2, 1, 0]]  # BGR2RGB

    # Run the model
    out = sess.run([sess.graph.get_tensor_by_name('num_detections:0'),
                    sess.graph.get_tensor_by_name('detection_scores:0'),
                    sess.graph.get_tensor_by_name('detection_boxes:0'),
                    sess.graph.get_tensor_by_name('detection_classes:0')],
                    feed_dict={'image_tensor:0': inp.reshape(1, inp.shape[0], inp.shape[1], 3)})

    # Visualize detected bounding boxes.
    num_detections = int(out[0][0])
    for i in range(num_detections):
        classId = int(out[3][0][i])
        score = float(out[1][0][i])
        bbox = [float(v) for v in out[2][0][i]]
        if score > 0.3:
            if classId in classes:
                class_name = classes[classId]
            else:
                clase_name = str(classId)

            x = bbox[1] * cols
            y = bbox[0] * rows
            right = bbox[3] * cols
            bottom = bbox[2] * rows
            cv.putText(img, str(class_name), (int(x), int(y)),  cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 1, cv.LINE_AA)
            cv.rectangle(img, (int(x), int(y)), (int(right), int(bottom)), (255, 255, 255), thickness=2)

# Resize image
resized_image = cv.resize(img, (1280, 960))
# cv.imshow('TensorFlow MobileNet-SSD', resized_image)
# # Before resizing
# cv.imshow('TensorFlow MobileNet-SSD', img)
cv.imwrite('ex.png',img)

