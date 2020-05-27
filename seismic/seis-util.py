def slicing(cube, type, loc, a_line):

  """
  Slicing a seismic cube to inline section, crossline section, or timeslice section

  Input:

  cube: 3d numpy array, data (output of segyio read)
  type: 'il' for inline slicing, 'xl' for xline slicing, 'ts' for time slicing
  loc: the location of inline, crossline, or timeslice depends on the type
       you're choosing (integer/float)
  a_line: array of inline, crossline, and timeslice locations, depends on the 
          type you're choosing (1D numpy array)
  """

  import numpy as np

  if type == 'il':
    id = np.where(a_line == loc)[0][0]
    slices = data[id,:,:]
  
  if type == 'xl':
    id = np.where(a_line == loc)[0][0]
    slices = data[:,id,:]
  
  if type == 'ts':
    id = np.where(a_line == loc)[0][0]
    slices = data[:,:,id]
  
  return(slices)

def display_slice(slices, type, b_line, c_line, cmap, vmin, vmax):

  """
  Display the slice

  Input:

  slices: the slice data, 2D numpy array
  type: 'il' for inline slicing, 'xl' for xline slicing, 'ts' for time slicing
  b_line, c_line: array of inline, crossline, and timeslice, depends on the 
                  type you're choosing (1D numpy array)
  * for 'il': b_line = crossline array, c_line = twt array
  * for 'xl': b_line = inline array, c_line = twt array
  * for 'ts': b_line = inline array, c_line = crossline array

  cmap: matplotlib pyplot colormaps ('gray', 'RdBu', 'seismic', 
        jet, Accent, ...)
  vmin, vmax: the minimum and maximum range for colormap. Many options:
  * None, None: normal and default plotting
  * specified vmin, vmax (e.g. vmin = 0, vmax = 1000)
  * vmin = -percentile99, vmax = +percentile99, percentiles of the cube

  """

  import numpy as np
  import matplotlib.pyplot as plt

  if type == 'il' or type == 'xl':
    extent = [b_line[0], b_line[-1], c_line[-1], c_line[0]]
    p1 = plt.imshow(slices.T, vmin=vmin, vmax=vmax, aspect='auto', extent=extent, cmap=cmap)
    plt.colorbar(p1)
   
  if type == 'ts':
    extent = [b_line[0], b_line[-1], c_line[0], c_line[-1]]
    p1 = plt.imshow(slices.T, vmin=vmin, vmax=vmax, aspect='auto', extent=extent, cmap=cmap)
    plt.colorbar(p1)
