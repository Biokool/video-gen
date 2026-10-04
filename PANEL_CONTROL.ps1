# PANEL_CONTROL.ps1 — usado por INICIAR.bat
# Si el panel (Streamlit, puerto 8501) ya esta corriendo, lo DETIENE y
# espera a que se libere el puerto; si no corria, no hace nada.
# Siempre sale con 0 para no cortar el .bat.
$ErrorActionPreference = 'SilentlyContinue'

function Get-PanelProcs {
    @(Get-CimInstance Win32_Process -Filter "Name='python.exe' or Name='pythonw.exe'" |
        Where-Object { $_.CommandLine -match 'streamlit' -and $_.CommandLine -match 'app\.py' })
}

function Test-PuertoLibre {
    -not (Get-NetTCPConnection -LocalPort 8501 -State Listen -ErrorAction SilentlyContinue)
}

$procs = Get-PanelProcs

if ($procs.Count -eq 0 -and (Test-PuertoLibre)) {
    Write-Host "      El panel no estaba corriendo: lo arranco."
    exit 0
}

$ids = @()
foreach ($p in $procs) { $ids += $p.ProcessId }
$sock = @(Get-NetTCPConnection -LocalPort 8501 -State Listen -ErrorAction SilentlyContinue)
foreach ($c in $sock) { if ($c.OwningProcess -and $ids -notcontains $c.OwningProcess) { $ids += $c.OwningProcess } }

foreach ($id in $ids) { Stop-Process -Id $id -Force -ErrorAction SilentlyContinue }
if ($ids.Count -gt 0) {
    Write-Host ("      Panel ya corria (PID " + ($ids -join ', ') + "): detenido, ahora lo reinicio.")
}

# Espera activa a que Windows suelte el puerto 8501 (hasta 15 s)
$ok = $false
for ($i = 0; $i -lt 15; $i++) {
    Start-Sleep -Seconds 1
    $left = @(Get-CimInstance Win32_Process -Filter "Name='python.exe' or Name='pythonw.exe'" |
        Where-Object { $_.CommandLine -match 'streamlit' -and $_.CommandLine -match 'app\.py' })
    foreach ($p in $left) { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue }
    if (Test-PuertoLibre) { $ok = $true; break }
}
if (-not $ok) {
    Write-Host "      AVISO: el puerto 8501 sigue ocupado; reintenta en unos segundos."
}
exit 0
