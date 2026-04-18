param(
    [string]$Path = "C:\Users\mypc\.gemini\REFLECTIONS.md",
    [int]$MaxBuffer = 5
)

# Read file
$content = Get-Content $Path -Raw

# Pattern to find all <syn> blocks (multi-line)
$pattern = '(?s)<syn id="(.*?)" date=".*?" type=".*?">.*?RULE: (.*?)\s*</syn>'
$matches = [regex]::Matches($content, $pattern)

if ($matches.Count -le $MaxBuffer) {
    # No compaction needed
    return
}

$toCompactCount = $matches.Count - $MaxBuffer
$compactedRules = @()
$newContent = $content

# Select the oldest ones (first matches)
for ($i = 0; $i -lt $toCompactCount; $i++) {
    $fullBlock = $matches[$i].Value
    $id = $matches[$i].Groups[1].Value
    $rule = $matches[$i].Groups[2].Value.Trim()
    
    # Format the core rule
    $compactedRules += "- [$id]: $rule"
    
    # Remove from content
    $newContent = $newContent.Replace($fullBlock, "").Trim()
}

# The # [CORE] marker is where we append
$coreHeader = "# [CORE]"
$activeHeader = "# 🧊 RECENT SYNAPSES"

# Find [CORE] section and [ACTIVE] section
if ($newContent -match "(?s)# \[CORE\](.*?)(# 🧊|$)") {
    $existingRules = $Matches[1].Trim()
    $updatedRules = if ($existingRules) { "$existingRules`n$($compactedRules -join "`n")" } else { $compactedRules -join "`n" }
    
    # Re-assemble the file
    $headerPart = $newContent.Substring(0, $newContent.IndexOf($coreHeader) + $coreHeader.Length)
    $activePart = $newContent.Substring($newContent.IndexOf($activeHeader))
    
    $finalContent = "$headerPart`n$updatedRules`n`n$activePart"
    
    # Write back
    $finalContent | Set-Content $Path
    Write-Host "Compacted $toCompactCount items in $Path." -ForegroundColor Cyan
}
