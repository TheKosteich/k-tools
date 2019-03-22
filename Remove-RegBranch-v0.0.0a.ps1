<#
Project Remove-RegBranch
Version 0.0.0a

Description: The script for delete remote registry branch on multiple computers

Konstantin Tornovskiy (c) Dec 2016
coolship@yandex.ru
#>

# Скрипт для автоматического удаления веток реестра на компьютерах
# При выполнение происходит проверка доступности хостов


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
	# Find service RemoteRegistry. If it is stopped than run this service
	Get-Service RemoteRegistry -ComputerName $online[$lo] | where {$_.status -eq 'stopped'} | Set-Service -Status Running
	
	# Wait service running
	Start-Sleep -Seconds 5
	
	# Remove registry key
	reg delete \\CompName\hklm\SOFTWARE\Microsoft\Cryptography\Calais\SmartCards\eToken_JAVA_10b_Default /f
	reg delete \\CompName\hklm\SOFTWARE\Microsoft\Cryptography\Calais\SmartCards\eToken_JAVA_10_Default /f
	reg delete \\CompName\hklm\SOFTWARE\Microsoft\Cryptography\Calais\SmartCards\eToken_PRO_M420b_Default /f
	reg delete \\CompName\hklm\SOFTWARE\Microsoft\Cryptography\Calais\SmartCards\eToken_PRO32_Default /f
	reg delete \\CompName\hklm\SOFTWARE\Microsoft\Cryptography\Calais\SmartCards\eToken_R2_Default /f
	
	# Stop RemoteRegistry service after redistry branch delete
	(get-service -ComputerName $online[$lo] -Name RemoteRegistry).Stop()
	
	$lo++
}