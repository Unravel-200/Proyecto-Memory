#Requires -Version 5.1

<#
.SYNOPSIS
Ejecuta comprobaciones de solo lectura antes o después del QA del Player v0.1.0.

.DESCRIPTION
Valida la rama, el commit mínimo, Git LFS, configuración de Unreal/Enhanced Input
y los archivos fuente requeridos. En modo Postflight también comprueba que los
assets esperados existan, que Git no muestre rutas fuera del alcance y, si se
proporciona, que el Output Log no contenga los diagnósticos propios conocidos.

El script no abre Unreal, no compila, no crea evidencias y no modifica Git.

.PARAMETER Phase
Preflight exige un worktree limpio antes de abrir Unreal. Postflight permite los
cambios esperados de la integración y comprueba su allowlist.

.PARAMETER ConfirmHardwareReady
Confirma que el operador comprobó temperatura, ventilación y consumo del equipo.
El script no puede medir de forma fiable esa condición por sí solo.

.PARAMETER AllowDirty
Convierte un worktree sucio en WARN durante Preflight. Solo sirve para desarrollar
y probar este script; no debe usarse para iniciar una sesión real de Editor.

.PARAMETER LogPath
Ruta al Output Log que se inspeccionará; es obligatoria durante Postflight.

.PARAMETER EngineRoot
Ruta opcional a la instalación de UE 5.8. Si se omite, se busca en el registro de
Epic y en la ruta predeterminada de Program Files.

.PARAMETER AsJson
Emite un único objeto JSON para archivarlo como evidencia mediante redirección.

.EXAMPLE
.\Tools\QA\Invoke-PlayerQACheck.ps1 -Phase Preflight -ConfirmHardwareReady

.EXAMPLE
.\Tools\QA\Invoke-PlayerQACheck.ps1 -Phase Postflight -LogPath .\UnrealProject\Saved\Logs\ProyectoMemoria.log

.EXAMPLE
.\Tools\QA\Invoke-PlayerQACheck.ps1 -Phase Preflight -ConfirmHardwareReady -AsJson
#>

[CmdletBinding()]
param(
    [ValidateSet("Preflight", "Postflight")]
    [string]$Phase = "Preflight",

    [switch]$ConfirmHardwareReady,

    [switch]$AllowDirty,

    [string]$LogPath,

    [string]$EngineRoot,

    [switch]$AsJson
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\.."))
$ExpectedBranch = "feature/v0.1-player-cameras"
$MinimumCommit = "5eccd8e"
$Checks = @()

$RequiredProjectPaths = @(
    "EDITOR_SETUP_V0.1.md",
    "HANDOFF_CODEX.md",
    "QA_PLAYER_V0.1.md",
    "UnrealProject/ProyectoMemoria.uproject",
    "UnrealProject/Config/DefaultInput.ini",
    "UnrealProject/Source/ProyectoMemoria/ProyectoMemoria.Build.cs",
    "UnrealProject/Source/ProyectoMemoria/Player/PMPlayerCharacter.h",
    "UnrealProject/Source/ProyectoMemoria/Player/PMPlayerCharacter.cpp",
    "UnrealProject/Source/ProyectoMemoria/Player/PMPlayerController.h",
    "UnrealProject/Source/ProyectoMemoria/Player/PMPlayerController.cpp",
    "UnrealProject/Source/ProyectoMemoria/Player/PMCameraModeComponent.h",
    "UnrealProject/Source/ProyectoMemoria/Player/PMCameraModeComponent.cpp"
)

$ExpectedAssetPaths = @(
    "UnrealProject/Content/Input/Actions/IA_Move.uasset",
    "UnrealProject/Content/Input/Actions/IA_Look.uasset",
    "UnrealProject/Content/Input/Actions/IA_Sprint.uasset",
    "UnrealProject/Content/Input/Actions/IA_Crouch.uasset",
    "UnrealProject/Content/Input/Actions/IA_ToggleCamera.uasset",
    "UnrealProject/Content/Input/Mappings/IMC_Player.uasset",
    "UnrealProject/Content/Blueprints/Player/BP_PlayerCharacter.uasset",
    "UnrealProject/Content/Blueprints/Player/BP_PlayerController.uasset",
    "UnrealProject/Content/Blueprints/Levels/BP_GameMode_DeveloperTesting.uasset",
    "UnrealProject/Content/Maps/L_Developer_Testing.umap"
)

$RequiredBaselineLfsPaths = @(
    "UnrealProject/Content/Blueprints/Test/BP_TestActor.uasset",
    "UnrealProject/Content/Maps/L_Developer_Testing.umap"
)

$AllowedPostflightPaths = @($ExpectedAssetPaths) + @("QA_PLAYER_V0.1.md")

$ForbiddenLogMessages = @(
    "has no IMC_Player assigned",
    "has one or more unassigned IA_* assets",
    "has an incomplete camera setup",
    "APMPlayerController requires EnhancedInputComponent"
)

$ExpectedQAIds = @(
    "PRE-01", "PRE-02", "PRE-03", "PRE-04", "PRE-05", "PRE-06",
    "PRE-07", "PRE-08", "PRE-09",
    "SET-01", "SET-02", "SET-03",
    "MAP-01", "MAP-02", "MAP-03", "MAP-04", "MAP-05", "MAP-06",
    "BP-01", "BP-02", "BP-03", "BP-04", "BP-05", "BP-06", "LVL-01",
    "GEO-01", "GEO-02", "GEO-03", "GEO-04", "GEO-05", "GEO-06", "GEO-07",
    "PLR-PIE-001",
    "PLR-MOV-001", "PLR-MOV-002", "PLR-MOV-003", "PLR-MOV-004",
    "PLR-MOV-005", "PLR-MOV-006",
    "PLR-CRO-001", "PLR-CRO-002", "PLR-CRO-003", "PLR-CRO-004",
    "PLR-CRO-005", "PLR-CRO-006", "PLR-CRO-007", "PLR-CRO-008",
    "PLR-CRO-AUT-001", "PLR-CRO-009",
    "PLR-CAM-001", "PLR-CAM-002", "PLR-CAM-003", "PLR-CAM-004",
    "PLR-CAM-005", "PLR-CAM-006", "PLR-VIS-001",
    "PLR-ENV-001", "PLR-ENV-002", "PLR-ENV-003", "PLR-ENV-004",
    "PLR-PAD-001", "PLR-PAD-002", "PLR-PERF-001",
    "PLR-REG-001", "PLR-REG-002", "PLR-REG-003", "PLR-REG-004",
    "PLR-REG-005",
    "EVC-01", "EVC-02", "EVC-03", "EVC-04", "EVC-05", "EVC-06",
    "EVC-07", "EVC-08", "EVC-09", "EVC-10", "EVC-11"
)

$ConditionalQAIds = @("PRE-09", "PLR-VIS-001")

function Add-QACheck {
    param(
        [Parameter(Mandatory = $true)]
        [ValidateSet("PASS", "WARN", "FAIL")]
        [string]$Status,

        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [string]$Detail
    )

    $script:Checks += [PSCustomObject]@{
        Status = $Status
        Name = $Name
        Detail = $Detail
    }
}

function Invoke-GitReadOnly {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    $Output = @()
    $ExitCode = -1
    $PreviousErrorActionPreference = $ErrorActionPreference
    try {
        # Windows PowerShell 5.1 convierte stderr nativo en ErrorRecord. Se usa
        # Continue localmente para poder capturarlo y devolver un check estructurado.
        $ErrorActionPreference = "Continue"
        $Output = @(
            & git --no-optional-locks -C $script:RepoRoot @Arguments 2>&1 |
                ForEach-Object { [string]$_ }
        )
        $ExitCode = $LASTEXITCODE
    }
    finally {
        $ErrorActionPreference = $PreviousErrorActionPreference
    }

    return [PSCustomObject]@{
        ExitCode = $ExitCode
        Output = ($Output -join [Environment]::NewLine).Trim()
    }
}

function Test-PathGroup {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [string[]]$RelativePaths
    )

    $Missing = @(
        $RelativePaths |
            Where-Object {
                -not (Test-Path -LiteralPath (Join-Path $script:RepoRoot $_) -PathType Leaf)
            }
    )

    if ($Missing.Count -eq 0) {
        Add-QACheck -Status "PASS" -Name $Name -Detail ("{0} rutas presentes." -f $RelativePaths.Count)
        return
    }

    Add-QACheck -Status "FAIL" -Name $Name -Detail ("Faltan: {0}" -f ($Missing -join ", "))
}

function Get-GitStatusEntries {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string]$NulDelimitedOutput
    )

    if ([string]::IsNullOrWhiteSpace($NulDelimitedOutput)) {
        return @()
    }

    $Records = @($NulDelimitedOutput -split ([char]0) | Where-Object {
        -not [string]::IsNullOrWhiteSpace($_)
    })
    $Entries = @()

    for ($Index = 0; $Index -lt $Records.Count; $Index++) {
        $Record = $Records[$Index]
        if ($Record.Length -lt 4) {
            $Entries += [PSCustomObject]@{
                Status = "!!"
                Path = $Record
                OriginalPath = $null
                Raw = $Record
            }
            continue
        }

        $StatusCode = $Record.Substring(0, 2)
        $Path = $Record.Substring(3).Replace("\", "/")
        $OriginalPath = $null

        if ($StatusCode -match "[RC]") {
            $Index++
            if ($Index -lt $Records.Count) {
                $OriginalPath = $Records[$Index].Replace("\", "/")
            }
        }

        $Entries += [PSCustomObject]@{
            Status = $StatusCode
            Path = $Path
            OriginalPath = $OriginalPath
            Raw = $Record
        }
    }

    return @($Entries)
}

function Get-QAResultAudit {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $ValidStates = @("NOT RUN", "PASS", "FAIL", "BLOCKED")
    $Rows = @()
    $Issues = @()

    foreach ($Line in (Get-Content -Encoding UTF8 -LiteralPath $Path)) {
        if (-not $Line.StartsWith("|")) {
            continue
        }

        $RawCells = $Line.Split("|")
        if ($RawCells.Count -lt 4) {
            continue
        }

        $Cells = @(
            $RawCells[1..($RawCells.Count - 2)] |
                ForEach-Object { $_.Trim() }
        )
        $Id = $Cells[0]
        if ($Id -notmatch "^(PRE|SET|MAP|BP|LVL|GEO|PLR|EVC)-[A-Z0-9-]+$") {
            continue
        }

        $StateIndexes = @()
        for ($CellIndex = 0; $CellIndex -lt $Cells.Count; $CellIndex++) {
            if ($ValidStates -contains $Cells[$CellIndex]) {
                $StateIndexes += $CellIndex
            }
        }

        if ($StateIndexes.Count -ne 1) {
            $Issues += "{0}: se esperó exactamente un estado y se encontraron {1}." -f $Id, $StateIndexes.Count
            continue
        }

        $StateIndex = $StateIndexes[0]
        $State = $Cells[$StateIndex]
        $Evidence = if ($StateIndex + 1 -lt $Cells.Count) {
            $Cells[$StateIndex + 1]
        }
        else {
            ""
        }

        if ($State -ne "NOT RUN" -and [string]::IsNullOrWhiteSpace($Evidence)) {
            $Issues += "{0}: el estado {1} requiere evidencia no vacía." -f $Id, $State
        }

        $Rows += [PSCustomObject]@{
            Id = $Id
            State = $State
            Evidence = $Evidence
        }
    }

    $DuplicateIds = @(
        $Rows | Group-Object Id | Where-Object { $_.Count -gt 1 } |
            ForEach-Object { $_.Name }
    )
    if ($DuplicateIds.Count -gt 0) {
        $Issues += "IDs duplicados: {0}." -f ($DuplicateIds -join ", ")
    }

    $ObservedIds = @($Rows | ForEach-Object { $_.Id } | Sort-Object -Unique)
    $MissingIds = @($script:ExpectedQAIds | Where-Object { $ObservedIds -notcontains $_ })
    if ($MissingIds.Count -gt 0) {
        $Issues += "IDs faltantes: {0}." -f ($MissingIds -join ", ")
    }

    $UnexpectedIds = @($ObservedIds | Where-Object { $script:ExpectedQAIds -notcontains $_ })
    if ($UnexpectedIds.Count -gt 0) {
        $Issues += "IDs no reconocidos: {0}." -f ($UnexpectedIds -join ", ")
    }

    return [PSCustomObject]@{
        Rows = @($Rows)
        Issues = @($Issues)
    }
}

function Write-QAResultAndExit {
    $Failed = @($script:Checks | Where-Object { $_.Status -eq "FAIL" }).Count
    $Warnings = @($script:Checks | Where-Object { $_.Status -eq "WARN" }).Count
    $Overall = if ($Failed -gt 0) { "FAIL" } elseif ($Warnings -gt 0) { "WARN" } else { "PASS" }

    $Result = [PSCustomObject]@{
        Tool = "Invoke-PlayerQACheck.ps1"
        Timestamp = (Get-Date).ToString("o")
        Phase = $script:Phase
        RepoRoot = $script:RepoRoot
        Overall = $Overall
        FailureCount = $Failed
        WarningCount = $Warnings
        Checks = @($script:Checks)
    }

    if ($script:AsJson) {
        $Result | ConvertTo-Json -Depth 5
    }
    else {
        "Player QA {0} — {1}" -f $script:Phase, $Overall
        "Repositorio: {0}" -f $script:RepoRoot
        ""
        foreach ($Check in $script:Checks) {
            "[{0}] {1}: {2}" -f $Check.Status, $Check.Name, $Check.Detail
        }
        ""
        "Resumen: {0} FAIL, {1} WARN, {2} comprobaciones." -f $Failed, $Warnings, $script:Checks.Count
    }

    if ($Failed -gt 0) {
        exit 1
    }

    exit 0
}

$GitCommand = Get-Command git -ErrorAction SilentlyContinue
if (-not $GitCommand) {
    Add-QACheck -Status "FAIL" -Name "Git" -Detail "git no está disponible en PATH."
    Write-QAResultAndExit
}

if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot ".git"))) {
    Add-QACheck -Status "FAIL" -Name "Repositorio" -Detail ("No se encontró .git en {0}." -f $RepoRoot)
    Write-QAResultAndExit
}

Add-QACheck -Status "PASS" -Name "Git" -Detail ("Detectado: {0}" -f $GitCommand.Source)
Test-PathGroup -Name "Documentos, configuración y C++" -RelativePaths $RequiredProjectPaths
Test-PathGroup -Name "Assets base LFS" -RelativePaths $RequiredBaselineLfsPaths

$TopLevel = Invoke-GitReadOnly -Arguments @("rev-parse", "--show-toplevel")
if ($TopLevel.ExitCode -eq 0 -and [System.IO.Path]::GetFullPath($TopLevel.Output) -eq $RepoRoot) {
    Add-QACheck -Status "PASS" -Name "Raíz Git" -Detail $TopLevel.Output
}
else {
    Add-QACheck -Status "FAIL" -Name "Raíz Git" -Detail ("Resultado inesperado: {0}" -f $TopLevel.Output)
}

$Branch = Invoke-GitReadOnly -Arguments @("branch", "--show-current")
if ($Branch.ExitCode -eq 0 -and $Branch.Output -eq $ExpectedBranch) {
    Add-QACheck -Status "PASS" -Name "Rama" -Detail $Branch.Output
}
else {
    Add-QACheck -Status "FAIL" -Name "Rama" -Detail ("Esperada {0}; actual {1}." -f $ExpectedBranch, $Branch.Output)
}

$Head = Invoke-GitReadOnly -Arguments @("rev-parse", "HEAD")
if ($Head.ExitCode -eq 0 -and $Head.Output -match "^[0-9a-f]{40}$") {
    Add-QACheck -Status "PASS" -Name "HEAD" -Detail $Head.Output
}
else {
    Add-QACheck -Status "FAIL" -Name "HEAD" -Detail ("No se pudo resolver HEAD: {0}" -f $Head.Output)
}

$Ancestor = Invoke-GitReadOnly -Arguments @("merge-base", "--is-ancestor", $MinimumCommit, "HEAD")
if ($Ancestor.ExitCode -eq 0) {
    Add-QACheck -Status "PASS" -Name "Commit mínimo" -Detail ("HEAD contiene {0}." -f $MinimumCommit)
}
else {
    Add-QACheck -Status "FAIL" -Name "Commit mínimo" -Detail ("HEAD no contiene {0} o Git no pudo comprobarlo." -f $MinimumCommit)
}

$StatusOutput = ""
$StatusExitCode = -1
$PreviousErrorActionPreference = $ErrorActionPreference
try {
    $ErrorActionPreference = "Continue"
    $StatusOutput = (& git --no-optional-locks -C $RepoRoot -c core.quotepath=false status --porcelain=v1 -z --untracked-files=all 2>&1 | Out-String)
    $StatusExitCode = $LASTEXITCODE
}
finally {
    $ErrorActionPreference = $PreviousErrorActionPreference
}
$StatusEntries = @()
if ($StatusExitCode -ne 0) {
    Add-QACheck -Status "FAIL" -Name "Estado Git" -Detail $StatusOutput.Trim()
}
else {
    $StatusEntries = @(Get-GitStatusEntries -NulDelimitedOutput $StatusOutput)
}

if ($StatusExitCode -eq 0 -and $Phase -eq "Preflight") {
    if ($StatusEntries.Count -eq 0) {
        Add-QACheck -Status "PASS" -Name "Worktree" -Detail "Limpio."
    }
    elseif ($AllowDirty) {
        $StatusSummary = $StatusEntries | ForEach-Object { "{0} {1}" -f $_.Status, $_.Path }
        Add-QACheck -Status "WARN" -Name "Worktree" -Detail ("Sucio, permitido solo para desarrollo: {0}" -f ($StatusSummary -join ", "))
    }
    else {
        $StatusSummary = $StatusEntries | ForEach-Object { "{0} {1}" -f $_.Status, $_.Path }
        Add-QACheck -Status "FAIL" -Name "Worktree" -Detail ("Debe estar limpio antes de abrir Unreal: {0}" -f ($StatusSummary -join ", "))
    }
}
elseif ($StatusExitCode -eq 0) {
    $UnmergedCodes = @("DD", "AU", "UD", "UA", "DU", "AA", "UU")
    $UnsupportedEntries = @(
        $StatusEntries | Where-Object {
            $UnmergedCodes -contains $_.Status -or
            $_.Status -match "[DRCTU!]" -or
            ($_.Status -ne "??" -and $_.Status -notmatch "^[ AM]{2}$")
        }
    )
    if ($UnsupportedEntries.Count -gt 0) {
        $UnsupportedSummary = $UnsupportedEntries |
            ForEach-Object { "{0} {1}" -f $_.Status, $_.Path }
        Add-QACheck -Status "FAIL" -Name "Tipos de cambio postflight" -Detail ("Conflictos, renombres, copias o eliminaciones no permitidos: {0}" -f ($UnsupportedSummary -join ", "))
    }
    else {
        Add-QACheck -Status "PASS" -Name "Tipos de cambio postflight" -Detail "Solo altas y modificaciones sin conflictos."
    }

    $ChangedPaths = @(
        $StatusEntries | ForEach-Object {
            $_.Path
            if (-not [string]::IsNullOrWhiteSpace($_.OriginalPath)) {
                $_.OriginalPath
            }
        }
    )
    $UnexpectedPaths = @(
        $ChangedPaths | Where-Object { $AllowedPostflightPaths -notcontains $_ }
    )

    if ($UnexpectedPaths.Count -eq 0) {
        $Detail = if ($ChangedPaths.Count -eq 0) {
            "Worktree limpio; no hay rutas inesperadas."
        }
        else {
            "Solo rutas permitidas: {0}" -f ($ChangedPaths -join ", ")
        }
        Add-QACheck -Status "PASS" -Name "Allowlist postflight" -Detail $Detail
    }
    else {
        Add-QACheck -Status "FAIL" -Name "Allowlist postflight" -Detail ("Rutas fuera de alcance: {0}" -f ($UnexpectedPaths -join ", "))
    }
}

$LfsVersion = Invoke-GitReadOnly -Arguments @("lfs", "version")
if ($LfsVersion.ExitCode -eq 0) {
    Add-QACheck -Status "PASS" -Name "Git LFS" -Detail $LfsVersion.Output
}
else {
    Add-QACheck -Status "FAIL" -Name "Git LFS" -Detail "Git LFS no está disponible; no abrir una sesión que creará uasset/umap."
}

if ($LfsVersion.ExitCode -eq 0) {
    $LfsListing = Invoke-GitReadOnly -Arguments @("lfs", "ls-files", "--long")
    if ($LfsListing.ExitCode -ne 0) {
        Add-QACheck -Status "FAIL" -Name "Objetos LFS base" -Detail ("No se pudo consultar Git LFS: {0}" -f $LfsListing.Output)
    }
    else {
        $LfsEntries = @{}
        foreach ($Line in ($LfsListing.Output -split "\r?\n")) {
            if ($Line -match "^([0-9a-f]{64}) ([*-]) (.+)$") {
                $LfsEntries[$Matches[3].Replace("\", "/")] = [PSCustomObject]@{
                    Oid = $Matches[1]
                    Marker = $Matches[2]
                }
            }
        }

        $MissingLfsEntries = @($RequiredBaselineLfsPaths | Where-Object {
            -not $LfsEntries.ContainsKey($_)
        })
        $PointerOnlyEntries = @($RequiredBaselineLfsPaths | Where-Object {
            $LfsEntries.ContainsKey($_) -and $LfsEntries[$_].Marker -eq "-"
        })

        if ($MissingLfsEntries.Count -eq 0 -and $PointerOnlyEntries.Count -eq 0) {
            Add-QACheck -Status "PASS" -Name "Objetos LFS base" -Detail "BP_TestActor y L_Developer_Testing están registrados e hidratados."
        }
        else {
            $Problems = @()
            if ($MissingLfsEntries.Count -gt 0) {
                $Problems += "no registrados: {0}" -f ($MissingLfsEntries -join ", ")
            }
            if ($PointerOnlyEntries.Count -gt 0) {
                $Problems += "solo pointer, ejecutar git lfs pull: {0}" -f ($PointerOnlyEntries -join ", ")
            }
            Add-QACheck -Status "FAIL" -Name "Objetos LFS base" -Detail ($Problems -join " | ")
        }
    }
}

$Attributes = Invoke-GitReadOnly -Arguments @(
    "check-attr", "filter", "--",
    "UnrealProject/Content/__QA_Probe__.uasset",
    "UnrealProject/Content/__QA_Probe__.umap"
)
if ($Attributes.ExitCode -eq 0 -and @($Attributes.Output -split "\r?\n" | Where-Object { $_ -match "filter: lfs$" }).Count -eq 2) {
    Add-QACheck -Status "PASS" -Name "Atributos LFS" -Detail "uasset y umap usan filter=lfs."
}
else {
    Add-QACheck -Status "FAIL" -Name "Atributos LFS" -Detail $Attributes.Output
}

$UProjectPath = Join-Path $RepoRoot "UnrealProject/ProyectoMemoria.uproject"
try {
    $UProject = Get-Content -Raw -Encoding UTF8 -LiteralPath $UProjectPath | ConvertFrom-Json
    if ([string]$UProject.EngineAssociation -eq "5.8") {
        Add-QACheck -Status "PASS" -Name "Asociación uproject" -Detail "EngineAssociation=5.8."
    }
    else {
        Add-QACheck -Status "FAIL" -Name "Asociación uproject" -Detail ("EngineAssociation={0}; se requiere 5.8." -f $UProject.EngineAssociation)
    }
}
catch {
    Add-QACheck -Status "FAIL" -Name "Asociación uproject" -Detail ("No se pudo leer el uproject: {0}" -f $_.Exception.Message)
}

$DetectedEngineRoot = $EngineRoot
if ([string]::IsNullOrWhiteSpace($DetectedEngineRoot)) {
    $EngineRegistryPaths = @(
        "HKLM:\SOFTWARE\EpicGames\Unreal Engine\5.8",
        "HKLM:\SOFTWARE\WOW6432Node\EpicGames\Unreal Engine\5.8"
    )
    foreach ($RegistryPath in $EngineRegistryPaths) {
        if (Test-Path -LiteralPath $RegistryPath) {
            $RegistryValue = Get-ItemProperty -LiteralPath $RegistryPath -ErrorAction SilentlyContinue
            $InstalledProperty = if ($RegistryValue) {
                $RegistryValue.PSObject.Properties["InstalledDirectory"]
            }
            else {
                $null
            }
            if ($InstalledProperty -and -not [string]::IsNullOrWhiteSpace([string]$InstalledProperty.Value)) {
                $DetectedEngineRoot = [string]$InstalledProperty.Value
                break
            }
        }
    }
}

if ([string]::IsNullOrWhiteSpace($DetectedEngineRoot) -and $env:ProgramFiles) {
    $DefaultEngineRoot = Join-Path $env:ProgramFiles "Epic Games/UE_5.8"
    if (Test-Path -LiteralPath $DefaultEngineRoot -PathType Container) {
        $DetectedEngineRoot = $DefaultEngineRoot
    }
}

if ([string]::IsNullOrWhiteSpace($DetectedEngineRoot)) {
    Add-QACheck -Status "FAIL" -Name "Instalación UE 5.8" -Detail "No se encontró; proporcione -EngineRoot."
}
else {
    $EditorExecutable = Join-Path $DetectedEngineRoot "Engine/Binaries/Win64/UnrealEditor.exe"
    if (Test-Path -LiteralPath $EditorExecutable -PathType Leaf) {
        Add-QACheck -Status "PASS" -Name "Instalación UE 5.8" -Detail $EditorExecutable
    }
    else {
        Add-QACheck -Status "FAIL" -Name "Instalación UE 5.8" -Detail ("No existe UnrealEditor.exe bajo {0}." -f $DetectedEngineRoot)
    }
}

$DefaultInputPath = Join-Path $RepoRoot "UnrealProject/Config/DefaultInput.ini"
$ExpectedInputLines = @(
    "DefaultPlayerInputClass=/Script/EnhancedInput.EnhancedPlayerInput",
    "DefaultInputComponentClass=/Script/EnhancedInput.EnhancedInputComponent"
)
if (-not (Test-Path -LiteralPath $DefaultInputPath)) {
    Add-QACheck -Status "FAIL" -Name "Enhanced Input config" -Detail ("No existe: {0}" -f $DefaultInputPath)
}
else {
    try {
        $DefaultInput = Get-Content -Raw -Encoding UTF8 -LiteralPath $DefaultInputPath
        $ActiveInputLines = @(
            $DefaultInput -split "\r?\n" |
                ForEach-Object { $_.Trim() } |
                Where-Object { $_ -and $_ -notmatch "^[;#]" }
        )
        $PlayerInputAssignments = @($ActiveInputLines | Where-Object { $_ -match "^DefaultPlayerInputClass=" })
        $InputComponentAssignments = @($ActiveInputLines | Where-Object { $_ -match "^DefaultInputComponentClass=" })
        if ($PlayerInputAssignments.Count -eq 1 -and
            $InputComponentAssignments.Count -eq 1 -and
            $PlayerInputAssignments[0] -eq $ExpectedInputLines[0] -and
            $InputComponentAssignments[0] -eq $ExpectedInputLines[1]) {
            Add-QACheck -Status "PASS" -Name "Enhanced Input config" -Detail "Las clases Enhanced predeterminadas están configuradas."
        }
        else {
            $ObservedAssignments = @($PlayerInputAssignments) + @($InputComponentAssignments)
            Add-QACheck -Status "FAIL" -Name "Enhanced Input config" -Detail ("Asignaciones activas inesperadas o duplicadas: {0}" -f ($ObservedAssignments -join ", "))
        }
    }
    catch {
        Add-QACheck -Status "FAIL" -Name "Enhanced Input config" -Detail ("No se pudo leer DefaultInput.ini: {0}" -f $_.Exception.Message)
    }
}

$BuildCsPath = Join-Path $RepoRoot "UnrealProject/Source/ProyectoMemoria/ProyectoMemoria.Build.cs"
if (-not (Test-Path -LiteralPath $BuildCsPath)) {
    Add-QACheck -Status "FAIL" -Name "Enhanced Input module" -Detail ("No existe: {0}" -f $BuildCsPath)
}
else {
    try {
        $BuildCs = Get-Content -Raw -Encoding UTF8 -LiteralPath $BuildCsPath
        if ($BuildCs -match '(?m)^\s*"EnhancedInput"\s*,?\s*$') {
            Add-QACheck -Status "PASS" -Name "Enhanced Input module" -Detail "ProyectoMemoria.Build.cs declara EnhancedInput."
        }
        else {
            Add-QACheck -Status "FAIL" -Name "Enhanced Input module" -Detail "ProyectoMemoria.Build.cs no declara EnhancedInput."
        }
    }
    catch {
        Add-QACheck -Status "FAIL" -Name "Enhanced Input module" -Detail ("No se pudo leer Build.cs: {0}" -f $_.Exception.Message)
    }
}

$UnrealProcesses = @(
    Get-Process -Name @("UnrealEditor", "UnrealEditor-Cmd", "ShaderCompileWorker") -ErrorAction SilentlyContinue
)
if ($UnrealProcesses.Count -eq 0) {
    Add-QACheck -Status "PASS" -Name "Procesos Unreal" -Detail "No se detectaron."
}
else {
    $ProcessSummary = $UnrealProcesses | ForEach-Object { "{0}({1})" -f $_.ProcessName, $_.Id }
    Add-QACheck -Status "FAIL" -Name "Procesos Unreal" -Detail ("Cerrar antes de continuar: {0}" -f ($ProcessSummary -join ", "))
}

if ($Phase -eq "Preflight") {
    if ($ConfirmHardwareReady) {
        Add-QACheck -Status "PASS" -Name "Confirmación de hardware" -Detail "El operador confirmó temperatura, ventilación y consumo normales."
    }
    else {
        Add-QACheck -Status "WARN" -Name "Confirmación de hardware" -Detail "Requiere confirmación humana; vuelva a ejecutar con -ConfirmHardwareReady."
    }
}
else {
    Test-PathGroup -Name "Assets requeridos" -RelativePaths $ExpectedAssetPaths

    $ExistingExpectedAssets = @($ExpectedAssetPaths | Where-Object {
        Test-Path -LiteralPath (Join-Path $RepoRoot $_) -PathType Leaf
    })
    $IgnoredAssets = @()
    $InvisibleAssets = @()
    $VisibleStatusPaths = @($StatusEntries | ForEach-Object { $_.Path })
    foreach ($AssetPath in $ExistingExpectedAssets) {
        $IgnoreCheck = Invoke-GitReadOnly -Arguments @("check-ignore", "-q", "--", $AssetPath)
        if ($IgnoreCheck.ExitCode -eq 0) {
            $IgnoredAssets += $AssetPath
            continue
        }

        $TrackedCheck = Invoke-GitReadOnly -Arguments @("ls-files", "--error-unmatch", "--", $AssetPath)
        if ($TrackedCheck.ExitCode -ne 0 -and $VisibleStatusPaths -notcontains $AssetPath) {
            $InvisibleAssets += $AssetPath
        }
    }

    if ($IgnoredAssets.Count -eq 0 -and $InvisibleAssets.Count -eq 0) {
        Add-QACheck -Status "PASS" -Name "Visibilidad Git de assets" -Detail ("{0} assets existentes están tracked o visibles como cambios." -f $ExistingExpectedAssets.Count)
    }
    else {
        $VisibilityProblems = @()
        if ($IgnoredAssets.Count -gt 0) {
            $VisibilityProblems += "ignorados: {0}" -f ($IgnoredAssets -join ", ")
        }
        if ($InvisibleAssets.Count -gt 0) {
            $VisibilityProblems += "no tracked ni visibles: {0}" -f ($InvisibleAssets -join ", ")
        }
        Add-QACheck -Status "FAIL" -Name "Visibilidad Git de assets" -Detail ($VisibilityProblems -join " | ")
    }

    $QAPath = Join-Path $RepoRoot "QA_PLAYER_V0.1.md"
    if (-not (Test-Path -LiteralPath $QAPath)) {
        Add-QACheck -Status "FAIL" -Name "Resultados QA" -Detail ("No existe: {0}" -f $QAPath)
    }
    else {
        try {
            $QAAudit = Get-QAResultAudit -Path $QAPath
            if ($QAAudit.Issues.Count -gt 0) {
                Add-QACheck -Status "FAIL" -Name "Estructura QA" -Detail ($QAAudit.Issues -join " | ")
            }
            else {
                Add-QACheck -Status "PASS" -Name "Estructura QA" -Detail ("{0} IDs únicos, un estado por fila y evidencia para resultados ejecutados." -f $QAAudit.Rows.Count)

                $RequiredNonPass = @(
                    $QAAudit.Rows | Where-Object {
                        $ConditionalQAIds -notcontains $_.Id -and $_.State -ne "PASS"
                    }
                )
                $ConditionalInvalid = @(
                    $QAAudit.Rows | Where-Object {
                        $ConditionalQAIds -contains $_.Id -and
                        $_.State -ne "PASS" -and $_.State -ne "BLOCKED"
                    }
                )
                $ConditionalBlocked = @(
                    $QAAudit.Rows | Where-Object {
                        $ConditionalQAIds -contains $_.Id -and $_.State -eq "BLOCKED"
                    }
                )

                if ($RequiredNonPass.Count -gt 0 -or $ConditionalInvalid.Count -gt 0) {
                    $BlockingRows = @($RequiredNonPass) + @($ConditionalInvalid)
                    $BlockingSummary = @(
                        $BlockingRows | Select-Object -First 12 |
                            ForEach-Object { "{0}={1}" -f $_.Id, $_.State }
                    )
                    $RemainingCount = $BlockingRows.Count - $BlockingSummary.Count
                    $RemainingText = if ($RemainingCount -gt 0) {
                        " y {0} más" -f $RemainingCount
                    }
                    else {
                        ""
                    }
                    Add-QACheck -Status "FAIL" -Name "Resultados QA" -Detail ("{0} filas impiden aceptación: {1}{2}." -f $BlockingRows.Count, ($BlockingSummary -join ", "), $RemainingText)
                }
                elseif ($ConditionalBlocked.Count -gt 0) {
                    $BlockedSummary = $ConditionalBlocked | ForEach-Object { $_.Id }
                    Add-QACheck -Status "WARN" -Name "Resultados QA" -Detail ("QA obligatorio aprobado; bloqueos condicionales documentados: {0}" -f ($BlockedSummary -join ", "))
                }
                else {
                    Add-QACheck -Status "PASS" -Name "Resultados QA" -Detail "Las 79 filas esperadas están en PASS con evidencia."
                }
            }
        }
        catch {
            Add-QACheck -Status "FAIL" -Name "Resultados QA" -Detail ("No se pudo auditar la matriz: {0}" -f $_.Exception.Message)
        }
    }

    if ([string]::IsNullOrWhiteSpace($LogPath)) {
        Add-QACheck -Status "FAIL" -Name "Output Log" -Detail "Postflight requiere -LogPath para validar la evidencia de la sesión."
    }
    else {
        $ResolvedLogPath = if ([System.IO.Path]::IsPathRooted($LogPath)) {
            $LogPath
        }
        else {
            Join-Path $RepoRoot $LogPath
        }

        if (-not (Test-Path -LiteralPath $ResolvedLogPath -PathType Leaf)) {
            Add-QACheck -Status "FAIL" -Name "Output Log" -Detail ("No existe como archivo: {0}" -f $ResolvedLogPath)
        }
        else {
            try {
                $LogItem = Get-Item -LiteralPath $ResolvedLogPath
                if ($LogItem.Length -le 0) {
                    Add-QACheck -Status "FAIL" -Name "Output Log" -Detail "El archivo está vacío."
                }
                elseif ($LogItem.Extension -ne ".log") {
                    Add-QACheck -Status "FAIL" -Name "Output Log" -Detail ("La extensión debe ser .log; se recibió {0}." -f $LogItem.Extension)
                }
                else {
                    $RequiredLogMarkers = @(
                        "Log file open,",
                        "LogInit: Display: Running engine for game: ProyectoMemoria"
                    )
                    $MissingLogMarkers = @($RequiredLogMarkers | Where-Object {
                        -not (Select-String -LiteralPath $ResolvedLogPath -SimpleMatch -Quiet -Pattern $_)
                    })
                    if ($MissingLogMarkers.Count -gt 0) {
                        Add-QACheck -Status "FAIL" -Name "Output Log" -Detail ("No parece un log de ProyectoMemoria: faltan {0}." -f ($MissingLogMarkers -join ", "))
                    }
                    else {
                        $LogHits = @(Select-String -LiteralPath $ResolvedLogPath -SimpleMatch -Pattern $ForbiddenLogMessages)
                        if ($LogHits.Count -eq 0) {
                            Add-QACheck -Status "PASS" -Name "Output Log" -Detail ("Log UE válido, {0} bytes, modificado {1:o}; sin diagnósticos propios prohibidos." -f $LogItem.Length, $LogItem.LastWriteTime)
                        }
                        else {
                            $HitMessages = $LogHits | ForEach-Object { "línea {0}: {1}" -f $_.LineNumber, $_.Line.Trim() }
                            Add-QACheck -Status "FAIL" -Name "Output Log" -Detail ($HitMessages -join " | ")
                        }
                    }
                }
            }
            catch {
                Add-QACheck -Status "FAIL" -Name "Output Log" -Detail ("No se pudo leer el log: {0}" -f $_.Exception.Message)
            }
        }
    }
}

Write-QAResultAndExit
