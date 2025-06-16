import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: loginView
    
    // Señales
    signal loginSuccess()
    
    // Propiedades
    property bool isLoading: false
    
    gradient: Gradient {
        GradientStop { position: 0.0; color: "#2C3E50" }
        GradientStop { position: 1.0; color: "#34495E" }
    }
    
    // Contenedor central
    Rectangle {
        anchors.centerIn: parent
        width: Math.min(500, parent.width * 0.7)  // Aumentado de 400 a 500
        height: Math.min(650, parent.height * 0.85)  // Aumentado de 550 a 650
        
        color: "#ECF0F1"
        radius: 20
        border.color: "#BDC3C7"
        border.width: 2
        
        // Sombra
        Rectangle {
            anchors.fill: parent
            anchors.topMargin: 5
            anchors.leftMargin: 5
            color: "#7F8C8D"
            radius: parent.radius
            z: -1
            opacity: 0.3
        }
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 40  // Aumentado de 30 a 40
            spacing: 25  // Aumentado de 20 a 25
            
            // Logo y título
            Column {
                Layout.alignment: Qt.AlignHCenter
                spacing: 15  // Aumentado de 12 a 15
                
                Rectangle {
                    width: 90  // Aumentado de 70 a 90
                    height: 90  // Aumentado de 70 a 90
                    radius: 45
                    color: "#3498DB"
                    anchors.horizontalCenter: parent.horizontalCenter
                    
                    Text {
                        anchors.centerIn: parent
                        text: "🔒"
                        font.pixelSize: 45  // Aumentado de 35 a 45
                        color: "white"
                    }
                }
                
                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "Sistema de Control de Presión"
                    font.pixelSize: 20  // Aumentado de 16 a 20
                    font.bold: true
                    color: "#2C3E50"
                    horizontalAlignment: Text.AlignHCenter
                    wrapMode: Text.WordWrap
                    width: parent.parent.width - 60  // Aumentado margen
                }
                
                Text {
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "Iniciar Sesión"
                    font.pixelSize: 16  // Aumentado de 13 a 16
                    color: "#7F8C8D"
                }
            }
            
            // Formulario de login
            Column {
                Layout.fillWidth: true
                spacing: 20  // Aumentado de 15 a 20
                
                // Campo usuario
                Column {
                    width: parent.width
                    spacing: 8  // Aumentado de 5 a 8
                    
                    Text {
                        text: "Usuario:"
                        font.pixelSize: 16  // Aumentado de 14 a 16
                        font.bold: true
                        color: "#2C3E50"
                    }
                    
                    TextField {
                        id: usernameField
                        width: parent.width
                        height: 50  // Aumentado de 40 a 50
                        font.pixelSize: 16  // Aumentado de 14 a 16
                        placeholderText: "Ingrese su usuario"
                        
                        background: Rectangle {
                            color: "#FFFFFF"
                            border.color: parent.activeFocus ? "#3498DB" : "#BDC3C7"
                            border.width: 2
                            radius: 8
                        }
                        
                        Keys.onReturnPressed: passwordField.forceActiveFocus()
                    }
                }
                
                // Campo contraseña
                Column {
                    width: parent.width
                    spacing: 8  // Aumentado de 5 a 8
                    
                    Text {
                        text: "Contraseña:"
                        font.pixelSize: 16  // Aumentado de 14 a 16
                        font.bold: true
                        color: "#2C3E50"
                    }
                    
                    TextField {
                        id: passwordField
                        width: parent.width
                        height: 50  // Aumentado de 40 a 50
                        font.pixelSize: 16  // Aumentado de 14 a 16
                        echoMode: TextInput.Password
                        placeholderText: "Ingrese su contraseña"
                        
                        background: Rectangle {
                            color: "#FFFFFF"
                            border.color: parent.activeFocus ? "#3498DB" : "#BDC3C7"
                            border.width: 2
                            radius: 8
                        }
                        
                        Keys.onReturnPressed: loginButton.clicked()
                    }
                }
            }
            
            // Botón de login
            Button {
                id: loginButton
                Layout.fillWidth: true
                Layout.preferredHeight: 55  // Aumentado de 45 a 55
                Layout.topMargin: 15  // Aumentado de 10 a 15
                
                enabled: !isLoading && usernameField.text.trim() !== "" && passwordField.text.trim() !== ""
                
                background: Rectangle {
                    color: parent.enabled ? (parent.pressed ? "#2980B9" : "#3498DB") : "#BDC3C7"
                    radius: 10
                    border.color: parent.enabled ? "#2471A3" : "#95A5A6"
                    border.width: 1
                }
                
                contentItem: Row {
                    anchors.centerIn: parent
                    spacing: 12  // Aumentado de 10 a 12
                    
                    Text {
                        text: isLoading ? "⏳" : "🔑"
                        font.pixelSize: 18  // Aumentado de 16 a 18
                        color: "white"
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    
                    Text {
                        text: isLoading ? "Iniciando sesión..." : "Iniciar Sesión"
                        font.pixelSize: 18  // Aumentado de 16 a 18
                        font.bold: true
                        color: "white"
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }
                
                onClicked: {
                    if (!isLoading) {
                        attemptLogin()
                    }
                }
            }
            
            // Información de usuario por defecto
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 80  // Aumentado de 70 a 80
                color: "#D5DBDB"
                radius: 8
                border.color: "#AEB6BF"
                border.width: 1
                
                Column {
                    anchors.centerIn: parent
                    spacing: 6  // Aumentado de 4 a 6
                    
                    Text {
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: "Usuario por defecto:"
                        font.pixelSize: 14  // Aumentado de 12 a 14
                        color: "#566573"
                        font.bold: true
                    }
                    
                    Text {
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: "Usuario: admin | Contraseña: admin123"
                        font.pixelSize: 13  // Aumentado de 11 a 13
                        color: "#566573"
                    }
                }
            }
            
            // Mensaje de resultado
            Text {
                id: messageText
                Layout.fillWidth: true
                Layout.preferredHeight: 30  // Aumentado de 25 a 30
                
                text: ""
                font.pixelSize: 14  // Aumentado de 12 a 14
                color: "#E74C3C"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                wrapMode: Text.WordWrap
                visible: text !== ""
            }
            
            // Espaciador mínimo
            Item { 
                Layout.fillHeight: true 
                Layout.minimumHeight: 15  // Aumentado de 10 a 15
            }
        }
    }
    
    // Funciones (preservadas sin cambios)
    function attemptLogin() {
        isLoading = true
        messageText.text = ""
        
        // Llamar al controlador de autenticación
        if (authController) {
            authController.login(usernameField.text, passwordField.text)
        }
    }
    
    function showMessage(message, isError) {
        messageText.text = message
        messageText.color = isError ? "#E74C3C" : "#27AE60"
        isLoading = false
    }
    
    // Connections para manejar el resultado del login
    Connections {
        target: authController
        
        function onLoginResult(success, message) {
            if (success) {
                showMessage(message, false)
                // Pequeño delay antes de cambiar a la vista principal
                delayTimer.start()
            } else {
                showMessage(message, true)
            }
        }
    }
    
    // Timer para delay después de login exitoso
    Timer {
        id: delayTimer
        interval: 1500
        repeat: false
        onTriggered: loginSuccess()
    }
    
    // Focus inicial
    Component.onCompleted: {
        usernameField.forceActiveFocus()
    }
}