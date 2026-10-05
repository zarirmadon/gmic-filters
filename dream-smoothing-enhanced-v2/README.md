# Dream Smoothing Enhanced v2

**Dream Smoothing Enhanced v2** is the second generation of my Dream Smoothing Enhanced filter, based on **Arto Huotari's original Dream Smoothing algorithm**.

The original Enhanced filter produced the painterly, flowing Dream Smoothing look I wanted, but it had three major problems: it became extremely slow on large images, the apparent scale and character of the effect changed as image resolution increased, and Dream Smoothing could produce unpleasant elongated wisps around sharp structures.

Development of v2 therefore started with some very specific goals: **gain a lot of speed, exploit CPU parallel processing, preserve the same useful Dream character at higher resolutions, and investigate ways of controlling those nasty wisps without destroying the effect itself.**

<br>

## How the big speed gains were achieved

The full-resolution source is now preserved while the expensive Dream operation runs on a separate resolution-aware working image.  
A reference Dream Scale of 50 corresponds to roughly a 1024-pixel long-side working image.  
Dream Scale dynamically changes this working resolution rather than simply resizing the entire processing pipeline.  
The working resolution is bounded to prevent impractically small or large processing sizes.  
After Dream processing, the result is reconstructed directly to the original image dimensions.  
This means the computationally expensive anisotropic processing can operate on dramatically fewer pixels.  
CPU parallel processing is exposed so G'MIC can divide compatible work between multiple threads.  
Spatial overlap provides neighbouring image context when that work is divided into regions.  
The original full-resolution source itself is never replaced by the reduced working image.  
Those who want the engineering details can study the code.

<br>

## Controls

**Passes (Iterations)** · *Range: 1–10 · Default: 3*

Controls the number of iterative Dream Smoothing passes. Each additional pass develops the anisotropic smoothing further, creating stronger and more elaborate painterly forms, while fewer passes remain closer to the source and process more quickly.

<br><br>

**Merging Option** · *Default: Alpha*

Controls how successive Dream-processing stages are combined. A wide selection of G'MIC blending modes is available, including **Alpha, Average, Multiply, Overlay, Screen, Softlight, Difference, Edges** and many others.

Changing the merge mode can substantially alter the visual character without changing the underlying Dream algorithm.

<br><br>

**Opacity** · *Range: 0–1 · Default: 0.8*

Controls the strength of the selected merging operation. Lower values reduce the influence of the incoming processed stage; higher values give it progressively greater influence.

<br><br>

**Reverse Order** · *Default: Off*

Reverses the order of the images used by the selected merging operation. This can produce quite different results with non-symmetrical blending modes and provides another way of shaping the Dream result without adding another processing stage.

<br><br>

**Smoothness** · *Range: 0–5 · Default: 0.8*

Controls smoothing used by the special **Edges** merge mode. It determines how smoothly the edge-based merge is formed. It does **not** simply act as a global blur or general Dream-strength control.

<br><br>

**Dream Scale** · *Range: 0–100 · Default: 50*

Controls the physical scale at which Dream Smoothing operates.

This is one of the major changes in v2. Instead of allowing image resolution to dictate the apparent size of the Dream effect, Dream Scale adjusts the internal working resolution around a reference scale.

At **50**, the Dream worker targets approximately **1024 pixels on the image's longest side**. Lower values move toward broader, larger-scale Dream forms; higher values provide progressively finer Dream structure.

| Dream Scale | Target long side |
|---:|---:|
| **0** | **512 px** |
| **25** | **~724 px** |
| **50** | **1024 px** |
| **75** | **~1448 px** |
| **100** | **2048 px** |

The scale is deliberately **exponential rather than linear**: every increase of 50 doubles the target Dream working resolution. The target is bounded to **512–2048 px** and will never exceed the source image's longest side.

In simple terms: **scale the brush, not the canvas.**

<br>

## Performance

**Parallel Processing** · *Default: Auto*

Controls the CPU threading used by the anisotropic smoothing operation.

Available choices are **Auto, One Thread, Two Threads, Four Threads, Eight Threads and Sixteen Threads**.

Auto is the convenient starting point, but the highest thread count is not necessarily the fastest on every CPU or image. Manual choices are therefore provided for machines where a particular thread count performs better.

<br><br>

**Spatial Overlap** · *Range: 0–256 · Default: 24*

Controls the amount of neighbouring image data available where parallel processing divides the image spatially.

The default overlap should normally be left alone. If visible band or region boundaries appear during parallel processing, increasing the value gives each processing region more surrounding context, at the cost of some additional computation.

<br>

## Output

Dream Smoothing Enhanced v2 always creates its result as a **new layer**, preserving the source layer.

<br>

## Credits & Attribution

**Dream Smoothing Enhanced v2**  
Filter design, artistic direction, development and testing: **Zarir Madon**

Based on **Dream Smoothing by Arto Huotari**, with the Arto-derived portions retaining their original **CeCILL provenance**.

DSE v2 additions are released under **GPL-3.0 where compatible**.

Implementation and coding assistance: **OpenAI GPT-5.6 Sol**, developed interactively with Zarir Madon.

**Zarir Madon**  
Portfolio: [zarirmadon.com](https://zarirmadon.com/)  
ZM Creative: [zmcreative.art](https://zmcreative.art/)
