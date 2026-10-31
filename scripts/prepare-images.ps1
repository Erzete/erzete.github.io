# Optional Windows asset helper. Originals are preserved; generated files are committed.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$projectRoot = Split-Path -Parent $PSScriptRoot
$thumbDirectory = Join-Path $projectRoot 'img/thumbs'
New-Item -ItemType Directory -Path $thumbDirectory -Force | Out-Null
$projects = Get-Content -LiteralPath (Join-Path $projectRoot 'content/projects.json') -Raw | ConvertFrom-Json
foreach ($project in $projects) {
    if (-not $project.thumbnail) { continue }
    $sourcePath = Join-Path $projectRoot $project.gallery[0].src
    $outputPath = Join-Path $projectRoot $project.thumbnail
    $sourceImage = [System.Drawing.Image]::FromFile($sourcePath)
    try {
        $targetWidth = [Math]::Min(900, $sourceImage.Width)
        $targetHeight = [int][Math]::Round($sourceImage.Height * $targetWidth / $sourceImage.Width)
        $thumbnail = New-Object System.Drawing.Bitmap($targetWidth, $targetHeight)
        $drawing = [System.Drawing.Graphics]::FromImage($thumbnail)
        try {
            $drawing.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $drawing.Clear([System.Drawing.Color]::White)
            $drawing.DrawImage($sourceImage, 0, 0, $targetWidth, $targetHeight)
            $thumbnail.Save($outputPath, [System.Drawing.Imaging.ImageFormat]::Png)
        } finally { $drawing.Dispose(); $thumbnail.Dispose() }
    } finally { $sourceImage.Dispose() }
}

# A raster social preview for platforms that do not accept SVG metadata images.
$preview = New-Object System.Drawing.Bitmap(1200, 630)
$canvas = [System.Drawing.Graphics]::FromImage($preview)
$canvas.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$canvas.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$background = [System.Drawing.ColorTranslator]::FromHtml('#faf9f6')
$ink = New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml('#282c29'))
$accent = New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml('#a5452f'))
$muted = New-Object System.Drawing.SolidBrush([System.Drawing.ColorTranslator]::FromHtml('#636760'))
$line = New-Object System.Drawing.Pen([System.Drawing.ColorTranslator]::FromHtml('#dedfd7'))
$titleFont = New-Object System.Drawing.Font('Georgia', 64, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
$italicFont = New-Object System.Drawing.Font('Georgia', 80, [System.Drawing.FontStyle]::Italic, [System.Drawing.GraphicsUnit]::Pixel)
$smallFont = New-Object System.Drawing.Font('Segoe UI', 21, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
try {
    $canvas.Clear($background)
    $canvas.DrawLine($line, 75, 80, 1125, 80)
    $canvas.DrawLine($line, 75, 540, 1125, 540)
    $canvas.DrawString('RAMA TRIDIGDAYA / IT ENGINEER', $smallFont, $accent, 75, 120)
    $canvas.DrawString('Making systems', $titleFont, $ink, 70, 225)
    $canvas.DrawString('work together.', $italicFont, $accent, 70, 310)
    $canvas.DrawString('Backend / ERP / Integrations', $smallFont, $muted, 75, 470)
    $canvas.DrawString('erzete.github.io', $smallFont, $muted, 940, 570)
    $preview.Save((Join-Path $projectRoot 'img/social-preview.png'), [System.Drawing.Imaging.ImageFormat]::Png)
} finally {
    $canvas.Dispose(); $preview.Dispose(); $ink.Dispose(); $accent.Dispose(); $muted.Dispose()
    $line.Dispose(); $titleFont.Dispose(); $italicFont.Dispose(); $smallFont.Dispose()
}
Write-Output 'Prepared four lightweight thumbnails and social preview.'
