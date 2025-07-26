Global $inputFolder = @ScriptDir & "\inputs"
Global $loadWait = 1950
Global $downloadWait = 400
Global $startTimer = TimerInit()

HotKeySet("^!p", "_PauseExecution") ; Ctrl+Alt+P para pausar la ejecución
HotKeySet("^!x", "_StopExecution") ; Ctrl+Alt+X para detener la ejecución

_LogNow("Hora de Inicio:")

Sleep(2000)

Local $counter = 1
While $counter <= 1
	Send("{ESC}")
	Local $searchHandle = FileFindFirstFile($inputFolder & "\*.txt")

	If $searchHandle <> -1 Then
		Local $fileName = FileFindNextFile($searchHandle)

		Local $source = "AZ"
		If StringLeft($fileName, 3) = "CC-" Then
			$source = "CC"
		EndIf

		Local $filePath = $inputFolder & "\" & $fileName
		Local $codes = FileReadToArray($filePath)

		If @error Then
			_LogNow("Error al leer archivo: " & $filePath)
			ContinueLoop
		EndIf

		; Ejecutar solo si estamos antes del minuto 48
		If @MIN >= 48 Then
			_LogNow("Muy cerca de la siguiente ejecucion automatica")
			_LogEnd()
			Exit
		EndIf

		_LogNow($counter & " Archivo a procesar: " & $fileName)
		_Save($codes, $source)

		FileDelete($filePath)
		FileClose($searchHandle)
		_LogNow($counter & " Archivo procesado: " & $fileName)
	Else
		_LogNow("No hay archivos para procesar. Exit")
		_LogEnd()
		Exit
	EndIf

	$counter += 1
WEnd

_LogEnd()
Exit

;--------------------------------------------
Func _LogNow($msn)
	Local $h = @HOUR, $m = @MIN, $s = @SEC
	ConsoleWrite($msn & " " & StringFormat("%02d:%02d:%02d", $h, $m, $s) & @CRLF)
EndFunc

Func _LogEnd()
	Local $elapsed = TimerDiff($startTimer)
	Local $totalSeconds = Int($elapsed / 1000)

	Local $h = Int($totalSeconds / 3600)
	Local $m = Int(Mod($totalSeconds, 3600) / 60)
	Local $s = Mod($totalSeconds, 60)

	Local $endH = @HOUR, $endM = @MIN, $endS = @SEC

	_LogNow("FIN -> Tiempo transcurrido: " & $h & "h " & $m & "m " & $s & "s")
	ConsoleWrite("Hora de finalizacion: " & StringFormat("%02d:%02d:%02d", $endH, $endM, $endS) & @CRLF)
EndFunc

;--------------------------------------------
Func _Save($codes, $source)
	_ValidateDownloadsFolder()
	Local $i = 1
	For $code In $codes
		Sleep(400)

		Local $url = "https://www.amazon.com/dp/" & $code
		If $source = 'CC' Then
			$url = "https://camelcamelcamel.com/product/" & $code
		EndIf

		ClipPut($url)
		Send("{F6}")
		Sleep(500)
		Send("^v")
		Sleep(400)
		Send("{Enter}")

		Local $fileName = $source & "-" & $code & "-" & $i
		ClipPut($fileName)
		Sleep($loadWait)
		ClipPut($fileName)

		Send("^s")
		Sleep($loadWait)
		Send("^v")
		Sleep(600)
		
		If $i = 1 Then
			Send("{TAB}")
			Sleep(300)
    		Send("{DOWN}")
			Sleep(200)
    		Send("{DOWN}")
			Sleep(200)
    		Send("{DOWN}")
			Sleep(200)
    		Send("{DOWN}")
			Sleep(300)
    		Send("{UP}")
			Sleep(300)
			Send("{Enter}")
			Sleep(300)
		EndIf

		Send("{Enter}")
		Sleep(300)
		Send("{LEFT}")
		Sleep(100)
		Send("{Enter}")

		Sleep($downloadWait)
		_LogNow($i & " " & $code)
		_BackToBrowser()
		Send("^{TAB}")
		$i += 1
	Next
EndFunc

Func _ValidateDownloadsFolder()
	_BackToBrowser()
	Local $url = "chrome://settings/downloads"
	ClipPut($url)
	Send("{F6}")
	Sleep(1000)
	Send("^v")
	Sleep(500)
	Send("{Enter}")
	Sleep(2000)
	Send("{TAB}")
	Sleep(500)
	Send("{TAB}")
	Sleep(500)
	Send("{Enter}")
	Sleep(2000)
	Send("{Enter}")
EndFunc

Func _BackToBrowser()
	MouseClick("left", 0, 140)
	Sleep(50)
EndFunc

Func _StopExecution()
	_LogEnd()
    MsgBox(0, "Info", "Ejecución detenida por el usuario.")
	Exit
EndFunc

Func _PauseExecution()
	_LogNow("Ejecucion Pausada")
    MsgBox(0, "Pausa", "Presiona OK para continuar.")
	_BackToBrowser()
EndFunc

