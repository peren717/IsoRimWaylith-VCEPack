# Review sheet of round 2 (user review 1): the refinery and the deep tank only. Sprite directly above the game camera view, then side views
# with the 1.60 storey line. Chinese labels, for a phone.
# usage: vce_b1_sheet_v2.ps1 -r <render dir> -tex <tex dir> -out <png>
param([string]$r,[string]$tex,[string]$out)
Add-Type -AssemblyName System.Drawing
$GREEN=[System.Drawing.Color]::FromArgb(107,127,97)
$BACK=[System.Drawing.Color]::FromArgb(32,32,36)
$fname='Microsoft YaHei'
$fT=New-Object System.Drawing.Font($fname,26,[System.Drawing.FontStyle]::Bold)
$fC=New-Object System.Drawing.Font($fname,22,[System.Drawing.FontStyle]::Bold)
$fR=New-Object System.Drawing.Font($fname,18,[System.Drawing.FontStyle]::Bold)
$white=[System.Drawing.Brushes]::White
$CELL=550;$GAP=6;$LW=74;$FRAME=3.9
function Sprite($gfx,$name,$w,$h,$x,$y){
 $br=New-Object System.Drawing.SolidBrush $GREEN;$gfx.FillRectangle($br,$x,$y,$CELL,$CELL);$br.Dispose()
 $gfx.InterpolationMode='HighQualityBicubic';$ppc=$CELL/$FRAME
 $im=[System.Drawing.Image]::FromFile("$tex\$name.png")
 $gfx.DrawImage($im,[single]($x+($CELL-$w*$ppc)/2),[single]($y+($CELL-$h*$ppc)/2),[single]($w*$ppc),[single]($h*$ppc));$im.Dispose() }
function Img($gfx,$p,$x,$y){ $im=[System.Drawing.Image]::FromFile($p);$gfx.InterpolationMode='HighQualityBicubic';$gfx.DrawImage($im,$x,$y,$CELL,$CELL);$im.Dispose() }
$cols=@(
 @{t='精炼厂';a='DeepchemRefinery';w=3;h=3;m='refinery_game';s='refinery_front';st='精炼厂 正面'},
 @{t='深层化学物罐 朝北';a='DeepchemTank_north';w=2;h=3;m='tank_deep_N_game';s='tank_deep_N_front';st='储罐 端面'},
 @{t='深层化学物罐 朝东';a='DeepchemTank_east';w=3;h=2;m='tank_deep_E_game';s='tank_deep_N_side';st='储罐 侧面'})
$TOPH=66;$HEAD=48
$PW=$LW+3*($CELL+$GAP)+10;$PH=$TOPH+$HEAD+2*($CELL+$GAP)+$HEAD+$CELL+14
$bmp=New-Object System.Drawing.Bitmap $PW,$PH;$gfx=[System.Drawing.Graphics]::FromImage($bmp);$gfx.Clear($BACK);$gfx.TextRenderingHint='AntiAliasGridFit'
$gfx.DrawString('Vanilla Chemfuel Expanded  3D 模型 第二轮（红线 = 1.60 层高）',$fT,$white,14,10)
$sf=New-Object System.Drawing.StringFormat;$sf.Alignment='Center'
$y0=$TOPH;$y1=$y0+$HEAD;$y2=$y1+$CELL+$GAP;$y3=$y2+$CELL+$GAP;$y4=$y3+$HEAD
$ground=$y4+$CELL/2+($FRAME/2-0.2)*$CELL/$FRAME
for($i=0;$i -lt 3;$i++){ $x=$LW+$i*($CELL+$GAP);$cl=$cols[$i]
 $gfx.DrawString($cl.t,$fC,$white,(New-Object System.Drawing.RectangleF $x,($y0+4),$CELL,42),$sf)
 Sprite $gfx $cl.a $cl.w $cl.h $x $y1
 Img $gfx "$r\$($cl.m).png" $x $y2
 $gfx.DrawString($cl.st,$fC,$white,(New-Object System.Drawing.RectangleF $x,($y3+4),$CELL,42),$sf)
 Img $gfx "$r\$($cl.s).png" $x $y4
 $py=[single]($ground-1.60*$CELL/$FRAME);$pen=New-Object System.Drawing.Pen ([System.Drawing.Color]::Red),2;$gfx.DrawLine($pen,$x,$py,$x+$CELL,$py);$pen.Dispose() }
$gfx.DrawString('原版',$fR,$white,6,($y1+$CELL/2-16))
$gfx.DrawString('3D',$fR,$white,16,($y2+$CELL/2-16))
$gfx.DrawString('侧视',$fR,$white,6,($y4+$CELL/2-16))
$bmp.Save($out,[System.Drawing.Imaging.ImageFormat]::Png);$gfx.Dispose();$bmp.Dispose()
