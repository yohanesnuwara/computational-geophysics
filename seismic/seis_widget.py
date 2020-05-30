"""
Interactive seismic viewer (example: Dutch F3 Data)

Input:

data, inlines, crosslines, twt, sample_rate, vm: output from segyio.read
data: the whole cube (3D numpy array)
inlines: inline locations (1D numpy array)
crosslines: crossline locations (1D numpy array)
twt: two-way travel time (1D numpy array)
sample_rate: sampling rate (float)
vm: 99th percentile of data

"""

from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual, ToggleButtons
import ipywidgets as widgets

type = ToggleButtons(description='Selection',options=['Inline','Crossline',
                                                      'Timeslice'])
cmap_button = ToggleButtons(description='Colormaps',options=['gray','seismic',
                                                             'RdBu','PuOr'])

@interact

def seis_widget(type=type, inline_loc=(min(inlines), max(inlines)), 
                xline_loc=(min(crosslines), max(crosslines)),
                timeslice_loc=(min(twt), max(twt), sample_rate), 
                cmap=cmap_button):

  if type == 'Inline':

    with segyio.open(filename) as f: 
        inline_slice = f.iline[inline_loc]  

        plt.figure(figsize=(20, 10))
        plt.title('Dutch F3 Seismic at Inline {}'.format(inline_loc))
        extent = [crosslines[0], crosslines[-1], twt[-1], twt[0]]

        p1 = plt.imshow(inline_slice.T, cmap=cmap, aspect='auto', extent=extent,
                        vmin=-vm, vmax=vm)

        plt.xlabel('Crossline'); plt.ylabel('TWT')
        plt.show()

  if type == 'Crossline':

    with segyio.open(filename) as f:
        xline_slice = f.xline[xline_loc]  

        plt.figure(figsize=(20, 10))
        plt.title('Dutch F3 Seismic at Crossline {}'.format(xline_loc))
        extent = [inlines[0], inlines[-1], twt[-1], twt[0]]

        p1 = plt.imshow(xline_slice.T, cmap=cmap, aspect='auto', extent=extent, 
                        vmin=-vm, vmax=vm)

        plt.xlabel('Inline'); plt.ylabel('TWT')
        plt.show()
  
  if type == 'Timeslice':

    id = np.where(twt == timeslice_loc)[0][0]
    tslice = data[:,:,id]

    plt.figure(figsize=(7,10))
    plt.title('Dutch F3 Seismic at Timeslice {} ms'.format(timeslice_loc))
    extent = [inlines[0], inlines[-1], crosslines[-1], crosslines[0]]

    p1 = plt.imshow(tslice.T, cmap=cmap, aspect='auto', extent=extent, 
                    vmin=-vm, vmax=vm)


    plt.xlabel('Inline'); plt.ylabel('Crossline')
    plt.gca().xaxis.set_ticks_position('top') # axis on top
    plt.gca().xaxis.set_label_position('top') # label on top
    plt.xlim(min(inlines), max(inlines))
    plt.ylim(min(crosslines), max(crosslines))
    plt.axis('equal')
    plt.show()   
