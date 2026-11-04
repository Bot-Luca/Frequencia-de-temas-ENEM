# render_pdf2_ano.ps1 — T6: generalizaçăo do render_pdf2.ps1 (rota WinRT validada no T0).
# Rota EFETIVA: RenderToStreamAsync (memória) + DataReader -> [System.IO.File]::WriteAllBytes.
# NÃO usa RenderToPageSizeAsync (não projeta neste PowerShell, conforme T0).
# Zero instalaçăo, zero rede. PDF original só leitura. PNGs gravados em OutDir (dados\raster\<ano>).
param(
  [string]$PdfPath,
  [string]$OutDir,
  [int]$Width = 1500,
  [string]$Suffix = ''
)
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Data.Pdf.PdfDocument,Windows.Data.Pdf,ContentType=WindowsRuntime]
$null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.StorageFolder,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.IRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.InMemoryRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.DataReader,Windows.Storage.Streams,ContentType=WindowsRuntime]

$asOpGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
$asAction    = ([System.windowsRuntimeSystemExtensions].GetMethods() | Where-Object { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncAction' })[0]
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

Write-Output ('PARAM PdfPath=' + $pdfPath + ' OutDir=' + $OutDir + ' Width=' + $Width + ' Suffix=[' + $Suffix + ']')

# garante pasta de saída
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir | Out-Null }

$pdfFile = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($pdfPath)) ([Windows.Storage.StorageFile])
$pdf     = Await ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($pdfFile)) ([Windows.Data.Pdf.PdfDocument])
Write-Output ('PageCount=' + $pdf.PageCount)
Write-Output ('IsPasswordProtected=' + $pdf.IsPasswordProtected)

$outFolder = Await ([Windows.Storage.StorageFolder]::GetFolderFromPathAsync($OutDir)) ([Windows.Storage.StorageFolder])

$opts = New-Object Windows.Data.Pdf.PdfPageRenderOptions
$opts.DestinationWidth = $Width

foreach ($n in 1..$pdf.PageCount) {
  $page = $pdf.GetPage($n - 1)
  try {
    $name     = 'pp' + $n + $Suffix + '.png'
    $outFile  = Await ($outFolder.CreateFileAsync($name, [Windows.Storage.CreationCollisionOption]::ReplaceExisting)) ([Windows.Storage.StorageFile])
    $destPath = [System.IO.Path]::Combine($OutDir, $name)
    $mem = New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
    try {
      # ROTA: RenderToStreamAsync em memoria + drenagem via DataReader + WriteAllBytes
      AwaitAction ($page.RenderToStreamAsync($mem, $opts))
      $total = [int]$mem.Size
      if ($total -le 0) { throw ('render em memoria produziu 0 bytes') }
      $dr = New-Object Windows.Storage.Streams.DataReader($mem.GetInputStreamAt(0))
      try {
        $null = Await ($dr.LoadAsync([uint32]$total)) ([uint32])
        $buf = New-Object 'System.Byte[]' $total
        $dr.ReadBytes($buf)
      } finally { try { $dr.Dispose() } catch {} }
      [System.IO.File]::WriteAllBytes($destPath, $buf)
      $mode = 'RenderToStreamAsync+DataReader->File.WriteAllBytes'
    } finally { try { $mem.Dispose() } catch {} }
    $fi = New-Object System.IO.FileInfo($destPath)
    Write-Output ('rendered ' + $name + ' via ' + $mode + ' bytes=' + $fi.Length)
  } catch {
    Write-Output ('RENDER_ERROR pg' + $n + ': ' + $_.Exception.ToString().Split("`n")[0])
  } finally {
    try { $page.Dispose() } catch {}
  }
}
Get-ChildItem -LiteralPath $OutDir -Filter 'pp*.png' | ForEach-Object { Write-Output ('FILE ' + $_.Name + ' ' + $_.Length) }
try { $pdf.Dispose() } catch {}
Write-Output 'DONE'
