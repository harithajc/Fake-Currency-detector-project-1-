#module OpenCV has an massive set of tools specifically built for computer vision and image processing
import cv2

#converting the image to grayscale so that lighting and colour dont matter much ,we are concentrating more on the shape and content 
real_note = cv2.imread('real_note.jpg', cv2.IMREAD_GRAYSCALE)
test_note = cv2.imread('test_note.jpg', cv2.IMREAD_GRAYSCALE)

#Creating the "Magnifying Glass" (ORB).Instead of looking at a blank patch of paper, it specifically searches for "corners" and unique textures.
orb = cv2.ORB_create()

#passing both our real note and our test note through the ORB detector.

#kp (Keypoints): These are the exact X and Y coordinates on the image where the algorithm found something unique
kp1, des1 = orb.detectAndCompute(real_note, None)

#des (Descriptors): This is the mathematical description of what that keypoint looks like.
kp2, des2 = orb.detectAndCompute(test_note, None)

#compare the fingerprints,BFMatcher (Brute-Force Matcher).
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches = bf.match(des1, des2)

#Sometimes a piece of text on the fake note slightly resembles a different piece of text on the real note. This line sorts our list of matches based on their "distance" (mathematical difference). A lower distance means the match is highly accurate. We push the most accurate matches to the top of the list.
matches = sorted(matches, key=lambda x: x.distance)

#The Final Test 
score = len(matches)
threshold = 150 

if score >= threshold:
    print("✅ Result: Currency is likely REAL.")
else:
    print("❌ Result: Currency is likely FAKE.")

#Results

#we use cv2.drawMatches() to actually draw colorful lines connecting the top 50 matches between the two images. cv2.imshow() pops open a window on your screen so you can visually see exactly what the computer saw and matched.
result_image = cv2.drawMatches(real_note, kp1, test_note, kp2, matches[:50], None, flags=2)
cv2.imshow("Feature Matching", result_image)

