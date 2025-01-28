import os
import glob

def delete_cropped_images(directory, prefix):
    """
    Deletes all images with the specified prefix in the specified directory.

    Parameters:
    directory (str): The path to the directory containing the images.
    prefix (str): The prefix of the files to delete.
    """
    # Construct the search pattern for the files with the specified prefix
    search_pattern = os.path.join(directory, f"{prefix}*")

    # Use glob to find all files that match the search pattern
    files_to_delete = glob.glob(search_pattern)

    # Iterate over the list of files and delete each one
    for file_path in files_to_delete:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

# Example usage:
directory = r'screenshot'  # Replace with the path to your directory
prefix = 'cropped_screenshot_'  # Replace with the prefix of your files
delete_cropped_images(directory, prefix)
