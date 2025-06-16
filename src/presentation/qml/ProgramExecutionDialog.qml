import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    id: executionDialog
    
    property var programData: null
    property bool isExecuting: false
    
    signal executionRequested(int programId)
    signal stopRequested()
    
    anchors.centerIn: parent
    width: Math.min(600, parent.width * 0.9)
    height: Math.min(400, parent.height * 0.8)
    
    title: "Ejecutar Programa"
    modal: true
    
    background: Rectangle {
        color: "#ECF0F1"
        radius: 12
        border.color: "#3498DB"
        border.width: 2
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30
        spacing: 20
        
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
                anchors.margins: 20
                spacing: 10
                
                Text {
                    text: programData ? programData.name : ""
                    font.pixelSize: 20
                    font.bold: true
                    color: "#2C3E50"
                    Layout.fillWidth: true
                }
                
                Text {
                    text: programData ? programData.description : ""
                    font.pixelSize: 14
                    color: "#7F8C8D"
                    Layout.fillWidth: true
                    wrapMode: Text.WordWrap
                    visible: text !== ""
                }
                
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 30
                    
                    Column {
                        spacing: 4
                        
                        Text {
                            text: "Presión"
                            font.pixelSize: 12
                            color: "#95A5A6"
                            font.bold: true
                        }
                        
                        Text {
                            text: programData ? 
                                  `${programData.min_pressure} - ${programData.max_pressure} PSI` : ""
                            font.pixelSize: 16
                            color: "#2C3E50"
                            font.bold: true
                        }
                    }
                    
                    Column {
                        spacing: 4
                        
                        Text {
                            text: "Duración Total"
                            font.pixelSize: 12
                            color: "#95A5A6"
                            font.bold: true
                        }
                        
                        Text {
                            text: programData ? `${programData.program_duration} minutos` : ""
                            font.pixelSize: 16
                            color: "#2C3E50"
                            font.bold: true
                        }
                    }
                    
                    Column {
                        spacing: 4
                        
                        Text {
                            text: "Tiempo a Presión Mín."
                            font.pixelSize: 12
                            color: "#95A5A6"
                            font.bold: true
                        }
                        
                        Text {
                            text: programData ? `${programData.time_to_min_pressure} minutos` : ""
                            font.pixelSize: 16
                            color: "#2C3E50"
                            font.bold: true
                        }
                    }
                }
            }
        }
        
        // Estado de ejecución
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 80
            color: isExecuting ? "#D5F4E6" : "#FADBD8"
            radius: 10
            border.color: isExecuting ? "#27AE60" : "#E74C3C"
            border.width: 2
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 15
                
                Text {
                    text: isExecuting ? "●" : "○"
                    font.pixelSize: 30
                    color: isExecuting ? "#27AE60" : "#E74C3C"
                }
                
                Column {
                    Layout.fillWidth: true
                    spacing: 5
                    
                    Text {
                        text: isExecuting ? "PROGRAMA EN EJECUCIÓN" : "PROGRAMA DETENIDO"
                        font.pixelSize: 16
                        font.bold: true
                        color: isExecuting ? "#27AE60" : "#E74C3C"
                    }
                    
                    Text {
                        id: statusText
                        text: isExecuting ? "Presión controlada automáticamente" : "Listo para iniciar"
                        font.pixelSize: 12
                        color: "#566573"
                    }
                }
            }
        }
        
        // Progreso (solo visible durante ejecución)
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 60
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
                        text: "Progreso:"
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
                        color: "#3498DB"
                    }
                }
            }
        }
        
        // Botones de control
        RowLayout {
            Layout.fillWidth: true
            Layout.topMargin: 20
            spacing: 20
            
            Button {
                text: "Cerrar"
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                enabled: !isExecuting
                
                background: Rectangle {
                    color: parent.enabled ? 
                           (parent.pressed ? "#95A5A6" : "#BDC3C7") : "#D5DBDB"
                    radius: 8
                    border.color: "#85929E"
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    color: "#2C3E50"
                    font.pixelSize: 16
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: executionDialog.close()
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
    
    // Connections para manejar eventos de ejecución
    Connections {
        target: executionController
        
        function onExecutionStarted(executionId) {
            isExecuting = true
            statusText.text = "Programa iniciado - Control automático de presión"
        }
        
        function onExecutionFinished(executionId, status) {
            isExecuting = false
            statusText.text = status === "completed" ? "Programa completado exitosamente" : "Programa detenido"
            
            // Auto-cerrar después de un delay si se completó
            if (status === "completed") {
                closeTimer.start()
            }
        }
        
        function onProgressUpdated(elapsed, remaining, percentage) {
            progressBar.value = percentage
            progressText.text = `${percentage}%`
            
            let elapsedMin = Math.floor(elapsed / 60)
            let elapsedSec = elapsed % 60
            let remainingMin = Math.floor(remaining / 60)
            let remainingSec = remaining % 60
            
            statusText.text = `Transcurrido: ${elapsedMin.toString().padStart(2, '0')}:${elapsedSec.toString().padStart(2, '0')} | Restante: ${remainingMin.toString().padStart(2, '0')}:${remainingSec.toString().padStart(2, '0')}`
        }
        
        function onStatusChanged(status) {
            if (isExecuting) {
                statusText.text = status
            }
        }
    }
    
    // Timer para auto-cerrar al completar
    Timer {
        id: closeTimer
        interval: 3000
        repeat: false
        onTriggered: executionDialog.close()
    }
    
    // Función para abrir con programa específico
    function openForProgram(program) {
        programData = program
        isExecuting = executionController ? executionController.isRunning : false
        open()
    }
}