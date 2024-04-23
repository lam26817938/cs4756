import airsim
import cv2
import numpy as np

# Connect to the AirSim simulator 
client = airsim.CarClient()
client.confirmConnection()

# Get camera images from the simulator
responses = client.simGetImages([
    airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)
])

for response in responses:
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)
    img_rgb = img1d.reshape(response.height, response.width, 3)

    # Save or process the image
    cv2.imwrite('frame.png', img_rgb)