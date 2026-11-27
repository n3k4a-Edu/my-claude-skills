# Pulls the upstream skill repos and rebuilds the library. Review `git diff --stat`, then commit and push.
$Repo = Split-Path $PSScriptRoot -Parent
$Sources = Join-Path $HOME '.claude\skill-sources'
New-Item -ItemType Directory -Force $Sources | Out-Null
$upstreams = @{
    'ecc' = 'https://github.com/affaan-m/ECC.git'
    'mattpocock-skills' = 'https://github.com/mattpocock/skills.git'
    'ponytail' = 'https://github.com/DietrichGebert/ponytail.git'
    'coreyhaines-marketing' = 'https://github.com/coreyhaines31/marketingskills.git'
    'strix' = 'https://github.com/usestrix/strix.git'
    'img2threejs' = 'https://github.com/img2threejs/img2threejs.git'
}
foreach ($name in $upstreams.Keys) {
    $dir = Join-Path $Sources $name
    if (Test-Path (Join-Path $dir '.git')) { Write-Host "pull $name"; git -C $dir pull --ff-only }
    elseif ($upstreams[$name]) { Write-Host "clone $name"; git clone --depth 1 $upstreams[$name] $dir }
    else { Write-Host "skip $name (no local clone)" -ForegroundColor Yellow }
}
Push-Location $Repo
uv run python -I tools/build_library.py
git status --short | Select-Object -First 20
Pop-Location
