import matplotlib.pyplot as plt
import numpy as np
import cv2
import datetime
import time


class CodeCycler:
    def __init__(self, spacing_ratio, markersize):
        self.spacing_ratio = spacing_ratio
        self.markersize = markersize
    
    def generate_marker_grid(self, seconds):
        assert 0 <= seconds <= 59, "Seconds must be between 0 and 59"
        
        # Generate a marker image
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        marker_image = cv2.aruco.generateImageMarker(dictionary, seconds, self.markersize)
        marker_image = np.array(marker_image)

        M = marker_image

        # Define the size of the whitespace and the number of rows and columns of tiles
        whitespace = int(self.spacing_ratio * self.markersize)
        num_rows = 5  # Number of rows of tiles
        num_cols = 10  # Number of columns of tiles

        # Calculate the size of the new image
        tile_width = M.shape[1]
        tile_height = M.shape[0]
        new_width = num_cols * tile_width + (num_cols + 1) * whitespace
        new_height = num_rows * tile_height + (num_rows + 1) * whitespace

        # Initialize the new image with zeros (black)
        new_image = 255 * np.ones((new_height, new_width), dtype=np.uint8)

        # Tile the image
        for row in range(num_rows):
            for col in range(num_cols):
                top_left_y = row * tile_height + (row + 1) * whitespace
                top_left_x = col * tile_width + (col + 1) * whitespace
                new_image[top_left_y:top_left_y + tile_height, top_left_x:top_left_x + tile_width] = M
        
        return new_image
    
    def run(self, single=False):
        fig, ax = plt.subplots()  # Create a figure and an axes
        ax.set_xticks([])  # Remove x-axis ticks
        ax.set_yticks([])  # Remove y-axis ticks
        
        while True:
            try:
                current_utc_time = datetime.datetime.utcnow()
                one_second_later = current_utc_time + datetime.timedelta(seconds=1)
                
                seconds = int(current_utc_time.second)
                print(seconds)
                
                image = self.generate_marker_grid(seconds)
                image_h, image_w = image.shape
                white_image = 255.0 * np.ones((image_h, image_w), dtype=np.uint8)
                
                n_cycles = 1              
                for _ in range(n_cycles):
                    ax.clear()  # Clear the previous image
                    ax.imshow(image, cmap='gray')  # Display the new image
                    plt.pause(1 / (2 * n_cycles) - 0.05)
                    
                    ax.clear()  # Clear the previous image
                    ax.imshow(white_image, cmap='gray')  # Display the new image
                    plt.pause(1 / (2 * n_cycles) - 0.05)
                    
                    plt.draw()  # Redraw the current figure              
                
                current_utc_time_new = datetime.datetime.utcnow()
                utc_time_delta = one_second_later - current_utc_time_new
                                
                time.sleep(max(0, utc_time_delta.total_seconds()))
                
                if single:
                    plt.show()
                    break
                
                
            except KeyboardInterrupt:
                print("Signal shutdown...")
                break
        plt.close()  # Close the plot window when done


if __name__ == "__main__":
    code_cycler = CodeCycler(spacing_ratio=0.1, markersize=50)
    code_cycler.run(single=False)

