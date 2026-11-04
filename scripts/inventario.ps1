# inventario.ps1 — T0: inventario local de ferramentas/bibliotecas PDF (zero instalacao, zero rede)
# Grava TUDO em C:\Users\Luca\AppData\Local\Temp\opencode\enem_t0\inventario.txt + marca OK/AUSENTE no final.
$ErrorActionPreference = 'Continue'
$lines = New-Object 'System.Collections.Generic.List[string]'
$lines.Add('=== INVENTARIO T0 - ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ' ===')

$lines.Add('')
$lines.Add('--- python --version ---')
$v = (& python --version) 2>&1 | Out-String
$lines.Add($v.TrimEnd())

$lines.Add('')
$lines.Add('--- python -c "import pypdf, pdfminer" ---')
$i1 = (& python -c "import pypdf, pdfminer; print('IMPORT_OK pypdf+pdfminer')") 2>&1 | Out-String
$rc1 = $LASTEXITCODE
$lines.Add($i1.TrimEnd())
$lines.Add('(exit=' + $rc1 + ')')

$lines.Add('')
$lines.Add('--- python -c "import fitz" (PyMuPDF) ---')
$i2 = (& python -c "import fitz; print('IMPORT_OK fitz/PyMuPDF'); print(fitz.version)") 2>&1 | Out-String
$rc2 = $LASTEXITCODE
$lines.Add($i2.TrimEnd())
$lines.Add('(exit=' + $rc2 + ')')

$lines.Add('')
$lines.Add('--- python -m pip list (linhas com pyp|pdf|fitz) ---')
$pl = (& python -m pip list) 2>&1 | Out-String
$fl = @(($pl -split "`r?`n") | Where-Object { $_ -match 'pyp|pdf|fitz' })
if ($fl.Count -gt 0) { foreach ($l in $fl) { $lines.Add($l) } } else { $lines.Add('(nenhuma linha correspondente)') }

$targets = @('gs','gswin64c','mutool','qpdf','pdftk','soffice','magick','pdftotext')
$wres = @{}
foreach ($t in $targets) {
  $lines.Add('')
  $lines.Add('--- where.exe ' + $t + ' ---')
  $w = (& where.exe $t) 2>&1 | Out-String
  $rc = $LASTEXITCODE
  $lines.Add($w.TrimEnd())
  $wres[$t] = (($rc -eq 0) -and ($w -notmatch 'Could not find files'))
}

$lines.Add('')
$lines.Add('=== RESUMO OK/AUSENTE ===')
[string]$py = if ($v -match 'Python\s+\d') { 'OK' } else { 'AUSENTE' }
[string]$s1 = if ($rc1 -eq 0 -and $i1 -match '(?m)^IMPORT_OK') { 'OK' } else { 'AUSENTE (import falhou, traceback acima)' }
[string]$s2 = if ($rc2 -eq 0 -and $i2 -match '(?m)^IMPORT_OK') { 'OK' } else { 'AUSENTE (import falhou, traceback acima)' }
[string]$s3 = if ($fl.Count -gt 0) { 'OK (' + ($fl.Count) + ' linha(s))' } else { 'AUSENTE (nenhum pacote pyp|pdf|fitz listado)' }
$lines.Add('python: ' + $py)
$lines.Add('python import pypdf+pdfminer: ' + $s1)
$lines.Add('python import fitz (PyMuPDF): ' + $s2)
$lines.Add('pip list (pacotes pyp|pdf|fitz): ' + $s3)
foreach ($t2 in $targets) {
  [string]$sw = if ($wres[$t2]) { 'OK' } else { 'AUSENTE' }
  $lines.Add('where ' + $t2 + ': ' + $sw)
}

Set-Content -LiteralPath (Join-Path $PSScriptRoot 'inventario.txt') -Value $lines -Encoding UTF8
Write-Output 'INVENTARIO_GRAVADO'
Get-Content -LiteralPath (Join-Path $PSScriptRoot 'inventario.txt')
