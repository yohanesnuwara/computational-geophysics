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

def sliceCube(cube, type='il', 
              inline_loc=400, 
              xline_loc=None, 
              timeslice_loc=None, 
              display=False, 
              cmap='gray', figsize=None, vmin=None, vmax=None):
  
  """
  Slicing 3D seismic cube into 2D slice, and display it (optional)
  
  NOTE: Static display. If you want interactive display, use: sliceViewer

  INPUT:

  cube: 3D seismic output of openSegy3D

  type: specify the type of slice
    * 'il' for inline
    * 'xl' for crossline
    * 'ts' for timeslice)

  inline_loc: preferred location of inline, if you specify type='il', 
              no need to input xline_loc, timeslice_loc

  xline_loc: preferred location of crossline, if you specify type='xl', 
             no need to input inline_loc, timeslice_loc

  timeslice_loc: preferred location of timeslice, if you specify type='ts', 
                 no need to input inline_loc, xline_loc

  display: Display option. Default is False
    * False : Your output is the slice (2D numpy array).
    * True  : Your output is plot of the slice.

  If your display=True, configure the display details:
    * cmap: Matplotlib colormaps. 
    * figsize: figure size (2-size tuple)
    * vmin: lowest limit for colormap 
    * vmax: upper limit for colormap 

  OUTPUT:

  slice : 2D numpy array,  if display=True is specified
  plot  : Seismic display, if display=False is specified
  """

  import numpy as np
  import matplotlib.pyplot as plt

  # Unwrap cube
  inline_array, xline_array, timeslice_array = cube.inlines, cube.crosslines, cube.twt
  cube = cube.data

  if type == 'il':
    id = np.where(inline_array == inline_loc)[0][0]
    inline_slice = cube[id,:,:]
    
    if display == False:
      return(inline_slice)
        
    if display == True:
      plt.figure(figsize=figsize)
      plt.title('Inline {}'.format(inline_loc), size=20, pad=20)
      extent = [xline_array[0], xline_array[-1], timeslice_array[-1], timeslice_array[0]]

      p1 = plt.imshow(inline_slice.T, cmap=cmap, aspect='auto', extent=extent,
                      vmin=vmin, vmax=vmax)

      plt.colorbar()
      plt.xlabel('Crossline', size=15); plt.ylabel('TWT', size=15)
      plt.show()

  if type == 'xl':

    id = np.where(xline_array == xline_loc)[0][0]
    xline_slice = cube[:,id,:]

    if display == False:
      return(xline_slice)
    
    if display == True:
      plt.figure(figsize=figsize)
      plt.title('Crossline {}'.format(xline_loc), size=20, pad=20)
      extent = [inline_array[0], inline_array[-1], timeslice_array[-1], timeslice_array[0]]

      p1 = plt.imshow(xline_slice.T, cmap=cmap, aspect='auto', extent=extent, 
                      vmin=vmin, vmax=vmax)

      plt.colorbar()
      plt.xlabel('Inline', size=15); plt.ylabel('TWT', size=15)
      plt.show()
  
  if type == 'ts':

    id = np.where(timeslice_array == timeslice_loc)[0][0]
    tslice = cube[:,:,id]

    if display == False:
      return(tslice)

    if display == True:

      plt.figure(figsize=figsize)
      plt.title('Timeslice {} ms'.format(timeslice_loc), size=20, pad=20)
      extent = [inline_array[0], inline_array[-1], xline_array[-1], xline_array[0]]

      p1 = plt.imshow(tslice.T, cmap=cmap, aspect='auto', extent=extent, 
                      vmin=vmin, vmax=vmax)

      plt.colorbar()
      plt.xlabel('Inline', size=15); plt.ylabel('Crossline', size=15)
      plt.xlim(min(inline_array), max(inline_array))
      plt.ylim(min(xline_array), max(xline_array))
      plt.axis('equal')
      plt.show()  

def sliceViewer(cube, cube_name=" "):
  """
  Interactive viewer of 2D slice from a 3D seismic volume data

  NOTE: Interactive display. If you want static display, use: sliceCube

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
                                      max=max(twt), step=sample_rate)
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
