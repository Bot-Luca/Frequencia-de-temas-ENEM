# render_pdf2.ps1 — T0: rendereizacao WinRT Windows.Data.Pdf CORRIGIDA (sem instalacao, sem rede).
# Bug corrigido do render_pdf.ps1: OpenAsync(ReadWrite) + GetOutputStreamAt(0).FlushAsync() produzia PNGs
# invalidos (0 linhas / vazios). Padrao confiavel adotado: OpenTransactedWriteAsync (StorageStreamTransaction)
# — o commit atomico acontece no Close/Dispose da transacao. Restricoes: PDF original SOMENTE leitura;
# PNGs gravados EXCLUSIVAMENTE em C:\Users\Luca\AppData\Local\Temp\opencode\enem_t0.
# Fallback (se OpenTransactedWriteAsync falhar): RenderToStreamAsync em memoria + DataWriter/DataReader para
# copiar o PNG inteiro para um caminho .NET comum (File.WriteAllBytes).
param(
  [int[]]$Pages = @(10,11,12),
  [int]$Width = 1500,
  [string]$Suffix = ''
)
$ErrorActionPreference = 'Stop'
$pdfPath = 'C:\Users\Luca\Documents\ENEM\2025\2025_Humanas_Prova.pdf'
$outDir  = 'C:\Users\Luca\AppData\Local\Temp\opencode\enem_t0'

Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Data.Pdf.PdfDocument,Windows.Data.Pdf,ContentType=WindowsRuntime]
$null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.StorageFolder,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.IRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.InMemoryRandomAccessStream,Windows.Storage.Streams,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.DataReader,Windows.Storage.Streams,ContentType=WindowsRuntime]
$null = [Windows.Storage.Streams.DataWriter,Windows.Storage.Streams,ContentType=WindowsRuntime]

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

Write-Output ('PARAM Pages=' + ($Pages -join ',') + ' Width=' + $Width + ' Suffix=[' + $Suffix + ']')

$pdfFile = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($pdfPath)) ([Windows.Storage.StorageFile])
$pdf     = Await ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($pdfFile)) ([Windows.Data.Pdf.PdfDocument])
Write-Output ('PageCount=' + $pdf.PageCount)
Write-Output ('IsPasswordProtected=' + $pdf.IsPasswordProtected)

$outFolder = Await ([Windows.Storage.StorageFolder]::GetFolderFromPathAsync($outDir)) ([Windows.Storage.StorageFolder])

foreach ($n in $Pages) {
  if ($n -gt $pdf.PageCount) { Write-Output ('skip page ' + $n + ' (out of range)'); continue }
  $page = $pdf.GetPage($n - 1)
  try {
    $name     = 'pg' + $n + $Suffix + '.png'
    $outFile  = Await ($outFolder.CreateFileAsync($name, [Windows.Storage.CreationCollisionOption]::ReplaceExisting)) ([Windows.Storage.StorageFile])
    $destPath = [System.IO.Path]::Combine($outDir, $name)
    $opts = New-Object Windows.Data.Pdf.PdfPageRenderOptions
    $opts.DestinationWidth = $Width
    $mode = ''
    try {
      # --- ROTA CORRIGIDA: gravacao transacionada (commit no Dispose/Close) ---
      $txnType = [Windows.Storage.StorageStreamTransaction,Windows.Storage,ContentType=WindowsRuntime]
      $txn = Await ($outFile.OpenTransactedWriteAsync()) $txnType
      try {
        AwaitAction ($page.RenderToPageSizeAsync($txn.Stream, $page.Size, $opts))
        $txn.Dispose()   # commit
        $mode = 'OpenTransactedWriteAsync+RenderToPageSizeAsync (commit ok)'
      } catch {
        try { $txn.Dispose() } catch {}
        throw
      }
    } catch {
      # --- FALLBACK: render em memoria + copia dos bytes via DataWriter/DataReader ---
      Write-Output ('transacted falhou em pg' + $n + ' -> fallback memoria (' + $_.Exception.Message + ')')
      $mem = New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
      try {
        AwaitAction ($page.RenderToStreamAsync($mem, $opts))
        $total = [int]$mem.Size
        if ($total -le 0) { throw ('render em memoria produziu 0 bytes') }
        $dw = New-Object Windows.Storage.Streams.DataWriter($mem.GetOutputStreamAt(0))
        try { $null = Await ($dw.StoreAsync()) ([uint32]); $null = Await ($dw.FlushAsync()) ([bool]) } catch {}
        try { $dw.Dispose() } catch {}
        $dr = New-Object Windows.Storage.Streams.DataReader($mem.GetInputStreamAt(0))
        try {
          $null = Await ($dr.LoadAsync([uint32]$total)) ([uint32])
          $buf = New-Object 'System.Byte[]' $total
          $dr.ReadBytes($buf)
        } finally { try { $dr.Dispose() } catch {} }
        [System.IO.File]::WriteAllBytes($destPath, $buf)
        $mode = 'FALLBACK RenderToStreamAsync+DataWriter/DataReader->File.WriteAllBytes'
      } finally { try { $mem.Dispose() } catch {} }
    }
    $fi = New-Object System.IO.FileInfo($destPath)
    Write-Output ('rendered ' + $name + ' via ' + $mode + ' bytes=' + $fi.Length)
  } catch {
    Write-Output ('RENDER_ERROR pg' + $n + ': ' + $_.Exception.ToString().Split("`n")[0])
  } finally {
    try { $page.Dispose() } catch {}
  }
}
Get-ChildItem -LiteralPath $outDir -Filter 'pg*.png' | ForEach-Object { Write-Output ('FILE ' + $_.Name + ' ' + $_.Length) }
try { $pdf.Dispose() } catch {}
Write-Output 'DONE'
