# SessionStart hook: names the project's stack so Claude picks skills for it.
$dir = (Get-Location).Path
$found = [System.Collections.Generic.List[string]]::new()
function Test-Here($pattern) { [bool](Get-ChildItem -LiteralPath $dir -Filter $pattern -Force -ErrorAction SilentlyContinue | Select-Object -First 1) }
function Read-Text($name) { $p = Join-Path $dir $name; if (Test-Path -LiteralPath $p) { Get-Content -LiteralPath $p -Raw -ErrorAction SilentlyContinue } else { '' } }

if (Test-Here 'wp-config.php' -or (Test-Path (Join-Path $dir 'wp-content'))) { $found.Add('WordPress') }
$pkg = Read-Text 'package.json'
if ($pkg) {
    foreach ($fw in 'next', 'react', 'vue', 'nuxt', '@angular/core', 'svelte', 'vite', 'expo', 'react-native', 'express', '@nestjs/core', 'electron') {
        if ($pkg -match ('"' + [regex]::Escape($fw) + '"\s*:')) { $found.Add($fw) }
    }
    if ($found.Count -eq 0 -or ($found -notcontains 'next' -and $found -notcontains 'react')) { $found.Add('Node.js') }
}
$composer = Read-Text 'composer.json'
if ($composer -match 'laravel/framework' -or (Test-Here 'artisan')) { $found.Add('Laravel') } elseif ($composer) { $found.Add('PHP') }
if (Test-Here 'manage.py') { $found.Add('Django') }
elseif ((Test-Here 'pyproject.toml') -or (Test-Here 'requirements.txt')) { $found.Add('Python') }
if ((Test-Here 'pom.xml') -or (Test-Here 'build.gradle*')) { $found.Add('Java/Kotlin') }
if ((Test-Here '*.csproj') -or (Test-Here '*.sln')) { $found.Add('.NET') }
if (Test-Here 'go.mod') { $found.Add('Go') }
if (Test-Here 'Cargo.toml') { $found.Add('Rust') }
if (Test-Here 'Gemfile') { $found.Add('Ruby') }
if (Test-Here 'pubspec.yaml') { $found.Add('Flutter') }
if ((Test-Here '*.xcodeproj') -or (Test-Here 'Package.swift')) { $found.Add('iOS/Swift') }
if (Test-Here 'project.godot') { $found.Add('Godot') }
if (Test-Here '*.uproject') { $found.Add('Unreal') }
if ((Test-Path (Join-Path $dir 'Assets')) -and (Test-Path (Join-Path $dir 'ProjectSettings'))) { $found.Add('Unity project') }
if (Get-ChildItem -LiteralPath $dir -Directory -Filter '*_Data' -ErrorAction SilentlyContinue | Where-Object { Test-Path (Join-Path $_.FullName 'Managed') }) { $found.Add('Unity game build') }
if (Test-Here '*.blend') { $found.Add('Blender') }
if ((Test-Here 'Dockerfile') -or (Test-Here 'docker-compose*.yml') -or (Test-Here 'compose*.yml')) { $found.Add('Docker') }
if (Test-Here '*.tf') { $found.Add('Terraform') }
if (Test-Path (Join-Path $dir 'prisma')) { $found.Add('Prisma') }
if (Test-Path (Join-Path $dir 'supabase')) { $found.Add('Supabase') }
if (($found.Count -eq 0) -and ((Test-Here '*.exe') -or (Test-Here '*.dll') -or (Test-Here '*.apk'))) { $found.Add('binaries to analyse') }

if ($found.Count -gt 0) {
    $list = ($found | Select-Object -Unique) -join ', '
    Write-Output "Project stack detected: $list. When the user gives a task here, use the skill-library skill (with the routing in CLAUDE.md) to pick the best skills for this stack and the task's goal before starting."
}
