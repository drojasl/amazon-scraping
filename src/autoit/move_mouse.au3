Global $stopFlag = False
HotKeySet("^!x", "_StopExecution") ; Ctrl+Alt+X para detener la ejecución

ConsoleWrite("Mensaje en consola" & @CRLF)
While 1
    If $stopFlag Then
        MsgBox(0, "Info", "Ejecución detenida por el usuario.")
        Exit
    EndIf

    MouseMove(100, 100, 0)
    MouseMove(200, 200, 5)

    Sleep(600000) ; Esperar 60 segundos
WEnd

Func _StopExecution()
    $stopFlag = True
EndFunc
