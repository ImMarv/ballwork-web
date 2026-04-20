param(
    [string]$BaseUrl = "http://host.docker.internal:8080",
    [string]$SeasonYear = "2023",
  [int]$SearchLimit = 10,
  [ValidateSet("safe", "aggressive")]
  [string]$LoadProfile = "safe"
)

$repoRoot = Resolve-Path "$PSScriptRoot\.."

Write-Host "Running Scenario 1 against $BaseUrl"

$startRate = 20
$preAllocatedVus = 100
$maxVus = 800
$stage1Target = 100
$stage1Duration = "1m"
$stage2Target = 200
$stage2Duration = "2m"
$stage3Target = 300
$stage3Duration = "2m"
$stage4Duration = "1m"
$thinkTimeSeconds = 0

if ($LoadProfile -eq "aggressive") {
  $startRate = 50
  $preAllocatedVus = 50
  $maxVus = 800
  $stage1Target = 100
  $stage2Target = 250
  $stage3Target = 500
  $thinkTimeSeconds = 0.1
}

Write-Host "Using load profile: $LoadProfile"

docker run --rm -i `
  -v "${repoRoot}:/work" `
  -w /work `
  -e BASE_URL=$BaseUrl `
  -e SEASON_YEAR=$SeasonYear `
  -e SEARCH_LIMIT=$SearchLimit `
  -e START_RATE=$startRate `
  -e PREALLOCATED_VUS=$preAllocatedVus `
  -e MAX_VUS=$maxVus `
  -e STAGE1_TARGET=$stage1Target `
  -e STAGE1_DURATION=$stage1Duration `
  -e STAGE2_TARGET=$stage2Target `
  -e STAGE2_DURATION=$stage2Duration `
  -e STAGE3_TARGET=$stage3Target `
  -e STAGE3_DURATION=$stage3Duration `
  -e STAGE4_DURATION=$stage4Duration `
  -e THINK_TIME_SECONDS=$thinkTimeSeconds `
  grafana/k6 run k6/scenarios/scenario1-search-and-fetch.js