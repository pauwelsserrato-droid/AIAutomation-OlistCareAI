param(
    [Parameter(Mandatory = $true)]
    [string]$WebhookUrl
)

$ErrorActionPreference = "Continue"
$payloadDirectory = Join-Path $PSScriptRoot "..\tests\payloads"
$payloads = Get-ChildItem -LiteralPath $payloadDirectory -Filter "*.json" | Sort-Object Name

foreach ($payload in $payloads) {
    Write-Host "Ejecutando $($payload.Name)" -ForegroundColor Cyan
    $body = Get-Content -LiteralPath $payload.FullName -Raw
    try {
        $response = Invoke-WebRequest -Uri $WebhookUrl -Method Post -ContentType "application/json" -Body $body
        Write-Host "HTTP $($response.StatusCode) $($response.Content)" -ForegroundColor Green
    }
    catch {
        if ($_.Exception.Response) {
            $status = [int]$_.Exception.Response.StatusCode
            Write-Host "HTTP $status - respuesta esperada para un camino de validacion o error" -ForegroundColor Yellow
        }
        else {
            Write-Host $_.Exception.Message -ForegroundColor Red
        }
    }
    Write-Host "Revisar n8n, Airtable y Slack antes de continuar con el siguiente caso."
    Read-Host "Presionar Enter para continuar"
}
