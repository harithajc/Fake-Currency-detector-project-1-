#module OpenCV has an massive set of tools specifically built for computer vision and image processing
import cv2
#converting the image to grayscale so that lighting and colour dont matter much ,we are concentrating more on the shape and content 
real_note = cv2.imread('real_note.jpg', cv2.IMREAD_GRAYSCALE)
test_note = cv2.imread('test_note.jpg', cv2.IMREAD_GRAYSCALE)
#Creating the "Magnifying Glass" (ORB).Instead of looking at a blank patch of paper, it specifically searches for "corners" and unique textures.
orb = cv2.ORB_create()
