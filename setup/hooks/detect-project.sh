#!/usr/bin/env bash
# SessionStart hook: names the project's stack so Claude picks skills for it.
found=()
has() { compgen -G "$1" >/dev/null; }
[ -f wp-config.php ] || [ -d wp-content ] && found+=(WordPress)
if [ -f package.json ]; then
  for fw in next react vue nuxt @angular/core svelte vite expo react-native express @nestjs/core electron; do
    grep -q "\"$fw\"[[:space:]]*:" package.json && found+=("$fw")
  done
  [ ${#found[@]} -eq 0 ] && found+=(Node.js)
fi
if [ -f artisan ] || { [ -f composer.json ] && grep -q laravel/framework composer.json; }; then found+=(Laravel)
elif [ -f composer.json ]; then found+=(PHP); fi
if [ -f manage.py ]; then found+=(Django); elif [ -f pyproject.toml ] || [ -f requirements.txt ]; then found+=(Python); fi
{ [ -f pom.xml ] || has 'build.gradle*'; } && found+=(Java/Kotlin)
{ has '*.csproj' || has '*.sln'; } && found+=(.NET)
[ -f go.mod ] && found+=(Go)
[ -f Cargo.toml ] && found+=(Rust)
[ -f Gemfile ] && found+=(Ruby)
[ -f pubspec.yaml ] && found+=(Flutter)
{ has '*.xcodeproj' || [ -f Package.swift ]; } && found+=(iOS/Swift)
[ -f project.godot ] && found+=(Godot)
has '*.uproject' && found+=(Unreal)
[ -d Assets ] && [ -d ProjectSettings ] && found+=("Unity project")
has '*.blend' && found+=(Blender)
{ [ -f Dockerfile ] || has 'docker-compose*.yml' || has 'compose*.yml'; } && found+=(Docker)
has '*.tf' && found+=(Terraform)
[ -d prisma ] && found+=(Prisma)
[ -d supabase ] && found+=(Supabase)
if [ ${#found[@]} -gt 0 ]; then
  list=$(printf '%s, ' "${found[@]}"); list=${list%, }
  echo "Project stack detected: $list. When the user gives a task here, use the skill-library skill (with the routing in CLAUDE.md) to pick the best skills for this stack and the task's goal before starting."
fi
