param(
    [string[]]$Arguments
)

$packageRoot = Split-Path -Parent $PSScriptRoot
$packageRoot = Join-Path $packageRoot 'Builds\PlayerV0.1\Windows'
$game = Join-Path $packageRoot 'ProyectoMemoria\Binaries\Win64\ProyectoMemoria.exe'

if (-not (Test-Path -LiteralPath $game)) {
    throw "No se encontró el ejecutable jugable: $game"
}

Start-Process -FilePath $game -WorkingDirectory (Split-Path -Parent $game) -ArgumentList $Arguments
