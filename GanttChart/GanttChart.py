import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
import matplotlib.dates
from matplotlib.dates import WEEKLY,MONTHLY, DateFormatter, rrulewrapper, RRuleLocator 
import numpy as np
from collections import OrderedDict
  
def _create_date(datetxt):
	"""Creates the date"""
	day,month,year=datetxt.split('-')
	date = dt.datetime(int(year), int(month), int(day))
	mdate = matplotlib.dates.date2num(date) 
	return mdate
 
def CreateGanttChart(fname):
	"""
	Create gantt charts with matplotlib
	Give file name.
	""" 
	
	d = OrderedDict()
	d['None'] = 'black'
	d['Josh'] = 'orange'
	d['Juppe'] = 'red'
	
	ylabels = []
	customDates = []
	colors = []
	
	try:
		textlist=open(fname).readlines()
	except:
		print "Failed to Read File"
	
	for tx in textlist:
		if not tx.startswith('#'):
			ylabel, startdate, enddate, person = tx.split(',')
			ylabels.append(ylabel)
			customDates.append([startdate, enddate])
			colors.append(d[person.replace('\n','')])
	
	ilen=len(ylabels)
	pos = np.arange(0.5,ilen*0.5+0.5,0.5)
	task_dates = {}
	for i,task in enumerate(ylabels):
		task_dates[task] = customDates[i]
	
	fig = plt.figure(figsize=(20,8))
	ax = fig.add_subplot(111)
	for i in range(len(ylabels)):
		start_date,end_date = task_dates[ylabels[i]]
		ax.barh((i*0.5)+0.5, float(end_date) - float(start_date), left=float(start_date), height=0.3, align='center', edgecolor='black', color=colors[i], alpha = 0.8)
	
	locsy, labelsy = plt.yticks(pos,ylabels)
	plt.setp(labelsy, fontsize = 14)
	plt.title(fname[:-4])
	
	ax.set_xlabel("Days")
	ax.set_ylim(ymin = -0.1, ymax = ilen*0.5+0.5)
	ax.grid(color = 'k', linestyle = ':')
	
	labelsx = ax.get_xticklabels()
	plt.setp(labelsx, fontsize=10)

	font = font_manager.FontProperties(size='small')
	ax.legend(loc=1,prop=font)

	ax.invert_yaxis()
	fig.autofmt_xdate()
	plt.savefig(fname[:-3] + 'png')
	if fname != "Rebuild.txt":
		plt.legend(d.keys())
	else:
		plt.legend(d.keys()[:-1])
	plt.show()

CreateGanttChart("Timeline.txt")