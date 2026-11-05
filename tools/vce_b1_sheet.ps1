# One-page review sheet of batch B1 (the user reviews on a phone): per block the mod's sprite directly above the model at the game camera,
# one shape or state per column, 4 columns, Chinese labels. Also a full check sheet (more angles, top-down overlay on the art, height lines).
# usage: vce_b1_sheet.ps1 -r <render dir> -tex <tex dir> -out <one-page png> [-check <check png>] [-v v1]
param([string]$r,[string]$tex,[string]$out,[string]$check='',[string]$title='Vanilla Chemfuel Expanded  3D 模型 第一批')
Add-Type -AssemblyName System.Drawing
$GREEN=[System.Drawing.Color]::FromArgb(107,127,97)
$BG=[System.Drawing.Color]::FromArgb(32,32,36)
$font='Microsoft YaHei'
$fT=New-Object System.Drawing.Font($font,26,[System.Drawing.FontStyle]::Bold)
$fC=New-Object System.Drawing.Font($font,20,[System.Drawing.FontStyle]::Bold)
$fR=New-Object System.Drawing.Font($font,18,[System.Drawing.FontStyle]::Bold)
$white=[System.Drawing.Brushes]::White
$CELL=420;$GAP=6;$LW=74
function Sprite($g,$items,$x,$y,$sz,$frame){
 # items: @(name, wCells, hCells, dzCells) drawn in order, centred
 $b=New-Object System.Drawing.SolidBrush $GREEN;$g.FillRectangle($b,$x,$y,$sz,$sz);$b.Dispose()
 $st=$g.Save();$g.SetClip((New-Object System.Drawing.Rectangle $x,$y,$sz,$sz));$g.InterpolationMode='HighQualityBicubic'
 $ppc=$sz/$frame
 foreach($it in $items){ $im=[System.Drawing.Image]::FromFile("$tex\$($it[0]).png");$w=$it[1]*$ppc;$h=$it[2]*$ppc
  $g.DrawImage($im,[single]($x+($sz-$w)/2),[single]($y+($sz-$h)/2-$it[3]*$ppc),[single]$w,[single]$h);$im.Dispose() }
 $g.Restore($st) }
function Img($g,$p,$x,$y,$sz){ if(Test-Path $p){$im=[System.Drawing.Image]::FromFile($p);$g.InterpolationMode='HighQualityBicubic';$g.DrawImage($im,$x,$y,$sz,$sz);$im.Dispose()}else{Write-Warning "missing $p"} }

$pumpRest=@(@('DeepchemPumpjack',3,3,0),@('DeepchemPumpjack_Pump',3,3,0),@('DeepchemPumpjack_Bottom',3,3,0))
$pumpTop=@(@('DeepchemPumpjack',3,3,0),@('DeepchemPumpjack_Pump',3,3,1.1),@('DeepchemPumpjack_Bottom',3,3,0))
$blocks=@(
 @{name='储罐';cols=@(
  @{t='化学燃料罐 朝北';s=@(,@('ChemfuelTank_north',2,3,0));f=3.9;m='tank_chem_N'},
  @{t='化学燃料罐 朝东';s=@(,@('ChemfuelTank_east',3,2,0));f=3.9;m='tank_chem_E'},
  @{t='深层化学物罐 朝北';s=@(,@('DeepchemTank_north',2,3,0));f=3.9;m='tank_deep_N'},
  @{t='深层化学物罐 朝东';s=@(,@('DeepchemTank_east',3,2,0));f=3.9;m='tank_deep_E'})},
 @{name='出料 进料';cols=@(
  @{t='化学燃料出料口';s=@(,@('ChemfuelTap',1,1,0));f=1.5;m='tap_chem'},
  @{t='深层化学物出料口';s=@(,@('DeepchemTap',1,1,0));f=1.5;m='tap_deep'},
  @{t='化学燃料进料口';s=@(,@('ChemfuelDrain',1,1,0));f=1.5;m='drain_chem'},
  @{t='深层化学物进料口';s=@(,@('DeepchemDrain',1,1,0));f=1.5;m='drain_deep'})},
 @{name='阀门';cols=@(
  @{t='化学燃料阀 开';s=@(,@('ChemfuelValve',1,1,0));f=1.5;m='valve_chem_on'},
  @{t='化学燃料阀 关';s=@(,@('ChemfuelValve_Off',1,1,0));f=1.5;m='valve_chem_off'},
  @{t='深层化学物阀 开';s=@(,@('DeepchemValve',1,1,0));f=1.5;m='valve_deep_on'},
  @{t='深层化学物阀 关';s=@(,@('DeepchemValve_Off',1,1,0));f=1.5;m='valve_deep_off'})},
 @{name='大型';cols=@(
  @{t='精炼厂';s=@(,@('DeepchemRefinery',3,3,0));f=3.9;m='refinery'},
  @{t='抽油机 最低';s=$pumpRest;f=3.9;m='pumpjack_rest'},
  @{t='抽油机 最高';s=$pumpTop;f=3.9;m='pumpjack_top'},
  @{t='深层化学物 物品';s=@(,@('Deepchem',0.85,0.85,0));f=1.0;m='item'})}
)
$PW=$LW+4*($CELL+$GAP)+10;$TOPH=66;$HEAD=46;$PH=$TOPH+$blocks.Count*($HEAD+2*($CELL+$GAP)+14)
$bmp=New-Object System.Drawing.Bitmap $PW,$PH;$g=[System.Drawing.Graphics]::FromImage($bmp);$g.Clear($BG);$g.TextRenderingHint='AntiAliasGridFit'
$g.DrawString($title,$fT,$white,14,10)
$y=$TOPH
foreach($b in $blocks){
 for($i=0;$i -lt 4;$i++){ $x=$LW+$i*($CELL+$GAP);$cl=$b.cols[$i]
  $sf=New-Object System.Drawing.StringFormat;$sf.Alignment='Center'
  $g.DrawString($cl.t,$fC,$white,(New-Object System.Drawing.RectangleF $x,($y+4),$CELL,40),$sf)
  Sprite $g $cl.s $x ($y+$HEAD) $CELL $cl.f
  Img $g "$r\$($cl.m)_game.png" $x ($y+$HEAD+$CELL+$GAP) $CELL }
 $g.DrawString("原版",$fR,$white,6,($y+$HEAD+$CELL/2-16))
 $g.DrawString("3D",$fR,$white,16,($y+$HEAD+$CELL+$GAP+$CELL/2-16))
 $y+=$HEAD+2*($CELL+$GAP)+14 }
$bmp.Save($out,[System.Drawing.Imaging.ImageFormat]::Png)
# JPEG halves for the phone
$half=$TOPH+2*($HEAD+2*($CELL+$GAP)+14)
$enc=[System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders()|?{$_.MimeType -eq 'image/jpeg'}
$ep=New-Object System.Drawing.Imaging.EncoderParameters 1;$ep.Param[0]=[System.Drawing.Imaging.EncoderParameter]::new([System.Drawing.Imaging.Encoder]::Quality,[long]90)
$base=[IO.Path]::Combine([IO.Path]::GetDirectoryName($out),[IO.Path]::GetFileNameWithoutExtension($out))
$p1=$bmp.Clone((New-Object System.Drawing.Rectangle 0,0,$PW,$half),$bmp.PixelFormat);$p1.Save("${base}_part1.jpg",$enc,$ep);$p1.Dispose()
$p2=$bmp.Clone((New-Object System.Drawing.Rectangle 0,$half,$PW,($PH-$half)),$bmp.PixelFormat);$p2.Save("${base}_part2.jpg",$enc,$ep);$p2.Dispose()
$g.Dispose();$bmp.Dispose()

if($check){
 # check sheet: each row a shape, columns game, turned 45, back, front (red 1.60, cyan 1.65 lines), side, top, top over art 50 %, play size
 $rows=@(
  @{m='tank_chem_N';art='ChemfuelTank_north';w=2;h=3;f=3.9},@{m='tank_chem_E';art='ChemfuelTank_east';w=3;h=2;f=3.9},
  @{m='tank_deep_N';art='DeepchemTank_north';w=2;h=3;f=3.9},@{m='tank_deep_E';art='DeepchemTank_east';w=3;h=2;f=3.9},
  @{m='tap_chem';art='ChemfuelTap';w=1;h=1;f=1.5},@{m='drain_deep';art='DeepchemDrain';w=1;h=1;f=1.5},
  @{m='valve_chem_on';art='ChemfuelValve';w=1;h=1;f=1.5},@{m='valve_deep_off';art='DeepchemValve_Off';w=1;h=1;f=1.5},
  @{m='refinery';art='DeepchemRefinery';w=3;h=3;f=3.9},@{m='pumpjack_rest';art='DeepchemPumpjack';w=3;h=3;f=3.9},@{m='pumpjack_top';art='DeepchemPumpjack';w=3;h=3;f=3.9},
  @{m='item';art='Deepchem';w=0.85;h=0.85;f=1.0})
 $c=250;$cols='game','g45','back','front','side','top'
 $PW2=12+($cols.Count+1)*($c+4)+210;$PH2=44+$rows.Count*($c+30)
 $bmp=New-Object System.Drawing.Bitmap $PW2,$PH2;$g=[System.Drawing.Graphics]::FromImage($bmp);$g.Clear($BG);$g.TextRenderingHint='AntiAliasGridFit'
 $fS=New-Object System.Drawing.Font('Segoe UI',12,[System.Drawing.FontStyle]::Bold)
 $g.DrawString('check sheet: game, turned 45, back, front and side (red 1.60, cyan 1.65), top, top over the art 50%, play size (50 px a cell)',$fS,$white,10,10)
 $y=40
 foreach($row in $rows){ $g.DrawString($row.m,$fS,$white,10,$y);$y+=24;$x=10
  foreach($v in $cols){ Img $g "$r\$($row.m)_$v.png" $x $y $c
   if($v -eq 'front' -or $v -eq 'side'){ $ppc=$c/$row.f; $base=$y+$c-($row.f/2-($row.f/2-0.2))*0 ; $yc=$row.f/2-0.2; $ground=$y+$c/2+$yc*$ppc
    foreach($ln in @(@(1.60,[System.Drawing.Color]::Red),@(1.65,[System.Drawing.Color]::Cyan))){ $py=$ground-$ln[0]*$ppc; if($py -gt $y){$pen=New-Object System.Drawing.Pen $ln[1];$g.DrawLine($pen,$x,[single]$py,$x+$c,[single]$py);$pen.Dispose()} } }
   $x+=$c+4 }
  # overlay: art, then the top view at half strength
  $b=New-Object System.Drawing.SolidBrush $GREEN;$g.FillRectangle($b,$x,$y,$c,$c);$b.Dispose()
  $im=[System.Drawing.Image]::FromFile("$tex\$($row.art).png");$ppc=$c/$row.f;$w=$row.w*$ppc;$h=$row.h*$ppc
  $g.DrawImage($im,[single]($x+($c-$w)/2),[single]($y+($c-$h)/2),[single]$w,[single]$h);$im.Dispose()
  $im=[System.Drawing.Image]::FromFile("$r\$($row.m)_top.png");$cm=New-Object System.Drawing.Imaging.ColorMatrix;$cm.Matrix33=0.5;$ia=New-Object System.Drawing.Imaging.ImageAttributes;$ia.SetColorMatrix($cm)
  $g.DrawImage($im,(New-Object System.Drawing.Rectangle $x,$y,$c,$c),0,0,$im.Width,$im.Height,[System.Drawing.GraphicsUnit]::Pixel,$ia);$im.Dispose()
  $x+=$c+4
  $g.InterpolationMode='NearestNeighbor';$im=[System.Drawing.Image]::FromFile("$r\$($row.m)_play.png");$g.DrawImage($im,$x,$y,$im.Width,$im.Height);$im.Dispose()
  $y+=$c+6 }
 $bmp.Save($check,[System.Drawing.Imaging.ImageFormat]::Png);$g.Dispose();$bmp.Dispose()
}
