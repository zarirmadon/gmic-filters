# ✨ Dream Smoothing Enhanced v2

<br>

> **A faster, resolution-aware evolution of Dream Smoothing Enhanced — designed to preserve its flowing painterly character on modern high-resolution images.**

<br>

**Dream Smoothing Enhanced v2** is the second generation of my Dream Smoothing Enhanced filter, based on **Arto Huotari's original Dream Smoothing algorithm**.

<br>

The original Enhanced filter produced the painterly, flowing Dream Smoothing look I wanted, but it exposed three major problems:

<br>

- 🐌 **Large images became extremely slow to process**
- 🔍 **The apparent scale and character changed as image resolution increased**
- 🌫️ **Sharp structures could produce unpleasant elongated wisps and trails**

<br>

Development of v2 therefore began with four clear goals:

<br>

- ⚡ **Gain a lot of speed**
- 🧵 **Use CPU parallel processing where it genuinely helps**
- 🖼️ **Keep the same useful Dream character at higher resolutions**
- 🌫️ **Investigate ways of controlling the nasty wisps without destroying the effect itself**

<br>

The intention was not to replace Dream Smoothing with a different smoothing algorithm. The challenge was to preserve what makes the original effect distinctive while making it practical for high-resolution artwork.

<br><br>

## ⚡ How the big speed gains were achieved

<br>

The major performance improvement comes from changing **where the expensive Dream processing happens**, while keeping the original image at full resolution.

<br>

- 🖼️ **Full-resolution source preserved** — the original source remains at its native dimensions throughout the process.
- ⚙️ **Dedicated Dream worker** — the expensive Dream operation runs on a separate, resolution-aware working image.
- 📐 **Reference-scale processing** — Dream Scale 50 targets roughly a **1024 px long-side** Dream worker.
- ↕️ **Dynamic working resolution** — Dream Scale changes the internal Dream-processing resolution instead of shrinking the entire processing pipeline.
- 🚧 **Bounded processing size** — the worker is constrained to a practical **512–2048 px** long-side range and never exceeds the source.
- 🔄 **Full-size reconstruction** — the processed Dream result is reconstructed directly to the original image dimensions before final output.
- 🧮 **Far fewer expensive pixels** — computationally heavy anisotropic processing can therefore operate on dramatically less image data.
- 🧵 **CPU parallel processing** — compatible G'MIC processing can be divided between multiple CPU threads.
- 🧩 **Spatial overlap** — neighbouring context is retained where parallel work is divided spatially.
- 🔬 **Source code tells the rest** — those interested in the exact implementation can follow the processing path in the code.

<br>

> **The practical result:** a very large reduction in processing time while retaining the characteristic Dream Smoothing appearance at high resolutions.

<br><br>

## 🎛️ Controls

<br>

**Passes (Iterations)** · *Range: 1–10 · Default: 3*

<br>

Controls the number of iterative Dream Smoothing passes. Each additional pass develops the anisotropic smoothing further, creating stronger and more elaborate painterly forms, while fewer passes remain closer to the source and process more quickly.

<br><br>

**Merging Option** · *Default: Alpha*

<br>

Controls how successive Dream-processing stages are combined. A wide selection of G'MIC blending modes is available, including **Alpha, Average, Multiply, Overlay, Screen, Softlight, Difference, Edges** and many others.

<br>

Changing the merge mode can substantially alter the visual character without changing the underlying Dream algorithm.

<br>

> 💡 **Tip:** Try **Shapeaverage** when you want to push Dream Smoothing toward an extreme effect. Also experiment with the other merging modes — several can produce quite distinct looks.

<br><br>

**Opacity** · *Range: 0–1 · Default: 0.8*

<br>

Controls the strength of the selected merging operation. Lower values reduce the influence of the incoming processed stage; higher values give it progressively greater influence.

<br><br>

**Reverse Order** · *Default: Off*

<br>

Reverses the order of the images used by the selected merging operation. This can produce quite different results with non-symmetrical blending modes and provides another way of shaping the Dream result without adding another processing stage.

<br><br>

**Smoothness** · *Range: 0–5 · Default: 0.8*

<br>

Controls smoothing used by the special **Edges** merge mode. It determines how smoothly the edge-based merge is formed. It does **not** simply act as a global blur or general Dream-strength control.

<br><br>

**Equalize** · *Default: Off*

<br>

Equalizes the tonal range after each iterative Dream-processing stage. It is disabled by default to preserve the normal Dream Smoothing tonal behaviour, but can be enabled for a more strongly redistributed tonal result.

<br><br>

**Dream Scale** · *Range: 0–100 · Default: 50*

<br>

Controls the physical scale at which Dream Smoothing operates.

<br>

This is one of the major changes in v2. Instead of allowing image resolution to dictate the apparent size of the Dream effect, Dream Scale adjusts the internal working resolution around a reference scale.

<br>

At **50**, the Dream worker targets approximately **1024 pixels on the image's longest side**. Lower values move toward broader, larger-scale Dream forms; higher values provide progressively finer Dream structure.

<br>

| Dream Scale | Target long side |
|:---:|---:|
| **0** | **512 px** |
| **25** | **~724 px** |
| **50** | **1024 px** |
| **75** | **~1448 px** |
| **100** | **2048 px** |

<br>

The scale is deliberately **exponential rather than linear**: every increase of 50 doubles the target Dream working resolution. The target is bounded to **512–2048 px** and will never exceed the source image's longest side.

<br>

> 🎨 **In simple terms: scale the brush, not the canvas.**

<br><br>

## 🚀 Performance

<br>

**Parallel Processing** · *Default: Auto*

<br>

Controls the CPU threading used by the anisotropic smoothing operation.

<br>

Available choices are **Auto, One Thread, Two Threads, Four Threads, Eight Threads and Sixteen Threads**.

<br>

> 💡 **Tip:** Auto is the convenient starting point, but the highest thread count is not necessarily the fastest on every CPU or image. Manual choices are provided because a particular thread count may perform better on some hardware.

<br><br>

**Spatial Overlap** · *Range: 0–256 · Default: 24*

<br>

Controls the amount of neighbouring image data available where parallel processing divides the image spatially.

<br>

The default overlap should normally be left alone. If visible band or region boundaries appear during parallel processing, increasing the value gives each processing region more surrounding context, at the cost of some additional computation.

<br><br>

## 🖼️ Output

<br>

> **Dream Smoothing Enhanced v2 always creates its result as a new layer. The source layer is preserved.**

<br><br>

## 👤 Credits & Attribution

**Dream Smoothing Enhanced v2**\
Filter design, development and testing: **Zarir Madon**

Implementation and coding assistance: **OpenAI GPT-5.6 Sol**.

Based on **Dream Smoothing by Arto Huotari**, with the Arto-derived portions retaining their original **CeCILL provenance**.

DSE v2 additions are released under **GPL-3.0 where compatible**.

**Zarir Madon**\
🌐 Portfolio: [www.zarirmadon.com](https://www.zarirmadon.com/)\
🎨 ZM Creative: [www.zmcreative.art](https://www.zmcreative.art/)
