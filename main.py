import cv2
import numpy as np
import os
from PIL import Image
import argparse

def balance_green(image):
    #because of the apparent issue with the green channel , we blurr it and then reduce brightness
    b_channel, g_channel, r_channel = cv2.split(image)
    green_channel_blurred = cv2.GaussianBlur(g_channel, (7, 7), 0)
    scale_factor = 0.9
    green_channel_denoised = cv2.multiply(green_channel_blurred, np.array([scale_factor]))
    balanced_image = cv2.merge([b_channel, green_channel_denoised, r_channel])
    balanced_image = np.clip(balanced_image, 0, 255).astype(np.uint8)
    return balanced_image

def create_mask(image):
    #this is for locating the black circle
    gray_org_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh_xray = cv2.threshold(gray_org_image, 1, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh_xray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mask_circle = np.zeros_like(gray_org_image, dtype=np.uint8)
    for contour in contours:
        if len(contour) >= 5:
            ellipse = cv2.fitEllipse(contour)
            (center, (MA, ma), angle) = ellipse
            if 0.8 < MA / ma < 1.2:
                cv2.drawContours(mask_circle, [contour], -1, 255, thickness=cv2.FILLED)
    return mask_circle

def inpaint_circle(image, mask):
    #after identifying the dark circle ,this fills it with content based on its neighbour region
    mask = mask.astype(np.uint8)
    inpainted_image = cv2.inpaint(image, mask, inpaintRadius=100, flags=cv2.INPAINT_NS)
    return inpainted_image

def rotate_image(image, angle):
    #to solve the misalignment
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, -angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h))
    return rotated

def xray(image):
    alpha = 0.4
    beta = 5
    linear_contrast_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    yuv_xray_image = cv2.cvtColor(linear_contrast_image, cv2.COLOR_BGR2YUV)
    yuv_xray_image[:, :, 0] = cv2.equalizeHist(yuv_xray_image[:, :, 0])
    histeq_xray = cv2.cvtColor(yuv_xray_image, cv2.COLOR_YUV2BGR)
    
    mask_circle = create_mask(histeq_xray)
    inpainted_xray_image = inpaint_circle(histeq_xray, mask_circle)
    result_xray = cv2.cvtColor(inpainted_xray_image, cv2.COLOR_BGR2RGB)
    return result_xray

def process_image(single_image_path):
    xray_image = cv2.imread(single_image_path)
    xray_image = balance_green(xray_image)
    xray_image = xray(xray_image)

    return xray_image

def process_images_in_directory(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for filename in os.listdir(input_dir):
        if filename.endswith((".jpg", ".jpeg", ".png")):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            processed_image = process_image(input_path)
            Image.fromarray(processed_image).save(output_path)
            print(f"Processed and saved: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process pneumonia and healthy xray images.")
    parser.add_argument(type=str)
    parser.add_argument('input_directory', type=str)


    args = parser.parse_args()

    input_directory = args.input_directory
    output_directory = '/image_processing_files/Results'

    process_images_in_directory(input_directory, output_directory)
