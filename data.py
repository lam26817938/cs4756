import airsim
import time
import os
from datetime import datetime

# Base directory where all runs will be stored
base_directory = 'airsim_data'
if not os.path.exists(base_directory):
    os.makedirs(base_directory)

# Create a new directory for each run based on the current timestamp
run_id = datetime.now().strftime('%Y%m%d_%H%M%S')
run_directory = os.path.join(base_directory, run_id)
os.makedirs(run_directory)

# Connect to the AirSim simulator
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)
car_controls = airsim.CarControls()

# Main loop
while True:
    # Get state of the car
    car_state = client.getCarState()
    print(f"Speed {car_state.speed}, Gear {car_state.gear}")

    # Set the controls for the car
    car_controls.throttle = 1
    car_controls.steering = 1
    client.setCarControls(car_controls)

    # Let car drive a bit
    time.sleep(1)

    # Collect camera and sensor images
    responses = client.simGetImages([
        airsim.ImageRequest(0, airsim.ImageType.DepthVis),
        airsim.ImageRequest(1, airsim.ImageType.DepthPlanar, True),
        airsim.ImageRequest(0, airsim.ImageType.Scene),
        airsim.ImageRequest(1, airsim.ImageType.Segmentation),
        airsim.ImageRequest(0, airsim.ImageType.Infrared),
        airsim.ImageRequest(0, airsim.ImageType.Lidar, True)
    ])
    print(f'Retrieved images: {len(responses)}')

    # Save images in the specified run directory
    for idx, response in enumerate(responses):
        if response.pixels_as_float:
            # Handle float data (LIDAR and depth)
            filename = os.path.join(run_directory, f'py1_{idx}.pfm')
            print(f"Type {response.image_type}, size {len(response.image_data_float)}")
            airsim.write_pfm(filename, airsim.get_pfm_array(response))
        else:
            # Handle visual data (RGB, segmentation, infrared)
            filename = os.path.join(run_directory, f'py1_{idx}.png')
            print(f"Type {response.image_type}, size {len(response.image_data_uint8)}")
            airsim.write_file(filename, response.image_data_uint8)

    # Log additional telemetry data
    with open(os.path.join(run_directory, 'telemetry.csv'), 'a') as f:
        f.write(f"{datetime.now().isoformat()}, {car_state.speed}, {car_state.gear}, {car_controls.steering}, {car_controls.throttle}\n")
