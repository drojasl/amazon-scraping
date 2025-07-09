Global $inputFolder = @ScriptDir & "\inputs"
Local $loadWait = 3000
Local $downloadWait = 7000
Local $startTimer = TimerInit()

; Get initial time
Local $startHour = @HOUR
Local $startMin = @MIN
Local $startSec = @SEC

ConsoleWrite("Hora de Inicio: " & StringFormat("%02d:%02d:%02d", $startHour, $startMin, $startSec) & @CRLF)

Sleep(3000)

Local $counter = 1
While $counter <= 2
	Local $searchHandle = FileFindFirstFile($inputFolder & "\*.txt")

	If $searchHandle <> -1 Then
		Local $fileName = FileFindNextFile($searchHandle)
		ConsoleWrite($counter & " Archivo a procesar: " & $fileName & @CRLF)

		$source = "AZ"
		If StringLeft($fileName, 3) = "CC-" Then
			$source = "CC"
		EndIf

		Local $filePath = $inputFolder & "\" & $fileName
		Local $codes = FileReadToArray($filePath)

		If @error Then
			ConsoleWrite("Error al leer archivo: " & $filePath & @CRLF)
			ContinueLoop
		EndIf

		_Save($codes, $source)

		FileDelete($filePath)
		FileClose($searchHandle)
	Else
		ConsoleWrite("No hay archivos para procesar. Exit")
		MsgBox(0, "Tiempo de ejecución", "No hay archivos para procesar")
		Exit
	EndIf

	$counter += 1
WEnd

Local $elapsed = TimerDiff($startTimer)

; Convert to seconds
Local $totalSeconds = Int($elapsed / 1000)

; Calculate hours, minutes, and seconds
Local $elapsedHours = Int($totalSeconds / 3600)
Local $elapsedMinutes = Int(Mod($totalSeconds, 3600) / 60)
Local $elapsedSeconds = Mod($totalSeconds, 60)

; Get end time
Local $endHour = @HOUR
Local $endMin = @MIN
Local $endSec = @SEC

; Show result
ConsoleWrite("FIN -> Tiempo transcurrido: " & $elapsedHours & "h " & $elapsedMinutes & "m " & $elapsedSeconds & "s" & @CRLF)
ConsoleWrite("Hora de finalizacion: " & StringFormat("%02d:%02d:%02d", $endHour, $endMin, $endSec) & @CRLF)
Exit

Func _Save($codes, $source)
	Local $i = 1
	For $code In $codes
		Sleep(500)
		MouseClick("left", 0, 0)

		$url = "https://www.amazon.com/dp/" & $code
		If $source = 'CC' Then
			$url = "https://camelcamelcamel.com/product/" & $code
		EndIf

		ClipPut($url)
		ClipPut($url)
		Send("{Esc}")
		Send("{F6}")
		Sleep(500)
		MouseClick("left", 0, 0)
		Send("^v")
		Sleep(500)
		Send("{Enter}")

		; Wait for page load
		$fileName = $source & "-" & $code
		ClipPut($fileName)
		Sleep($loadWait)
		MouseClick("left", 0, 0)
		ClipPut($fileName)

		; Save page
		Send("{Esc}")
		Send("^s")
		Sleep(2000)
		MouseClick("left", 0, 0)
		Send("^v")
		Sleep(3000)
		MouseClick("left", 0, 0)
		Send("{Enter}")

		; Confirm overwrite alert
		Sleep(500)
		Send("{Esc}")
		Send("{Enter}")

		; Wait for download
		Sleep($downloadWait)
		ConsoleWrite($i & " " & $code & @CRLF)
		MouseClick("left", 0, 0)
		Send("{Esc}")
		Send("^{TAB}")
		$i += 1
	Next
EndFunc   ;==>_Save
