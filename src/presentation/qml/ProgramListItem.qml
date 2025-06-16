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
    
    height: 140  // Aumentado de 120 a 140
    color: "#FFFFFF"
    radius: 10  // Aumentado de 8 a 10
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
        anchors.margins: 20  // Aumentado de 15 a 20
        spacing: 20  // Aumentado de 15 a 20
        
        // Información principal del programa
        Column {
            Layout.fillWidth: true
            spacing: 12  // Aumentado de 8 a 12
            
            Text {
                text: programData ? programData.name : ""
                font.pixelSize: 18  // Aumentado de 16 a 18
                font.bold: true
                color: "#2C3E50"
                elide: Text.ElideRight
                width: parent.width
            }
            
            Text {
                text: programData ? programData.description : ""
                font.pixelSize: 14  // Aumentado de 12 a 14
                color: "#7F8C8D"
                elide: Text.ElideRight
                width: parent.width
                visible: text !== ""
            }
            
            RowLayout {
                spacing: 25  // Aumentado de 20 a 25
                
                Column {
                    spacing: 4  // Aumentado de 2 a 4
                    
                    Text {
                        text: "Presión"
                        font.pixelSize: 12  // Aumentado de 10 a 12
                        color: "#95A5A6"
                        font.bold: true
                    }
                    
                    Text {
                        text: programData ? 
                              `${programData.min_pressure} - ${programData.max_pressure} PSI` : ""
                        font.pixelSize: 14  // Aumentado de 12 a 14
                        color: "#2C3E50"
                        font.bold: true
                    }
                }
                
                Column {
                    spacing: 4  // Aumentado de 2 a 4
                    
                    Text {
                        text: "Duración"
                        font.pixelSize: 12  // Aumentado de 10 a 12
                        color: "#95A5A6"
                        font.bold: true
                    }
                    
                    Text {
                        text: programData ? `${programData.program_duration} min` : ""
                        font.pixelSize: 14  // Aumentado de 12 a 14
                        color: "#2C3E50"
                        font.bold: true
                    }
                }
                
                Column {
                    spacing: 4  // Aumentado de 2 a 4
                    
                    Text {
                        text: "Tiempo a mín."
                        font.pixelSize: 12  // Aumentado de 10 a 12
                        color: "#95A5A6"
                        font.bold: true
                    }
                    
                    Text {
                        text: programData ? `${programData.time_to_min_pressure} min` : ""
                        font.pixelSize: 14  // Aumentado de 12 a 14
                        color: "#2C3E50"
                        font.bold: true
                    }
                }
            }
        }
        
        // Botones de acción
        Column {
            spacing: 12  // Aumentado de 8 a 12
            
            Button {
                text: "Ejecutar"
                width: 100  // Aumentado de 80 a 100
                height: 35  // Aumentado de 30 a 35
                
                background: Rectangle {
                    color: parent.pressed ? "#F39C12" : "#F1C40F"
                    radius: 8  // Aumentado de 6 a 8
                    border.color: "#D68910"
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    color: "#2C3E50"
                    font.pixelSize: 14  // Aumentado de 12 a 14
                    font.bold: true
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: executeRequested()
            }
            
            RowLayout {
                spacing: 8  // Aumentado de 5 a 8
                visible: canManage
                
                Button {
                    text: "✏"
                    width: 45  // Aumentado de 35 a 45
                    height: 30  // Aumentado de 25 a 30
                    
                    background: Rectangle {
                        color: parent.pressed ? "#2980B9" : "#3498DB"
                        radius: 6  // Aumentado de 4 a 6
                        border.color: "#2471A3"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 14  // Aumentado de 12 a 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: editRequested()
                }
                
                Button {
                    text: "🗑"
                    width: 45  // Aumentado de 35 a 45
                    height: 30  // Aumentado de 25 a 30
                    
                    background: Rectangle {
                        color: parent.pressed ? "#C0392B" : "#E74C3C"
                        radius: 6  // Aumentado de 4 a 6
                        border.color: "#A93226"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 14  // Aumentado de 12 a 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: deleteRequested()
                }
            }
        }
    }
}