#!/usr/bin/env python3

from alpidedaqboard import alpidedaqboard
import argparse
import datetime
import os
import array
import json
from tqdm import tqdm
import os

now=datetime.datetime.now()

def suffixed_int(i):
    if i[-1]=='G': return int(i[:-1])*1000*1000*1000
    if i[-1]=='M': return int(i[:-1])*1000*1000
    if i[-1]=='k': return int(i[:-1])*1000
    return int(i)

parser=argparse.ArgumentParser(description='The mighty threshold scanner')
parser.add_argument('--serial' ,'-s',help='serial number of the DAQ board')
parser.add_argument('--chipid' ,'-c',type=int,help='Chip ID (default: 0x10)',default=0x10)
parser.add_argument('--vcasn'  ,'-v',type=int,help='ALPIDE VCASN DAC setting')
parser.add_argument('--vcasn2' ,'-w',type=int,help='ALPIDE VCASN2 DAC setting')
parser.add_argument('--vclip'  ,'-x',type=int,help='ALPIDE VCLIP DAC setting')
parser.add_argument('--ithr'   ,'-i',type=int,help='ALPIDE ITHR DAC setting')
parser.add_argument('--vresetd',     type=int,help='ALPIDE VRESETD DAC setting (default: 147)',default=147)
parser.add_argument('--dctrl'  ,     action='store_true',help='use readout via DCTRL')
parser.add_argument('--strobelength','-l',type=int,help='strobe length (@ALPIDE clks) (default=100)',default=3600)
#parser.add_argument('--spacing','-d',type=int,help='trigger sapcing (@80MHz) (default = 2 x strobelength+10')
parser.add_argument('--ntrg'   ,'-n',type=suffixed_int,help='number of triggers per setting (default=100k)',default='1')
parser.add_argument('--output' ,'-o',help='name of file to which events are written')
parser.add_argument('--params' ,'-p',help='name of file to which settings are written')
parser.add_argument('--path' ,help='Path to directory for data saving',default=".")
parser.add_argument('--dtime',help='Total time to measure in seconds',default="1")
parser.add_argument('--analyse', '-a', type=bool, help='automaticly analyse the data after the measurement has been completed', default=True)
args=parser.parse_args()

#if not args.spacing: args.spacing=args.strobelength*2+10

if args.serial:
    fname='fhrscan-%s-%s'%(args.serial,now.strftime('%Y%m%d_%H%M%S'))
else:
    fname='fhrscan-%s'%(now.strftime('%Y%m%d_%H%M%S'))
if not args.output: args.output=fname+'.raw'
if not args.params: args.params=fname+'.json'

if args.path != '.':  #creating new directory
    try:
        os.mkdir(args.path)
    except OSError:
        print ("Creation of the directory %s failed" %args.path)



with open('%s/%s'%(args.path,args.params),'w') as f:
    f.write(json.dumps(vars(args)))

try:
    daq=alpidedaqboard.ALPIDEDAQBoard(args.serial)
except ValueError as e:
    ntrg(e)
    raise SystemExit(-1)

# Well, power has a too bad connotation sometimes.
daq.power_on()
print(daq.power_status())

#just in case we got up on the wrong side of the fw...
daq.fw_reset()
daq.alpide_cmd_issue(0xD2) # GRST for ALPIDE
# now for monitoring, also start clean
daq.fw_clear_monitoring()


if args.vcasn : daq.alpide_reg_write(0x604,args.vcasn ,chipid=args.chipid)
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

daq.trg.ctrl.write(0b1110) # master mode,  mask ext trg, mask ext busy, do not force forced busy
daq.trgseq.dt_set.write(4000) # 50 us
daq.trg.opcode.write(0x55) # TRG OPCODE

daq.alpide_reg_write(0x602,args.vresetd,chipid=args.chipid)

daq.trgseq.ntrg_set.write(1) # for the time being: ping pong
with open('%s/%s'%(args.path,args.output),'wb') as datafile:
    
    # loop over set amount of time instead of over n_triggers
    tstart=datetime.datetime.now()
    dt = 0
    while dt < int(args.dtime):
        daq.trgseq.start.issue()
        ev=daq.event_read()
        datafile.write(ev)
        #print(f"{dt}: {ev}")
        #print(ev)

        tcurr = datetime.datetime.now()
        dt = (tcurr-tstart).total_seconds()
    
    #for itrg in tqdm(range(args.ntrg)):
        #daq.trgseq.start.issue()
        #ev=daq.event_read()
        #datafile.write(ev)
    tend=datetime.datetime.now()

dtreal=(tend-tstart).total_seconds()
dtalive=args.ntrg*args.strobelength/40e6

daq.trgmon.lat.issue()
print('TRGMON: Triggers sent: %d'    %daq.trgmon.ntrgacc.read())
print('TRGMON: avg rdo time: %.1f us'%(daq.trgmon.tbsy_rdo.read()/daq.trgmon.ntrgacc.read()/80e6/1e-6))
print('ALPIDE: Triggers: %d'         %daq.alpide_reg_read(0x0009,chipid=args.chipid))
print('ALPIDE: Strobes: %d'          %daq.alpide_reg_read(0x000A,chipid=args.chipid))
print('ALPIDE: Matrix readouts: %d'  %daq.alpide_reg_read(0x000B,chipid=args.chipid))
print('ALPIDE: Frames: %d'           %daq.alpide_reg_read(0x000C,chipid=args.chipid))

print('Life time: %6.2f %%'%(dtalive/dtreal*100))

filename= '%s/%s'%(args.path,args.output)

if args.analyse:
    os.system(f'/home/alpide/alpide-daq-software/analyses/hitmap.py {filename}')




