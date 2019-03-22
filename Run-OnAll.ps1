<#
Project Run-OnAll
Version 0.0.0b

Description: The script run someone on all accesseble computers

Konstantin Tornovskiy (c) Dec 2016
coolship@yandex.ru
#>

# Функция проверки доступности хостов
function Check-Online {
param($computername)
test-connection -count 1 -ComputerName $computername -TimeToLive 5 -asJob |
Wait-Job |
Receive-Job |
Where-Object { $_.StatusCode -eq 0 } |
Select-Object -ExpandProperty Address
}

$ips = 1..255 | ForEach-Object { "10.61.44.$_" }
$online = Check-Online -computername $ips
$ips = 1..255 | ForEach-Object { "10.61.45.$_" }
$online = $online + (Check-Online -computername $ips)
$ips = 1..255 | ForEach-Object { "10.61.46.$_" }
$online = $online + (Check-Online -computername $ips)
$ips = 1..255 | ForEach-Object { "10.61.47.$_" }
$online = $online + (Check-Online -computername $ips)
$online

$online_count = $online.Length - 1
$lo = 0

while ($lo -lt $online_count){

	# get hostname by IP
	$result = [System.Net.Dns]::gethostentry($online[$lo])

	#################################
	## Run someone on $online[$lo] ##
	#################################

	Invoke-Command -ComputerName $result.hostname -ScriptBlock { Start-Process -FilePath "C:\Program Files (x86)\Crypto Pro\CSP\cpverify.exe" -ArgumentList "-rm", "system"}
		
	$lo++
}