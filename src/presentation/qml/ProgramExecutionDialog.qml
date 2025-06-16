import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    id: executionDialog
    
    property var programData: null
    property bool isExecuting: false
    property string currentPhase: "setup"
    property bool hasAlarm: false
    property string alarmType: ""
    
    signal executionRequested(int programId)
    signal stopRequested()
    
    anchors.centerIn: parent
    width: Math.min(800, parent.width * 0.95)  // Más ancho para incluir gauge
    height: Math.min(600, parent.height * 0.9)
    
    title: isExecuting ? "Programa en Ejecución" : "Ejecutar Programa"
    modal: true
    
    // No permitir cerrar si hay programa en ejecución
    closePolicy: isExecuting ? Popup.NoAutoClose : Popup.CloseOnEscape | Popup.CloseOnPressOutside
    
    background: Rectangle {
        color: "#ECF0F1"
        radius: 12
        border.color: hasAlarm && alarmType === "red" ? "#E74C3C" : "#3498DB"
        border.width: hasAlarm && alarmType === "red" ? 4 : 2
        
        // Efecto de parpadeo para alarma roja
        SequentialAnimation on border.color {
            running: hasAlarm && alarmType === "red"
            loops: Animation.Infinite
            
            ColorAnimation {
                to: "#FF0000"
                duration: 500
            }
            ColorAnimation {
                to: "#E74C3C"
                duration: 500
            }
        }
    }
    
    RowLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20
        
        // Panel izquierdo - Información y controles
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 15
            
            // Información del programa
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 120
                color: "#FFFFFF"
                radius: 10
                border.color: "#BDC3C7"
                border.width: 1
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 8
                    
                    Text {
                        text: programData ? programData.name : ""
                        font.pixelSize: 18
                        font.bold: true
                        color: "#2C3E50"
                        Layout.fillWidth: true
                    }
                    
                    Text {
                        text: programData ? programData.description : ""
                        font.pixelSize: 12
                        color: "#7F8C8D"
                        Layout.fillWidth: true
                        wrapMode: Text.WordWrap
                        visible: text !== ""
                    }
                    
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 20
                        
                        Column {
                            spacing: 2
                            
                            Text {
                                text: "Presión"
                                font.pixelSize: 10
                                color: "#95A5A6"
                                font.bold: true
                            }
                            
                            Text {
                                text: programData ? 
                                      `${programData.min_pressure} - ${programData.max_pressure} PSI` : ""
                                font.pixelSize: 14
                                color: "#2C3E50"
                                font.bold: true
                            }
                        }
                        
                        Column {
                            spacing: 2
                            
                            Text {
                                text: "Duración"
                                font.pixelSize: 10
                                color: "#95A5A6"
                                font.bold: true
                            }
                            
                            Text {
                                text: programData ? `${programData.program_duration} min` : ""
                                font.pixelSize: 14
                                color: "#2C3E50"
                                font.bold: true
                            }
                        }
                        
                        Column {
                            spacing: 2
                            
                            Text {
                                text: "Setup Max"
                                font.pixelSize: 10
                                color: "#95A5A6"
                                font.bold: true
                            }
                            
                            Text {
                                text: programData ? `${programData.time_to_min_pressure} min` : ""
                                font.pixelSize: 14
                                color: "#2C3E50"
                                font.bold: true
                            }
                        }
                    }
                }
            }
            
            // Estado de ejecución y fase
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                color: _getPhaseColor()
                radius: 10
                border.color: _getPhaseBorderColor()
                border.width: 2
                
                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 15
                    
                    Text {
                        text: _getPhaseIcon()
                        font.pixelSize: 30
                        color: _getPhaseTextColor()
                    }
                    
                    Column {
                        Layout.fillWidth: true
                        spacing: 4
                        
                        Text {
                            text: _getPhaseTitle()
                            font.pixelSize: 16
                            font.bold: true
                            color: _getPhaseTextColor()
                        }
                        
                        Text {
                            text: _getPhaseDescription()
                            font.pixelSize: 12
                            color: _getPhaseTextColor()
                        }
                    }
                }
            }
            
            // Mensaje de alarma (solo visible cuando hay alarma)
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                color: alarmType === "red" ? "#FADBD8" : "#D5F4E6"
                radius: 8
                border.color: alarmType === "red" ? "#E74C3C" : "#27AE60"
                border.width: 2
                visible: hasAlarm
                
                Text {
                    id: alarmMessageText
                    anchors.centerIn: parent
                    text: ""
                    font.pixelSize: 14
                    font.bold: true
                    color: alarmType === "red" ? "#C0392B" : "#27AE60"
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap
                    width: parent.width - 20
                }
            }
            
            // Progreso (visible durante ejecución)
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                color: "#FFFFFF"
                radius: 10
                border.color: "#BDC3C7"
                border.width: 1
                visible: isExecuting
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 15
                    spacing: 8
                    
                    RowLayout {
                        Layout.fillWidth: true
                        
                        Text {
                            text: currentPhase === "setup" ? "Progreso Setup:" : "Progreso Programa:"
                            font.pixelSize: 14
                            color: "#2C3E50"
                            font.bold: true
                        }
                        
                        Text {
                            id: progressText
                            text: "0%"
                            font.pixelSize: 14
                            color: "#3498DB"
                            font.bold: true
                            Layout.fillWidth: true
                            horizontalAlignment: Text.AlignRight
                        }
                    }
                    
                    ProgressBar {
                        id: progressBar
                        Layout.fillWidth: true
                        from: 0
                        to: 100
                        value: 0
                        
                        background: Rectangle {
                            color: "#ECF0F1"
                            radius: 4
                            border.color: "#BDC3C7"
                            border.width: 1
                        }
                        
                        contentItem: Rectangle {
                            width: progressBar.visualPosition * parent.width
                            height: parent.height
                            radius: 4
                            color: currentPhase === "setup" ? "#F39C12" : "#3498DB"
                        }
                    }
                    
                    Text {
                        id: statusText
                        Layout.fillWidth: true
                        text: "Listo para iniciar"
                        font.pixelSize: 11
                        color: "#566573"
                        wrapMode: Text.WordWrap
                    }
                }
            }
            
            // Botones de control
            RowLayout {
                Layout.fillWidth: true
                Layout.topMargin: 10
                spacing: 15
                
                Button {
                    text: "Cerrar"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    enabled: !isExecuting  // Solo habilitado si no hay ejecución
                    
                    background: Rectangle {
                        color: parent.enabled ? 
                               (parent.pressed ? "#95A5A6" : "#BDC3C7") : "#D5DBDB"
                        radius: 8
                        border.color: "#85929E"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.enabled ? parent.text : "No se puede cerrar"
                        color: parent.enabled ? "#2C3E50" : "#7F8C8D"
                        font.pixelSize: 14
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        if (!isExecuting) {
                            executionDialog.close()
                        }
                    }
                }
                
                Button {
                    text: isExecuting ? "Detener Ejecución" : "Iniciar Ejecución"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    
                    background: Rectangle {
                        color: isExecuting ? 
                               (parent.pressed ? "#C0392B" : "#E74C3C") :
                               (parent.pressed ? "#27AE60" : "#2ECC71")
                        radius: 8
                        border.color: isExecuting ? "#A93226" : "#229954"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 16
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        if (isExecuting) {
                            stopRequested()
                        } else {
                            if (programData) {
                                executionRequested(programData.id)
                            }
                        }
                    }
                }
            }
        }
        
        // Panel derecho - Gauge de presión
        Rectangle {
            Layout.preferredWidth: 300
            Layout.fillHeight: true
            color: "#FFFFFF"
            radius: 12
            border.color: "#BDC3C7"
            border.width: 1
            
            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15
                
                Text {
                    text: "Manómetro"
                    font.pixelSize: 16
                    font.bold: true
                    color: "#2C3E50"
                    Layout.alignment: Qt.AlignHCenter
                }
                
                PressureGauge {
                    id: executionGauge
                    Layout.alignment: Qt.AlignHCenter
                    size: 220
                    value: executionController ? executionController.currentPressure : 0
                    minValue: 0
                    maxValue: programData ? Math.max(100, programData.max_pressure * 1.2) : 100
                    
                    // Mostrar zonas de presión del programa
                    property real programMinPressure: programData ? programData.min_pressure : 0
                    property real programMaxPressure: programData ? programData.max_pressure : 100
                }
                
                // Leyenda de presiones
                Column {
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 8
                    
                    Row {
                        spacing: 10
                        anchors.horizontalCenter: parent.horizontalCenter
                        
                        Rectangle {
                            width: 12
                            height: 12
                            color: "#2ECC71"
                            radius: 6
                        }
                        Text {
                            text: `Mínima: ${programData ? programData.min_pressure : 0} PSI`
                            font.pixelSize: 12
                            color: "#2C3E50"
                        }
                    }
                    
                    Row {
                        spacing: 10
                        anchors.horizontalCenter: parent.horizontalCenter
                        
                        Rectangle {
                            width: 12
                            height: 12
                            color: "#E74C3C"
                            radius: 6
                        }
                        Text {
                            text: `Máxima: ${programData ? programData.max_pressure : 100} PSI`
                            font.pixelSize: 12
                            color: "#2C3E50"
                        }
                    }
                    
                    Text {
                        text: `Actual: ${executionController ? executionController.currentPressure.toFixed(1) : "0.0"} PSI`
                        font.pixelSize: 14
                        font.bold: true
                        color: "#3498DB"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }
                }
            }
        }
    }
    
    // Funciones auxiliares para estados
    function _getPhaseColor() {
        if (hasAlarm && alarmType === "red") return "#FADBD8"
        if (hasAlarm && alarmType === "green") return "#D5F4E6"
        
        switch(currentPhase) {
            case "setup": return "#FFF3CD"
            case "running": return "#D1ECF1"
            case "completed": return "#D5F4E6"
            default: return "#F8F9FA"
        }
    }
    
    function _getPhaseBorderColor() {
        if (hasAlarm && alarmType === "red") return "#E74C3C"
        if (hasAlarm && alarmType === "green") return "#27AE60"
        
        switch(currentPhase) {
            case "setup": return "#F39C12"
            case "running": return "#3498DB"
            case "completed": return "#27AE60"
            default: return "#BDC3C7"
        }
    }
    
    function _getPhaseTextColor() {
        if (hasAlarm && alarmType === "red") return "#C0392B"
        if (hasAlarm && alarmType === "green") return "#27AE60"
        
        switch(currentPhase) {
            case "setup": return "#D68910"
            case "running": return "#2471A3"
            case "completed": return "#229954"
            default: return "#566573"
        }
    }
    
    function _getPhaseIcon() {
        if (hasAlarm && alarmType === "red") return "⚠️"
        if (hasAlarm && alarmType === "green") return "✅"
        
        switch(currentPhase) {
            case "setup": return "⏳"
            case "running": return "▶️"
            case "completed": return "✅"
            default: return "⭕"
        }
    }
    
    function _getPhaseTitle() {
        if (hasAlarm && alarmType === "red") return "ALARMA ACTIVADA"
        if (hasAlarm && alarmType === "green") return "PROGRAMA COMPLETADO"
        
        switch(currentPhase) {
            case "setup": return "FASE DE SETUP"
            case "running": return "PROGRAMA EN EJECUCIÓN"
            case "completed": return "PROGRAMA COMPLETADO"
            default: return "LISTO PARA EJECUTAR"
        }
    }
    
    function _getPhaseDescription() {
        if (hasAlarm && alarmType === "red") return "Revisar condiciones de presión"
        if (hasAlarm && alarmType === "green") return "Ejecución finalizada correctamente"
        
        switch(currentPhase) {
            case "setup": return "Subiendo a presión mínima..."
            case "running": return "Control automático de presión"
            case "completed": return "Ejecución finalizada"
            default: return "Presione Iniciar para comenzar"
        }
    }
    
    // Connections para manejar eventos de ejecución
    Connections {
        target: executionController
        
        function onExecutionStarted(executionId) {
            isExecuting = true
            hasAlarm = false
            currentPhase = "setup"
        }
        
        function onExecutionFinished(executionId, status) {
            isExecuting = false
            currentPhase = "completed"
            
            if (status === "completed") {
                hasAlarm = true
                alarmType = "green"
                alarmMessageText.text = "¡Programa completado exitosamente!"
                
                // Auto-cerrar después de un delay
                closeTimer.start()
            } else {
                hasAlarm = false
            }
        }
        
        function onProgressUpdated(elapsed, remaining, percentage) {
            progressBar.value = percentage
            progressText.text = `${percentage}%`
        }
        
        function onStatusChanged(status) {
            statusText.text = status
        }
    }
    
    // Connections para manejar cambios de fase y alarmas
    Connections {
        target: executionController ? executionController.execution_service : null
        
        function onPhaseChanged(phase) {
            currentPhase = phase
            console.log("Fase cambiada a:", phase)
        }
        
        function onAlarmTriggered(alarmType, message) {
            hasAlarm = true
            executionDialog.alarmType = alarmType
            alarmMessageText.text = message
            console.log("Alarma:", alarmType, message)
        }
    }
    
    // Timer para auto-cerrar al completar
    Timer {
        id: closeTimer
        interval: 5000
        repeat: false
        onTriggered: {
            if (!isExecuting) {
                executionDialog.close()
            }
        }
    }
    
    // Función para abrir con programa específico
    function openForProgram(program) {
        programData = program
        isExecuting = executionController ? executionController.isRunning : false
        currentPhase = "setup"
        hasAlarm = false
        open()
    }
}