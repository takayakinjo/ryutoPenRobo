import numpy as np
import cv2
import penrobo

im = np.ones((400, 400, 3), np.uint8)*255
 
pr = penrobo.penRobo()

pr.start(im)

#pr.pen_up()

#pr.move_to(im, 20, 10)

#pr.pen_down()
#pr.move_to(im, 25, 100)

pr.line(im, 100, 100, 200, 300)
pr.line(im, 300, 300, 100, 100)
pr.rect(im, 10, 50, 350, 350)
pr.point(im, 200, 10)

pr.circle(im, 200, 200, 100, 180, 270)
pr.erase(im)

pr.number(im, 0)
pr.erase(im)
pr.number(im, 1)
pr.erase(im)
pr.number(im, 2)
pr.erase(im)
pr.number(im, 3)
#pr.erase(im)
pr.number(im, 4)
#pr.erase(im)
pr.number(im, 5)
#pr.erase(im)
pr.number(im, 6)
#pr.erase(im)
pr.number(im, 7)
#pr.erase(im)
pr.number(im, 8)
#pr.erase(im)
pr.number(im, 9)

cv2.waitKey(0)
cv2.destroyAllWindows()

