$apkPath = "frontend/app/build/outputs/apk/debug/app-debug.apk"
if (Test-Path $apkPath) {
    Write-Host "Installing $apkPath..." -ForegroundColor Cyan
    adb install -r $apkPath
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nInstall Successful!" -ForegroundColor Green
    } else {
        Write-Host "`nInstall Failed! Ensure a device/emulator is connected." -ForegroundColor Red
        exit $LASTEXITCODE
    }
} else {
    Write-Host "APK not found at $apkPath. Please run build_app.ps1 first." -ForegroundColor Red
    exit 1
}
