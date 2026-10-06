# Create Desktop Shortcuts for HEIC to PNG Standalone Executables
$wsh = New-Object -ComObject WScript.Shell
$desktopPath = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::Desktop)
$currentDir = Split-Path -Parent $MyInvocation.MyCommand.Path

$guiExe = Join-Path $currentDir "dist\HEIC-to-PNG-Converter.exe"
$dragDropExe = Join-Path $currentDir "dist\HEIC-Drag-Drop.exe"

# Delete old shortcuts completely to clear any stale Windows icon caches
$old1 = Join-Path $desktopPath "HEIC-to-PNG-App.lnk"
$old2 = Join-Path $desktopPath "HEIC-Drag-Drop-Convert.lnk"
if (Test-Path $old1) { Remove-Item $old1 -Force }
if (Test-Path $old2) { Remove-Item $old2 -Force }

# 1. Desktop shortcut for GUI app (Points to standalone EXE with embedded blue camera icon)
$shortcutPath1 = Join-Path $desktopPath "HEIC-to-PNG-App.lnk"
$shortcut1 = $wsh.CreateShortcut($shortcutPath1)
$shortcut1.TargetPath = $guiExe
$shortcut1.WorkingDirectory = (Split-Path -Parent $guiExe)
$shortcut1.Description = "HEIC to PNG Converter - Standalone GUI"
$shortcut1.Save()

# 2. Desktop shortcut for Drag-and-Drop (Points to standalone EXE with embedded lightning drop icon)
$shortcutPath2 = Join-Path $desktopPath "HEIC-Drag-Drop-Convert.lnk"
$shortcut2 = $wsh.CreateShortcut($shortcutPath2)
$shortcut2.TargetPath = $dragDropExe
$shortcut2.WorkingDirectory = (Split-Path -Parent $dragDropExe)
$shortcut2.Description = "Drag and drop HEIC files onto this shortcut to convert directly to PNG"
$shortcut2.Save()

Write-Host "Success! Shortcuts now point directly to native standalone .exe files!" -ForegroundColor Green
Write-Host "  1. HEIC-to-PNG-App.lnk       -> HEIC-to-PNG-Converter.exe (Embedded Native Blue Icon)" -ForegroundColor Cyan
Write-Host "  2. HEIC-Drag-Drop-Convert.lnk -> HEIC-Drag-Drop.exe (Embedded Native Lightning Icon)" -ForegroundColor Yellow
