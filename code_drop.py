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

from time import time
from math import floor

class CodeDrop:
    """the class for the drops on the screen"""
    def __init__(self, x, y, yMax, speed, persistence):
        self.x = x
        self.origin = y
        self.min = y
        self.max = y
        self.yMax = yMax  # the greatest position on the Y axis that a drop can be
        self.speed = speed
        self.persistence = persistence # the time that the point of origin of the drop will take to start falling down
        self.birth = time()

    def getX(self):
        return self.x

    def getMin(self):
        return self.min

    def getMax(self):
        return self.max

    def update(self):
        """function to be called between each frame to determine the new position of the drop"""
        lasted = time() - self.birth
        offset = lasted - self.persistence
        if offset < 0:
            offset = 0
        self.min = floor(offset * self.speed + self.origin)
        self.max = floor(lasted * self.speed + self.origin)
        if self.min > self.yMax:
            self.min = self.yMax
        if self.max > self.yMax:
            self.max = self.yMax
