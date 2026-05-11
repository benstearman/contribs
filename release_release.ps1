Write-Host "DEPLOYMENT Generating Release Build and Deploying to Landing Page..." -ForegroundColor Cyan

# 1. Build the Release APK
Write-Host "BUILDING Building Release APK..." -ForegroundColor Gray
Set-Location frontend
./gradlew assembleRelease
if ($LASTEXITCODE -ne 0) {
    Write-Host "FAILED Build Failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}

# 2. Locate the APK
# Note: Gradle produces app-release-unsigned.apk if no signing config is provided.
$sourceApk = "app/build/outputs/apk/release/app-release-unsigned.apk"
if (-not (Test-Path $sourceApk)) {
    # Try alternate name just in case
    $sourceApk = "app/build/outputs/apk/release/app-release.apk"
}

$destination = "../landing/contribs-release.apk"

# 3. Move and Rename
if (Test-Path $sourceApk) {
    Copy-Item -Path $sourceApk -Destination $destination -Force
    Write-Host "SUCCESS APK released to landing/contribs-release.apk" -ForegroundColor Green
} else {
    Write-Host "FAILED Could not find source APK at $sourceApk" -ForegroundColor Red
    exit 1
}

# 4. Update index.md to point to the release build
Write-Host "UPDATING Updating landing page links..." -ForegroundColor Gray
$indexPath = "../landing/index.md"
if (Test-Path $indexPath) {
    $content = Get-Content $indexPath
    $newContent = $content -replace "contribs-debug.apk", "contribs-release.apk"
    $newContent = $newContent -replace "Download the Android APK", "Download the Android APK (Release)"
    $newContent | Set-Content $indexPath
    Write-Host "SUCCESS landing/index.md updated." -ForegroundColor Green
}

Set-Location ..
Write-Host "DONE Deployment complete! Remember to commit and push to update the live site." -ForegroundColor Cyan
