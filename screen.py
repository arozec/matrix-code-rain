# matrix code rain
# Copyright (C) 2015  Antoine Rozec

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

from code_drop import CodeDrop

from random import choice, random, randrange, uniform
import string
from math import floor
from os import get_terminal_size
from io import StringIO
from time import time, sleep

class Screen:
	"""the class that handle display and drop management"""
	def __init__(self,
			fps = 24, # number of frames per second
			dropDensity = 0.07, # how many new drops will appear each second (arbitrary value)
			dropSpeedRange = (15, 35), # the minimum and maximum speed that a drop may fall at in lines per second
			dropPersistenceRange = (0.5, 5), # the minimum and maximum time that a drop may keep pouring before falling
			chanceDropNotOnTop = 0.33, # the chance a drop has not to appear at the very top of the screen (0 beeing 0 percent and 1 beeing 100 percent)
			dropHeightRangePop = (0.25, 0.75)): # the minimum and maximum portion of the screen on the Y axis, that a drop may appear at (0 beeing 0 percent and 1 beeing 100 percent)
		self.width, self.height = get_terminal_size()
		self.frameDuration = 1 / fps
		self.dropDensity = dropDensity / fps # dividing by fps to keep the same rate of appearance since the process of drop creation is handled on a frame basis rather than a time basis
		self.dropSpeedRange = dropSpeedRange
		self.dropPersistenceRange = dropPersistenceRange
		self.chanceDropNotOnTop = chanceDropNotOnTop
		tmpMin = floor(dropHeightRangePop[0] * self.height)
		tmpMax = floor(dropHeightRangePop[1] * self.height)
		self.dropHeightRangePop = (tmpMin, tmpMax)
		self.dropList = []
		self.randomString = '' # to minimize the number of calls to a random function (which are quite time consuming), we choose to iterate over a single randomized string when composing the frame
		self.rsl = 1000 # the length of the string
		self.rsc = 0 # the index counter of the string
		myPrintable = string.ascii_letters + string.digits + string.punctuation
		for i in range(self.rsl):
			self.randomString += choice(myPrintable)
		self.pixels = [] # nested arrays of booleans representing if a pixel is blank or not
		for x in range(self.width):
			self.pixels.append([])
			for y in range(self.height):
				self.pixels[x].append(False)

	def __repr__(self):
		"""rendering function"""
		output = StringIO() # file like container to efficiently append white spaces or character to the render output depending on the status of the pixel
		for i in range(self.height):
			for j in range(self.width):
				if self.pixels[j][i]:
					if self.rsc == self.rsl:
						self.rsc = 0
					output.write(self.randomString[self.rsc])
					self.rsc += 1
				else:
					output.write(' ')
		return output.getvalue()

	def clearPixels(self):
		"""reset pixels function"""
		for x in range(self.width):
			for y in range(self.height):
				self.pixels[x][y] = False

	def newDrops(self):
		"""drop creation at each frame"""
		for x in range(self.width):
			if random() < self.dropDensity:
				self.createDrop(x)

	def update(self):
		"""creates a new frame and delete drops that are at the bottom of the screen"""
		toBeDeleted = []
		for i, drop in enumerate(self.dropList):
			drop.update()
			x = drop.getX()
			if drop.getMin() == self.height:
				toBeDeleted.append(i)
			else:
				for y in range(drop.getMin(), drop.getMax()):
					self.pixels[x][y] = True
		for i, j in enumerate(toBeDeleted):
			del self.dropList[j - i]

	def createDrop(self, x):
		"""creates a drop with random attributes"""
		if random() < self.chanceDropNotOnTop:
			y = randrange(*self.dropHeightRangePop)
		else:
			y = 0
		speed = uniform(*self.dropSpeedRange)
		persistence = uniform(*self.dropPersistenceRange)
		self.dropList.append(CodeDrop(x, y, self.height, speed, persistence))

	def wait(self, start):
		"""waits for the appropriate amount of time between each frame"""
		passedTime = time() - start
		if passedTime < self.frameDuration:
			sleep(self.frameDuration - passedTime)

	def run(self):
		"""main function, makes the program run forever"""
		while True:
			start = time()
			self.clearPixels()
			self.newDrops()
			self.update()
			print(self)
			self.wait(start)
