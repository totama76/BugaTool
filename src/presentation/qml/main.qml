import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: window
    visible: true
    width: 800
    height: 480
    title: "Sistema de Control de Presión - v0.1.0"
    
    // Configuración para pantalla táctil
    flags: Qt.FramelessWindowHint | Qt.Window
    
    // Stack para manejar las diferentes vistas
    StackView {
        id: stackView
        anchors.fill: parent
        
        // Vista inicial: Login o Dashboard dependiendo del estado de autenticación
        initialItem: authController && authController.isAuthenticated ? dashboardComponent : loginComponent
        
        // Componente de Login
        Component {
            id: loginComponent
            
            LoginView {
                onLoginSuccess: {
                    stackView.replace(dashboardComponent)
                }
            }
        }
        
        // Componente de Dashboard (vista principal)
        Component {
            id: dashboardComponent
            
            Rectangle {
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#2C3E50" }
                    GradientStop { position: 1.0; color: "#34495E" }
                }
                
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 20
                    spacing: 20
                    
                    // Header con título, usuario y estado
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 80
                        color: "transparent"
                        border.color: "#3498DB"
                        border.width: 2
                        radius: 10
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            
                            Text {
                                text: "Control de Presión"
                                font.pixelSize: 24
                                font.bold: true
                                color: "#ECF0F1"
                                Layout.fillWidth: true
                            }
                            
                            // Información del usuario
                            Column {
                                spacing: 2
                                
                                Text {
                                    text: authController ? authController.currentUsername : ""
                                    font.pixelSize: 14
                                    font.bold: true
                                    color: "#3498DB"
                                    horizontalAlignment: Text.AlignRight
                                }
                                
                                Text {
                                    text: authController ? authController.currentRole : ""
                                    font.pixelSize: 12
                                    color: "#BDC3C7"
                                    horizontalAlignment: Text.AlignRight
                                }
                            }
                            
                            // Botón gestionar programas (solo para administradores)
                            Button {
                                text: "Programas"
                                visible: authController ? authController.canManagePrograms : false
                                
                                background: Rectangle {
                                    color: parent.pressed ? "#8E44AD" : "#9B59B6"
                                    radius: 6
                                    border.color: "#7D3C98"
                                    border.width: 1
                                }
                                
                                contentItem: Text {
                                    text: parent.text
                                    color: "white"
                                    font.pixelSize: 12
                                    font.bold: true
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                                
                                onClicked: {
                                    stackView.push(programManagementComponent)
                                }
                            }
                            
                            // Botón logout
                            Button {
                                text: "Salir"
                                
                                background: Rectangle {
                                    color: parent.pressed ? "#C0392B" : "#E74C3C"
                                    radius: 6
                                    border.color: "#A93226"
                                    border.width: 1
                                }
                                
                                contentItem: Text {
                                    text: parent.text
                                    color: "white"
                                    font.pixelSize: 12
                                    font.bold: true
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                                
                                onClicked: {
                                    authController.logout()
                                    stackView.replace(loginComponent)
                                }
                            }
                        }
                    }
                    
                    // Área central con gauge de presión (funcionalidad existente preservada)
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "transparent"
                        border.color: "#34495E"
                        border.width: 1
                        radius: 15
                        
                        PressureGauge {
                            id: pressureGauge
                            anchors.centerIn: parent
                            size: Math.min(parent.width, parent.height) * 0.7
                            value: mainController ? mainController.currentPressure : 0
                            minValue: 0
                            maxValue: 100
                        }
                    }
                    
                    // Panel de control inferior (funcionalidad existente preservada)
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 100
                        color: "transparent"
                        border.color: "#34495E"
                        border.width: 1
                        radius: 10
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 15
                            spacing: 20
                            
                            Button {
                                text: "Iniciar Simulación"
                                Layout.preferredWidth: 150
                                Layout.fillHeight: true
                                
                                background: Rectangle {
                                    color: parent.pressed ? "#27AE60" : "#2ECC71"
                                    radius: 8
                                    border.color: "#229954"
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
                                
                                onClicked: {
                                    if (mainController) {
                                        mainController.startSimulation()
                                    }
                                }
                            }
                            
                            Button {
                                text: "Detener Simulación"
                                Layout.preferredWidth: 150
                                Layout.fillHeight: true
                                
                                background: Rectangle {
                                    color: parent.pressed ? "#C0392B" : "#E74C3C"
                                    radius: 8
                                    border.color: "#A93226"
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
                                
                                onClicked: {
                                    if (mainController) {
                                        mainController.stopSimulation()
                                    }
                                }
                            }
                            
                            Item { Layout.fillWidth: true }
                            
                            Column {
                                spacing: 5
                                
                                Text {
                                    text: "Presión Actual"
                                    color: "#BDC3C7"
                                    font.pixelSize: 12
                                    horizontalAlignment: Text.AlignHCenter
                                }
                                
                                Text {
                                    text: (mainController ? mainController.currentPressure.toFixed(1) : "0.0") + " PSI"
                                    color: "#ECF0F1"
                                    font.pixelSize: 18
                                    font.bold: true
                                    horizontalAlignment: Text.AlignHCenter
                                }
                            }
                        }
                    }
                }
            }
        }
        
        // Componente de Gestión de Programas
        Component {
            id: programManagementComponent
            
            ProgramManagementView {
                onBackToMain: {
                    stackView.pop()
                }
            }
        }
    }
}