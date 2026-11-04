# extract_all.ps1 - extrai texto dos PDFs de Humanas (provas + gabaritos) com watchdog por arquivo.
# Reexecutavel: pula arquivos ja extraidos. Log em dados\extract_log2.txt.
param(
  [string]$Root = 'C:\Users\Luca\Documents\ENEM',
  [string]$Project = 'C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA',
  [int[]]$Years = @(2020,2021,2022,2023,2024,2025),
  [int]$PerFileTimeoutSec = 240
)
$ErrorActionPreference = 'Continue'
$scriptOne = Join-Path $Project 'scripts\word_extract_one.ps1'
$txtDir = Join-Path $Project 'dados\texto'
New-Item -ItemType Directory -Force -Path $txtDir | Out-Null
$log = Join-Path $Project 'dados\extract_log2.txt'
function Write-Log([string]$m) {
  $line = (Get-Date -Format 'HH:mm:ss') + ' ' + $m
  Add-Content -LiteralPath $log -Value $line -Encoding UTF8
  Write-Output $line
}
Write-Log "EXTRACT ALL start"
foreach ($y in $Years) {
  foreach ($kind in @('Prova','Gabarito')) {
    $src = Join-Path $Root ("$y\${y}_Humanas_$kind.pdf")
    $dst = Join-Path $txtDir ("{0}_Humanas_{1}.txt" -f $y, $kind)
    if (-not (Test-Path -LiteralPath $src)) { Write-Log ("SKIP nao existe " + $src); continue }
    if ((Test-Path -LiteralPath $dst) -and ((Get-Item -LiteralPath $dst).Length -gt 100)) { Write-Log ("SKIP ja feito " + $dst); continue }
    $slog = Join-Path $Project ("dados\_step_{0}_{1}.log" -f $y, $kind)
    Remove-Item -LiteralPath $slog -Force -ErrorAction SilentlyContinue
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = 'powershell.exe'
    $psi.Arguments = '-NoProfile -NonInteractive -ExecutionPolicy Bypass -File "' + $scriptOne + '" -PdfPath "' + $src + '" -OutTxt "' + $dst + '" -StepLog "' + $slog + '"'
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true
    $pr = [System.Diagnostics.Process]::Start($psi)
    $ok = $pr.WaitForExit($PerFileTimeoutSec * 1000)
    if (-not $ok) {
      try { $pr.Kill() } catch {}
      Get-Process winword -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -eq 0 } | ForEach-Object { Stop-Process -Id $_.Id -Force -ErrorAction SilentlyContinue }
      if ((Test-Path -LiteralPath $dst) -and ((Get-Item -LiteralPath $dst).Length -gt 100)) { Write-Log ("TIMEOUT-mas-salvou $y $kind") } else { Write-Log ("TIMEOUT $y $kind") }
      continue
    }
    if ($pr.ExitCode -ne 0) { Write-Log ("FALHOU $y $kind exit=" + $pr.ExitCode); continue }
    if ((Test-Path -LiteralPath $dst) -and ((Get-Item -LiteralPath $dst).Length -gt 100)) {
      Write-Log ("OK {0} {1} bytes={2}" -f $y, $kind, (Get-Item -LiteralPath $dst).Length)
    } else { Write-Log ("SEM SAIDA $y $kind") }
  }
}
Write-Log "EXTRACT ALL DONE"
