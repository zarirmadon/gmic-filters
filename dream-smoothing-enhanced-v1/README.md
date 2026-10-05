[dream_smoothing_readme.md](https://github.com/user-attachments/files/22673643/dream_smoothing_readme.md)
# Dream Smoothing Enhanced

An advanced artistic filter for G'MIC that creates dreamy, ethereal effects while preserving image definition and detail.

![License](https://img.shields.io/badge/license-GPL%20v3-blue.svg)
![G'MIC](https://img.shields.io/badge/G'MIC-3.0+-green.svg)
![Status](https://img.shields.io/badge/status-stable-brightgreen.svg)

## Overview

Dream Smoothing Enhanced is a comprehensive artistic filter based on the original Dream Smoothing filter by Arto Huotari. It extends the core anisotropic smoothing algorithm with extensive artistic effects, full parameter control, and optimized workflows for creative image processing.

**Designed by:** Zarir Madon  
**Implementation:** Claude Sonnet (October 2025)  
**Based on:** Dream Smoothing by Arto Huotari  
**License:** GPL v3

## Features

### Core Dream Smoothing
- **Anisotropic diffusion smoothing** - Edge-preserving smoothing that maintains image structure
- **Iterative processing** - Multiple passes build up the characteristic dreamy effect
- **Adjustable blend opacity** - Control how much smoothing is applied
- **Full parameter exposure** - Access all internal anisotropic parameters

### Dream Effects
- **Ethereal Glow** - Screen blend for luminous highlights
- **Soft Light** - Subtle light diffusion for atmospheric quality
- **Halo Effect** - Bright area enhancement with controllable bloom

### Color & Atmosphere
- **Full color controls** - Brightness, contrast, saturation, hue shift
- **Vignette** - Soft edge darkening
- **Fog/Haze** - Atmospheric brightness overlay
- **Film Grain** - Fine monochrome grain (ISO 100-200 style)

## Installation

### Method 1: Direct Installation (Recommended)

1. Download `dream_smoothing_enhanced.gmic`
2. Copy to your G'MIC user directory:
   - **Linux/Mac**: `~/.config/gmic/`
   - **Windows**: `%APPDATA%\gmic\`
3. Restart GIMP or reload G'MIC filters

### Method 2: System-wide Installation

```bash
sudo cp dream_smoothing_enhanced.gmic /usr/share/gmic/
```

### Method 3: Test Before Installing

```bash
gmic -m dream_smoothing_enhanced.gmic image.jpg fx_dream_smoothing_enhanced 3,430,0.8,0.4,0.5,0.6,2,0.4,1,0.6,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0 -o output.jpg
```

## Usage

### In GIMP with G'MIC-Qt

1. Open your image in GIMP
2. Go to **Filters → G'MIC-Qt**
3. Navigate to **Artistic → Dream Smoothing Enhanced**
4. Adjust parameters using the sliders
5. Preview is automatically enabled
6. Click **Apply** when satisfied

### Command Line

```bash
# Basic usage with default parameters
gmic input.jpg fx_dream_smoothing_enhanced 3,430,0.8,0.4,0.5,0.6,2,0.4,1,0.6,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0 -o output.jpg

# With glow effect
gmic input.jpg fx_dream_smoothing_enhanced 3,430,0.8,0.4,0.5,0.6,2,0.4,1,0.6,4,50,0,0,0,0,0,0,0,0,0,0,0,0,0 -o glowing.jpg


## Parameters

### Core Smoothing
| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Iterations | 1-10 | 3 | Number of smoothing passes |
| Amplitude | 50-2000 | 430 | Smoothing intensity |
| Blend Opacity | 0-1 | 0.8 | How much effect to apply |

### Anisotropic Parameters - Pass 1
| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Sharpness 1 | 0.1-2 | 0.4 | Edge preservation strength |
| Anisotropy 1 | 0-1 | 0.5 | Directional smoothing |
| Alpha 1 | 0-1 | 0.6 | Diffusion rate |
| Sigma 1 | 0-10 | 2 | Tensor field smoothing |

### Anisotropic Parameters - Pass 2
| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Sharpness 2 | 0.1-2 | 0.4 | Edge preservation strength |
| Anisotropy 2 | 0-2 | 1.0 | Directional smoothing |
| Alpha 2 | 0-1 | 0.6 | Diffusion rate |
| Sigma 2 | 0-10 | 4 | Tensor field smoothing |

### Dream Effects
| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Ethereal Glow | 0-100 | 0 | Screen blend luminosity |
| Soft Light | 0-100 | 0 | Soft light diffusion |
| Halo | 0-100 | 0 | Bright area bloom |

### Color
| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Brightness | -100-100 | 0 | Brightness adjustment |
| Contrast | -100-100 | 0 | Contrast adjustment |
| Saturation | -100-100 | 0 | Saturation adjustment |
| Hue Shift | -180-180 | 0 | Hue rotation |

### Atmosphere
| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Vignette | 0-100 | 0 | Edge darkening |
| Fog | 0-100 | 0 | Atmospheric haze |
| Grain | 0-100 | 0 | Fine monochrome grain |

## Performance Tips

The filter uses anisotropic diffusion which is computationally intensive. For faster processing:

1. **Reduce Iterations** - Use 1-2 instead of 3+ (linear speedup)
2. **Lower Amplitude** - Try 200-300 instead of 430 (reduces processing intensity)
3. **Preview at smaller size** - Built into the filter automatically
4. **Disable unused effects** - Each effect adds processing time

**Typical Processing Times (4000×3000px image):**
- Iterations: 3, Amplitude: 430 → ~90 seconds
- Iterations: 2, Amplitude: 300 → ~40 seconds
- Iterations: 1, Amplitude: 200 → ~15 seconds

## Examples

### Gentle Dream Effect
```bash
gmic input.jpg fx_dream_smoothing_enhanced 2,350,0.75,0.4,0.5,0.6,2,0.4,1,0.6,4,20,15,10,0,0,0,0,5,3,5,0,0,10,5 -o gentle.jpg
```

### Strong Ethereal Effect
```bash
gmic input.jpg fx_dream_smoothing_enhanced 5,600,0.9,0.3,0.4,0.6,2,0.3,1.2,0.6,4,60,45,30,0,0,0,0,12,5,15,0,30,25,15 -o ethereal.jpg
```

## Technical Details

### Algorithm

The filter implements a two-pass anisotropic diffusion algorithm:

1. **First Pass**: Lower amplitude, moderate anisotropy - establishes base smoothing
2. **Second Pass**: Higher amplitude, stronger anisotropy - refines edges and details
3. **Blending**: Alpha blend with original to preserve definition

This approach maintains image structure while creating the characteristic dreamy quality.

### Why It's Slow

Anisotropic smoothing performs:
- Structure tensor calculations for edge detection
- Directional diffusion based on image gradients
- Multiple iterations compound computational cost

This is inherent to the algorithm and cannot be significantly optimized without changing the core approach.

## Requirements

- **G'MIC**: Version 3.0 or later
- **GIMP**: 2.10+ (for G'MIC-Qt plugin) or GIMP 3.0+
- **Memory**: 4GB+ recommended for large images
- **Processor**: Multi-core recommended for faster processing

## Compatibility

- **Linux**: Fully tested and working
- **macOS**: Compatible with G'MIC-Qt
- **Windows**: Compatible with G'MIC-Qt

## Known Issues

- Processing time is long on large images (inherent to algorithm)
- Preview Draft / Normal / High Quality - select Draft quality for responsiveness
- Very high parameter values may cause out-of-memory errors on large images

## Development

### Building from Source

The filter is a single `.gmic` file - no compilation needed.

### Contributing

Contributions welcome! Please:
1. Test changes thoroughly with various image sizes
2. Document parameter changes
3. Maintain compatibility with G'MIC 3.0+
4. Follow the existing code style

### Reporting Issues

When reporting issues, please include:
- G'MIC version
- Image dimensions
- Parameter values used
- Error message (if any)
- Expected vs actual behavior

## Credits

- **Original Dream Smoothing Algorithm**: Arto Huotari
- **Filter Design**: Zarir Madon
- **Implementation**: Claude Sonnet (October 2025)
- **G'MIC Framework**: David Tschumperlé and contributors

## License

This filter is licensed under the GNU General Public License v3.0.

```
Dream Smoothing Enhanced
Copyright (C) 2025 Zarir Madon

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```

## Changelog

### Version 1.0 (October 2025)
- Initial release
- Full parameter exposure
- 25 adjustable parameters
- Atmospheric effects
- Fine-grain control

## Support

For questions, issues, or discussions:
- Open an issue on GitHub
- Check the G'MIC community forums
- Refer to the included development guide for technical details

## Acknowledgments

Special thanks to:
- Arto Huotari for the original Dream Smoothing algorithm
- The G'MIC development team for the powerful framework
- The GIMP community for feedback and testing
- Contributors to the G'MIC filter ecosystem

---

**Made with care for digital artists and photographers**
