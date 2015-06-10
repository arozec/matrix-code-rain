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

from argparse import ArgumentParser, RawDescriptionHelpFormatter

def getArgs():
        """creating argument parser, then return the result as a dictionnary to be fed to the sreen constructor"""
        parser = ArgumentParser(formatter_class = RawDescriptionHelpFormatter, description = 'this program displays on the terminal falling drops of code, like in the matrix movie. Press "Ctrl C" to end program. WARNING: set your terminal not to display an infinite number of lines since this program may generate up to several thouthands of lines per second, you may quickly run out of memory')
        parser.add_argument('-f', '--fps', nargs = '?', type = int, help = 'the number of frames per second at which the program displays (if the screen stutters, try decreasing this value, base value: 24)')
        parser.add_argument('-d', '--density', nargs = '?', type = float, help= 'a decimal number representing how frequently drops will appear on the screen (arbitrary value, base value 0.07)')
        parser.add_argument('-s', '--speed', nargs = 2, type = float, help = 'two decimal or integers decribing the range of possible speeds for the drops to fall at (values expressed in lines per second, base values: 15 35)')
        parser.add_argument('-p', '--persistence', nargs = 2, type = float, help = 'two decimal or integers decribing the range of possible duration that the drop can pour before falling down the screen (values expressed in seconds, base values: 0.5 5)')
        parser.add_argument('-n', '--notontop', nargs = '?', type =  float, help = 'a decimal number describing the chance for a drop not to appear on top of the screen, base value: 0.33 meaning 33%% chance')
        parser.add_argument('-m', '--middlerange',  nargs = 2, type =  float, help = 'two decimal or integers decribing the proportion of the screen in which the drops that will not appear on top of the screen will appear in (base value: 0.25 0.75, meaning between 1/4 and 3/4 of the screen)')

        args = parser.parse_args()
        result = {}
        if args.fps != None:
                result['fps'] = args.fps
        if args.density != None:
                result['dropDensity'] = args.density
        if args.speed != None:
                result['dropSpeedRange'] = swap(args.speed)
        if args.persistence != None:
                result['dropPersistenceRange'] = swap(args.persistence)
        if args.notontop != None:
                result['chanceDropNotOnTop'] = args.notontop
        if args.middlerange != None:
                result['dropHeightRangePop'] = swap(args.middlerange)
        return result

def swap(arg):
        """swaping values if the greatest is before the least, then returning the couple of values as a tuple"""
        if arg[0] > arg[1]:
                return (arg[1], arg[0])
        else:
                return tuple(arg)
