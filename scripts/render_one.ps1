# render_one.ps1 — rasteriza um PDF especifico via WinRT Windows.Data.Pdf
# Uso: powershell -File render_one.ps1 -Pdf "<pdf>" -OutDir "<dir>" -Prefix "pp" -Width 1500 -Pages 1,2,3
# Se -Pages for omitido, rasteriza todas as paginas.
param(
  [Parameter(Mandatory=$true)][string]$PdfPath,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [string]$Prefix = 'pp',
  [int]$Width = 1500,
  [int[]]$Pages = @()
)
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

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

$pdfFile = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($PdfPath)) ([Windows.Storage.StorageFile])
$pdf     = Await ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($pdfFile)) ([Windows.Data.Pdf.PdfDocument])
Write-Output ('PDF=' + $PdfPath + ' PageCount=' + $pdf.PageCount + ' IsPasswordProtected=' + $pdf.IsPasswordProtected)

$list = if ($Pages.Count -gt 0) { $Pages } else { 1..$pdf.PageCount }
$ok = 0; $fail = 0
foreach ($n in $list) {
  if ($n -lt 1 -or $n -gt $pdf.PageCount) { Write-Output ('skip ' + $n); continue }
  $page = $pdf.GetPage($n - 1)
  $name = $Prefix + $n.ToString('D2') + '.png'
  $dest = [System.IO.Path]::Combine($OutDir, $name)
  try {
    $opts = New-Object Windows.Data.Pdf.PdfPageRenderOptions
    $opts.DestinationWidth = $Width
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
      if ($fi.Length -gt 20000) { $ok++ } else { $fail++; Write-Output ('PEQUENO ' + $name + ' ' + $fi.Length) }
    } finally { try { $mem.Dispose() } catch {} }
  } catch {
    $fail++
    Write-Output ('ERRO pg' + $n + ': ' + $_.Exception.ToString().Split("`n")[0])
  } finally { try { $page.Dispose() } catch {} }
}
Write-Output ('OK=' + $ok + ' FAIL=' + $fail)
try { $pdf.Dispose() } catch {}
Write-Output 'DONE'
