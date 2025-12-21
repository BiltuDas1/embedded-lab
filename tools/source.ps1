function cross-compile {
  $compileScript = Join-Path $PSScriptRoot "windows" "compile.bat"
  $uploadScript = Join-Path $PSScriptRoot "windows" "upload.bat"
  $eraseScript = Join-Path $PSScriptRoot "windows" "erase.bat"
  $buildPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".." "build"))
  $lastBuildLog = Join-Path $buildPath "lastbuild.txt"

  if ($args.Count -eq 0) {
    Write-Host "Usage:  cross-compile <path>" -ForegroundColor Cyan
    Write-Host "Example: cross-compile ."
    return
  }

  if ($args[0] -eq ".") {
    $current = $PWD.Path
    & "$compileScript" "$current"
  } elseif ($args[0] -eq "--upload") {
    $lastBuild = (Get-Content "$lastBuildLog" -First 1).Trim()

    $lastBuildPath = Join-Path $buildPath $lastBuild
    if (-not (Test-Path -Path "$lastBuildPath")) {
      Write-Host "[Error] build folder got corrupted, recompile and try again." -ForegroundColor Red
      return
    }

    & "$uploadScript" "$lastBuild"
  } elseif ($args[0] -eq "--reset") {
    & "$eraseScript"
  } elseif ($args[0] -eq "--clean-build") {
    Remove-Item -Path ".\build" -Recurse -Force
  } elseif (Test-Path -Path $args[0] -PathType Container) {
    $argsPath = (Resolve-Path $args[0]).Path.TrimEnd('\')
    & "$compileScript" $argsPath
  } else {
    Write-Error "invalid argument"
  }
}
