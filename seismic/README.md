# Documentation for `seis_package`

`seis_util`<br>
|_____ `slicing`<br>
|_____ `display_slice`<br>
|_____ `frequency_spectrum`<br>

`seis_attribute`<br>
|_____ `attribute_2d`<br>
|_____ `display_attribute`

## Structure of `attribute_2d` function

```
attribute_2d(cube, type='il', inline_loc=400, xline_loc=1000, timeslice_loc=1404, attribute_class='CompleTrace', attribute_type='cosphase', **spec=...)`
```

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

## List of Attributes (sorted alphabetically) & its Details

|**Attribute Class**|**Attribute Type**|**Description**|**Input**|**Specified Input**|**Output**|
|:--:|:--:|:--:|:--:|:--:|:--:|
|`Amplitude`|`fder`|first derivative|`cube`|`axis=-1`||
|`Amplitude`|`gradmag`|gradient magnitude<br> using Gaussian operator|`cube`|`sigmas=(1,1,1)`||
|`Amplitude`|`reflin`|reflection intensity|`cube`|`kernel=(1,1,9)`||
|`Amplitude`|`rms`|root mean square|`cube`|`kernel=(1,1,9)`||
|`Amplitude`|`sder`|second derivative|`cube`|`axis=-1`||
|`CompleTrace`|`ampacc`|amplitude acceleration|`cube`|||
|`CompleTrace`|`ampcontrast`|relative amplitude contrast|`cube`|||
|`CompleTrace`|`apolar`|apparent polarity|`cube`|||
|`CompleTrace`|`cosphase`|cosine of instantaneous<br> phase|`cube`|||
|`CompleTrace`|`domfreq`|dominant frequency|`cube`|`sample_rate=4`||
|`CompleTrace`|`enve`|envelope|`cube`|||
|`CompleTrace`|`freqcontrast`|frequency change|`cube`|`sample_rate=4`||
|`CompleTrace`|`inband`|instantaneous bandwidth|`cube`|||
|`CompleTrace`|`infreq`|instantaneous frequency|`cube`|`sample_rate=4`||
|`CompleTrace`|`inphase`|instantaneous phase|`cube`|||
|`CompleTrace`|`quality`|quality factor|`cube`|`sample_rate=4`||
|`CompleTrace`|`resamp`|response amplitude|`cube`|||
|`CompleTrace`|`resfreq`|response frequency|`cube`|`sample_rate=4`||
|`CompleTrace`|`resphase`|response phase|`cube`|||
|`CompleTrace`|`sweet`|sweetness|`cube`|`sample_rate=4`||
|`DipAzm`|`dipgrad`|gradient dips from<br> inline, crossline,<br> and z-gradients|`cube`|`dip_factor=10`,<br> `kernel=(3,3,3)`||
|`DipAzm`|`gst`|inner product of<br> gradient structure<br> tensors (GST)|`cube`|`kernel`||
|`DipAzm`|`gstdip2d`|2D gradient dips<br> from GST|`cube`|`dip_factor=10`,<br> `kernel=(3,3,3)`||
|`DipAzm`|`gstdip3d`|3D gradient dips<br> from GST|`cube`|||
|`DipAzm`|`gstazm3d`|3D azimuth<br> from GST|`cube`|`dip_factor=10`,<br> `kernel=(3,3,3)`||
|`EdgeDetection`|`chaos`|multi-trace chaos|`cube`|`kernel=(3,3,9)`||
|`EdgeDetection`|`curv`|volume curvature<br> from 3D seismic dips|`cube`|`dip_factor=10`,<br> `kernel=(3,3,3)`||
|`EdgeDetection`|`eigen`|eigen semblance|`cube`|`kernel=(3,3,9)`||
|`EdgeDetection`|`gstdisc`|discontinuity from<br> eigenvalues of GST|`cube`|`kernel=(3,3,9)`||
|`EdgeDetection`|`semblance`|semblance|`cube`|`kernel=(3,3,9)`||
