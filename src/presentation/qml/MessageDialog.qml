import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    id: messageDialog
    
    property alias messageText: messageLabel.text
    property bool isError: false
    
    anchors.centerIn: parent
    width: Math.min(400, parent.width * 0.8)
    height: 150
    
    modal: true
    
    background: Rectangle {
        color: "#ECF0F1"
        radius: 10
        border.color: messageDialog.isError ? "#E74C3C" : "#27AE60"
        border.width: 2
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20
        
        Text {
            id: messageLabel
            Layout.fillWidth: true
            font.pixelSize: 14
            color: "#2C3E50"
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
        }
        
        Button {
            text: "Aceptar"
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 100
            Layout.preferredHeight: 35
            
            background: Rectangle {
                color: parent.pressed ? "#2980B9" : "#3498DB"
                radius: 6
                border.color: "#2471A3"
                border.width: 1
            }
            
            contentItem: Text {
                text: parent.text
                color: "white"
                font.pixelSize: 14
                font.bold: true
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            
            onClicked: messageDialog.close()
        }
    }
    
    function showMessage(message, error) {
        messageText = message
        isError = error || false
        open()
    }
}