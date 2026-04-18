param (
    [Parameter(Mandatory=$true)]
    [string]$Id,

    [Parameter(Mandatory=$true)]
    [string]$Obj,

    [string]$Type = "PREF", # PREF, ERROR, ARCH

    [string]$Cause = "Not specified",
    
    [string]$Rule = "Follow current project standards",

    [int]$MaxBuffer = 5
)

$date = Get-Date -Format "yyyy-MM-dd"
$globalRefPath = "C:\Users\mypc\.gemini\REFLECTIONS.md"
$localRefPath = ".\reflection.md"
$scriptsDir = Split-Path -Parent $PSCommandPath

$entry = @"

<syn id="$Id" date="$date" type="$Type">
OBJ: $Obj
CAUSE: $Cause
RULE: $Rule
</syn>
"@

# Update Global Memory
if (Test-Path $globalRefPath) {
    Add-Content -Path $globalRefPath -Value $entry
} else {
    Set-Content -Path $globalRefPath -Value "# Global Wisdom & Reflections`n$entry"
}

# Update Project Memory
if (Test-Path $localRefPath) {
    Add-Content -Path $localRefPath -Value $entry
} else {
    Set-Content -Path $localRefPath -Value "# Project Wisdom`n$entry"
}

# Trigger Compaction Logic (Deterministic / External)
$compactScript = Join-Path $scriptsDir "compact_memory.ps1"
if (Test-Path $compactScript) {
    powershell -File $compactScript -Path $globalRefPath -MaxBuffer $MaxBuffer
    powershell -File $compactScript -Path $localRefPath -MaxBuffer $MaxBuffer
}

Write-Host "Synapse harvested and compacted. Token-efficiency maximized." -ForegroundColor Green
