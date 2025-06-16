import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: programManagementView
    
    // Señales
    signal backToMain()
    
    gradient: Gradient {
        GradientStop { position: 0.0; color: "#2C3E50" }
        GradientStop { position: 1.0; color: "#34495E" }
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20
        
        // Header
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 60
            color: "transparent"
            border.color: "#3498DB"
            border.width: 2
            radius: 10
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 15
                
                Button {
                    text: "← Volver"
                    
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
                    
                    onClicked: backToMain()
                }
                
                Text {
                    text: "Gestión de Programas"
                    font.pixelSize: 20
                    font.bold: true
                    color: "#ECF0F1"
                    Layout.fillWidth: true
                    horizontalAlignment: Text.AlignHCenter
                }
                
                Button {
                    text: "Nuevo Programa"
                    visible: programController ? programController.canManage : false
                    
                    background: Rectangle {
                        color: parent.pressed ? "#27AE60" : "#2ECC71"
                        radius: 6
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
                        programFormDialog.openForCreate()
                    }
                }
            }
        }
        
        // Barra de búsqueda
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            color: "#ECF0F1"
            radius: 8
            border.color: "#BDC3C7"
            border.width: 1
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 10
                spacing: 10
                
                TextField {
                    id: searchField
                    Layout.fillWidth: true
                    placeholderText: "Buscar programas..."
                    font.pixelSize: 14
                    
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
                    implicitWidth: 40
                    
                    background: Rectangle {
                        color: parent.pressed ? "#2980B9" : "#3498DB"
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 16
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
                    implicitWidth: 40
                    
                    background: Rectangle {
                        color: parent.pressed ? "#C0392B" : "#E74C3C"
                        radius: 4
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "white"
                        font.pixelSize: 12
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
            }
        }
        
        // Lista de programas
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#ECF0F1"
            radius: 10
            border.color: "#BDC3C7"
            border.width: 1
            
            ScrollView {
                anchors.fill: parent
                anchors.margins: 10
                
                ListView {
                    id: programListView
                    model: programController ? programController.programs : []
                    spacing: 10
                    
                    delegate: ProgramListItem {
                        width: programListView.width
                        programData: modelData
                        canManage: programController ? programController.canManage : false
                        
                        onEditRequested: {
                            programFormDialog.openForEdit(programData)
                        }
                        
                        onDeleteRequested: {
                            deleteConfirmDialog.programToDelete = programData
                            deleteConfirmDialog.open()
                        }
                        
                        onExecuteRequested: {
                            // TODO: Implementar ejecución de programa
                            messageDialog.showMessage("Funcionalidad de ejecución próximamente", false)
                        }
                    }
                    
                    // Mensaje cuando no hay programas
                    Text {
                        anchors.centerIn: parent
                        text: searchField.text !== "" ? "No se encontraron programas" : "No hay programas creados"
                        font.pixelSize: 16
                        color: "#7F8C8D"
                        visible: programListView.count === 0
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
    
    // Dialog de confirmación para eliminar
    Dialog {
        id: deleteConfirmDialog
        
        property var programToDelete: null
        
        anchors.centerIn: parent
        width: Math.min(400, parent.width * 0.8)
        height: 200
        
        title: "Confirmar Eliminación"
        modal: true
        
        background: Rectangle {
            color: "#ECF0F1"
            radius: 10
            border.color: "#BDC3C7"
            border.width: 2
        }
        
        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 20
            
            Text {
                Layout.fillWidth: true
                text: deleteConfirmDialog.programToDelete ? 
                      `¿Está seguro que desea eliminar el programa "${deleteConfirmDialog.programToDelete.name}"?` : ""
                font.pixelSize: 14
                color: "#2C3E50"
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
            }
            
            RowLayout {
                Layout.fillWidth: true
                
                Button {
                    text: "Cancelar"
                    Layout.fillWidth: true
                    
                    background: Rectangle {
                        color: parent.pressed ? "#95A5A6" : "#BDC3C7"
                        radius: 6
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        color: "#2C3E50"
                        font.pixelSize: 14
                        font.bold: true
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: deleteConfirmDialog.close()
                }
                
                Button {
                    text: "Eliminar"
                    Layout.fillWidth: true
                    
                    background: Rectangle {
                        color: parent.pressed ? "#C0392B" : "#E74C3C"
                        radius: 6
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
}