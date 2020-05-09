
class Config:
	def __init__(self):
		#Image drawing
		self.rectangle_color = (255,255,255)
		self.rectangle_thickness = 5
		self.rectangle_height = 100
		self.rectangle_width = 100


		#font for drawing image
		self.font_scale = 2
		self.font_color = (255,255,255)
		self.font_thickness = 3

		#glues, stored as (name, strength) pairs
		self.glues = [
				("a",2),
				("b",1),
				("c",2),
				("d",0)
			]

		#tiles, stored as (name,(glue_list)) where glue_list is stored in west,north,east,south order
		self.tiles = [
				("t1",("a","b","c","a")),
				("t2",("a","a","a","a")),
				("t3",("b","b","b","b")),
				("t4",("c","c","c","c"))
		]

		#seed tiles stored as (coordinate,tilename) pairs
		self.seed_tiles = [
				((0,0),"t1"),
				((1,0),"t2")
		]

		#temperature
		self.temperature = 2

		#max new tiles to add
		self.max_iters = 1000

		#save image or not and if so folder
		self.save_images = True
		self.save_folder = "./NewVideoImages/"











