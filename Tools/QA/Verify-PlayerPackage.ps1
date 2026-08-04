param(
    [string]$PackageRoot = '',
    [switch]$Shipping,
    [switch]$LaunchSmoke,
    [int]$SmokeSeconds = 8
)

if ([string]::IsNullOrWhiteSpace($PackageRoot)) {
    $repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
    $relative = if ($Shipping) { 'Builds\PlayerV0.1\Shipping\Windows' } else { 'Builds\PlayerV0.1\Windows' }
    $PackageRoot = Join-Path $repo $relative
}

$PackageRoot = (Resolve-Path -LiteralPath $PackageRoot).Path
$binaryName = if ($Shipping) { 'ProyectoMemoria-Win64-Shipping.exe' } else { 'ProyectoMemoria.exe' }
$binary = Join-Path $PackageRoot "ProyectoMemoria\Binaries\Win64\$binaryName"
$pak = Join-Path $PackageRoot 'ProyectoMemoria\Content\Paks\ProyectoMemoria-Windows.pak'
$ucas = Join-Path $PackageRoot 'ProyectoMemoria\Content\Paks\ProyectoMemoria-Windows.ucas'
$required = @($binary, $pak, $ucas)

foreach ($path in $required) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Falta un archivo esencial del paquete: $path"
    }
}

Write-Output "Package: $PackageRoot"
Write-Output "Configuration: $(if ($Shipping) { 'Shipping' } else { 'Development' })"
foreach ($path in $required) {
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $path).Hash
    $item = Get-Item -LiteralPath $path
    Write-Output "$($item.Name) size=$($item.Length) sha256=$hash"
}

if ($LaunchSmoke) {
    $workingDirectory = Split-Path -Parent $binary
    $process = Start-Process -FilePath $binary -WorkingDirectory $workingDirectory -ArgumentList '-nullrhi', '-nosound' -PassThru
    Start-Sleep -Seconds $SmokeSeconds
    if ($process.HasExited) {
        throw "El proceso terminó antes del smoke test (exit=$($process.ExitCode))."
    }
    Stop-Process -Id $process.Id -Force
    Write-Output "Launch smoke: PASS ($SmokeSeconds s)"
}
