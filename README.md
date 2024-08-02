# xray_image_processing

Damaged Xray images’ processing


Before applying any processing , we must analyze the images to understand the issues with them and what would be the best way to solve them for better classification of pneumonia.

 

By printing a sample image, we can see the problems in the images , so far it appears to have an unbalancing in the color channels and , there’s alot of noise , the slight rotation to the left and the big black circle .

To understand the unbalance of the colors we show the three-color channels separately :

 

It’s clear that the biggest problem is with the green channel , it has noise the most and very bright compared to the others so we start with this point 
 


This function isolates the green channel of the image, applies Gaussian blur to reduce noise, and then reduces the intensity by multiplying it by a scale factor (0.9). The blue and red channels are left unchanged. This step is beneficial for noise reduction and slight adjustment of brightness in the green channel, which is be particularly relevant to the observations in the distribution of the colors.

And then for handling the black circle we create two functions , one that is responsible for finding the black dot and the other fills that region in the original image based on the surrounding area. 
 

The create_mask(image) function converts the image to grayscale and creates a binary mask that detects and marks bright regions, drawing contours based on detected shapes and focusing on elliptical areas that may be significant in medical images. This mask is later used by the inpaint_circle(image, mask) function to in paint the image, a process that reconstructs lost or deteriorated parts using the cv2.INPAINT_NS method, which is effective for small regions. This inpainting helps clean up the X-ray image by removing or filling in bright areas that could obscure or distort important diagnostic details.

  
XRAY image after inpainting on grayscale 


For the slight misalignment we define this function to rotate the image by a specified angle. 
 

A lot of angle values were tried and the best one was 5 degrees counterclockwise (using -angle) , it helped making the image visually alligned but it didn’t help in the accuracy of the classifier.

To enhance contrast and remove the noise from the image the xray function is used to enhance the images by adjusting contrast, applying histogram equalization, and performing inpainting to improve the visibility of diagnostic features. It begins by enhancing the contrast and brightness using linear scaling and then converts the image to the YUV color space, where histogram equalization is applied to the luminance channel, making details more pronounced. The image is then converted back to the BGR color space, and a mask is created to identify specific regions, such as bright spots that may need correction. Inpainting is applied to these masked areas to fill in or remove artifacts, followed by brightening specific regions to ensure critical areas are clearly visible. Finally, the image is converted to RGB format and returned, resulting in a processed X-ray image with improved clarity and reduced noise, making it more suitable for medical analysis.

 

Finally we wrap it all in the process image function that reads an image and apply all that was explained before , this helps with the organization of the code and the reuse of all functions to loop and  process all images in the directory .


 




As instructed a main function was implemented to run the code , it takes an input directory and saves the processed images in the output directory named Results
 


After running the classify.py that uses the pre_trained model, we got the below results , which are a significant improvement from when the original images were used that gave 55% accuracy.

  

After the image processing we reach 77% accuracy


 

![image](https://github.com/user-attachments/assets/1ba61f9d-59d1-4332-8e47-253fe930ad58)
