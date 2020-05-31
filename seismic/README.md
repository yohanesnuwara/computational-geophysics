# Documentation for `seis_package`

`seis_util`<br>
|_____ `slice_cube`: Slicing a 3D seismic cube into inline, crossline, or timeslice 2D section. Then, display it.<br>
|_____ `frequency_spectrum`: Computing frequency spectrum of the whole 3D seismic cube, or 2D sections (inline or crossline)<br>

`seis_attribute`<br>
|_____ `attribute_2d`: Computing attribute of a 2D seismic data<br>
|_____ `attribute_3d`<br>
|_____ `display_attribute`: Display into a computed attribute section

# `segyio_read.py` program

```
Inline range from 100 to 750
Crossline range from 300 to 1250
TWT from 4.0 to 1848.0
Sample rate: 4.0 ms
'The 99th percentile is 6517; the max amplitude is 32767'
```

# `seis_util`

## `slice_cube`

### Structure of `slice_cube` function

```
def slice_cube(cube, type='il', inline_loc=400, inline_array=inlines, xline_loc=None, xline_array=None, timeslice_loc=None, timeslice_array=None, display='Yes', cmap='gray', figsize=None, vmin=None, vmax=None) 
```

### Input variables

|**Variable**|**Type**|**Description**|**Options**|
|:--:|:--:|:--:|:--:|
|`cube`|3D numpy array|3D seismic data output of `segyio.tools.cube`||
|`type`|string|specify the type of slice|`il` for inline<br>`xl` for crossline<br>`ts` for timeslice|
|`inline_loc`|integer|preferred location of inline, if `type='il'` is chosen||
|`xline_loc`|integer|preferred location of crossline, if `type='xl'` is chosen||
|`timeslice_loc`|integer|preferred location of timeslice, if `type='ts'` is chosen||
|`inline_array`|1D numpy array|array of inline locations<br> output of `segyio.read`||
|`xline_array`|1D numpy array|array of crossline locations<br> output of `segyio.read`||
|`timeslice_array`|1D numpy array|array of timeslice locations<br> output of `segyio.read`||
|`display`|string|display option|<ul> <li>`Yes`display slice</li> <li>`No`don't display slice<br>output only `slice`</li> </ul>|
|`cmap`|string|(Only for `Yes` display) colormap option, default is `gray`|`seismic`, `RdBu`, `PuOr`, `Accent`, etc.|
|`figsize`|2-size tuple|(Only for `Yes` display) figure size, default is `None`|example: `(20,10)`|
|`vmin`|float/int|(Only for `Yes` display) lowest limit for colormap, default is `None`|example: 99th percentile value, see `segyio_read.py`|
|`vmax`|float/int|(Only for `Yes` display) upper limit for colormap, default is `None`|example: 99th percentile value, see `segyio_read.py`|

### Use

**Slicing at inline 400 of a 3D seismic cube WITHOUT any display of it (`display='No'`)**

> No need to specify `crossline_array` and `timeslice_array` for this option.

```
slice_cube(cube=data, type='il', inline_loc=400, inline_array=inlines, display='No')
```

**Slicing at inline 400 of a 3D seismic cube WITH the display of it (`display='Yes'`)**

> Must specify all `inline_array`, `crossline_array` and `timeslice_array` for this option.

Display specification:
* Colormap `seismic`
* Size figure `(20,10)`
* Lower and upper limit are the 99th percentiles of the 3D cube data, `vm`, as output of `segyio.read` [(See section above)]()

```
slice_cube(cube=data, type='il', inline_loc=400, inline_array=inlines, crossline_array=crosslines, timeslice_array=twt, display='Yes', cmap='gray', figsize=(20,10), vmin=-vm, vmax=vm)
```

### Outputs

The outputs of two options are different. The use of variable option `display='Yes'` results BOTH `slice` and the display of seismic in `plt.show`, while the use of variable option `display='No'` results ONLY the `slice`. 

**Slicing at inline 400 of a 3D seismic cube WITHOUT any display of it (`display='No'`)**
```
array([[    0.,     0.,     0., ...,   408.,  1717.,   389.],
       [    0.,     0.,     0., ...,   221.,  1021.,  1023.],
       [    0.,     0.,     0., ..., -1242.,   714.,  1032.],
       ...,
       [    0.,   -78.,  -101., ..., -1076.,   -84.,  1029.],
       [    0.,   -17.,   -35., ...,  2061.,   722., -1503.],
       [    0.,  -500.,   417., ...,  1331.,  1570.,  1016.]],
      dtype=float32)
```

**Slicing at inline 400 of a 3D seismic cube WITH the display of it (`display='Yes'`)**

![image](https://user-images.githubusercontent.com/51282928/83354775-1108f900-a385-11ea-9ba9-9c8866a62cbd.png)

## `frequency_spectrum`

# `seis_attribute`

## `attribute_2d`

### Structure of `attribute_2d` function

```
attribute_2d(cube, output='2d', type='il', inline_loc=400, xline_loc=1000, timeslice_loc=1404, attribute_class='CompleTrace', attribute_type='cosphase', **spec=...)
```

### Input variables

|**Variable**|**Type**|**Description**|**Options**|
|:--:|:--:|:--:|:--:|
|`cube`|3D numpy array|3D seismic data output of `segyio.tools.cube`||
|`type`|string|specify the type of slice|`il` for inline<br>`xl` for crossline<br>`ts` for timeslice|
|`inline_loc`|integer|preferred location of inline, if `type='il'` is chosen||
|`xline_loc`|integer|preferred location of crossline, if `type='xl'` is chosen||
|`timeslice_loc`|integer|preferred location of timeslice, if `type='ts'` is chosen||
|`attribute_class`|string|class of attribute|See list below|
|`attribute_type`|string|type of attribute depends on its class|See list below|
|`**spec`|any|specified inputs depends on its attribute type|See list below|

### List of Attributes (sorted alphabetically) & its Details

|**Attribute Class**|**Attribute Type**|**Description**|**Input**|**Specified Input**|**Output**|
|:--:|:--:|:--:|:--:|:--:|:--:|
|`Amplitude`|`fder`|first derivative|`cube`|`axis=-1`|`slice` or `cube`|
|`Amplitude`|`gradmag`|gradient magnitude<br> using Gaussian operator|`cube`|`sigmas=(1,1,1)`|`slice` or `cube`|
|`Amplitude`|`reflin`|reflection intensity|`cube`|`kernel=(1,1,9)`|`slice` or `cube`|
|`Amplitude`|`rms`|root mean square|`cube`|`kernel=(1,1,9)`|`slice` or `cube`|
|`Amplitude`|`sder`|second derivative|`cube`|`axis=-1`|`slice` or `cube`|
|`CompleTrace`|`ampacc`|amplitude acceleration|`cube`||`slice` or `cube`|
|`CompleTrace`|`ampcontrast`|relative amplitude contrast|`cube`||`slice` or `cube`|
|`CompleTrace`|`apolar`|apparent polarity|`cube`||`slice` or `cube`|
|`CompleTrace`|`cosphase`|cosine of instantaneous<br> phase|`cube`||`slice` or `cube`|
|`CompleTrace`|`domfreq`|dominant frequency|`cube`|`sample_rate=4`|`slice` or `cube`|
|`CompleTrace`|`enve`|envelope|`cube`||`slice` or `cube`|
|`CompleTrace`|`freqcontrast`|frequency change|`cube`|`sample_rate=4`|`slice` or `cube`|
|`CompleTrace`|`inband`|instantaneous bandwidth|`cube`||`slice` or `cube`|
|`CompleTrace`|`infreq`|instantaneous frequency|`cube`|`sample_rate=4`|`slice` or `cube`|
|`CompleTrace`|`inphase`|instantaneous phase|`cube`||`slice` or `cube`|
|`CompleTrace`|`quality`|quality factor|`cube`|`sample_rate=4`|`slice` or `cube`|
|`CompleTrace`|`resamp`|response amplitude|`cube`||`slice` or `cube`|
|`CompleTrace`|`resfreq`|response frequency|`cube`|`sample_rate=4`|`slice` or `cube`|
|`CompleTrace`|`resphase`|response phase|`cube`||`slice` or `cube`|
|`CompleTrace`|`sweet`|sweetness|`cube`|`sample_rate=4`|`slice` or `cube`|
|`DipAzm`|`dipgrad`|gradient dips from<br> inline, crossline,<br> and z-gradients|`cube`|`dip_factor=10`,<br> `kernel=(3,3,3)`|`slice` or `cube` <ul> <li>`il_dip`inline dip</li> <li>`xl_dip`crossline dip</li> </ul>|
|`DipAzm`|`gst`|inner product of<br> gradient structure<br> tensors (GST)|`cube`|`kernel`|`slice` or `cube`<br>inner products of gradient<br>`gi2`, `gj2`, `gk2`,<br> `gigj`, `gigk`, `gjgk`|
|`DipAzm`|`gstdip2d`|2D gradient dips<br> from GST|`cube`|`dip_factor=10`,<br> `kernel=(3,3,3)`|`slice` or `cube` <ul> <li>`il_dip`inline dip</li> <li>`xl_dip`crossline dip</li> </ul>|
|`DipAzm`|`gstdip3d`|3D gradient dips<br> from GST|`cube`||`slice` or `cube`|
|`DipAzm`|`gstazm3d`|3D azimuth<br> from GST|`cube`|`dip_factor=10`,<br> `kernel=(3,3,3)`|`slice` or `cube`|
|`EdgeDetection`|`chaos`|multi-trace chaos|`cube`|`kernel=(3,3,9)`|`slice` or `cube`|
|`EdgeDetection`|`curv`|volume curvature<br> from 3D seismic dips|`cube`|`dip_factor=10`,<br> `kernel=(3,3,3)`|`slice` or `cube`<br>curvatures<br>`H`, `K`, `Kmax`,<br> `Kmin`, `KMPos`, `KMNeg`|
|`EdgeDetection`|`eigen`|eigen semblance|`cube`|`kernel=(3,3,9)`|`slice` or `cube`|
|`EdgeDetection`|`gstdisc`|discontinuity from<br> eigenvalues of GST|`cube`|`kernel=(3,3,9)`|`slice` or `cube`|
|`EdgeDetection`|`semblance`|semblance|`cube`|`kernel=(3,3,9)`|`slice` or `cube`|
