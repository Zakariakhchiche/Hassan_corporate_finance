Add-Type -AssemblyName System.Windows.Forms
$Screen = [System.Windows.Forms.Screen]::PrimaryScreen
$Width  = $Screen.Bounds.Width
$Height = $Screen.Bounds.Height
$Left   = $Screen.Bounds.Left
$Top    = $Screen.Bounds.Top
$Bitmap = New-Object System.Drawing.Bitmap $Width, $Height
$Graphic = [System.Drawing.Graphics]::FromImage($Bitmap)
$Graphic.CopyFromScreen($Left, $Top, 0, 0, $Bitmap.Size)
$Bitmap.Save("C:\Users\zkhch\.openclaw\workspace\screen.png")
$Graphic.Dispose()
$Bitmap.Dispose()
