import metaclass as mtc
import numpy as np
from collections import OrderedDict

# From the cryo schematics: 
#   - in the 947 cells the helium flows in the B1 direction
#   - in the 947 cells we enter from th quad side

fname = 'twiss_lhcb1.tfs'
ob = mtc.twiss(fname)
names = ob.NAME
ob = None #other fields are not sorted, I get rid of the object

# Find IP1
i_IP1 = np.where(map(lambda s:s=='IP1',names))[0][0]
# resort
names = names[i_IP1:]+names[:i_IP1]

arc_cryocells = {}

list_sectors = 'S12 S23 S34 S45 S56 S67 S78 S81'.split()

for sector in list_sectors:

    rside = 'R'+sector[1]
    lside = 'L'+sector[2]


    first_cell = '11'+rside+'_CV943'
    last_cell = '11'+lside+'_CV947'
    first_element = 'MQ.11'+rside+'.B1'


    list_cryonames = []
    for cc in xrange(1, 34, 2):
        for vname in ['CV947', 'CV943']:
            cryoname = str(cc)+rside+'_'+vname
            list_cryonames.append(cryoname)

    for cc in xrange(33, 0, -2):
        for vname in ['CV947', 'CV943']:
            cryoname = str(cc)+lside+'_'+vname
            list_cryonames.append(cryoname)


    if first_cell not in list_cryonames:
        raise ValueError('What?!')

    if last_cell not in list_cryonames:
        raise ValueError('What?!')

    if first_element not in names:
        raise ValueError('What?!')

    while not(names[0]==first_element):
        names.pop(0)

    while not(list_cryonames[0]==first_cell):
        list_cryonames.pop(0)
    i_last = np.where(map(lambda s:s==last_cell,list_cryonames))[0][0]
    list_cryonames = list_cryonames[:i_last+1]


    cryocells = OrderedDict([(name, None) for name in list_cryonames])
    for cname in list_cryonames:
        this_list = []
        while len(this_list)<4:
            nn = names.pop(0)
            if nn.startswith('MQ.') or nn.startswith('MB.'):
                this_list.append(nn)
        cryocells[cname] = this_list

    with open(sector+'_cells.txt', 'w') as fid:
        for cc in cryocells:
            fid.write('%s: %s\n'%(cc, repr(cryocells[cc])))

    arc_cryocells[sector] = cryocells

import pickle
with open('arc_cryocells.pkl', 'wb') as fid:
    pickle.dump(arc_cryocells, fid)












