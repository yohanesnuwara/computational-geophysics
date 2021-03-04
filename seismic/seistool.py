def openSegy3D(filename):
  """
  Open 3D seismic volume in SEGY or SGY format 
  """
  import segyio

  try:
    with segyio.open(filename) as f:

      data = segyio.tools.cube(f)

      inlines = f.ilines
      crosslines = f.xlines
      twt = f.samples
      sample_rate = segyio.tools.dt(f) / 1000

      print('Successfully read \n')
      print('Inline range from', inlines[0], 'to', inlines[-1])
      print('Crossline range from', crosslines[0], 'to', crosslines[-1])
      print('TWT from', twt[0], 'to', twt[-1])   
      print('Sample rate:', sample_rate, 'ms')  

      try:
        rot, cdpx, cdpy = segyio.tools.rotation(f, line="fast")
        print('Survey rotation: {:.2f} deg'.format(rot))      
      except:
        print("Survey rotation not recognized")  

      cube = dict({"data": data,
                   "inlines": inlines,
                   "crosslines": crosslines,
                   "twt": twt,
                   "sample_rate": sample_rate})
      
      # See Stackoverflow: https://stackoverflow.com/questions/4984647/accessing-dict-keys-like-an-attribute
      class AttrDict(dict):
          def __init__(self, *args, **kwargs):
              super(AttrDict, self).__init__(*args, **kwargs)
              self.__dict__ = self  

      cube = AttrDict(cube)

  except:
    print("openSegy cannot read your data")  

  return cube 

def sliceViewer(cube, cube_name=" "):
  """
  Interactive viewer of 2D slice from a 3D seismic volume data


  """
  from ipywidgets import interact, interactive, fixed, interact_manual, ToggleButtons
  import ipywidgets as widgets
  import numpy as np
  import matplotlib.pyplot as plt

  # Access data and properties of cube
  data, inlines, crosslines, twt, sample_rate = cube.data, cube.inlines,\
                                                cube.crosslines, cube.twt,\
                                                cube.sample_rate                                         

  # Interactive plotting
  type = ToggleButtons(description='Selection',
                       options=['Inline','Crossline','Timeslice'])
  cmap_button = ToggleButtons(description='Colormaps',
                              options=['gray','seismic','RdBu','PuOr','Accent'])
  
  inline_loc = widgets.IntSlider(value=min(inlines), min=min(inlines), 
                                 max=max(inlines))
  xline_loc = widgets.IntSlider(value=min(crosslines), min=min(crosslines), 
                                max=max(crosslines))
  timeslice_loc = widgets.FloatSlider(value=min(twt), min=min(twt), 
                                      max=max(inlines), step=sample_rate)
  vmin = widgets.FloatSlider(value=np.amin(data), min=np.amin(data), 
                             max=np.amax(data))
  vmax = widgets.FloatSlider(value=np.amax(data), min=np.amin(data), 
                             max=np.amax(data))

  @interact   
  def f(type=type, inline_loc=inline_loc, xline_loc=xline_loc,
        timeslice_loc=timeslice_loc, vmin=vmin, vmax=vmax, cmap=cmap_button):  
    
    if type == 'Inline':

      # with segyio.open(filename) as f: 
      inline_slice = data[inline_loc-inlines[0],:,:]  

      plt.figure(figsize=(20, 10))
      plt.title('{} Seismic at Inline {}'.format(cube_name, inline_loc))
      extent = [crosslines[0], crosslines[-1], twt[-1], twt[0]]

      p1 = plt.imshow(inline_slice.T, cmap=cmap, aspect='auto', extent=extent,
                      vmin=vmin, vmax=vmax, interpolation='bicubic')
      plt.colorbar()

      plt.xlabel('Crossline'); plt.ylabel('TWT')
      plt.show()

    if type == 'Crossline':

      # with segyio.open(filename) as f:
      xline_slice = data[:,xline_loc-crosslines[0],:]  

      plt.figure(figsize=(20, 10))
      plt.title('{} Seismic at Crossline {}'.format(cube_name, xline_loc))
      extent = [inlines[0], inlines[-1], twt[-1], twt[0]]

      p1 = plt.imshow(xline_slice.T, cmap=cmap, aspect='auto', extent=extent, 
                      vmin=vmin, vmax=vmax, interpolation='bicubic')
      plt.colorbar()

      plt.xlabel('Inline'); plt.ylabel('TWT')
      plt.show()
    
    if type == 'Timeslice':

      id = np.where(twt == timeslice_loc)[0][0]
      tslice = data[:,:,id]

      plt.figure(figsize=(8,10))
      plt.title('{} Seismic at Timeslice {} ms'.format(cube_name, timeslice_loc))
      extent = [inlines[0], inlines[-1], crosslines[-1], crosslines[0]]

      p1 = plt.imshow(tslice.T, cmap=cmap, aspect='auto', extent=extent, 
                      vmin=vmin, vmax=vmax, interpolation='bicubic')
      plt.colorbar()


      plt.xlabel('Inline'); plt.ylabel('Crossline')
      plt.gca().xaxis.set_ticks_position('top') # axis on top
      plt.gca().xaxis.set_label_position('top') # label on top
      plt.xlim(min(inlines), max(inlines))
      plt.ylim(min(crosslines), max(crosslines))
      plt.axis('equal')
      plt.show()   
