<div align="center">

# 🎨 G'MIC Filters & Plugins Gallery

[![G'MIC Version](https://img.shields.io/badge/G'MIC-v3.2%2B-7b2cbf?style=for-the-badge)](https://gmic.eu/)
[![Auto Updated](https://img.shields.io/badge/Workflow-Auto--Updated-00b4d8?style=for-the-badge&logo=githubactions)](https://github.com/zarirmadon/gmic-filters)
[![License](https://img.shields.io/badge/License-MIT-emerald?style=for-the-badge)](LICENSE)

<p><i>A curated, high-performance collection of custom filters, film simulations, and digital art scripts for G'MIC.</i></p>

---

</div>

## 📂 Plugin Directory

<!-- START_PLUGIN_SECTION -->
<table>
  <thead>
    <tr>
      <th align="center" width="22%">Preview</th>
      <th align="left" width="25%">Plugin / Folder</th>
      <th align="left" width="41%">Description</th>
      <th align="center" width="12%">Explore</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td align="center">
        <a href="./Film-Emulation">
          <img src="./Film-Emulation/preview.png" alt="Film Emulation Preview" width="140" style="border-radius: 6px;" min-height="70" />
        </a>
      </td>
      <td><b>🎞️ Film-Emulation</b></td>
      <td>Analog film stock simulation presets, color grading matrices, and realistic grain generators.</td>
      <td align="center"><a href="./Film-Emulation"><code>View ➔</code></a></td>
    </tr>
    <tr>
      <td align="center">
        <a href="./Glitch-FX">
          <img src="./Glitch-FX/preview.png" alt="Glitch FX Preview" width="140" style="border-radius: 6px;" min-height="70" />
        </a>
      </td>
      <td><b>👾 Glitch-FX</b></td>
      <td>Digital artifact simulation, RGB chromatic aberration, datamoshing, and CRT scanlines.</td>
      <td align="center"><a href="./Glitch-FX"><code>View ➔</code></a></td>
    </tr>
    <tr>
      <td align="center">
        <a href="./Painterly-Filters">
          <img src="./Painterly-Filters/preview.png" alt="Painterly Filters Preview" width="140" style="border-radius: 6px;" min-height="70" />
        </a>
      </td>
      <td><b>🖌️ Painterly-Filters</b></td>
      <td>Transforms photography into oil painting, watercolor stroke effects, and impasto textures.</td>
      <td align="center"><a href="./Painterly-Filters"><code>View ➔</code></a></td>
    </tr>
    <tr>
      <td align="center">
        <a href="./Vector-Tools">
          <img src="./Vector-Tools/preview.png" alt="Vector Tools Preview" width="140" style="border-radius: 6px;" min-height="70" />
        </a>
      </td>
      <td><b>📐 Vector-Tools</b></td>
      <td>Edge detection scripts, SVG contour tracing utilities, and high-contrast halftone stylizers.</td>
      <td align="center"><a href="./Vector-Tools"><code>View ➔</code></a></td>
    </tr>
  </tbody>
</table>
<!-- END_PLUGIN_SECTION -->

<br/>

## 🚀 Quick Installation

Add custom filters directly into your local G'MIC configuration:

```bash
# Linux / macOS
curl -sSL https://raw.githubusercontent.com/zarirmadon/gmic-filters/main/user.gmic >> ~/.config/gmic/user.gmic

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/zarirmadon/gmic-filters/main/user.gmic" -OutFile "$env:APPDATA/gmic/user.gmic"
```

---

<div align="center">
  <sub>Maintained by <a href="https://github.com/zarirmadon">@zarirmadon</a> • Powered by G'MIC</sub>
</div>