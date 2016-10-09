#! /usr/bin/env python

import os, sys, argparse
from subprocess import Popen, PIPE

def getstatusoutput(cmd):
	"""Return (status, output) of executing cmd in a shell. Friendly to Windows also."""

	import sys
	mswindows = (sys.platform == "win32")

	import os
	if not mswindows:
		cmd = '{ ' + cmd + '; }'

	pipe = os.popen(cmd + ' 2>&1', 'r')
	text = pipe.read()
	sts = pipe.close()
	if sts is None: sts = 0
	if text[-1:] == '\n': text = text[:-1]
	return sts, text


parser = argparse.ArgumentParser(description='Draw contour of specified grid data.')
parser.add_argument('data', type=str, help='the path name of the data, or a function of x and y')
parser.add_argument('-g', '--gnuplot', metavar='gnuplot_pathname', type=str, help='the path name of gnuplot executable, \
in case it\'s not in the environment variable PATH')
parser.add_argument('-f', '--tofile', action='store_true', default=False, help='save the contour to a png file')
parser.add_argument('-l', '--levels',type=int, help='specify a nominal number of levels; \
the actual number will be adjusted by gnuplot to give simple labels.')
parser.add_argument('-i','--incremental_levels', metavar=('start', 'step', 'end'), type=float, nargs=3, help='\
specify levels from <start> to <end> with increment of <step>')
parser.add_argument('-d', '--discrete_levels', metavar='L', type=float, nargs='+', help='specify discrete levels')
parser.add_argument('-t', '--title', type=str, help='specify the tile of the image')
parser.add_argument('-x', '--xlabel', type=str, default='X axis', help='specify the x-lable')
parser.add_argument('-y', '--ylabel', type=str, default='Y axis', help='specify the y-lable')
parser.add_argument('-b', '--disable_label', action='store_true', default=False, help='turn off labels of the contour lines')

args = parser.parse_args()



# deal with optional argument 'gnuplot'
gnuplot_found = False
if args.gnuplot:
	if os.path.exists(args.gnuplot):
		gnuplot_pathname = args.gnuplot
		gnuplot_found = True
if not gnuplot_found:
	if sys.platform == 'win32':
		status, gnuplot_pathname = getstatusoutput('where gnuplot')
	else:
		status, gnuplot_pathname = getstatusoutput('which gnuplot')
	if status:
		sys.stderr.write('gnuplot executable not found\n')
		sys.exit(1)
gnuplotPipe = Popen(gnuplot_pathname, stdin = PIPE,stdout=PIPE,stderr=PIPE)
gnuplot = gnuplotPipe.stdin

# deal with optional argument 'tofile'
if args.tofile:
	gnuplot.write('set terminal png transparent small linewidth 2 medium enhanced\n')
	gnuplot.write('set output "{0}_contour.png"\n'.format(args.data))
elif sys.platform == 'win32':
	gnuplot.write("set term qt persist\n")
else:
	gnuplot.write("set term x11 persist\n")

# deal with optional argument 'levels'
if args.levels:
	gnuplot.write('set cntrparam levels {0}\n'.format(str(args.levels)))

# deal with optional argument 'incremental_levels'
if args.incremental_levels:
	gnuplot.write('set cntrparam levels incremental {0}\n'.format(','.join(str(x) for x in args.incremental_levels)))

# deal with optional argument 'discrete_levels'
if args.discrete_levels:
	gnuplot.write('set cntrparam levels discrete {0}\n'.format(','.join(str(x) for x in args.discrete_levels)))

# deal with optional argument 'title'
if args.title:
	title = args.title
else:
	title = 'contour map of ' + args.data


gnuplot.write('''
set xlabel "{0}"
set ylabel "{1}"
set title "{2}"
set contour base
set cntrlabel  format '%8.3g' font ',10' start 2 interval 20
unset surface
unset ztics
set view 0,0
unset label
set key at screen 0.2, 0.9 right top vertical Right noreverse enhanced noautotitle nobox
'''.format(args.xlabel, args.ylabel, title))


bad_data_info = '''
"Cannot contour non grid data" just means that you need for each X the same number of Y's. 
And Remember to add empty lines between groups of data.
'''


# deal with postional argument 'data'
if os.path.exists(args.data):

	# deal with optional argument diable_label
	if not args.disable_label:
		gnuplot.write('splot "{0}" with lines, "{0}" with labels\n'.format(args.data))
	else:
		gnuplot.write('splot "{0}" with lines\n'.format(args.data))

	out, err = gnuplotPipe.communicate()
	if err:
		sys.stderr.write('bad data format:\n'+err)
		if 'Cannot contour non grid data' in err:
			sys.stderr.write(bad_data_info)
		sys.exit(1)

else:
	# input data may be a function

	# deal with optional argument diable_label
	if not args.disable_label:
		gnuplot.write('splot {0} with lines, {0} with labels\n'.format(args.data))
	else:
		gnuplot.write('splot {0} with lines\n'.format(args.data))

	out, err = gnuplotPipe.communicate()
	if gnuplotPipe.returncode:
		sys.stderr.write('data not found or function format is uncorrect:\n'+err)
		sys.exit(1)






