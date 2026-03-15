from flask import Flask, render_template, request
import cv2
import os

app = Flask(__name__)

# 1. Lock in the exact folder paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# 2. Auto-create the static folder if it doesn't exist!
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# We added 'POST' here so the server is allowed to receive the image
@app.route('/', methods=['GET', 'POST'])
def home():
    result_message = None  # This will hold our ✅ or ❌ answer
    show_image = False # This will tell our HTML if an image is ready to show

    # If the user clicked the "Check Currency" button...
    if request.method == 'POST':
        # 1. CATCH THE IMAGE from the HTML form
        file = request.files['currency_image']
        
        # 2. SAVE IT temporarily so OpenCV can read it
        filepath = "uploaded_test_note.jpg"
        file.save(filepath)

        # 3. THE KITCHEN: Run your exact OpenCV math!
        real_note = cv2.imread('real_note.jpg', cv2.IMREAD_GRAYSCALE)
        test_note = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)

        if real_note is not None and test_note is not None:
            orb = cv2.ORB_create()
            kp1, des1 = orb.detectAndCompute(real_note, None)
            kp2, des2 = orb.detectAndCompute(test_note, None)

            # Safety check: make sure the image isn't totally blank
            if des1 is not None and des2 is not None:
                bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
                matches = bf.match(des1, des2)
                # Sort matches so we only draw the best ones!
                matches = sorted(matches, key=lambda x: x.distance)
                score = len(matches)

                #DRAW AND SAVE THE MATCHES IMAGE
                result_image = cv2.drawMatches(real_note, kp1, test_note, kp2, matches[:50], None, flags=2)
                
                # Save the image into the static folder so HTML can see it
                cv2.imwrite('static/match_result.jpg', result_image)
                show_image = True

                # The Passing Grade
                threshold = 150 
                if score >= threshold:
                    result_message = f"✅ REAL (Match Score: {score})"
                else:
                    result_message = f"❌ FAKE (Match Score: {score})"
            else:
                result_message = "❌ FAKE (Could not read any security features)"
        else:
            result_message = "⚠️ Error: Make sure your real_note.jpg is in the folder!"

    # 4. THE DELIVERY: Send the HTML page back, along with the final answer!
    return render_template('index.html', final_result=result_message)

if __name__ == '__main__':
    app.run(debug=True)