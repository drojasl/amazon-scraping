Sleep(1000)
MouseClick("left", 460, 800)
MouseClick("left", 460, 800)
Sleep(2000)
MouseClick("left", 460, 170)
Sleep(2000)
MouseClick("left", 600, 170)
Sleep(500)
Send("{END}")
	
Local $i = 1
While $i <= 25
    Sleep(500)
    Send("{F2}")
	Sleep(500)
	Send("{F2}")
    Sleep(1000)
    Send("^c")

    ; Espera un momento para que el portapapeles se actualice
    Sleep(500)

    ; Obtiene el texto del portapapeles
    $copiedText = ClipGet()

    ; Evalúa si el texto comienza con "AZ-" o "CC-"
    If StringLeft($copiedText, 3) = "AZ-" Or StringLeft($copiedText, 3) = "CC-" Or StringLeft($copiedText, 3) = "123" Or @MIN = 0 Then
		Send("{ESC}")
        ExitLoop
    EndIf

    Send("123"& $i)
	Sleep(1000)
	Send("{Enter}")
	Sleep(1000)
	Send("{Enter}")
	Sleep(1000)
	Send("{up}")
	$i += 1
Wend