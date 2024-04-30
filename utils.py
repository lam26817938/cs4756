import os

def rename_png_files(directory):
    # List all files in the directory
    files = os.listdir(directory)
    # Filter only PNG files
    png_files = [file for file in files if file.endswith('.png')]

    # Rename PNG files sequentially
    for i, png_file in enumerate(png_files):
        # Generate new file name
        new_name = f'img_{i}.png'
        # Construct full paths for old and new names
        old_path = os.path.join(directory, png_file)
        new_path = os.path.join(directory, new_name)
        # Rename the file
        os.rename(old_path, new_path)
        print(f'Renamed "{old_path}" to "{new_path}"')

# Directory containing PNG files to be renamed
directory = './record/images'

# Call the function to rename PNG files
rename_png_files(directory)
