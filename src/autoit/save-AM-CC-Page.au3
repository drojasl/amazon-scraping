Global $inputFolder = @ScriptDir & "\inputs"
Global $loadWait = 2500
Global $downloadWait = 1000
Global $startTimer = TimerInit()

HotKeySet("^!p", "_PauseExecution") ; Ctrl+Alt+P para pausar la ejecución
HotKeySet("^!x", "_StopExecution") ; Ctrl+Alt+X para detener la ejecución

_LogNow("Hora de Inicio:")

Sleep(2000)
_BackToBrowser()
Local $counter = 1
; 48
While $counter < 35
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

		; Ejecutar solo si estamos antes del minuto 57
		If @MIN >= 57 Then
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
	Local $i = 1
	For $code In $codes
		_BackToBrowser()
		Local $url = "https://www.amazon.com/dp/" & $code
		If $source = 'CC' Then
			$url = "https://camelcamelcamel.com/product/" & $code
		EndIf

		ClipPut($url)
		Send("{F6}")
		Sleep(500)
		Send("^v")
		Sleep(500)
		Send("{Enter}")

		Local $fileName = $code & "-" & $i
		;ClipPut($fileName)
		ClipPut($source)
		Sleep($loadWait)
		ClipPut($source)

		Send("^s")
		Sleep($loadWait)
		Send("^v")
		Sleep(100)
		ClipPut($fileName)
		Send("-")
		Sleep(50)
		ClipPut($fileName)
		Send("^v")
		Sleep(1000)

		Send("{Enter}")
		Sleep(300)
		Send("{LEFT}")
		Sleep(100)
		Send("{Enter}")

		Sleep($downloadWait)
		_LogNow($i & " " & $code)
		$i += 1
	Next
EndFunc

Func _BackToBrowser()
	MouseClick("left", 60, 30)
	Sleep(20)
	Send("{ESC}")
	MouseClick("left", 0, 140)
	Sleep(20)
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

