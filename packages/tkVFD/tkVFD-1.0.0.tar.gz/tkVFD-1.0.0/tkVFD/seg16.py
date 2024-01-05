## NOTES ##
'''

'''

## DEPENDENCIES ## 

from tkinter import Canvas, NW

from .utils import *
from .charLUTs import *

## DEFINITIONS ##

class seg16:

	def __init__(self, parent, width=None, height=None, 
		on_color=[204, 246, 250], off_color=[32, 32, 32], bg='black',
		use_DP=False, use_CC=False, use_Grid=True):

		self.parent = parent
		self.width = width
		self.height = height
		self.on_color = on_color
		self.off_color = off_color
		self.bg = bg
		self.use_DP = use_DP
		self.use_CC = use_CC
		self.use_Grid = use_Grid

		# generate list of graphics to load from file
		self.graphic_names = ['segA1_on', 'segA2_on', 'segB_on', 'segC_on',
			'segD1_on', 'segD2_on', 'segE_on', 'segF_on', 'segG1_on',
			'segG2_on', 'segH_on', 'segI_on', 'segJ_on', 'segK_on', 'segL_on',
			'segM_on', 'segA1_off', 'segA2_off', 'segB_off', 'segC_off',
			'segD1_off', 'segD2_off', 'segE_off', 'segF_off', 'segG1_off',
			'segG2_off', 'segH_off', 'segI_off', 'segJ_off', 'segK_off',
			'segL_off', 'segM_off']

		if self.use_DP:
			self.graphic_names.extend(['segDP_on', 'segDP_off'])

		if self.use_CC:
			self.graphic_names.extend(['segCC_on', 'segCC_off'])

		if self.use_Grid:
			self.graphic_names.append('Grid')

		# generate dictionary of graphic names and their path
		self.path_roster = {}
		rootdir = __file__.replace('seg16.py', '')
		for name in self.graphic_names:
			path = rootdir + '/Graphics/seg16/' + name + '.png'
			self.path_roster[name] = path

		self.graphic_roster = loadgraphics(self.path_roster)

		# crop graphics as required
		if self.use_DP == False and self.use_CC == False:
			self.graphic_roster = batch_crop(self.graphic_roster, 0.83, 1)
		
		# resize graphics
		self.graphic_roster = batch_resize(self.graphic_roster, 
			width=self.width, height=self.height)
		self.graphic_dims = getdims(self.graphic_roster['segB_on'])

		# recolor graphics
		for name in self.graphic_names:
			if 'on' in name:
				graphic = self.graphic_roster[name]
				color = self.on_color
				self.graphic_roster[name] = recolor(graphic, color)
			elif 'off' in name:
				graphic = self.graphic_roster[name]
				color = self.off_color
				self.graphic_roster[name] = recolor(graphic, color)

		self.disp = Canvas(self.parent, 
			width=self.graphic_dims[0], height=self.graphic_dims[1],
			bg=self.bg, highlightthickness=0)

		self.graphic_roster = Image2PhotoImage(self.graphic_roster)


	def control(self, switches, DP=None, CC=None):
		for i in range(len(switches)):
			switch = switches[i]
			seg = self.graphic_names[i].replace('_on', '')
			if switch == 1:
				seg_on = self.graphic_roster[seg + '_on']
				self.disp.create_image(0, 0, image=seg_on, anchor=NW)
			else:
				seg_off = self.graphic_roster[seg + '_off']
				self.disp.create_image(0, 0, image=seg_off, anchor=NW)

		if self.use_DP:
			if DP == 1:
				segDP_on = self.graphic_roster['segDP_on']
				self.disp.create_image(0, 0, image=segDP_on, anchor=NW)
			else:
				segDP_off = self.graphic_roster['segDP_off']
				self.disp.create_image(0, 0, image=segDP_off, anchor=NW)

		if self.use_CC:
			if CC == 1:
				segCC_on = self.graphic_roster['segCC_on']
				self.disp.create_image(0, 0, image=segCC_on, anchor=NW)
			else:
				segCC_off = self.graphic_roster['segCC_off']
				self.disp.create_image(0, 0, image=segCC_off, anchor=NW)

		if self.use_Grid:
			Grid = self.graphic_roster['Grid']
			self.disp.create_image(0, 0, image=Grid, anchor=NW)

		return self.disp


	def char(self, char, DP=None, CC=None):
		# seg16_LUT pulled from CharLUTs.py file
		self.disp = self.control(seg16_LUT[char], DP, CC)
		return self.disp


	def clear(self):
		self.disp.delete('all')
		return self.disp


## EXECUTABLE ## 

