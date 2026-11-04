# word_extract_one.ps1 - extrai texto de UM PDF via Word COM, com log de passos.
# Uso: powershell -File word_extract_one.ps1 -PdfPath <pdf> -OutTxt <txt> [-StepLog <log>]
param(
  [Parameter(Mandatory=$true)][string]$PdfPath,
  [Parameter(Mandatory=$true)][string]$OutTxt,
  [string]$StepLog = ''
)
$ErrorActionPreference = 'Stop'
function Write-Step([string]$m) {
  $line = (Get-Date -Format 'HH:mm:ss') + ' ' + $m
  if ($StepLog) { Add-Content -LiteralPath $StepLog -Value $line -Encoding UTF8 -ErrorAction SilentlyContinue }
  Write-Output $line
}
$doc = $null
$word = $null
try {
  Write-Step ("START " + $PdfPath)
  $tmp = Join-Path $env:TEMP ("enem_word_{0}.pdf" -f [guid]::NewGuid().ToString('N').Substring(0,8))
  Copy-Item -LiteralPath $PdfPath -Destination $tmp -Force
  Unblock-File -LiteralPath $tmp -ErrorAction SilentlyContinue
  Write-Step 'COPIADO temp'
  $word = New-Object -ComObject Word.Application
  Write-Step 'WORD criado'
  $word.Visible = $false
  $word.DisplayAlerts = 0
  try { $word.Options.ConfirmConversions = $false } catch {}
  try { $word.AutomationSecurity = 3 } catch {}
  Write-Step 'WORD configurado'
  $doc = $word.Documents.Open($tmp, [ref]$false, [ref]$true, [ref]$false)
  Write-Step 'DOC aberto'
  $text = $doc.Content.Text
  Write-Step ("TEXTO chars=" + $text.Length)
  Set-Content -LiteralPath $OutTxt -Value $text -Encoding UTF8
  Write-Step 'SALVO'
  $doc.Close([ref]0)
  $doc = $null
  Write-Step 'DOC fechado'
  $word.Quit()
  $word = $null
  Write-Step 'WORD encerrado'
  Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
  Write-Step 'END ok'
  exit 0
} catch {
  Write-Step ("ERRO: " + $_.Exception.Message)
  if ($doc) { try { $doc.Close([ref]0) } catch {} }
  if ($word) { try { $word.Quit() } catch {} }
  exit 1
}
