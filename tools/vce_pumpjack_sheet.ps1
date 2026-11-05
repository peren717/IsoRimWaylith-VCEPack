# Pumpjack review sheet (user review of the in-game sheet): sprite above the game camera view, rest and top of stroke, then side views with the 1.60 line.
# usage: vce_pumpjack_sheet.ps1 -r <render dir> -tex <tex dir> -out <png>
param([string]$r,[string]$tex,[string]$out)
Add-Type -AssemblyName System.Drawing
$GREEN=[System.Drawing.Color]::FromArgb(107,127,97)
$BACK=[System.Drawing.Color]::FromArgb(32,32,36)
$fname='Microsoft YaHei'
$fT=New-Object System.Drawing.Font($fname,24,[System.Drawing.FontStyle]::Bold)
$fC=New-Object System.Drawing.Font($fname,22,[System.Drawing.FontStyle]::Bold)
$fR=New-Object System.Drawing.Font($fname,18,[System.Drawing.FontStyle]::Bold)
$white=[System.Drawing.Brushes]::White
$CELL=640;$GAP=6;$LW=74;$FRAME=3.9
function Sprite($gfx,$dz,$x,$y){
 $br=New-Object System.Drawing.SolidBrush $GREEN;$gfx.FillRectangle($br,$x,$y,$CELL,$CELL);$br.Dispose()
 $st=$gfx.Save();$gfx.SetClip((New-Object System.Drawing.Rectangle $x,$y,$CELL,$CELL));$gfx.InterpolationMode='HighQualityBicubic';$ppc=$CELL/$FRAME;$sz=3*$ppc
 foreach($it in @(@('DeepchemPumpjack',0),@('DeepchemPumpjack_Pump',$dz),@('DeepchemPumpjack_Bottom',0))){
  $im=[System.Drawing.Image]::FromFile("$tex\$($it[0]).png");$gfx.DrawImage($im,[single]($x+($CELL-$sz)/2),[single]($y+($CELL-$sz)/2-$it[1]*$ppc),[single]$sz,[single]$sz);$im.Dispose() }
 $gfx.Restore($st) }
function Img($gfx,$p,$x,$y){ $im=[System.Drawing.Image]::FromFile($p);$gfx.InterpolationMode='HighQualityBicubic';$gfx.DrawImage($im,$x,$y,$CELL,$CELL);$im.Dispose() }
$TOPH=60;$HEAD=48
$PW=$LW+2*($CELL+$GAP)+10;$PH=$TOPH+$HEAD+2*($CELL+$GAP)+$HEAD+$CELL+14
$bmp=New-Object System.Drawing.Bitmap $PW,$PH;$gfx=[System.Drawing.Graphics]::FromImage($bmp);$gfx.Clear($BACK);$gfx.TextRenderingHint='AntiAliasGridFit'
$gfx.DrawString('抽油机 第二版（红线 = 1.60）',$fT,$white,14,10)
$sf=New-Object System.Drawing.StringFormat;$sf.Alignment='Center'
$y0=$TOPH;$y1=$y0+$HEAD;$y2=$y1+$CELL+$GAP;$y3=$y2+$CELL+$GAP;$y4=$y3+$HEAD
$ground=$y4+$CELL/2+($FRAME/2-0.2)*$CELL/$FRAME
$cols=@(@('最低',0,'pumpjack_rest_game','pumpjack_rest_side','侧面 最低'),@('最高',1.1,'pumpjack_top_game','pumpjack_top_side','侧面 最高'))
for($i=0;$i -lt 2;$i++){ $x=$LW+$i*($CELL+$GAP);$cl=$cols[$i]
 $gfx.DrawString($cl[0],$fC,$white,(New-Object System.Drawing.RectangleF $x,($y0+4),$CELL,42),$sf)
 Sprite $gfx $cl[1] $x $y1
 Img $gfx "$r\$($cl[2]).png" $x $y2
 $gfx.DrawString($cl[4],$fC,$white,(New-Object System.Drawing.RectangleF $x,($y3+4),$CELL,42),$sf)
 Img $gfx "$r\$($cl[3]).png" $x $y4
 $py=[single]($ground-1.60*$CELL/$FRAME);$pen=New-Object System.Drawing.Pen ([System.Drawing.Color]::Red),2;$gfx.DrawLine($pen,$x,$py,$x+$CELL,$py);$pen.Dispose() }
$gfx.DrawString('原版',$fR,$white,6,($y1+$CELL/2-16))
$gfx.DrawString('3D',$fR,$white,16,($y2+$CELL/2-16))
$gfx.DrawString('侧视',$fR,$white,6,($y4+$CELL/2-16))
$bmp.Save($out,[System.Drawing.Imaging.ImageFormat]::Png);$gfx.Dispose();$bmp.Dispose()
