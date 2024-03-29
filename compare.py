from skimage.measure import compare_ssim
import cv2
import numpy as np
from datetime import datetime
from tkinter import messagebox

def compare(src_img_path, ref_img_path, mode="gui"):
    if (mode == "gui"):
        log = ""

    try:
        if (mode == "gui"):
            log += "".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Signature Comparison process started..."])
        else:
            print("".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Signature Comparison process started..."]))

        src = cv2.imread(src_img_path)
        ref = cv2.imread(ref_img_path)

        h1, w1, c1 = src.shape
        h2, w2, c2 = ref.shape

        if ((h1 > h2) or (w1 > w2)):
            src = cv2.resize(src, (w2, h2))
        elif ((h2 > h1)  or (w2 > w1)):
            ref = cv2.resize(ref, (w1, h1))

        if (mode == "gui"):
            log += "".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Converting images to grayscale."])
        else:
            print("".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Converting images to grayscale."]))
        
        # Convert images to grayscale
        src_gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
        ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)

        if (mode == "gui"):
            log += "".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Computing Structural Similarity Index between two images"])
        else:
            print("".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Computing Structural Similarity Index between two images"]))

        #Compute SSIM between two images
        (score, diff) = compare_ssim(src_gray, ref_gray, full=True)

        # The diff image contains the actual image differences between the two images and is represented as a floating point data type in the range [0,1] so we must convert the array to 8-bit unsigned integers in the range [0,255] src we can use it with OpenCV
        diff = (diff * 255).astype("uint8")

        #Threshold the difference image, followed by finding contours to obtain the regions of the two input images that differ
        thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if len(contours) == 2 else contours[1]

        mask = np.zeros(src.shape, dtype='uint8')
        filled_ref = ref.copy()

        similarity = round(score * 100, 2)

        result = ""
        if (similarity >= 0.00 and similarity <= 30.00):
            result = "POOR MATCH"
        elif (similarity > 30.00 and similarity <= 60.00):
            result = "AVERAGE MATCH"
        elif (similarity > 60.00 and similarity <= 90.00):
            result = "GOOD MATCH"
        else:
            result = "EXCELLENT MATCH"
        
        if (mode == "gui"):
            log += "".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Signature Comparison process completed."])
            
            messagebox.showinfo("Success", "".join(["Image Similarity: ", str(similarity), "%.", "\n\nResult: ", result]))
        else:
            print("".join(["\n", str(datetime.now().time()).split(".")[0], " ", "Signature Comparison process completed.", "\nSUCCESS:\nImage Similarity: ", str(similarity), "%.\nResult: ", result])) 

    except Exception as e:
        if (mode == "gui"):
            messagebox.showerror("Error", "".join(["Error: ", str(e)]))
        else:
            print("Error: {}".format(str(e)))

    finally:
        if (mode == "gui"):
            return log
