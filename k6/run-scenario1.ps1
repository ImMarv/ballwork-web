param(
    [string]$BaseUrl = "http://host.docker.internal:8080",
    [string]$SeasonYear = "2023",
    [int]$SearchLimit = 10
)

$workspace = Resolve-Path "$PSScriptRoot\.."

Write-Host "Running Scenario 1 against $BaseUrl"

docker run --rm -i `
  -v "${PWD}:/work" `
  -w /work `
  -e BASE_URL=http://host.docker.internal:8080 `
  -e START_RATE=2 `
  -e PREALLOCATED_VUS=10 `
  -e MAX_VUS=30 `
  -e STAGE1_TARGET=5 -e STAGE1_DURATION=1m `
  -e STAGE2_TARGET=15 -e STAGE2_DURATION=2m `
  -e STAGE3_TARGET=25 -e STAGE3_DURATION=2m `
  -e STAGE4_DURATION=30s `
  -e THINK_TIME_SECONDS=0.8 `
  grafana/k6 run k6/scenarios/scenario1-search-and-fetch.js