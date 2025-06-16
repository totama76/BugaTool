import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: programItem
    
    property var programData: null
    property bool canManage: false
    property bool isExecuting: false
    property string executingProgramName: ""
    
    signal editRequested()
    signal deleteRequested()
    signal executeRequested()
    signal viewExecutionRequested()
    
    // Determinar si este programa es el que se está ejecutando
    property bool isThisExecuting: isExecuting && programData && 
                                  executingProgramName === programData.name
    
    // Determinar si hay CUALQUIER ejecución activa (para bloquear)
    property bool anyExecutionActive: executionController ? executionController.isRunning : false
    
    height: 140
    color: isThisExecuting ? "#FFF8DC" : "#FFFFFF"
    radius: 10
    border.color: isThisExecuting ? "#F39C12" : "#D5DBDB"
    border.width: isThisExecuting ? 3 : 1
    
    // Efecto hover (solo si no está ejecutando)
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        
        onEntered: {
            if (!isThisExecuting) {
                parent.color = "#F8F9FA"
            }
        }
        onExited: {
            if (!isThisExecuting) {
                parent.color = "#FFFFFF"
            } else {
                parent.color = "#FFF8DC"
            }
        }
    }
    
    // Indicador de ejecución (animado)
    Rectangle {
        visible: isThisExecuting
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 10
        width: 140
        height: 25
        color: "#F39C12"
        radius: 12
        border.color: "#E67E22"
        border.width: 1
        
        // Animación de pulso
        SequentialAnimation on opacity {
            running: parent.visible
            loops: Animation.Infinite
            NumberAnimation { to: 0.6; duration: 1000 }
            NumberAnimation { to: 1.0; duration: 1000 }
        }
        
        Text {
            anchors.centerIn: parent
            text: "▶️ VER PROGRESO"
            color: "white"
            font.pixelSize: 9
            font.bold: true
        }
        
        MouseArea {
            anchors.fill: parent
            onClicked: {
                console.log("Clickeado indicador de ejecución")
                viewExecutionRequested()
            }
        }
    }
    
    RowLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20
        
        // Información principal del programa
        Column {
            Layout.fillWidth: true
            spacing: 12
            
            Text {
                text: programData ? programData.name : ""
                font.pixelSize: 18
                font.bold: true
                color: isThisExecuting ? "#D68910" : "#2C3E50"
                elide: Text.ElideRight
                width: parent.width
            }
            
            Text {
                text: programData ? programData.description : ""
                font.pixelSize: 14
                color: isThisExecuting ? "#B7950B" : "#7F8C8D"
                elide: Text.ElideRight
                width: parent.width
                visible: text !== ""
            }
            
            RowLayout {
                spacing: 25
                
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
                        font.pixelSize: 14
                        color: isThisExecuting ? "#D68910" : "#2C3E50"
                        font.bold: true
                    }
                }
                
                Column {
                    spacing: 4
                    
                    Text {
                        text: "Duración"
                        font.pixelSize: 12
                        color: "#95A5A6"
                        font.bold: true
                    }
                    
                    Text {
                        text: programData ? `${programData.program_duration} min` : ""
                        font.pixelSize: 14
                        color: isThisExecuting ? "#D68910" : "#2C3E50"
                        font.bold: true
                    }
                }
                
                Column {
                    spacing: 4
                    
                    Text {
                        text: "Tiempo a mín."
                        font.pixelSize: 12
                        color: "#95A5A6"
                        font.bold: true
                    }
                    
                    Text {
                        text: programData ? `${programData.time_to_min_pressure} min` : ""
                        font.pixelSize: 14
                        color: isThisExecuting ? "#D68910" : "#2C3E50"
                        font.bold: true
                    }
                }
            }
        }
        
        // Botones de acción
        Column {
            spacing: 12
            
            Button {
                text: {
                    if (isThisExecuting) return "Ver Progreso"
                    if (anyExecutionActive) return "Ejecución Activa"
                    return "Ejecutar"
                }
                width: 100
                height: 35
                enabled: isThisExecuting || !anyExecutionActive  // Solo ejecutar si no hay otra activa
                
                background: Rectangle {
                    color: {
                        if (!parent.enabled) return "#95A5A6"
                        return isThisExecuting ? "#F39C12" :
                               (parent.pressed ? "#F39C12" : "#F1C40F")
                    }
                    radius: 8
                    border.color: parent.enabled ? "#D68910" : "#7F8C8D"
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    color: {
                        if (!parent.enabled) return "#566573"
                        return isThisExecuting ? "white" : "#2C3E50"
                    }
                    font.pixelSize: 14
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    if (isThisExecuting) {
                        viewExecutionRequested()
                    } else if (!anyExecutionActive) {
                        executeRequested()
                    }
                }
            }
            
            RowLayout {
                spacing: 8
                visible: canManage
                
                Button {
                    text: "✏"
                    width: 45
                    height: 30
                    enabled: !anyExecutionActive  // Bloquear edición si hay ejecución activa
                    
                    background: Rectangle {
                        color: parent.enabled ?
                               (parent.pressed ? "#2980B9" : "#3498DB") : "#95A5A6"
                        radius: 6
                        border.color: parent.enabled ? "#2471A3" : "#7F8C8D"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: parent.enabled ? "white" : "#566573"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        if (!anyExecutionActive) {
                            editRequested()
                        }
                    }
                }
                
                Button {
                    text: "🗑"
                    width: 45
                    height: 30
                    enabled: !anyExecutionActive  // Bloquear eliminación si hay ejecución activa
                    
                    background: Rectangle {
                        color: parent.enabled ?
                               (parent.pressed ? "#C0392B" : "#E74C3C") : "#95A5A6"
                        radius: 6
                        border.color: parent.enabled ? "#A93226" : "#7F8C8D"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: parent.enabled ? "white" : "#566573"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        if (!anyExecutionActive) {
                            deleteRequested()
                        }
                    }
                }
            }
        }
    }
}