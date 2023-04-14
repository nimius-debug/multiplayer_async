from os import walk
import pygame

def import_folder(path):
	print("import_folder")
	surface_list = []
	print(walk(path))
	for _, __, img_files in walk(path):
		print("walk")
		print(img_files)
		for image in img_files:
			print(image)
			full_path = path + "\\" + image
			print(full_path)
			image_surf = pygame.image.load(full_path).convert_alpha()
			print(image_surf)
			surface_list.append(image_surf)

	return surface_list