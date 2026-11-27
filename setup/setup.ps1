# Installs this skill setup on a Windows machine. Safe to run again: it only adds what is missing.
#   powershell -ExecutionPolicy Bypass -File setup\setup.ps1             (full setup)
#   powershell -ExecutionPolicy Bypass -File setup\setup.ps1 -SkipPlugins (skills, CLAUDE.md, hook only)
param([switch]$SkipPlugins)
$ErrorActionPreference = 'Stop'
$Repo = Split-Path $PSScriptRoot -Parent
$Claude = Join-Path $HOME '.claude'
$Stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$Backup = Join-Path $Claude "setup-backup\$Stamp"
New-Item -ItemType Directory -Force (Join-Path $Claude 'skills') | Out-Null

function Save-Backup($path) {
    New-Item -ItemType Directory -Force $Backup | Out-Null
    Move-Item -LiteralPath $path -Destination $Backup
    Write-Host "  backed up $(Split-Path $path -Leaf) -> $Backup" -ForegroundColor DarkYellow
}

Write-Host '== Skills' -ForegroundColor Cyan
foreach ($dir in Get-ChildItem -LiteralPath (Join-Path $Repo 'skills') -Directory) {
    $target = Join-Path $Claude "skills\$($dir.Name)"
    $item = Get-Item -LiteralPath $target -Force -ErrorAction SilentlyContinue
    if ($item -and $item.LinkType -eq 'Junction' -and ($item.Target -contains $dir.FullName)) { continue }
    if ($item) { Save-Backup $target }
    New-Item -ItemType Junction -Path $target -Target $dir.FullName | Out-Null
    Write-Host "  linked $($dir.Name)"
}

Write-Host '== CLAUDE.md' -ForegroundColor Cyan
$src = Join-Path $PSScriptRoot 'CLAUDE.md'
$dst = Join-Path $Claude 'CLAUDE.md'
if ((Test-Path $dst) -and ((Get-FileHash $dst).Hash -eq (Get-FileHash $src).Hash)) {
    Write-Host '  already current'
} else {
    if (Test-Path $dst) { Copy-Item $dst (Join-Path $Claude "CLAUDE.md.bak-$Stamp") }
    Copy-Item $src $dst -Force
    Write-Host '  installed'
}

Write-Host '== Project-detection hook' -ForegroundColor Cyan
$settingsPath = Join-Path $Claude 'settings.json'
$hookScript = Join-Path $PSScriptRoot 'hooks\detect-project.ps1'
$command = "powershell -NoProfile -ExecutionPolicy Bypass -File `"$hookScript`""
$settings = if (Test-Path $settingsPath) { Get-Content $settingsPath -Raw -Encoding UTF8 | ConvertFrom-Json } else { [pscustomobject]@{} }
if (-not $settings.PSObject.Properties['hooks']) { $settings | Add-Member -NotePropertyName hooks -NotePropertyValue ([pscustomobject]@{}) }
if (-not $settings.hooks.PSObject.Properties['SessionStart']) { $settings.hooks | Add-Member -NotePropertyName SessionStart -NotePropertyValue @() }
$present = @($settings.hooks.SessionStart | ForEach-Object { $_.hooks } | Where-Object { $_.command -like '*detect-project.ps1*' })
if ($present.Count -gt 0) {
    Write-Host '  already installed'
} else {
    if (Test-Path $settingsPath) { Copy-Item $settingsPath (Join-Path $Claude "settings.json.bak-$Stamp") }
    $entry = [pscustomobject]@{ hooks = @([pscustomobject]@{ type = 'command'; command = $command }) }
    $settings.hooks.SessionStart = @($settings.hooks.SessionStart) + $entry
    $json = $settings | ConvertTo-Json -Depth 64
    [IO.File]::WriteAllText($settingsPath, $json, (New-Object Text.UTF8Encoding $false))
    Write-Host '  installed'
}

if (-not $SkipPlugins) {
    Write-Host '== Plugins' -ForegroundColor Cyan
    if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
        Write-Host '  claude CLI not found: install Claude Code, then run this script again.' -ForegroundColor Yellow
    } else {
        $list = Get-Content (Join-Path $PSScriptRoot 'plugins.json') -Raw -Encoding UTF8 | ConvertFrom-Json
        $ErrorActionPreference = 'Continue'
        foreach ($m in $list.marketplaces) {
            claude plugin marketplace add $m.source 2>&1 | Out-Null
            Write-Host "  marketplace $($m.name)"
        }
        foreach ($p in $list.plugins) {
            $out = claude plugin install $p 2>&1 | Out-String
            Write-Host "  $p : $(($out.Trim() -split "`n")[-1])"
        }
    }
}

Write-Host "`nDone. Restart Claude to load the skills." -ForegroundColor Green
