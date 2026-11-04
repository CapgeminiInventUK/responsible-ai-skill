# Builds responsible-ai-skill.zip with skill files at the zip root (no wrapper folder).
$root = $PSScriptRoot
$zipPath = Join-Path $root 'responsible-ai-skill.zip'
$exclude = '^(\.git|dist)(/|$)|^responsible-ai-skill\.zip$|^build-zip\.ps1$'

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
if (Test-Path $zipPath) { Remove-Item $zipPath }

$zip = [IO.Compression.ZipFile]::Open($zipPath, 'Create')
try {
    Get-ChildItem $root -Recurse -File -Force | ForEach-Object {
        $rel = $_.FullName.Substring($root.Length + 1).Replace('\', '/')
        if ($rel -notmatch $exclude) {
            [void][IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip, $_.FullName, $rel)
        }
    }
} finally { $zip.Dispose() }
Write-Host "Created $zipPath"
