# Documentation for `seis_package`

`seis_util`<br>
|_____ `slicing`<br>
|_____ `display_slice`<br>
|_____ `frequency_spectrum`<br>

`seis_attribute`<br>
|_____ `attribute_2d`<br>
|_____ `display_attribute`

## List of Attributes (sorted alphabetically) & its Details

|**Attribute Class**|**Attribute Type**|**Description**|**Input**|**Default Input**|**Output**|
|:--:|:--:|:--:|:--:|:--:|:--:|
|`Amplitude`|`fder`|first derivative||`axis=-1`||
|`Amplitude`|`gradmag`|gradient magnitude<br> using Gaussian operator||`sigmas=(1,1,1)`||
|`Amplitude`|`reflin`|reflection intensity||`kernel=(1,1,9)`||
|`Amplitude`|`rms`|root mean square||`kernel=(1,1,9)`||
|`Amplitude`|`sder`|second derivative||`axis=-1`||
|`CompleTrace`|`ampacc`|amplitude acceleration||||
|`CompleTrace`|`ampcontrast`|relative amplitude contrast||||
|`CompleTrace`|`apolar`|apparent polarity||||
|`CompleTrace`|`cosphase`|cosine of instantaneous<br> phase||||
|`CompleTrace`|`domfreq`|dominant frequency||`sample_rate=4`||
|`CompleTrace`|`enve`|envelope||||
|`CompleTrace`|`freqcontrast`|frequency change||`sample_rate=4`||
|`CompleTrace`|`inband`|instantaneous bandwidth||||
|`CompleTrace`|`infreq`|instantaneous frequency||`sample_rate=4`||
|`CompleTrace`|`inphase`|instantaneous phase||||
|`CompleTrace`|`quality`|quality factor||`sample_rate=4`||
|`CompleTrace`|`resamp`|response amplitude||||
|`CompleTrace`|`resfreq`|response frequency||`sample_rate=4`||
|`CompleTrace`|`resphase`|response phase||||
|`CompleTrace`|`sweet`|sweetness||`sample_rate=4`||
|`DipAzm`|`dipgrad`|gradient dips from<br> inline, crossline,<br> and z-gradients||`dip_factor=10`,<br> `kernel=(3,3,3)`||
|`DipAzm`|`gst`|inner product of<br> gradient structure<br> tensors (GST)||`kernel`||
|`DipAzm`|`gstdip2d`|2D gradient dips<br> from GST||`dip_factor=10`,<br> `kernel=(3,3,3)`||
|`DipAzm`|`gstdip3d`|3D gradient dips<br> from GST||||
|`DipAzm`|`gstazm3d`|3D azimuth<br> from GST||`dip_factor=10`,<br> `kernel=(3,3,3)`||
|`EdgeDetection`|`chaos`|multi-trace chaos||`kernel=(3,3,9)`||
|`EdgeDetection`|`curv`|volume curvature<br> from 3D seismic dips||`dip_factor=10`,<br> `kernel=(3,3,3)`||
|`EdgeDetection`|`eigen`|eigen semblance||`kernel=(3,3,9)`||
|`EdgeDetection`|`gstdisc`|discontinuity from<br> eigenvalues of GST||`kernel=(3,3,9)`||
|`EdgeDetection`|`semblance`|semblance||`kernel=(3,3,9)`||
