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
    slices = cube[id,:,:]
  
  if type == 'xl':
    id = np.where(a_line == loc)[0][0]
    slices = cube[:,id,:]
  
  if type == 'ts':
    id = np.where(a_line == loc)[0][0]
    slices = cube[:,:,id]
  
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
    extent = [b_line[0], b_line[-1], c_line[-1], c_line[0]]
    p1 = plt.imshow(slices.T, vmin=vmin, vmax=vmax, aspect='auto', extent=extent, cmap=cmap)
    plt.colorbar(p1)

def frequency_spectrum(data, type, il_array, xl_array, twt_array, sample_rate):

  """
  Compute the frequency spectrum of the whole cube, inline, or crossline
  cube

  Input:

  data: if you choose 'whole', data must be in 3D numpy array, if you choose
        either 'il' or 'xl', data must be in 2D numpy array (you should make
        the slice first using 'slicing' function)
  type: 'whole' for the whole cube, 'il' for inline section, 'xl' for
        crossline section 

  il_array (inline), xl_array (xline), twt_array (time) depend on the type
  you're choosing.

  * If type = 'il', then il_array = None, specify your xl_array and twt_array
  * If type = 'xl', then xl_array = None, specify your il_array and twt_array
  * If type = 'whole', then specify all your il_array, xl_array, and twt_array

  sample_rate: sampling rate of seismic data (in second) 

  Output:

  freq_seis: frequency
  spec_seis: seismic amplitude
  
  """

  import numpy as np
  import matplotlib.pyplot as plt

  if type == 'il':

    # transpose the slice 
    transp_slice = np.transpose(data)

    # take the average of each individual line traces

    # time
    min_time = 0
    max_time = len(twt)

    # crosslines
    xmin = 0
    xmax = len(xl_array)

    trace = np.mean(transp_slice[min_time:max_time, xmin:xmax], axis=1)

    Fs_seis = 1 / sample_rate  # Seconds.
    n_seis = len(trace)
    k_seis = np.arange(n_seis)
    T_seis = n_seis / Fs_seis
    freq_seis = k_seis / T_seis
    freq_seis = freq_seis[range(n_seis//2)]  # One side frequency range.

    spec_seis = np.fft.fft(trace) / n_seis  # FFT computing and normalization.
    spec_seis = spec_seis[range(n_seis//2)]

    # This is to smooth the spectrum over a window of 10.
    roll_win = np.ones(10) / 10
    spec_seis = np.convolve(spec_seis, roll_win, mode='same')

  if type == 'xl':

    # transpose the slice 
    transp_slice = np.transpose(data)

    # take the average of each individual line traces

    # time
    min_time = 0
    max_time = len(twt)

    # crosslines
    xmin = 0
    xmax = len(il_array)

    trace = np.mean(transp_slice[min_time:max_time, xmin:xmax], axis=1)

    Fs_seis = 1 / sample_rate  # Seconds.
    n_seis = len(trace)
    k_seis = np.arange(n_seis)
    T_seis = n_seis / Fs_seis
    freq_seis = k_seis / T_seis
    freq_seis = freq_seis[range(n_seis//2)]  # One side frequency range.

    spec_seis = np.fft.fft(trace) / n_seis  # FFT computing and normalization.
    spec_seis = spec_seis[range(n_seis//2)]

    # This is to smooth the spectrum over a window of 10.
    roll_win = np.ones(10) / 10
    spec_seis = np.convolve(spec_seis, roll_win, mode='same')
  
  if type == 'whole':

    # transpose the cube
    transp_cube = np.transpose(data)

    # time
    min_time = 0
    max_time = len(twt)

    # crosslines
    xmin = 0
    xmax = len(xl_array)

    # inlines
    ymin = 0
    ymax = len(il_array)

    mean_xl_traces = [] # mean of crossline traces of each inline section

    for i in range(ymax):
      mean_xl = np.mean(transp_cube[min_time:max_time, xmin:xmax, i], axis=1)
      mean_xl_traces.append(mean_xl)

    transp_xl = np.transpose(mean_xl_traces)

    # take average of each individual mean values of xl in the inline section

    trace = np.mean(transp_slice[min_time:max_time, ymin:ymax], axis=1)

    Fs_seis = 1 / sample_rate  # Seconds.
    n_seis = len(trace)
    k_seis = np.arange(n_seis)
    T_seis = n_seis / Fs_seis
    freq_seis = k_seis / T_seis
    freq_seis = freq_seis[range(n_seis//2)]  # One side frequency range.

    spec_seis = np.fft.fft(trace) / n_seis  # FFT computing and normalization.
    spec_seis = spec_seis[range(n_seis//2)]

    # This is to smooth the spectrum over a window of 10.
    roll_win = np.ones(10) / 10
    spec_seis = np.convolve(spec_seis, roll_win, mode='same')

  return(freq_seis, spec_seis)
