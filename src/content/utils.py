import cv2
import os

def is_file_size_valid(file_url, mb_limit):
	file_size = os.path.getsize(file_url)
	if file_size > mb_limit:
		return False
	return True