import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: programManagementView
    
    // Señales
    signal backToMain()
    
    // Propiedades para estado de ejecución
    property bool isExecuting: executionController ? executionController.isRunning : false
    property string executingProgramName: executionController ? executionController.currentProgramName : ""
    
    // Propiedad para acceso al dialog de ejecución (para uso externo)
    property alias executionDialog: executionDialog
    
    gradient: Gradient {
        GradientStop { position: 0.0; color: "#2C3E50" }
        GradientStop { position: 1.0; color: "#34495E" }
    }
    
    // Cargar programas cuando se muestra la vista
    Component.onCompleted: {
        console.log("ProgramManagementView cargada")
        if (programController) {
            programController.load_programs()
        }
        
        // Actualizar estado de ejecución
        updateExecutionState()
    }
    
    // Función para actualizar estado de ejecución
    function updateExecutionState() {
        isExecuting = executionController ? executionController.isRunning : false
        executingProgramName = executionController ? executionController.currentProgramName : ""
        console.log("Estado de ejecución actualizado:", isExecuting, executingProgramName)
    }
    
    // Función SEGURA para obtener datos del programa en ejecución
    function getCurrentExecutionProgramData() {
        if (!executionController || !executionController.isRunning) {
            console.log("No hay ejecución activa")
            return null
        }
        
        try {
            // Usar el slot del controller en lugar de acceso directo al servicio
            var currentInfo = executionController.get_current_execution_info()
            
            if (!currentInfo || !currentInfo.is_running) {
                console.log("No hay información de ejecución válida")
                return null
            }
            
            console.log("Información de ejecución obtenida:", JSON.stringify(currentInfo))
            
            // Crear objeto de datos del programa para el diálogo
            return {
                id: currentInfo.execution_id || 0,
                name: currentInfo.program_name || "Programa Actual",
                description: "Programa en ejecución",
                min_pressure: currentInfo.min_pressure || 0,
                max_pressure: currentInfo.max_pressure || 100,
                program_duration: (currentInfo.program_duration || 0) / 60,
                time_to_min_pressure: 5 // Valor por defecto
            }
        } catch (e) {
            console.log("Error obteniendo datos de ejecución:", e)
            return null
        }
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 30
        spacing: 25
        
        // Header
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 80
            color: "transparent"
            border.color: "#3498DB"
            border.width: 2
            radius: 10
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 20
                
                Button {
                    text: "← Volver"
                    implicitWidth: 120
                    implicitHeight: 40
                    
                    background: Rectangle {
                        color: parent.pressed ? "#2980B9" : "#3498DB"
                        radius: 8
                        border.color: "#2471A3"
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
                    
                    onClicked: backToMain()
                }
                
                Text {
                    text: "Gestión de Programas"
                    font.pixelSize: 24
                    font.bold: true
                    color: "#ECF0F1"
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter
                }
                
                // Indicador de estado de ejecución en header (clickeable)
                Rectangle {
                    visible: isExecuting
                    implicitWidth: 180
                    implicitHeight: 40
                    color: "#F39C12"
                    radius: 8
                    border.color: "#E67E22"
                    border.width: 1
                    
                    SequentialAnimation on opacity {
                        running: parent.visible
                        loops: Animation.Infinite
                        NumberAnimation { to: 0.7; duration: 1000 }
                        NumberAnimation { to: 1.0; duration: 1000 }
                    }
                    
                    Text {
                        anchors.centerIn: parent
                        text: `▶️ ${executingProgramName}`
                        color: "white"
                        font.pixelSize: 12
                        font.bold: true
                        elide: Text.ElideRight
                        width: parent.width - 10
                        horizontalAlignment: Text.AlignHCenter
                    }
                    
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            var programData = getCurrentExecutionProgramData()
                            if (programData) {
                                executionDialog.openForProgram(programData)
                            } else {
                                console.log("No se pudieron obtener los datos del programa en ejecución")
                            }
                        }
                    }
                }
                
                // Botón de limpieza (solo para administradores)
                Button {
                    text: "🧹 Limpiar"
                    visible: programController ? programController.canManage : false
                    implicitWidth: 120
                    implicitHeight: 40
                    
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
                        cleanupDialog.open()
                    }
                }
                
                Button {
                    text: "Nuevo Programa"
                    visible: programController ? programController.canManage : false
                    implicitWidth: 160
                    implicitHeight: 40
                    
                    background: Rectangle {
                        color: parent.pressed ? "#27AE60" : "#2ECC71"
                        radius: 8
                        border.color: "#229954"
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
                        programFormDialog.openForCreate()
                    }
                }
            }
        }
        
        // Barra de búsqueda
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 60
            color: "#ECF0F1"
            radius: 10
            border.color: "#BDC3C7"
            border.width: 1
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 15
                spacing: 15
                
                TextField {
                    id: searchField
                    Layout.fillWidth: true
                    height: 40
                    placeholderText: "Buscar programas..."
                    font.pixelSize: 16
                    
                    background: Rectangle {
                        color: "transparent"
                    }
                    
                    onTextChanged: {
                        searchTimer.restart()
                    }
                    
                    Timer {
                        id: searchTimer
                        interval: 500
                        repeat: false
                        onTriggered: {
                            if (programController) {
                                programController.search_programs(searchField.text)
                            }
                        }
                    }
                }
                
                Button {
                    text: "🔍"
                    implicitWidth: 50
                    implicitHeight: 40
                    
                    background: Rectangle {
                        color: parent.pressed ? "#2980B9" : "#3498DB"
                        radius: 6
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 18
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        if (programController) {
                            programController.search_programs(searchField.text)
                        }
                    }
                }
                
                Button {
                    text: "✖"
                    implicitWidth: 50
                    implicitHeight: 40
                    
                    background: Rectangle {
                        color: parent.pressed ? "#C0392B" : "#E74C3C"
                        radius: 6
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 14
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        searchField.text = ""
                        if (programController) {
                            programController.clear_search()
                        }
                    }
                }
                
                // Botón refrescar para forzar recarga
                Button {
                    text: "↻"
                    implicitWidth: 50
                    implicitHeight: 40
                    
                    background: Rectangle {
                        color: parent.pressed ? "#8E44AD" : "#9B59B6"
                        radius: 6
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 18
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        console.log("Refrescando lista de programas...")
                        if (programController) {
                            programController.refresh_programs()
                        }
                        updateExecutionState()
                    }
                }
            }
        }
        
        // Lista de programas
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#ECF0F1"
            radius: 12
            border.color: "#BDC3C7"
            border.width: 1
            
            ScrollView {
                anchors.fill: parent
                anchors.margins: 15
                
                ListView {
                    id: programListView
                    model: programController ? programController.programs : []
                    spacing: 15
                    
                    delegate: ProgramListItem {
                        width: programListView.width
                        programData: modelData
                        canManage: programController ? programController.canManage : false
                        
                        // Pasar estado de ejecución
                        isExecuting: programManagementView.isExecuting
                        executingProgramName: programManagementView.executingProgramName
                        
                        onEditRequested: {
                            programFormDialog.openForEdit(programData)
                        }
                        
                        onDeleteRequested: {
                            deleteConfirmDialog.programToDelete = programData
                            deleteConfirmDialog.open()
                        }
                        
                        onExecuteRequested: {
                            executionDialog.openForProgram(programData)
                        }
                        
                        onViewExecutionRequested: {
                            var programData = getCurrentExecutionProgramData()
                            if (programData) {
                                executionDialog.openForProgram(programData)
                            } else {
                                console.log("No se pudieron obtener los datos del programa en ejecución")
                            }
                        }
                    }
                    
                    // Mensaje cuando no hay programas
                    Text {
                        anchors.centerIn: parent
                        text: searchField.text !== "" ? "No se encontraron programas" : "No hay programas creados"
                        font.pixelSize: 18
                        color: "#7F8C8D"
                        visible: programListView.count === 0
                    }
                }
            }
        }
    }
    
    // Dialog de limpieza de ejecuciones fantasma
    Dialog {
        id: cleanupDialog
        
        anchors.centerIn: parent
        width: Math.min(500, parent.width * 0.8)
        height: 250
        
        title: "Limpiar Ejecuciones Fantasma"
        modal: true
        
        background: Rectangle {
            color: "#ECF0F1"
            radius: 12
            border.color: "#F39C12"
            border.width: 2
        }
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 30
            spacing: 20
            
            Text {
                Layout.fillWidth: true
                text: "Esta operación limpiará las ejecuciones 'fantasma' que pueden estar causando problemas de detección."
                font.pixelSize: 14
                color: "#2C3E50"
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            
            Text {
                Layout.fillWidth: true
                text: "Se marcarán como detenidas las ejecuciones con más de 24 horas sin actualizar."
                font.pixelSize: 12
                color: "#7F8C8D"
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            
            RowLayout {
                Layout.fillWidth: true
                spacing: 20
                
                Button {
                    text: "Cancelar"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 45
                    
                    background: Rectangle {
                        color: parent.pressed ? "#95A5A6" : "#BDC3C7"
                        radius: 8
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "#2C3E50"
                        font.pixelSize: 14
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: cleanupDialog.close()
                }
                
                Button {
                    text: "Limpiar Ahora"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 45
                    
                    background: Rectangle {
                        color: parent.pressed ? "#E67E22" : "#F39C12"
                        radius: 8
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
                        if (executionController) {
                            executionController.clean_phantom_executions()
                        }
                        cleanupDialog.close()
                    }
                }
            }
        }
    }
    
    // Dialog para crear/editar programas
    ProgramFormDialog {
        id: programFormDialog
        
        onProgramSaved: {
            // El controlador ya actualiza la lista automáticamente
        }
    }
    
    // Dialog de ejecución de programas - AQUÍ ESTÁ LA REFERENCIA QUE FALTABA
    ProgramExecutionDialog {
        id: executionDialog
        
        onExecutionRequested: function(programId) {
            if (executionController) {
                executionController.start_execution(programId)
            }
        }
        
        onStopRequested: {
            if (executionController) {
                executionController.stop_execution()
            }
        }
    }
    
    // Dialog de confirmación para eliminar
    Dialog {
        id: deleteConfirmDialog
        
        property var programToDelete: null
        
        anchors.centerIn: parent
        width: Math.min(500, parent.width * 0.8)
        height: 250
        
        title: "Confirmar Eliminación"
        modal: true
        
        background: Rectangle {
            color: "#ECF0F1"
            radius: 12
            border.color: "#BDC3C7"
            border.width: 2
        }
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 30
            spacing: 25
            
            Text {
                Layout.fillWidth: true
                text: deleteConfirmDialog.programToDelete ? 
                      `¿Está seguro que desea eliminar el programa "${deleteConfirmDialog.programToDelete.name}"?` : ""
                font.pixelSize: 16
                color: "#2C3E50"
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            
            RowLayout {
                Layout.fillWidth: true
                spacing: 20
                
                Button {
                    text: "Cancelar"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    
                    background: Rectangle {
                        color: parent.pressed ? "#95A5A6" : "#BDC3C7"
                        radius: 8
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "#2C3E50"
                        font.pixelSize: 16
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: deleteConfirmDialog.close()
                }
                
                Button {
                    text: "Eliminar"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 50
                    
                    background: Rectangle {
                        color: parent.pressed ? "#C0392B" : "#E74C3C"
                        radius: 8
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
                        if (programController && deleteConfirmDialog.programToDelete) {
                            programController.delete_program(deleteConfirmDialog.programToDelete.id)
                        }
                        deleteConfirmDialog.close()
                    }
                }
            }
        }
    }
    
    // Dialog para mensajes
    MessageDialog {
        id: messageDialog
    }
    
    // Connections para manejar resultados de operaciones
    Connections {
        target: programController
        
        function onOperationResult(success, message) {
            messageDialog.showMessage(message, !success)
        }
    }
    
    // Connections para limpieza de ejecuciones
    Connections {
        target: executionController
        
        function onCleanupCompleted(count) {
            console.log(`Limpieza completada: ${count} ejecuciones`)
            // Refrescar lista de programas después de limpieza
            if (programController) {
                programController.refresh_programs()
            }
        }
        
        function onOperationResult(success, message) {
            messageDialog.showMessage(message, !success)
        }
        
        // Actualizar estado cuando cambia la ejecución
        function onExecutionStateChanged() {
            updateExecutionState()
        }
        
        function onExecutionStarted(executionId) {
            updateExecutionState()
        }
        
        function onExecutionFinished(executionId, status) {
            updateExecutionState()
        }
    }
    
    // Debug: Connections para monitorear cambios
    Connections {
        target: programController
        
        function onProgramsChanged() {
            console.log("Programas actualizados en QML, total:", programController ? programController.programs.length : 0)
        }
    }
}