## NOTES ##
'''

'''

## DEPENDENCIES ## 

from PIL import Image, ImageTk

## DEFINITIONS ##

def loadgraphics(path_roster):
	graphic_names = list(path_roster.keys())
	graphic_roster = {}
	for name in graphic_names:
		path = path_roster[name]
		graphic = Image.open(path)
		graphic_roster[name] = graphic
	return graphic_roster


def getdims(graphic):
	[w, h] = graphic.size
	graphic_dims = [w, h]
	return graphic_dims


def crop(graphic, w_ratio, h_ratio):
	graphic_dims = getdims(graphic)
	cropped_graphic = graphic.crop((0, 0, graphic_dims[0]*w_ratio,
		graphic_dims[1]*h_ratio))
	return cropped_graphic


def batch_crop(graphic_roster, w_ratio, h_ratio):
	graphic_names = list(graphic_roster.keys())
	for name in graphic_names:
		graphic = graphic_roster[name]
		graphic_roster[name] = crop(graphic, w_ratio, h_ratio)
	return graphic_roster


def resize(graphic, width=None, height=None):
	[w, h] = getdims(graphic)
	if width != None and height != None:
		newsize = (width, height)
		resized_graphic = graphic.resize(newsize)
	elif width != None and height == None:
		aspect = w/h
		new_height = int(width/aspect)
		newsize = (width, new_height)
		resized_graphic = graphic.resize(newsize)
	elif width == None and height != None:
		aspect = w/h
		new_width = int(height * aspect)
		newsize = (new_width, height)
		resized_graphic = graphic.resize(newsize)
	else:
		resized_graphic = graphic
	return resized_graphic


def batch_resize(graphic_roster, width=None, height=None):
	graphic_names = list(graphic_roster.keys())
	for name in graphic_names:
		graphic = graphic_roster[name]
		graphic_roster[name] = resize(graphic, width, height)
	return graphic_roster


def recolor(graphic, color):
	[r, g, b, alpha] = graphic.split()
	red = r.point(lambda i: color[0])
	green = g.point(lambda i: color[1])
	blue = b.point(lambda i: color[2])
	recolored_graphic = Image.merge('RGBA', (red, green, blue, alpha))
	return recolored_graphic


def batch_recolor(graphic_roster, color):
	graphic_names = list(graphic_roster.keys())
	for name in graphic_names:
		graphic = graphic_roster[name]
		graphic_roster[name] = recolor(graphic, color)
	return graphic_roster


def Image2PhotoImage(graphic_roster):
	graphic_names = list(graphic_roster.keys())
	for name in graphic_names:
		graphic_roster[name] = ImageTk.PhotoImage(graphic_roster[name])
	return graphic_roster


## EXECUTABLE ## 

