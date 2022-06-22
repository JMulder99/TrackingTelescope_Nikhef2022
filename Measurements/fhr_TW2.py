#!/usr/bin/env python3

# fhr.py extended to work for 2 DAQ-boards. It should be quite easy to extend this file to work with even more boards.

from alpidedaqboard import alpidedaqboard
import argparse
import datetime
import os
import array
import json
from tqdm import tqdm
import os
import time

now=datetime.datetime.now()

def suffixed_int(i):
    if i[-1]=='G': return int(i[:-1])*1000*1000*1000
    if i[-1]=='M': return int(i[:-1])*1000*1000
    if i[-1]=='k': return int(i[:-1])*1000
    return int(i)

parser=argparse.ArgumentParser(description='The even mightier threshold scanner')
parser.add_argument('--serial1' ,'-s',help='serial number of the first DAQ board')
parser.add_argument('--serial2','-s2', help='serial number of the second DAQ board', default=False)
parser.add_argument('--prim', '-p', help='the primary board')
parser.add_argument('--chipid' ,'-c',type=int,help='Chip ID (default: 0x10)',default=0x10)
parser.add_argument('--vcasn_b2'  ,'-vc1',type=int,help='ALPIDE VCASN DAC setting for the second board')
parser.add_argument('--vcasn_b1'  ,'-vc2',type=int,help='ALPIDE VCASN DAC setting for the second board')
parser.add_argument('--vcasn2' ,'-w',type=int,help='ALPIDE VCASN2 DAC setting')
parser.add_argument('--vclip'  ,'-x',type=int,help='ALPIDE VCLIP DAC setting')
parser.add_argument('--ithr'   ,'-i',type=int,help='ALPIDE ITHR DAC setting')
parser.add_argument('--vresetd',     type=int,help='ALPIDE VRESETD DAC setting (default: 147)',default=147)
parser.add_argument('--dctrl'  ,     action='store_true',help='use readout via DCTRL')
parser.add_argument('--strobelength','-l',type=int,help='strobe length (@ALPIDE clks) (default=100)',default=100)
#parser.add_argument('--spacing','-d',type=int,help='trigger sapcing (@80MHz) (default = 2 x strobelength+10')
parser.add_argument('--ntrg'   ,'-n',type=suffixed_int,help='number of triggers per setting (default=100k)',default='100k')
parser.add_argument('--foldername' ,'-o',help='name of the folder where the datafiles will be saved.')
parser.add_argument('--path' ,help='Path to directory for data saving',default=".")
parser.add_argument('--dtime',help='Total time to measure in seconds',default="20")
args=parser.parse_args()

#if not args.spacing: args.spacing=args.strobelength*2+10

if not args.serial1 or not args.serial2:
	raise TypeError("Serial 1 and Serial 2 must be specified.") 

# setting the path / foldername
if not args.foldername: args.foldername = 'scan_'  + now.strftime('%Y%m%d_%H:%M:%S')
if args.path: args.path = args.path + '/' + args.foldername 
else: args.path = args.foldername

# making the new folder
try:
	os.mkdir(args.path)
except OSError:
	print ("Creation of the directory %s failed" %args.path)



with open('%s/params.json'%(args.path),'w') as f:
    f.write(json.dumps(vars(args)))

try:
	daq1=alpidedaqboard.ALPIDEDAQBoard(args.serial1)
	daq2=alpidedaqboard.ALPIDEDAQBoard(args.serial2)
	daqs=[daq1, daq2]
except ValueError as e:
	print(e)
	raise SystemExit(-1)

for serial, daq in zip([args.serial1, args.serial2], daqs):
	daq.power_on()
	print(daq.power_status())

	#just in case we got up on the wrong side of the fw...
	daq.fw_reset()
	daq.alpide_cmd_issue(0xD2) # GRST for ALPIDE
	# now for monitoring, also start clean
	daq.fw_clear_monitoring()


	if args.vcasn_b1 and serial == args.serial1: daq.alpide_reg_write(0x604,args.vcasn_b1 ,chipid=args.chipid)
	if args.vcasn_b2 and serial == args.serial2: daq.alpide_reg_write(0x604,args.vcasn_b2 ,chipid=args.chipid)
	if args.vcasn2: daq.alpide_reg_write(0x607,args.vcasn2,chipid=args.chipid)
	if args.vclip : daq.alpide_reg_write(0x608,args.vclip ,chipid=args.chipid)
	if args.ithr  : daq.alpide_reg_write(0x60E,args.ithr  ,chipid=args.chipid)

	daq.alpide_cmd_issue(0xE4) # PRST
	daq.alpide_reg_write(0x0004,0x0000           ,chipid=args.chipid) # disable busy monitoring
	daq.alpide_reg_write(0x0005,args.strobelength,chipid=args.chipid) # strobe length
	daq.alpide_reg_write(0x0010,0x0030           ,chipid=args.chipid) # initial token, SDR, disable manchester, previous token == self!!!
	daq.alpide_reg_write(0x0001,0x000D,chipid=args.chipid) # normal readout, TRG mode
	daq.alpide_pixel_mask_all(False   ,chipid=args.chipid) # unmask
	daq.alpide_pixel_pulsing_all(False,chipid=args.chipid) # just make sure these pulsing registers have the same value
	daq.alpide_cmd_issue(0x63) # RORST (needed!!!)

	if args.dctrl:
	    daq.alpide_reg_write(0x0001,0x020D,chipid=args.chipid) # normal readout, TRG mode, CMU RDO
	    daq.rdoctrl.delay_set.write(2*args.strobelength+100) # when to start reading (@80MHz, i.e. at least strobe-time x2 + sth.)
	    daq.rdoctrl.chipid.write(args.chipid)
	    daq.rdoctrl.ctrl.write(1) # enable DCTRL RDO
	    daq.rdomux.ctrl.write(2) # select DCTRL RDO
	else:
	    daq.alpide_reg_write(0x0001,0x000D,chipid=args.chipid) # normal readout, TRG mode
	    daq.rdopar.ctrl.write(1) # enable parallel port RDO
	    daq.rdomux.ctrl.write(1) # select parallel port RDO
	    daq.xonxoff.ctrl.write(1) # enable XON XOFF

	# daq.trg.ctrl.write(0b1110) # master mode,  mask ext trg, mask ext busy, do not force forced busy
	daq.trg.ctrl.write(0b0000) # replica
	daq.trgseq.dt_set.write(8000) # 100 ns
	daq.trg.opcode.write(0x55) # TRG OPCODE

	daq.alpide_reg_write(0x602,args.vresetd,chipid=args.chipid)
	daq.trgseq.ntrg_set.write(1) # for the time being: ping pong

if args.prim == args.serial1:
	daq1.trg.ctrl.write(0b1000)
else:
	daq2.trg.ctrl.write(0b1000)

# with open('%s/%s.raw'%(args.path, args.serial1),'wb') as datafile1, open('%s/%s.raw'%(args.path, args.serial2),'wb') as datafile2:
with open('%s/board1.raw'%(args.path),'wb') as datafile1, open('%s/board2.raw'%(args.path),'wb') as datafile2:

	datafiles = [datafile1, datafile2]

    # loop over set amount of time instead of over n_triggers
	tstart=datetime.datetime.now()
	dt = 0
	dt_temp = tstart
	while dt < int(args.dtime):

		if args.prim == args.serial1:
			daq1.trgseq.start.issue()
		else:
			daq2.trgseq.start.issue()
		
		ev1=daq1.event_read()
		ev2=daq2.event_read()

		if ev1 and ev2:
			datafile1.write(ev1)
			datafile2.write(ev2)

		tcurr = datetime.datetime.now()
		dt = (tcurr-tstart).total_seconds()

		# print(tcurr - dt_temp)
		dt_temp = tcurr

	tend=datetime.datetime.now()

#dtreal=
print((tend-tstart).total_seconds())
#dtalive=
print(args.ntrg*args.strobelength/40e6)

for serial, daq in zip([args.serial1, args.serial2], daqs):
	daq.trgmon.lat.issue()

	print(f"Board: {serial}")
	print('TRGMON: Triggers sent: %d'    %daq.trgmon.ntrgacc.read())
	print('TRGMON: avg rdo time: %.1f us'%(daq.trgmon.tbsy_rdo.read()/daq.trgmon.ntrgacc.read()/80e6/1e-6))
	print('ALPIDE: Triggers: %d'         %daq.alpide_reg_read(0x0009,chipid=args.chipid))
	print('ALPIDE: Strobes: %d'          %daq.alpide_reg_read(0x000A,chipid=args.chipid))
	print('ALPIDE: Matrix readouts: %d'  %daq.alpide_reg_read(0x000B,chipid=args.chipid))
	print('ALPIDE: Frames: %d'           %daq.alpide_reg_read(0x000C,chipid=args.chipid))








