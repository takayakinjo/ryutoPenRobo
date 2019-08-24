from __future__ import division
import math
import numpy as np
import cv2
import time
import Adafruit_PCA9685

pen = 0 # 0:up or 1:down

px = 0
py = 0

s1x = 125
s1y = 400
s2x = 125+130
s2y = 400

r1 = 350/2
r2 = 450/2
r2e = 540/2

speed = 4

img2 = np.ones((450, 450, 3), np.uint8)*255
# img3 = np.ones((450, 450, 3), np.uint8)*255

# servo settings usgin PCA9685
servo = Adafruit_PCA9685.PCA9685()

servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
servo_mid = int((servo_max+servo_min)/2)

# Set frequency to 60hz, good for servos.
servo.set_pwm_freq(60)

pwm_pen_up = 390
pwm_pen_up2 = 450
pwm_pen_down = 355

pz = pwm_pen_up

# 1 -120: 580 -45:385 30:210
# 2  75:375
#pwm1 = [385, 385, 385]
#pwm2 = [150, 375, 600]
pwm1 = [580, 385, 210]
pwm2 = [580, 375, 210]
s1angle = [-120, -45, 30]
s2angle = [0, 75, 150]

def calcPwm(pwmList, angleList, angle):
    pwm = 0
    if angle < angleList[0]:
        pwm = pwmList[0]
    elif angle < angleList[1]:
        pwm = (pwmList[0] * (angleList[1]-angle) + pwmList[1] * (angle-angleList[0]))/(angleList[1]-angleList[0]) 
    elif angle < angleList[2]:
        pwm = (pwmList[1] * (angleList[2]-angle) + pwmList[2] * (angle-angleList[1]))/(angleList[2]-angleList[1])
    else:
        pwm = pwmList[2];
    return int(pwm)
        
class penRobo:

    def start(x):
        print("Start penrobo")
        cv2.rectangle(img2, (20, 20), (425, 260), (0,0,0), thickness=1)
        cv2.circle(img2, (s1x, s1y), 10, (0,0,0), 2)
        cv2.circle(img2, (s2x, s2y), 10, (0,0,0), 2)

        # cv2.circle(img2, (s1x, s1y), int(r1), (0,0,0), 1)

        cv2.imshow("penRobo2", img2)
        cv2.waitKey(10)
        
    def pen_up(x):
        global pen, pz
        #print("Pen up")
        pen = 0
        if pz < pwm_pen_up:
            step = 1
        else:
            step = -1
        for pz in range(pz, pwm_pen_up, step):
            servo.set_pwm(2, 0, pz)
            time.sleep(0.02)
        servo.set_pwm(2, 0, pwm_pen_up)
        pz = pwm_pen_up
        
    def pen_up2(x):
        global pen, pz
        #print("Pen up")
        pen = 1
        for pz in range(pz, pwm_pen_up2, 1):
            servo.set_pwm(2, 0, pz)
            time.sleep(0.02)
        servo.set_pwm(2, 0, pwm_pen_up2)
        pz = pwm_pen_up2
        
    def pen_down(x):
        global pen, pz
        #print("Pen down")
        pen = 1
        for pz in range(pz, pwm_pen_down, -1):
            servo.set_pwm(2, 0, pz)
            time.sleep(0.02)
        servo.set_pwm(2, 0, pwm_pen_down)
        pz = pwm_pen_down
                
    def pen_up_if_nessesary(x1, y1):
        global px, py
        if px != x1 or py != y1:
            penRobo.pen_up(0)
        
    def move_servo(x, x1, y1, z1):

        x2 = (x1/2.5) + 80
        y2 = (y1/2.6) + 40

        if pen == 1:
            cv2.circle(img2, (int(x2), int(y2)), 2, (0,0,0), -1)
        else:
            cv2.circle(img2, (int(x2), int(y2)), 2, (200,200,200), -1)

        dx1 = (x2-s1x)
        dy1 = (y2-s1y)
        df1 = math.sqrt(dx1*dx1+dy1*dy1)
            
        dx2 = (x2-s2x)
        dy2 = (y2-s2y)
        df2 = math.sqrt(dx2*dx2+dy2*dy2)

        #if df1 > r1+r2 or df2 > r1+r2:
        #    print("Out of bounds")
        #    return
        
        # TESTCODE
        # arm1
        a1 = x2 - s1x
        b1 = y2 - s1y
        c1 = (s1x * s1x + s1y * s1y - r1 * r1 - (x2 * x2 + y2 * y2 - r2e * r2e))/2

        d1 = a1*s1x + b1 * s1y + c1
        tmp = math.sqrt((a1*a1+b1*b1)*r1*r1-d1*d1)
        l1x1 = (-a1*d1+b1*tmp)/(a1*a1+b1*b1)+s1x
        l1x2 = (-a1*d1-b1*tmp)/(a1*a1+b1*b1)+s1x
        l1y1 = (-b1*d1-a1*tmp)/(a1*a1+b1*b1)+s1y
        l1y2 = (-b1*d1+a1*tmp)/(a1*a1+b1*b1)+s1y

        # pivot
        ap1 = 0
        if x2 - l1x1 != 0:
            ap1 = math.atan((y2-l1y1)/(x2-l1x1))

        pvx = x2 - math.cos(ap1-math.radians(39.6)) * (127)/2
        pvy = y2 - math.sin(ap1-math.radians(39.6)) * (127)/2
        
        #arm2
        a2 = pvx - s2x
        b2 = pvy - s2y
        c2 = (s2x * s2x + s2y * s2y - r1 * r1 - (pvx * pvx + pvy * pvy - r2 * r2))/2

        d2 = a2*s2x + b2 * s2y + c2
        tmp = math.sqrt((a2*a2+b2*b2)*r1*r1-d2*d2)
        l2x1 = (-a2*d2+b2*tmp)/(a2*a2+b2*b2)+s2x
        l2x2 = (-a2*d2-b2*tmp)/(a2*a2+b2*b2)+s2x
        l2y1 = (-b2*d2-a2*tmp)/(a2*a2+b2*b2)+s2y
        l2y2 = (-b2*d2+a2*tmp)/(a2*a2+b2*b2)+s2y

        img3 = img2.copy()

        cv2.circle(img3, (int(x2), int(y2)), 10, (255,0,0), 1)
        #arm1
        cv2.line(img3, (s1x, s1y), (int(l1x1), int(l1y1)), (255,0,0), thickness=3)
        cv2.line(img3, (int(x2), int(y2)), (int(pvx), int(pvy)), (0,255,0), thickness=3)
        cv2.line(img3, (int(pvx), int(pvy)), (int(l1x1), int(l1y1)), (0,255,0), thickness=3)
        cv2.circle(img3, (int(l1x1), int(l1y1)), 5, (255,0,0), -1)
        #arm2
        cv2.line(img3, (s2x, s2y), (int(l2x2), int(l2y2)), (255,0,0), thickness=3)
        cv2.line(img3, (int(pvx), int(pvy)), (int(l2x2), int(l2y2)), (0,255,0), thickness=3)
        cv2.circle(img3, (int(l2x2), int(l2y2)), 5, (255,0,0), -1)
        #pivot 
        cv2.circle(img3, (int(pvx), int(pvy)), 5, (255,0,0), -1)

        # servo angle
        dx1 = s1x - l1x1;
        dy1 = s1y - l1y1;
        if dy1 != 0:
            angle1 = -math.degrees(math.atan(dx1/dy1))
        else:
            angle1 = 0

        if dx1 > 0 and dy1 < 0:
            angle1 = angle1 - 180
            
        dx2 = s2x - l2x2;
        dy2 = s2y - l2y2;
        if dy2 != 0:
            angle2 = -math.degrees(math.atan(dx2/dy2))
        else:
            angle2 = 0

        if dx2 < 0 and dy2 < 0:
            angle2 = angle2 + 180

        s1pwm = calcPwm(pwm1, s1angle, angle1)
        s2pwm = calcPwm(pwm2, s2angle, angle2)

        # print(angle1, s1pwm, angle2, s2pwm)

        servo.set_pwm(0, 0, s1pwm)
        servo.set_pwm(1, 0, s2pwm)
        servo.set_pwm(2, 0, int(z1))

        # cv2.imshow("penRobo2", img3)
        # cv2.waitKey(1)
        
    def move_to(x, x1, y1):
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
                    penRobo.move_servo(0, xx, yy, pz)
            else:
                dxdy = float(dx)/float(dy)
                if py < y1:
                    step = speed
                else:
                    step = -speed
                for yy in range(py, y1, step):
                    xx = px + dxdy*(float(yy-py))
                    penRobo.move_servo(0, xx, yy, pz)

        penRobo.move_servo(0, x1, y1, pz) # make sure for the last
        
        px = x1
        py = y1
        # print("move to (",px,", ",py,")")

    def move_to3D(x, x1, y1, z1):
        global px, py, pz
        dx = x1 - px
        dy = y1 - py
        dz = z1 - pz
        if dz != 0:
            dxdz = float(dx)/float(dz)
            dydz = float(dy)/float(dz)
            if dz > 0:
                step = 1
            else:
                step = -1
            for zz in range(pz, z1, step):
                xx = px + dxdz*(float(zz-pz))
                yy = py + dydz*(float(zz-pz))
                penRobo.move_servo(0, xx, yy, zz)
                    
        penRobo.move_servo(0, x1, y1, z1) # make sure for the last
        
        px = x1
        py = y1
        pz = z1
        
    def point(x, x1, y1):
        penRobo.pen_up_if_nessesary(x1, y1)
        penRobo.move_to(0, x1, y1)
        penRobo.pen_down(0)
        penRobo.move_servo(0, x1, y1, pz)

    def line(x, x1, y1, x2, y2):
        penRobo.pen_up_if_nessesary(x1, y1)
        penRobo.move_to(0, x1, y1)
        penRobo.pen_down(0)
        penRobo.move_to(0, x2, y2)

    def rect(x, x1, y1, x2, y2):
        penRobo.pen_up_if_nessesary(x1, y1)
        penRobo.move_to(0, x1, y1)
        penRobo.pen_down(0)
        penRobo.move_to(0, x1, y2)
        penRobo.move_to(0, x2, y2)
        penRobo.move_to(0, x2, y1)
        penRobo.move_to(0, x1, y1)
            
    def circle(x, x1, y1, r, a1, a2):
        global speed
        xx = math.sin(math.radians(a1))*r + x1
        yy = -math.cos(math.radians(a1))*r + y1

        penRobo.pen_up_if_nessesary(int(xx), int(yy))
        penRobo.move_to(0, int(xx), int(yy))

        penRobo.pen_down(0)

        step = float(r)*0.025 * speed
        if a1 > a2:
            step = -step

        cte = (a2-a1)/step
        ct = 0
        ag = float(a1)
        while ct < cte:
            xx = math.sin(math.radians(ag))*r + x1
            yy = -math.cos(math.radians(ag))*r + y1
            penRobo.move_to(0, int(xx), int(yy))
            ag += step
            ct = ct+1

        xx = math.sin(math.radians(a2))*r + x1
        yy = -math.cos(math.radians(a2))*r + y1
        penRobo.move_to(0, int(xx), int(yy))
        
    def erase(x):
        global pz
        print("erasing...")
        cv2.rectangle(img2, (20, 20), (425, 260), (255,255,255), thickness=-1)
        cv2.rectangle(img2, (20, 20), (425, 260), (0,0,0), thickness=1)
        cv2.imshow("penRobo2", img2)
        cv2.waitKey(10)

        #up
        penRobo.pen_up2(0)

        penRobo.move_to(0, 770, 10)
        penRobo.move_to3D(0, 770, 30, pwm_pen_down)

#        penRobo.pen_down(0)
        
        penRobo.move_to(0, 0, 0)
        penRobo.move_to(0, 500, 150)
        penRobo.move_to(0, 0, 150)
        penRobo.move_to(0, 500, 300)
        penRobo.move_to(0, 0, 300)
        penRobo.move_to(0, 450, 70)
        penRobo.move_to(0, 770, 70)
        penRobo.move_to3D(0, 770, 70, pwm_pen_up2)
#        penRobo.pen_up2(0)
        penRobo.move_to(0, 200, 200)

    def home(x):
        penRobo.pen_up2(0)
        penRobo.move_to(0, 0, 0)

        
    def number(x, num):
        if num == 0:
            penRobo.circle(0, 200, 200, 150, 0, 360)
        elif num == 1:
            penRobo.line(0, 200,50,200,350)
        elif num == 2:
            penRobo.circle(0, 200, 150, 100, -90, 180)
            penRobo.line(0, 200, 250, 100, 350)
            penRobo.line(0, 100, 350, 300, 350)
