import cv2
import numpy as np

# A dummy function for the trackbars.
def nothing(x):
    pass

def main():
    """
    Control the color of the subtracted area using RGB trackbars.
    """
    try:
        # 1. Load the background image and the logo image
        background_image = cv2.imread("/root/hong_openCV/data/candies.png", cv2.IMREAD_COLOR)
        logo_image = cv2.imread("/root/hong_openCV/data/cow.png", cv2.IMREAD_COLOR)

        if background_image is None or logo_image is None:
            print("Error: Could not read one or more images. Please check the file paths.")
            return

        # 2. Resize the logo to match the background
        h, w = background_image.shape[:2]
        logo_resized = cv2.resize(logo_image, (w, h))

        # 3. Create a window and the trackbars
        window_name = "Image Subtraction"
        cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)
        
        cv2.createTrackbar("R", window_name, 0, 255, nothing)
        cv2.createTrackbar("G", window_name, 0, 255, nothing)
        cv2.createTrackbar("B", window_name, 0, 255, nothing)

        while True:
            # 4. Get the current trackbar positions
            r = cv2.getTrackbarPos("R", window_name)
            g = cv2.getTrackbarPos("G", window_name)
            b = cv2.getTrackbarPos("B", window_name)

            # 5. Create the color to fill the subtracted area
            fill_color = np.full(background_image.shape, (b, g, r), dtype=np.uint8)

            # 6. Perform the subtraction
            # We subtract the logo from the background where the logo exists
            subtracted_area = cv2.subtract(background_image, logo_resized)
            
            # 7. Create a mask from the logo to isolate the subtracted area
            gray_logo = cv2.cvtColor(logo_resized, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray_logo, 10, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            
            # 8. Separate the original background and the subtracted logo area
            background_only = cv2.bitwise_and(background_image, background_image, mask=mask_inv)
            
            # 9. Use the fill color to replace the subtracted area
            colored_subtracted_area = cv2.bitwise_and(fill_color, fill_color, mask=mask)

            # 10. Combine the unchanged background with the newly colored area
            final_image = cv2.add(background_only, colored_subtracted_area)
            
            # 11. Display the results
            cv2.imshow(window_name, final_image)

            # 12. Exit loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
