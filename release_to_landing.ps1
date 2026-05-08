Write-Host "🚀 Releasing Contribs App to Landing Page..." -ForegroundColor Cyan

# 1. Build the App
Set-Location frontend
./gradlew assembleDebug
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Build Failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

# 2. Locate and Move the APK
$sourceApk = "app/build/outputs/apk/debug/app-debug.apk"
$destination = "../landing/contribs-debug.apk"

if (Test-Path $sourceApk) {
    Copy-Item -Path $sourceApk -Destination $destination -Force
    Write-Host "✅ APK released to landing/contribs-debug.apk" -ForegroundColor Green
} else {
    Write-Host "❌ Could not find source APK at $sourceApk" -ForegroundColor Red
}

Set-Location ..
