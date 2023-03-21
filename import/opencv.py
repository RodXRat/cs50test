import cv2
from config import *
from triggerbot import *
from contour import *
import math


def get_classes():
    with open(LABELS, "r") as f:
        class_names = [cname.strip() for cname in f.readlines()]
        return class_names


def get_model():
    net = cv2.dnn.readNet(WEIGHTS, CONFIG)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(512, 512), scale=1 / 255, swapRB=True)
    return model


def do_detect(model, frame):
    classes, scores, boxes = model.detect(
        frame, float(JSON_DATA["CONFIDENCE_THRESHOLD"]), float(JSON_DATA["NMS_THRESHOLD"]))
    return classes, scores, boxes


def cycle_enemies(run, enemyNum, frame, arduino, classes, boxes, closestObject=[]):
    distances = []
    new_bbox = []
    if run == False:
        closest = 1000
        run = True
    else:
        closest = closestObject[BOX_DISTANCE]
    for i in range(enemyNum):

        X = float(boxes[i][0])
        Y = float(boxes[i][1])
        width = float(boxes[i][2])
        height = float(boxes[i][3])

        centerX = X + (width / 2)
        centerY = Y + (height / 2)
        
        distance = math.dist([centerX, centerY], [AIMPOINT, AIMPOINT])
        distances.insert(i, distance)

        # Create new "box" to be tracked and return it 
        closestObject.insert(BOX_X, X)
        closestObject.insert(BOX_Y, Y)
        closestObject.insert(BOX_WIDTH, width)
        closestObject.insert(BOX_HEIGHT, height)
        closestObject.insert(BOX_CENTERX, centerX)
        closestObject.insert(BOX_CENTERY, centerY)
        closestObject.insert(BOX_CCLOSESTX, X + (width / 2))
        closestObject.insert(BOX_CCLOSESTY, Y + (height ))
        closestObject.insert(BOX_DISTANCE, closest)
        closestObject.insert(BOX_CLASS, classes[i])
        
        new_bbox = boxes[i]

    difX, difY, frame = detect_head(frame, new_bbox, AIMPOINT, closestObject[BOX_CLASS]) # Pass the class to detect_head
    triggerbot = do_triggerbot(closestObject)
    # Update the line to point to the center of the contour
    cv2.line(frame, (int(closestObject[BOX_CENTERX]), int(closestObject[BOX_CENTERY])), (AIMPOINT, AIMPOINT),
         (255, 0, 0), 1, cv2.LINE_AA)

    if (SHOOT):
        triggerbot = 0

    data = 0

    return closestObject, run, data, difX, difY, triggerbot, new_bbox


def do_display_start(classes, scores, boxes, frame, class_names):
    if (JSON_DATA["DISPLAY"]):
        for (classID, score, box) in zip(classes, scores, boxes):
            color = COLORS[int(classID) % len(COLORS)]
            label = "%s : %f" % (class_names[int(classID)], score)
            cv2.rectangle(frame, box, color, 2)
            cv2.putText(
                frame, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


def do_display_end(start, end, frame):
    if (JSON_DATA["DISPLAY"]):
        fps_label = "FPS: %.2f" % (1 / (end - start))
        cv2.putText(frame, fps_label, (0, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("", frame)


def check_quit(sct):
    if cv2.waitKey(1) & 0xFF == ord("q") or cv2.waitKey(1) & 0xFF == ord("Q"):
        cv2.destroyAllWindows()
        sct.close()
        return True


def reset_tracking():
    closestObject = []
    difXLast, difYLast = 0, 0
    return closestObject, difXLast, difYLast
