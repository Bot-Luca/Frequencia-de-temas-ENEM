# extract_text.ps1 — extrai TEXTO dos PDFs do ENEM via Word COM (sem instalacao de libs).
# Copia cada PDF para %TEMP%, desbloqueia (Mark-of-the-Web), abre read-only no Word,
# extrai o texto completo e grava como .txt UTF-8 em <Project>\dados\texto\.
param(
  [string]$Root = 'C:\Users\Luca\Documents\ENEM',
  [string]$Project = 'C:\Users\Luca\Documents\ENEM\O ENEM foi estudado pela NASA',
  [int[]]$Years = @(2020,2021,2022,2023,2024,2025)
)
$ErrorActionPreference = 'Continue'
$txtDir = Join-Path $Project 'dados\texto'
New-Item -ItemType Directory -Force -Path $txtDir | Out-Null

$word = $null
try {
  $word = New-Object -ComObject Word.Application
} catch {
  Write-Output ('WORD INDISPONIVEL: ' + $_.Exception.Message)
  exit 2
}
$word.Visible = $false
$word.DisplayAlerts = 0
try { $word.Options.ConfirmConversions = $false } catch {}
Write-Output 'WORD COM pronto'

foreach ($y in $Years) {
  foreach ($kind in @('Prova','Gabarito')) {
    $src = Join-Path $Root ("$y\${y}_Humanas_$kind.pdf")
    if (-not (Test-Path -LiteralPath $src)) { Write-Output ("SKIP (nao existe): " + $src); continue }
    $tmp = Join-Path $env:TEMP ("enem_{0}_{1}_{2}.pdf" -f $y, $kind, [guid]::NewGuid().ToString('N').Substring(0,8))
    $dst = Join-Path $txtDir ("{0}_Humanas_{1}.txt" -f $y, $kind)
    try {
      Copy-Item -LiteralPath $src -Destination $tmp -Force
      Unblock-File -LiteralPath $tmp -ErrorAction SilentlyContinue
      $doc = $word.Documents.Open($tmp, [ref]$false, [ref]$true, [ref]$false)
      $text = $doc.Content.Text
      Set-Content -LiteralPath $dst -Value $text -Encoding utf8
      $nQ = ([regex]::Matches($text, 'Quest[aã]o')).Count
      Write-Output ("TEXTO {0} {1} -> chars={2} ocorrencias_Questao={3} -> {4}" -f $y, $kind, $text.Length, $nQ, $dst)
      $doc.Close([ref]0)
    } catch {
      Write-Output ("TEXTO {0} {1} FALHOU: {2}" -f $y, $kind, $_.Exception.Message.Split("`n")[0])
    } finally {
      Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
    }
  }
}
try { $word.Quit() } catch {}
Write-Output 'EXTRACT DONE'
