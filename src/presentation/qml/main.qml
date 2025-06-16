import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: window
    visible: true
    width: 1200
    height: 800
    title: "Sistema de Control de Presión - v0.1.0"
    
    // Configuración para pantalla táctil
    flags: Qt.Window
    
    // Stack para manejar las diferentes vistas
    StackView {
        id: stackView
        anchors.fill: parent
        
        // Vista inicial: Login (siempre empezar por aquí)
        initialItem: loginComponent
        
        // Componente de Login
        Component {
            id: loginComponent
            
            LoginView {
                onLoginSuccess: {
                    console.log("Login exitoso, navegando a dashboard")
                    stackView.replace(dashboardComponent)
                    
                    // Verificar ejecuciones después de un pequeño delay
                    executionCheckTimer.start()
                }
            }
        }
        
        // Timer para verificar ejecuciones después del login
        Timer {
            id: executionCheckTimer
            interval: 1000  // 1 segundo después del login
            repeat: false
            onTriggered: {
                console.log("Verificando ejecuciones después del login...")
                if (shouldShowExecutionAfterLogin && resumedProgramAfterLogin) {
                    console.log("Ejecución resumida detectada:", resumedProgramAfterLogin.name)
                    showExecutionResumedDialog()
                }
            }
        }
        
        // Función para mostrar el diálogo de ejecución resumida
        function showExecutionResumedDialog() {
            executionResumedDialog.open()
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
                    anchors.margins: 30
                    spacing: 25
                    
                    // Header con título, usuario y estado
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 100
                        color: "transparent"
                        border.color: "#3498DB"
                        border.width: 2
                        radius: 10
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 15
                            
                            Text {
                                text: "Control de Presión"
                                font.pixelSize: 28
                                font.bold: true
                                color: "#ECF0F1"
                                Layout.fillWidth: true
                            }
                            
                            // Información del usuario
                            Column {
                                spacing: 5
                                
                                Text {
                                    text: authController ? authController.currentUsername : ""
                                    font.pixelSize: 16
                                    font.bold: true
                                    color: "#3498DB"
                                    horizontalAlignment: Text.AlignRight
                                }
                                
                                Text {
                                    text: authController ? authController.currentRole : ""
                                    font.pixelSize: 14
                                    color: "#BDC3C7"
                                    horizontalAlignment: Text.AlignRight
                                }
                            }
                            
                            // Indicador de ejecución en curso
                            Rectangle {
                                visible: executionController ? executionController.isRunning : false
                                width: 120
                                height: 40
                                color: "#E74C3C"
                                radius: 8
                                border.color: "#C0392B"
                                border.width: 1
                                
                                // Efecto de parpadeo
                                SequentialAnimation on opacity {
                                    running: parent.visible
                                    loops: Animation.Infinite
                                    NumberAnimation { to: 0.3; duration: 800 }
                                    NumberAnimation { to: 1.0; duration: 800 }
                                }
                                
                                Text {
                                    anchors.centerIn: parent
                                    text: "🔴 EJECUTANDO"
                                    color: "white"
                                    font.pixelSize: 11
                                    font.bold: true
                                }
                                
                                MouseArea {
                                    anchors.fill: parent
                                    onClicked: {
                                        // Ir directamente a programas y abrir ejecución
                                        stackView.push(programManagementComponent)
                                        openCurrentExecutionTimer.start()
                                    }
                                }
                            }
                            
                            // Botón gestionar programas (solo para administradores)
                            Button {
                                text: "Programas"
                                visible: authController ? authController.canManagePrograms : false
                                implicitWidth: 120
                                implicitHeight: 40
                                
                                background: Rectangle {
                                    color: parent.pressed ? "#8E44AD" : "#9B59B6"
                                    radius: 8
                                    border.color: "#7D3C98"
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
                                    stackView.push(programManagementComponent)
                                }
                            }
                            
                            // Botón logout
                            Button {
                                text: "Salir"
                                implicitWidth: 80
                                implicitHeight: 40
                                
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
                            size: Math.min(parent.width, parent.height) * 0.6
                            value: mainController ? mainController.currentPressure : 0
                            minValue: 0
                            maxValue: 100
                        }
                    }
                    
                    // Panel de control inferior (funcionalidad existente preservada)
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 120
                        color: "transparent"
                        border.color: "#34495E"
                        border.width: 1
                        radius: 10
                        
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 20
                            spacing: 25
                            
                            Button {
                                text: "Iniciar Simulación"
                                Layout.preferredWidth: 180
                                Layout.fillHeight: true
                                enabled: !(executionController && executionController.isRunning)
                                
                                background: Rectangle {
                                    color: parent.enabled ? 
                                           (parent.pressed ? "#27AE60" : "#2ECC71") : "#95A5A6"
                                    radius: 10
                                    border.color: parent.enabled ? "#229954" : "#7F8C8D"
                                    border.width: 1
                                }
                                
                                contentItem: Text {
                                    text: parent.enabled ? parent.text : "Ejecución activa"
                                    color: "white"
                                    font.pixelSize: 16
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
                                Layout.preferredWidth: 180
                                Layout.fillHeight: true
                                
                                background: Rectangle {
                                    color: parent.pressed ? "#C0392B" : "#E74C3C"
                                    radius: 10
                                    border.color: "#A93226"
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
                                    if (mainController) {
                                        mainController.stopSimulation()
                                    }
                                }
                            }
                            
                            Item { Layout.fillWidth: true }
                            
                            Column {
                                spacing: 8
                                
                                Text {
                                    text: "Presión Actual"
                                    color: "#BDC3C7"
                                    font.pixelSize: 14
                                    horizontalAlignment: Text.AlignHCenter
                                }
                                
                                Text {
                                    text: (mainController ? mainController.currentPressure.toFixed(1) : "0.0") + " PSI"
                                    color: "#ECF0F1"
                                    font.pixelSize: 22
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
        
        // Timer para abrir ejecución actual
        Timer {
            id: openCurrentExecutionTimer
            interval: 500
            repeat: false
            onTriggered: {
                var programManagement = stackView.currentItem
                if (programManagement && programManagement.executionDialog && executionController.isRunning) {
                    // Obtener información del programa actual
                    var currentInfo = executionController.execution_service.get_current_execution_info()
                    if (currentInfo.is_running && currentInfo.program_name) {
                        // Simular datos del programa para abrir el diálogo
                        var programData = {
                            id: currentInfo.execution_id,
                            name: currentInfo.program_name,
                            min_pressure: currentInfo.min_pressure,
                            max_pressure: currentInfo.max_pressure,
                            program_duration: currentInfo.program_duration / 60
                        }
                        programManagement.executionDialog.openForProgram(programData)
                    }
                }
            }
        }
    }
    
    // Dialog para ejecución resumida
    Dialog {
        id: executionResumedDialog
        
        anchors.centerIn: parent
        width: Math.min(600, parent.width * 0.8)
        height: 350
        
        title: "Ejecución Resumida"
        modal: true
        
        background: Rectangle {
            color: "#ECF0F1"
            radius: 12
            border.color: "#F39C12"
            border.width: 3
        }
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 30
            spacing: 20
            
            Text {
                text: "🔄 Ejecución en Curso Detectada"
                font.pixelSize: 20
                font.bold: true
                color: "#D68910"
                Layout.alignment: Qt.AlignHCenter
            }
            
            Text {
                text: resumedProgramAfterLogin ? 
                      `Se detectó una ejecución interrumpida del programa:\n"${resumedProgramAfterLogin.name}"` : ""
                font.pixelSize: 16
                color: "#2C3E50"
                Layout.alignment: Qt.AlignHCenter
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
            }
            
            Text {
                text: "La ejecución ha sido resumida automáticamente."
                font.pixelSize: 14
                color: "#7F8C8D"
                Layout.alignment: Qt.AlignHCenter
                horizontalAlignment: Text.AlignHCenter
            }
            
            RowLayout {
                Layout.fillWidth: true
                Layout.topMargin: 20
                spacing: 20
                
                Button {
                    text: "Continuar en Dashboard"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    
                    background: Rectangle {
                        color: parent.pressed ? "#95A5A6" : "#BDC3C7"
                        radius: 8
                        border.color: "#85929E"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "#2C3E50"
                        font.pixelSize: 14
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        executionResumedDialog.close()
                    }
                }
                
                Button {
                    text: "Ir a Ejecución"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    
                    background: Rectangle {
                        color: parent.pressed ? "#E67E22" : "#F39C12"
                        radius: 8
                        border.color: "#D68910"
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
                        executionResumedDialog.close()
                        // Ir a programas y abrir ejecución
                        stackView.push(programManagementComponent)
                        openResumedExecutionTimer.start()
                    }
                }
            }
        }
        
        // Timer para abrir ejecución resumida
        Timer {
            id: openResumedExecutionTimer
            interval: 500
            repeat: false
            onTriggered: {
                var programManagement = stackView.currentItem
                if (programManagement && programManagement.executionDialog && resumedProgramAfterLogin) {
                    programManagement.executionDialog.openForProgram(resumedProgramAfterLogin)
                }
            }
        }
    }
    
    // Connections para manejar ejecución resumida
    Connections {
        target: executionController
        
        function onExecutionResumed(programData) {
            console.log("Señal de ejecución resumida recibida")
            // La verificación ya se hace en el timer después del login
        }
    }
}