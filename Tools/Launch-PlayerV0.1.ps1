param(
    [string[]]$Arguments,
    [switch]$Shipping
)

$packageRoot = Split-Path -Parent $PSScriptRoot
$packageRoot = Join-Path $packageRoot $(if ($Shipping) { 'Builds\PlayerV0.1\Shipping\Windows' } else { 'Builds\PlayerV0.1\Windows' })
$binary = if ($Shipping) { 'ProyectoMemoria-Win64-Shipping.exe' } else { 'ProyectoMemoria.exe' }
$game = Join-Path $packageRoot "ProyectoMemoria\Binaries\Win64\$binary"

if (-not (Test-Path -LiteralPath $game)) {
    throw "No se encontró el ejecutable jugable: $game"
}

Start-Process -FilePath $game -WorkingDirectory (Split-Path -Parent $game) -ArgumentList $Arguments
