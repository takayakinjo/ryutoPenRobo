import math
import numpy as np
from time import sleep
import cv2

pen = 0 # 0:up or 1:down

px = 0
py = 0

s1x = 125
s1y = 400
s2x = 125+130
s2y = 400

speed = 6

img2 = np.ones((450, 450, 3), np.uint8)*255

class penRobo:

    def start(x, im):
        print("Start penrobo")
        cv2.imshow("penRobo", im)
        cv2.rectangle(img2, (20, 20), (425, 260), (0,0,0), thickness=1)
        cv2.circle(img2, (s1x, s1y), 10, (0,0,0), 2)
        cv2.circle(img2, (s2x, s2y), 10, (0,0,0), 2)

        cv2.imshow("penRobo2", img2)
        cv2.waitKey(10)
        
    def pen_up(x):
        #print("Pen up")
        global pen
        pen = 0

    def pen_down(x):
        global pen
        if pen == 0:
            #print("Pen down")
            pen = 1

    def pen_up_if_nessesary(x1, y1):
        global px, py
        if px != x1 or py != y1:
            penRobo.pen_up(0)

        
    def move_servo(x, im, x1, y1):
        if pen == 1:
            cv2.circle(im, (int(x1), int(y1)), 3, (0,0,0), -1)
        else:
            cv2.circle(im, (int(x1), int(y1)), 3, (200,200,200), -1)
            
        cv2.imshow("penRobo", im)

        x2 = (x1/2) + 20
        y2 = (y1/2) + 40

        if pen == 1:
            cv2.circle(img2, (int(x2), int(y2)), 2, (0,0,0), -1)
        else:
            cv2.circle(img2, (int(x2), int(y2)), 2, (200,200,200), -1)

        cv2.imshow("penRobo2", img2)
        
        cv2.waitKey(1)
        #sleep(0.01)        
        
    def move_to(x, im, x1, y1):
        global px, py
        dx = x1 - px
        dy = y1 - py
        if dx != 0 or dy != 0:
            if abs(dx) > abs(dy):
                dydx = float(dy)/float(dx)
                if px < x1:
                    step = speed
                else:
                    step = -speed
                for xx in range(px, x1, step):
                    yy = py + dydx*(float(xx-px))
                    penRobo.move_servo(0, im, xx, yy)
            else:
                dxdy = float(dx)/float(dy)
                if py < y1:
                    step = speed
                else:
                    step = -speed
                for yy in range(py, y1, step):
                    xx = px + dxdy*(float(yy-py))
                    penRobo.move_servo(0, im, xx, yy)

        penRobo.move_servo(0, im, x1, y1) # make sure for the last
        
        px = x1
        py = y1
        # print("move to (",px,", ",py,")")
        
    def point(x, im, x1, y1):
        penRobo.pen_up_if_nessesary(x1, y1)
        penRobo.move_to(0, im, x1, y1)
        penRobo.pen_down(0)
        penRobo.move_servo(0, im, x1, y1)

    def line(x, im, x1, y1, x2, y2):
        penRobo.pen_up_if_nessesary(x1, y1)
        penRobo.move_to(0, im, x1, y1)
        penRobo.pen_down(0)
        penRobo.move_to(0, im, x2, y2)

    def rect(x, im, x1, y1, x2, y2):
        penRobo.pen_up_if_nessesary(x1, y1)
        penRobo.move_to(0, im, x1, y1)
        penRobo.pen_down(0)
        penRobo.move_to(0, im, x1, y2)
        penRobo.move_to(0, im, x2, y2)
        penRobo.move_to(0, im, x2, y1)
        penRobo.move_to(0, im, x1, y1)
            
    def circle(x, im, x1, y1, r, a1, a2):

        xx = math.sin(math.radians(a1))*r + x1
        yy = -math.cos(math.radians(a1))*r + y1

        penRobo.pen_up_if_nessesary(int(xx), int(yy))
        penRobo.move_to(0, im, int(xx), int(yy))

        penRobo.pen_down(0)

        step = float(r)*0.05
        if a1 > a2:
            step = -step

        cte = (a2-a1)/step
        ct = 0
        ag = float(a1)
        while ct < cte:
            xx = math.sin(math.radians(ag))*r + x1
            yy = -math.cos(math.radians(ag))*r + y1
            penRobo.move_to(0, im, int(xx), int(yy))
            ag += step
            ct = ct+1

        xx = math.sin(math.radians(a2))*r + x1
        yy = -math.cos(math.radians(a2))*r + y1
        penRobo.move_to(0, im, int(xx), int(yy))
        
    def erase(x, im):
        print("erasing...")
        cv2.rectangle(im, (0, 0), (400, 400), (255, 255, 255), thickness=-1)
        cv2.rectangle(img2, (20, 20), (425, 260), (255,255,255), thickness=-1)
        cv2.rectangle(img2, (20, 20), (425, 260), (0,0,0), thickness=1)
        cv2.imshow("penRobo", im)
        cv2.imshow("penRobo2", img2)
        cv2.waitKey(10)

        
    def number(x, im, num):
        if num == 0:
            penRobo.circle(0, im, 200, 200, 150, 0, 360)
        elif num == 1:
            penRobo.line(0, im, 200,50,200,350)
        elif num == 2:
            penRobo.circle(0, im, 200, 150, 100, -90, 180)
            penRobo.line(0, im, 200, 250, 100, 350)
            penRobo.line(0, im, 100, 350, 300, 350)
