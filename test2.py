import numpy as np
import cv2
import penrobo

im = np.ones((400, 400, 3), np.uint8)*255
 
pr = penrobo.penRobo()

pr.start()

#pr.pen_up()

#pr.move_to(im, 20, 10)

#pr.pen_down()
#pr.move_to(im, 25, 100)

#pr.line(100, 100, 200, 300)
#pr.line(300, 300, 100, 100)
pr.rect(0, 0, 600, 400)
pr.line(0, 0, 600, 400)
cv2.waitKey(0)
#pr.point(200, 10)

pr.circle(200, 200, 100, 180, 270)
pr.erase()

pr.number(0)
pr.erase()
pr.number(1)
pr.erase()
pr.number(2)
pr.erase()
pr.number(3)
#pr.erase()
pr.number(4)
#pr.erase()
pr.number(5)
#pr.erase()
pr.number(6)
#pr.erase()
pr.number(7)
#pr.erase()
pr.number(8)
#pr.erase()
pr.number(9)

cv2.waitKey(0)
cv2.destroyAllWindows()

