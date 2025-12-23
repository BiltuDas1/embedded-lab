function cross-compiler {
  $compileScript = Join-Path $PSScriptRoot "windows" "compile.bat"
  $uploadScript = Join-Path $PSScriptRoot "windows" "upload.bat"
  $eraseScript = Join-Path $PSScriptRoot "windows" "erase.bat"
  $buildPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".." "build"))
  $lastBuildLog = Join-Path $buildPath "lastbuild.txt"
  $libraryFolderName = "shared"
  $libraryPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".." $libraryFolderName))
  $gitPath = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".." ".git"))

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
  } elseif ($args[0] -eq "--install" -and $args.Count -eq 2 -and $args[1] -match '[:/](?<owner>[^/:]+)/(?<repo>[^/:]+?)(?:\.git)?$') {
    $owner = $Matches['owner']
    $repo = $Matches['repo']

    New-Item -ItemType Directory -Path $libraryPath -Force | Out-Null # Create Parent directories
    $savePath = Join-Path ((Resolve-Path $libraryPath -Relative)) "$owner-$repo"
    
    git submodule add $args[1] "$savePath"
  } elseif ($args[0] -eq "--uninstall" -and $args.Count -eq 2 -and $args[1] -match '[:/](?<owner>[^/:]+)/(?<repo>[^/:]+?)(?:\.git)?$') {
    $owner = $Matches['owner']
    $repo = $Matches['repo']

    New-Item -ItemType Directory -Path $libraryPath -Force | Out-Null # Create Parent directories
    $savePath = Join-Path ((Resolve-Path $libraryPath -Relative)) "$owner-$repo"
    $gitRemovePath = Join-Path $gitPath "modules" $libraryFolderName "$owner-$repo"

    git submodule deinit -f "$savePath"
    git rm -f "$savePath"
    Remove-Item -Recurse -Force "$gitRemovePath"
  } elseif (Test-Path -Path $args[0] -PathType Container) {
    $argsPath = (Resolve-Path $args[0]).Path.TrimEnd('\')
    & "$compileScript" $argsPath
  } else {
    Write-Error "invalid argument"
  }
}
