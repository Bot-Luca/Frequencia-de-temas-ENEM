# crop_zoom.ps1 — recorta e amplia uma regiao de um PNG (System.Drawing, sem instalacao)
param(
  [Parameter(Mandatory=$true)][string]$In,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [int]$X = 0,
  [int]$Y = 0,
  [int]$W = 0,
  [int]$H = 0,
  [double]$Scale = 2.0,
  [string]$Name = 'crop'
)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
Add-Type -AssemblyName System.Drawing
$src = [System.Drawing.Image]::FromFile($In)
try {
  Write-Output ('DIM ' + $src.Width + 'x' + $src.Height)
  $w = if ($W -gt 0) { $W } else { $src.Width }
  $h = if ($H -gt 0) { $H } else { $src.Height }
  $rect = New-Object System.Drawing.Rectangle($X, $Y, $w, $h)
  $crop = New-Object System.Drawing.Bitmap($w, $h)
  $g = [System.Drawing.Graphics]::FromImage($crop)
  $g.DrawImage($src, (New-Object System.Drawing.Rectangle(0,0,$w,$h)), $rect, [System.Drawing.GraphicsUnit]::Pixel)
  $g.Dispose()
  $nw = [int]($w * $Scale); $nh = [int]($h * $Scale)
  $big = New-Object System.Drawing.Bitmap($nw, $nh)
  $g2 = [System.Drawing.Graphics]::FromImage($big)
  $g2.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
  $g2.DrawImage($crop, 0, 0, $nw, $nh)
  $g2.Dispose()
  $dest = Join-Path $OutDir ($Name + '.png')
  $big.Save($dest, [System.Drawing.Imaging.ImageFormat]::Png)
  Write-Output ('SAVED ' + $dest + ' ' + $nw + 'x' + $nh)
  $big.Dispose(); $crop.Dispose()
} finally { $src.Dispose() }
