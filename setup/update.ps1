# Pulls the latest version of this repo and re-applies it. Run on any machine.
$Repo = Split-Path $PSScriptRoot -Parent
git -C $Repo pull --ff-only
& (Join-Path $PSScriptRoot 'setup.ps1') -SkipPlugins
if (Get-Command claude -ErrorAction SilentlyContinue) { claude plugin marketplace update }
