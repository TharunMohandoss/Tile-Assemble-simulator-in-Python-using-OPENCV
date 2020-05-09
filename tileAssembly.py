import cv2
import numpy as np
from config import Config
import random

random.seed(0)


# class Tile:
# 	def __init__(self,name,glues):
# 		self.name = name
# 		self.glues = glues

class Image:
	def __init__(self,tas,config):
		self.config = config
		self.current_config = tas.current_config
		current_config = tas.current_config
		self.tiles_add_order = tas.tiles_add_order

		positions = list(current_config.keys())
		if len(positions) == 0:
			print('Empty config hence empty image')
			return

		westmost  = positions[0][0]
		northmost = positions[0][1]
		eastmost  = positions[0][0]
		southmost = positions[0][1]

		for position in positions:
			westmost  = min(westmost,position[0])
			northmost = max(northmost,position[1])
			eastmost  = max(eastmost,position[0])
			southmost = min(southmost,position[1])

		#initialize image as black pixels
		height = ( northmost - southmost + 1 )*self.config.rectangle_height
		width  = ( eastmost - westmost + 1 )*self.config.rectangle_width
		self.image = np.zeros((height,width),np.uint8)

		frame_index = 0
		for position in self.tiles_add_order:
			pixel_y = (northmost - position[1])*self.config.rectangle_height
			pixel_x = (position[0] - westmost)*self.config.rectangle_width
			tile_name = self.current_config[position][0]
			self.drawSquare(
					position = (pixel_x,pixel_y),
					text = tile_name
				)
			if self.config.save_images:
				cv2.imwrite(self.config.save_folder+str(frame_index)+'.png',self.image)
				frame_index += 1





		#first find the leftmost, topmost, rightmost and bottommost tiles


	# def __init__(self,width,height,config):
	# 	self.image = np.zeros((height,width),np.uint8)
	# 	self.config = config

	def drawSquare(self,position,text):
		cv2.rectangle(
				img = self.image,
				pt1 = ( position[0] , position[1] ),
				pt2 = ( position[0] + self.config.rectangle_height , position[1] + self.config.rectangle_width ),
				color = self.config.rectangle_color,
				thickness = self.config.rectangle_thickness
			)

		cv2.putText(
				img = self.image,
				text = text,
				org = ( position[0] + int(self.config.rectangle_height*(0.5 - 0.1*len(text))) , position[1] + int(self.config.rectangle_width*0.55) ),
				fontFace = cv2.FONT_HERSHEY_PLAIN,
				fontScale = int(self.config.font_scale),
				color = self.config.font_color,
				thickness = int(self.config.font_thickness)
			)

	def showImage(self):
		cv2.imshow("Black Image",self.image)
		cv2.waitKey(0)
		exit(0)

class TAS:
	def __init__(self,config):
		self.config = config

		self.glue_dict = dict()
		for i in range(len(self.config.glues)):
			self.glue_dict[self.config.glues[i][0]] = self.config.glues[i]

		self.tile_dict = dict()
		for i in range(len(self.config.tiles)):
			self.tile_dict[self.config.tiles[i][0]] = self.config.tiles[i]

		#new tile candidates
		self.new_tile_candidates = dict()

		#add order for easy visualzation
		self.tiles_add_order = []

		#create seed tiles in current_config
		self.current_config = dict()
		for i in range(len(self.config.seed_tiles)):
			coordinates = self.config.seed_tiles[i][0]
			new_tile = self.tile_dict[self.config.seed_tiles[i][1]]
			self.addNewTile(
					coordinates = coordinates,
					tile = new_tile
				)

	def simulate(self,max_iters):
		for i in range(max_iters):
			new_tile_candidate_positions = list(self.new_tile_candidates.keys())
			if len(new_tile_candidate_positions) == 0:
				print('Simulation done, no more possible additions')
				return

			random_coordinate = random.choice(new_tile_candidate_positions)
			random_candidate_tile = random.choice(self.new_tile_candidates[random_coordinate])
			self.addNewTile(random_coordinate,random_candidate_tile)
		print('Max iters : ',max_iters,' reached')


	def addNewTile(self,coordinates,tile):
		if coordinates in self.current_config:
			print('Can\'t add tile since tile exists')
			return
		if coordinates in self.new_tile_candidates:
			del self.new_tile_candidates[coordinates]
		self.current_config[coordinates] = tile
		self.tiles_add_order.append(coordinates)
		self.updateNeighbouringTilesAsCandidates(coordinates)



	def updateNeighbouringTilesAsCandidates(self,coordinates):
		x = coordinates[0]
		y = coordinates[1]

		neighbours = [(-1,0),(1,0),(0,-1),(0,1)]

		for neighbour in neighbours:
			new_coordinates = (x+neighbour[0],y+neighbour[1])
			if new_coordinates not in self.current_config:
				self.updateCandidate(new_coordinates)

	def updateCandidate(self,coordinates):
		x = coordinates[0]
		y = coordinates[1]

		if (x,y) in self.current_config:
			print('Unexpected entry handled')
			if (x,y) in self.new_tile_candidates:
				del self.new_tile_candidates[(x,y)]
			return

		possible_tiles = []
		for candidate_tile in self.config.tiles:
			total_glue = 0

			#west position
			if (x-1,y) in self.current_config:
				current_tile = self.current_config[(x-1,y)]
				if current_tile[1][2] == candidate_tile[1][0]:
					total_glue += self.glue_dict[current_tile[1][2]][1]

			#north position
			if (x,y+1) in self.current_config:
				current_tile = self.current_config[(x,y+1)]
				if current_tile[1][3] == candidate_tile[1][1]:
					total_glue += self.glue_dict[current_tile[1][3]][1]

			#east position
			if (x+1,y) in self.current_config:
				current_tile = self.current_config[(x+1,y)]
				if current_tile[1][0] == candidate_tile[1][2]:
					total_glue += self.glue_dict[current_tile[1][0]][1]

			#south position
			if (x,y-1) in self.current_config:
				current_tile = self.current_config[(x,y-1)]
				if current_tile[1][1] == candidate_tile[1][3]:
					total_glue += self.glue_dict[current_tile[1][1]][1]

			if total_glue >= self.config.temperature:
				possible_tiles.append(candidate_tile)

		if len(possible_tiles)>0:
			self.new_tile_candidates[(x,y)] = possible_tiles
		elif (x,y) in self.new_tile_candidates:
			del self.new_tile_candidates[(x,y)]







config = Config()
tas = TAS(config)
tas.simulate(config.max_iters)
cur_image = Image(tas,config)
cur_image.showImage()

# print(tas.current_config)




# cur_image = Image(200,200,config)
# cur_image.drawSquare((0,0),"1")
# cur_image.showImage()



