import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    id: programFormDialog
    
    signal programSaved()
    
    property bool isEditMode: false
    property var currentProgram: null
    
    anchors.centerIn: parent
    width: Math.min(500, parent.width * 0.9)
    height: Math.min(600, parent.height * 0.9)
    
    title: isEditMode ? "Editar Programa" : "Nuevo Programa"
    modal: true
    
    background: Rectangle {
        color: "#ECF0F1"
        radius: 10
        border.color: "#BDC3C7"
        border.width: 2
    }
    
    ScrollView {
        anchors.fill: parent
        
        ColumnLayout {
            width: programFormDialog.width - 40
            spacing: 20
            anchors.margins: 20
            
            // Nombre del programa
            Column {
                Layout.fillWidth: true
                spacing: 5
                
                Text {
                    text: "Nombre del Programa *"
                    font.pixelSize: 14
                    font.bold: true
                    color: "#2C3E50"
                }
                
                TextField {
                    id: nameField
                    width: parent.width
                    height: 40
                    font.pixelSize: 14
                    placeholderText: "Ingrese el nombre del programa"
                    
                    background: Rectangle {
                        color: "#FFFFFF"
                        border.color: parent.activeFocus ? "#3498DB" : "#BDC3C7"
                        border.width: 2
                        radius: 8
                    }
                }
            }
            
            // Descripción
            Column {
                Layout.fillWidth: true
                spacing: 5
                
                Text {
                    text: "Descripción"
                    font.pixelSize: 14
                    font.bold: true
                    color: "#2C3E50"
                }
                
                ScrollView {
                    width: parent.width
                    height: 80
                    
                    TextArea {
                        id: descriptionField
                        placeholderText: "Descripción opcional del programa"
                        font.pixelSize: 14
                        wrapMode: TextArea.Wrap
                        
                        background: Rectangle {
                            color: "#FFFFFF"
                            border.color: parent.activeFocus ? "#3498DB" : "#BDC3C7"
                            border.width: 2
                            radius: 8
                        }
                    }
                }
            }
            
            // Presiones
            RowLayout {
                Layout.fillWidth: true
                spacing: 20
                
                Column {
                    Layout.fillWidth: true
                    spacing: 5
                    
                    Text {
                        text: "Presión Mínima (PSI) *"
                        font.pixelSize: 14
                        font.bold: true
                        color: "#2C3E50"
                    }
                    
                    SpinBox {
                        id: minPressureField
                        width: parent.width
                        height: 40
                        from: 0
                        to: 200
                        stepSize: 1
                        value: 10
                        
                        background: Rectangle {
                            color: "#FFFFFF"
                            border.color: "#BDC3C7"
                            border.width: 2
                            radius: 8
                        }
                    }
                }
                
                Column {
                    Layout.fillWidth: true
                    spacing: 5
                    
                    Text {
                        text: "Presión Máxima (PSI) *"
                        font.pixelSize: 14
                        font.bold: true
                        color: "#2C3E50"
                    }
                    
                    SpinBox {
                        id: maxPressureField
                        width: parent.width
                        height: 40
                        from: 1
                        to: 200
                        stepSize: 1
                        value: 80
                        
                        background: Rectangle {
                            color: "#FFFFFF"
                            border.color: "#BDC3C7"
                            border.width: 2
                            radius: 8
                        }
                    }
                }
            }
            
            // Tiempos
            RowLayout {
                Layout.fillWidth: true
                spacing: 20
                
                Column {
                    Layout.fillWidth: true
                    spacing: 5
                    
                    Text {
                        text: "Tiempo a Presión Mín. (min) *"
                        font.pixelSize: 14
                        font.bold: true
                        color: "#2C3E50"
                    }
                    
                    SpinBox {
                        id: timeToMinField
                        width: parent.width
                        height: 40
                        from: 1
                        to: 120
                        stepSize: 1
                        value: 5
                        
                        background: Rectangle {
                            color: "#FFFFFF"
                            border.color: "#BDC3C7"
                            border.width: 2
                            radius: 8
                        }
                    }
                }
                
                Column {
                    Layout.fillWidth: true
                    spacing: 5
                    
                    Text {
                        text: "Duración Total (min) *"
                        font.pixelSize: 14
                        font.bold: true
                        color: "#2C3E50"
                    }
                    
                    SpinBox {
                        id: durationField
                        width: parent.width
                        height: 40
                        from: 1
                        to: 1440
                        stepSize: 1
                        value: 30
                        
                        background: Rectangle {
                            color: "#FFFFFF"
                            border.color: "#BDC3C7"
                            border.width: 2
                            radius: 8
                        }
                    }
                }
            }
            
            // Botones
            RowLayout {
                Layout.fillWidth: true
                Layout.topMargin: 20
                
                Button {
                    text: "Cancelar"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 45
                    
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
                    
                    onClicked: programFormDialog.close()
                }
                
                Button {
                    text: isEditMode ? "Actualizar" : "Crear"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 45
                    
                    enabled: nameField.text.trim() !== ""
                    
                    background: Rectangle {
                        color: parent.enabled ? 
                               (parent.pressed ? "#27AE60" : "#2ECC71") : "#95A5A6"
                        radius: 8
                        border.color: parent.enabled ? "#229954" : "#7F8C8D"
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
                    
                    onClicked: saveProgram()
                }
            }
        }
    }
    
    // Funciones
    function openForCreate() {
        isEditMode = false
        currentProgram = null
        clearForm()
        open()
    }
    
    function openForEdit(program) {
        isEditMode = true
        currentProgram = program
        loadProgramData(program)
        open()
    }
    
    function clearForm() {
        nameField.text = ""
        descriptionField.text = ""
        minPressureField.value = 10
        maxPressureField.value = 80
        timeToMinField.value = 5
        durationField.value = 30
    }
    
    function loadProgramData(program) {
        nameField.text = program.name || ""
        descriptionField.text = program.description || ""
        minPressureField.value = program.min_pressure || 10
        maxPressureField.value = program.max_pressure || 80
        timeToMinField.value = program.time_to_min_pressure || 5
        durationField.value = program.program_duration || 30
    }
    
    function saveProgram() {
        if (!programController) return
        
        if (isEditMode && currentProgram) {
            programController.update_program(
                currentProgram.id,
                nameField.text,
                descriptionField.text,
                minPressureField.value,
                maxPressureField.value,
                timeToMinField.value,
                durationField.value
            )
        } else {
            programController.create_program(
                nameField.text,
                descriptionField.text,
                minPressureField.value,
                maxPressureField.value,
                timeToMinField.value,
                durationField.value
            )
        }
        
        programSaved()
        close()
    }
}