Write-Host "Building Contribs App (Debug)..." -ForegroundColor Cyan
Set-Location frontend
./gradlew assembleDebug
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nBuild Successful!" -ForegroundColor Green
} else {
    Write-Host "`nBuild Failed!" -ForegroundColor Red
    exit $LASTEXITCODE
}
Set-Location ..
