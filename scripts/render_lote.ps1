# render_lote.ps1 — rasteriza lotes de PDFs do ENEM via WinRT Windows.Data.Pdf
# (zero instalacao, zero rede). PDFs originais SOMENTE leitura.
# Usa a rota validada no T0: RenderToStreamAsync em memoria + DataWriter/DataReader
# -> [System.IO.File]::WriteAllBytes (a rota transacional nao projeta neste ambiente).
param(
  [string]$Root = 'C:\Users\Luca\Documents\ENEM',
  [string]$Project = 'C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA',
  [int[]]$Years = @(2020,2021,2022,2023,2024),
  [int]$Width = 1500
)
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Data.Pdf.PdfDocument,Windows.Data.Pdf,ContentType=WindowsRuntime]
$null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.StorageFolder,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.IRandomAccessStream,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.InMemoryRandomAccessStream,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.DataReader,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.DataWriter,Windows.Storage,ContentType=WindowsRuntime]

$asOpGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
$asAction    = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncAction' })[0]
if (-not $asOpGeneric) { throw 'AsTask(IAsyncOperation`1) nao encontrado' }
if (-not $asAction)    { throw 'AsTask(IAsyncAction) nao encontrado' }

function Await($op, $type) {
  $t = $asOpGeneric.MakeGenericMethod($type).Invoke($null, @($op))
  $t.Wait(-1) | Out-Null
  $t.Result
}
function AwaitAction($action) {
  $t = $asAction.Invoke($null, @($action))
  $t.Wait(-1) | Out-Null
}

function Render-Pdf {
  param([string]$PdfPath, [string]$OutDir, [string]$Prefix, [int]$RenderWidth)
  if (-not (Test-Path -LiteralPath $PdfPath)) { Write-Output ('FALTA PDF: ' + $PdfPath); return }
  New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
  $pdfFile = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($PdfPath)) ([Windows.Storage.StorageFile])
  $pdf     = Await ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($pdfFile)) ([Windows.Data.Pdf.PdfDocument])
  $outFolder = Await ([Windows.Storage.StorageFolder]::GetFolderFromPathAsync($OutDir)) ([Windows.Storage.StorageFolder])
  $ok = 0; $fail = 0
  for ($n = 1; $n -le $pdf.PageCount; $n++) {
    $page = $pdf.GetPage($n - 1)
    $name = $Prefix + $n.ToString('D2') + '.png'
    $dest = [System.IO.Path]::Combine($OutDir, $name)
    try {
      $opts = New-Object Windows.Data.Pdf.PdfPageRenderOptions
      $opts.DestinationWidth = $RenderWidth
      $mem = New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
      try {
        AwaitAction ($page.RenderToStreamAsync($mem, $opts))
        $total = [int]$mem.Size
        if ($total -le 0) { throw 'render 0 bytes' }
        $dw = New-Object Windows.Storage.Streams.DataWriter($mem.GetOutputStreamAt(0))
        try { $null = Await ($dw.StoreAsync()) ([uint32]); $null = Await ($dw.FlushAsync()) ([bool]) } catch {}
        try { $dw.Dispose() } catch {}
        $dr = New-Object Windows.Storage.Streams.DataReader($mem.GetInputStreamAt(0))
        try {
          $null = Await ($dr.LoadAsync([uint32]$total)) ([uint32])
          $buf = New-Object 'System.Byte[]' $total
          $dr.ReadBytes($buf)
        } finally { try { $dr.Dispose() } catch {} }
        [System.IO.File]::WriteAllBytes($dest, $buf)
        $fi = New-Object System.IO.FileInfo($dest)
        if ($fi.Length -gt 20000) { $ok++ } else { $fail++; Write-Output ('  PEQUENO ' + $name + ' ' + $fi.Length) }
      } finally { try { $mem.Dispose() } catch {} }
    } catch {
      $fail++
      Write-Output ('  ERRO pg' + $n + ': ' + $_.Exception.ToString().Split("`n")[0])
    } finally { try { $page.Dispose() } catch {} }
  }
  Write-Output ('  ' + [System.IO.Path]::GetFileName($PdfPath) + ' -> ' + $Prefix + ' ok=' + $ok + ' fail=' + $fail + ' paginas=' + $pdf.PageCount)
  try { $pdf.Dispose() } catch {}
}

# ---------- 1) Raster de provas e gabaritos ----------
foreach ($y in $Years) {
  Write-Output ('=== ' + $y + ' ===')
  Render-Pdf -PdfPath (Join-Path $Root "$y\${y}_Humanas_Prova.pdf")    -OutDir (Join-Path $Project "dados\raster\$y")     -Prefix 'pp'       -RenderWidth $Width
  Render-Pdf -PdfPath (Join-Path $Root "$y\${y}_Humanas_Gabarito.pdf") -OutDir (Join-Path $Project "dados\raster\$y\gabarito") -Prefix 'gab'    -RenderWidth $Width
}

# ---------- 2) Extracao de texto via Word COM (se disponivel) ----------
$word = $null
try {
  $word = New-Object -ComObject Word.Application
  Write-Output 'WORD COM: disponivel'
} catch {
  Write-Output ('WORD COM: indisponivel (' + $_.Exception.Message.Split("`n")[0] + ')')
}
if ($word) {
  $word.Visible = $false
  $word.DisplayAlerts = 0
  $txtDir = Join-Path $Project 'dados\texto'
  New-Item -ItemType Directory -Force -Path $txtDir | Out-Null
  foreach ($y in $Years + @(2025)) {
    foreach ($kind in @('Prova','Gabarito')) {
      $src = Join-Path $Root "$y\${y}_Humanas_$kind.pdf"
      if (-not (Test-Path -LiteralPath $src)) { continue }
      $tmp = Join-Path $env:TEMP ("enem_{0}_{1}_{2}.pdf" -f $y, $kind, [guid]::NewGuid().ToString('N').Substring(0,8))
      $dst = Join-Path $txtDir ("{0}_Humanas_{1}.txt" -f $y, $kind)
      try {
        Copy-Item -LiteralPath $src -Destination $tmp -Force
        Unblock-File -LiteralPath $tmp -ErrorAction SilentlyContinue
        $doc = $word.Documents.Open($tmp, [ref]$false, [ref]$true, [ref]$false)
        $doc.SaveAs2([ref]$dst, [ref]2, [ref]$false, [ref]'', [ref]$false, [ref]'', [ref]$false, [ref]$false, [ref]$false, [ref]$false, [ref]$false, [ref]65001)
        $doc.Close([ref]0)
        $len = (Get-Item -LiteralPath $dst).Length
        Write-Output ("  TEXTO $y $kind -> $len bytes")
      } catch {
        Write-Output ("  TEXTO $y $kind FALHOU: " + $_.Exception.Message.Split("`n")[0])
      } finally {
        Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
      }
    }
  }
  try { $word.Quit() } catch {}
}
Write-Output 'LOTE DONE'
