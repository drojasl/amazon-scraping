Global $stopFlag = False
Global $inputFolder = @ScriptDir & "\inputs"

HotKeySet("^!x", "_StopExecution") ; Ctrl+Alt+X para detener la ejecución

While 1
    If $stopFlag Then
        MsgBox(0, "Info", "Ejecución detenida por el usuario.")
        Exit
    EndIf

    Local $search = FileFindFirstFile($inputFolder & "\*.txt")

    If $search <> -1 Then
		Local $file = FileFindNextFile($search)
		$src = "AZ"
		If StringLeft($file, 3) = "CC-" Then
			$src = "CC"
		EndIf

		Local $filePath = $inputFolder & "\" & $file
		Local $codigos = FileReadToArray($filePath)

		If @error Then
			ConsoleWrite("Error al leer archivo: " & $filePath & @CRLF)
			ContinueLoop
		EndIf

		_Save($codigos, $src)
		
		FileDelete($filePath)

        FileClose($search)
    Else
		MsgBox(0, "Info", "No se encontraron archivos. Esperando 60 segundos...")
        Sleep(60000) ; Esperar 60 segundos
    EndIf
WEnd

Func _Save($codigos, $src)
	Sleep(3000);
	
	For $codigo In $codigos
		If $stopFlag Then
			ExitLoop
		EndIf

		Sleep(500)

		$url = "https://www.amazon.com/dp/" & $codigo
		If $src = 'CC' Then
			$url = "https://camelcamelcamel.com/product/" & $codigo
		EndIf

		ClipPut($url)
		ClipPut($url)
		send("{Esc}")
		Send("{F6}")
		Sleep(1000)
		Send("^v")
		Sleep(1000)
		send("{Enter}")
		
		; Esperar carga
		$file_name = $src & "-" & $codigo
		ClipPut($file_name)
		Sleep(4500)
		ClipPut($file_name)

		; Guardar
		send("{Esc}")
		Send("^s")
		Sleep(3000)
		Send("^v")
		Sleep(1000)
		send("{Enter}")

		; Alert Reemplazar
		Sleep(500)
		send("{Esc}")
		send("{Enter}")
		
		; Esperar descarga
		Sleep(8000)
		send("{Esc}")
		Send("^{TAB}")
    Next

EndFunc   ;==>_Save

Func _StopExecution()
    $stopFlag = True
EndFunc
