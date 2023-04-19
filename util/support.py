import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../server'))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../client'))
import pygame

#r'C:\Users\jorge\Alquimista\Hackton\pygameHack\multi_p\character'
def import_folder(path):
    # Initialize a hidden display
	# os.environ['SDL_VIDEODRIVER'] = 'dummy'
	
	# pygame.display.init()
	# pygame.display.set_mode()
 
 
	surface_list = []
	for _,_,img_files in os.walk(path):
		
		for image in img_files:
			full_path = path + '/' + image
			image_surf = pygame.image.load(full_path)
			
			print(image_surf)
			surface_list.append(image_surf)
			

	return surface_list