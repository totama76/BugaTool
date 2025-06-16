import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: programItem
    
    property var programData: null
    property bool canManage: false
    
    signal editRequested()
    signal deleteRequested()
    signal executeRequested()
    
    height: 120
    color: "#FFFFFF"
    radius: 8
    border.color: "#D5DBDB"
    border.width: 1
    
    // Efecto hover
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        
        onEntered: parent.color = "#F8F9FA"
        onExited: parent.color = "#FFFFFF"
    }
    
    RowLayout {
        anchors.fill: parent
        anchors.margins: 15
        spacing: 15
        
        // Información principal del programa
        Column {
            Layout.fillWidth: true
            spacing: 8
            
            Text {
                text: programData ? programData.name : ""
                font.pixelSize: 16
                font.bold: true
                color: "#2C3E50"
                elide: Text.ElideRight
                width: parent.width
            }
            
            Text {
                text: programData ? programData.description : ""
                font.pixelSize: 12
                color: "#7F8C8D"
                elide: Text.ElideRight
                width: parent.width
                visible: text !== ""
            }
            
            RowLayout {
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
                        font.pixelSize: 12
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
                        font.pixelSize: 12
                        color: "#2C3E50"
                        font.bold: true
                    }
                }
                
                Column {
                    spacing: 2
                    
                    Text {
                        text: "Tiempo a mín."
                        font.pixelSize: 10
                        color: "#95A5A6"
                        font.bold: true
                    }
                    
                    Text {
                        text: programData ? `${programData.time_to_min_pressure} min` : ""
                        font.pixelSize: 12
                        color: "#2C3E50"
                        font.bold: true
                    }
                }
            }
        }
        
        // Botones de acción
        Column {
            spacing: 8
            
            Button {
                text: "Ejecutar"
                width: 80
                height: 30
                
                background: Rectangle {
                    color: parent.pressed ? "#F39C12" : "#F1C40F"
                    radius: 6
                    border.color: "#D68910"
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    color: "#2C3E50"
                    font.pixelSize: 12
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: executeRequested()
            }
            
            RowLayout {
                spacing: 5
                visible: canManage
                
                Button {
                    text: "✏"
                    width: 35
                    height: 25
                    
                    background: Rectangle {
                        color: parent.pressed ? "#2980B9" : "#3498DB"
                        radius: 4
                        border.color: "#2471A3"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: editRequested()
                }
                
                Button {
                    text: "🗑"
                    width: 35
                    height: 25
                    
                    background: Rectangle {
                        color: parent.pressed ? "#C0392B" : "#E74C3C"
                        radius: 4
                        border.color: "#A93226"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 12
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: deleteRequested()
                }
            }
        }
    }
}