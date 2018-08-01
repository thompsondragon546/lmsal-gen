from colortext import Color
from datetime import datetime
import getpass
import numpy as np
import os
import time

MAIN_DIR = "/Users/%s/Desktop/lmsal" % getpass.getuser()

class Recorder(object):

	def __init__(self, database_name):
		self.DATABASE_NAME = "/Users/%s/Desktop/lmsal/resources/region-data/%s" % (getpass.getuser(), database_name)
		self.INFO = Color.RED + "[INFO]\t" + Color.YELLOW
		self.INFO_TAB = Color.RED + "[INFO]\t==> " + Color.YELLOW
		self.WRITE = Color.GREEN + "[WRITE]\t" + Color.YELLOW
		self.NEW_LINE = Color.WHITE + "\n" + "-" * 75

		with open(self.DATABASE_NAME, "w") as db:
			db.write("ID,INSTR,WAVLEN,DATE,TIME,PXL_X,PXL_Y,HPC_X,HPC_Y,PXL_SIZE_X,PXL_SIZE_Y,HPC_SIZE_X,HPC_SIZE_Y,INTEN_LOW_THRESH,INTEN_HIGH_THRESH,AVG_INTEN,MED_INTEN,MAX_INTEN,\n")

		print self.NEW_LINE

	def write_ID(self, ID):
		print self.INFO + "Loop ID %05d" % ID
		with open(self.DATABASE_NAME, "a") as db:
			print self.WRITE + "Recording ID"
			print self.INFO_TAB + "%05d" % ID
			db.write("%05d," % ID)
		self.rest()

	def write_gen_info(self, instr, wavelen):
		with open(self.DATABASE_NAME, "a") as db:
			print self.WRITE + "Recording instrument"
			print self.INFO_TAB + "%s" % instr
			db.write("%s," % instr)
			print self.WRITE + "Recording wavelength"
			print self.INFO_TAB + "%.1f" % wavelen.value
			db.write("%.1f," % wavelen.value)
		self.rest()

	def write_datetime(self, datetime):
		with open(self.DATABASE_NAME, "a") as db:
			when = datetime.strftime("%Y-%m-%d %H:%M:%S")
			print self.WRITE + "Recording date and time"
			date = when.split(" ")[0]
			time = when.split(" ")[1]
			print self.INFO_TAB + "%s" % date
			print self.INFO_TAB + "%s" % time
			db.write("%s,%s," % (date, time))
		self.rest()

	def write_xywhere(self, where):
		with open(self.DATABASE_NAME, "a") as db:
			where_x = where[0]
			where_y = where[1]
			print self.WRITE + "Recording cartesian pixel location"
			print self.INFO_TAB + "(%d,%d)" % (where_x, where_y)
			db.write("%d,%d," % (where_x, where_y))
		self.rest()

	def write_hpcwhere(self, where):
		with open(self.DATABASE_NAME, "a") as db:
			where_x = where.Tx.value
			where_y = where.Ty.value
			print self.WRITE + "Recording helioprojective coordinate location"
			print self.INFO_TAB + "(%.3f,%.3f)" % (where_x, where_y)
			db.write("%.3f,%.3f," % (where_x, where_y))
		self.rest()

	def write_xysize(self, size):
		with open(self.DATABASE_NAME, "a") as db:
			print self.WRITE + "Recording pixel size"
			print self.INFO_TAB + "%dx%d" % (size, size)
			db.write("%d,%d," % (size, size))
		self.rest()

	def write_hpcsize(self, bl, tr):
		with open(self.DATABASE_NAME, "a") as db:
			size_x = tr.Tx.value - bl.Tx.value
			size_y = tr.Ty.value - bl.Ty.value
			print self.WRITE + "Recording helioprojective size"
			print self.INFO_TAB + "%dx%d" % (size_x, size_y)
			db.write("%d,%d," % (size_x, size_y))
		self.rest()

	def write_inten(self, low_thresh, high_thresh, avg, med, max):
		with open(self.DATABASE_NAME, "a") as db:
			print self.WRITE + "Recording intensity low threshold"
			print self.INFO_TAB + "%.1f" % low_thresh
			db.write("%.1f," % low_thresh)
			print self.WRITE + "Recording intensity high threshold"
			print self.INFO_TAB + "%.1f" % high_thresh
			db.write("%.1f," % high_thresh)
			print self.WRITE + "Recording average intensity"
			print self.INFO_TAB + "%.3f" % avg
			db.write("%.3f," % avg)
			print self.WRITE + "Recording median intensity"
			print self.INFO_TAB + "%.3f" % med
			db.write("%.3f," % med)
			print self.WRITE + "Recording maximum intensity"
			print self.INFO_TAB + "%.1f" % max
			db.write("%.1f," % max)
		self.rest()

	def write_image(self, type, id, data, instr, wav):
		if type == 0:
			name = "raw image"
			dir = "resources/region-data/raw-images"
		elif type == 1:
			name = "binary image"
			dir = "resources/region-data/binary-images"
		elif type == 2:
			name = "threshold image"
			dir = "resources/region-data/threshold-images"
		
		print self.INFO_TAB + "%05d%s%d.npy" % (id, instr, int(wav.value))
		print self.WRITE + "Saving %s to %s" % (name, dir)
		np.save("%s/%s/%05d" % (MAIN_DIR, dir, id), data)
		self.rest()

	def new_line(self):
		with open(self.DATABASE_NAME, "rb+") as db:
			print self.INFO + "Finished entry; recording new line" + self.NEW_LINE
			db.seek(-1, os.SEEK_END)
			db.truncate()
			db.write("\n")
		self.rest()

	def error_line(self):
		with open(self.DATABASE_NAME, "a") as db:
			print self.INFO + "Off-disk loop identified; skipping"
			db.write("OFF_DISK," * 11)
		self.new_line()

	def rest(self):
		time.sleep(0.05)
