import QtQuick 2.15

Item {
    id: gauge
    
    property real value: 0
    property real minValue: 0
    property real maxValue: 100
    property int size: 200
    property color gaugeColor: "#3498DB"
    property color backgroundColor: "#ECF0F1"
    property color needleColor: "#E74C3C"
    
    width: size
    height: size
    
    // Validar valor antes de usar
    property real safeValue: isNaN(value) ? 0 : Math.max(minValue, Math.min(maxValue, value))
    property real valueRange: maxValue - minValue
    property real normalizedValue: valueRange > 0 ? (safeValue - minValue) / valueRange : 0
    
    // Círculo de fondo
    Rectangle {
        id: background
        anchors.centerIn: parent
        width: size
        height: size
        radius: size / 2
        color: backgroundColor
        border.color: "#BDC3C7"
        border.width: 3
    }
    
    // Arco de progreso
    Canvas {
        id: progressArc
        anchors.fill: background
        
        onPaint: {
            var ctx = getContext("2d")
            ctx.clearRect(0, 0, width, height)
            
            var centerX = width / 2
            var centerY = height / 2
            var radius = (Math.min(width, height) / 2) - 10
            
            // Ángulo inicial y final en radianes (de -135° a +135°)
            var startAngle = (225 * Math.PI) / 180   // 225°
            var endAngle = (45 * Math.PI) / 180      // 45°
            var safeNormalizedValue = isNaN(normalizedValue) ? 0 : Math.max(0, Math.min(1, normalizedValue))
            var currentAngle = startAngle + (endAngle - startAngle) * safeNormalizedValue
            
            // Dibujar arco de progreso
            ctx.beginPath()
            ctx.arc(centerX, centerY, radius, startAngle, currentAngle, false)
            ctx.lineWidth = 8
            ctx.strokeStyle = gaugeColor
            ctx.stroke()
        }
    }
    
    // Marcas de escala
    Repeater {
        model: 11
        
        Rectangle {
            // Ángulo de -135° a +135°
            property real angle: (-135 + (index / 10) * 270) * Math.PI / 180
            property real markRadius: size / 2 - 25
            
            x: size / 2 + Math.cos(angle) * markRadius - width / 2
            y: size / 2 + Math.sin(angle) * markRadius - height / 2
            
            width: index % 2 === 0 ? 3 : 2
            height: index % 2 === 0 ? 15 : 10
            color: "#7F8C8D"
            
            transform: Rotation {
                origin.x: width / 2
                origin.y: height / 2
                angle: angle * 180 / Math.PI + 90
            }
        }
    }
    
    // Etiquetas numéricas
    Repeater {
        model: 6
        
        Text {
            // Ángulo de -135° a +135°
            property real angle: (-135 + (index / 5) * 270) * Math.PI / 180
            property real labelRadius: size / 2 - 45
            property real labelValue: minValue + (index / 5) * (maxValue - minValue)
            
            x: size / 2 + Math.cos(angle) * labelRadius - width / 2
            y: size / 2 + Math.sin(angle) * labelRadius - height / 2
            
            text: Math.round(labelValue).toString()
            font.pixelSize: 12
            font.bold: true
            color: "#2C3E50"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }
    }
    
    // Aguja
    Rectangle {
        id: needle
        anchors.centerIn: parent
        width: 4
        height: size / 2 - 30
        color: needleColor
        radius: 2
        antialiasing: true
        
        transform: Rotation {
            origin.x: needle.width / 2
            origin.y: needle.height
            angle: {
                var safeNormalizedValue = isNaN(normalizedValue) ? 0 : Math.max(0, Math.min(1, normalizedValue))
                return (safeNormalizedValue * 270) - 135
            }
        }
    }
    
    // Centro de la aguja
    Rectangle {
        anchors.centerIn: parent
        width: 16
        height: 16
        radius: 8
        color: needleColor
        border.color: "#FFFFFF"
        border.width: 2
    }
    
    // Valor actual
    Text {
        anchors.centerIn: parent
        anchors.verticalCenterOffset: size / 4
        text: safeValue.toFixed(1) + " PSI"
        font.pixelSize: 16
        font.bold: true
        color: "#2C3E50"
        horizontalAlignment: Text.AlignHCenter
    }
    
    // Actualizar canvas cuando cambia el valor
    onNormalizedValueChanged: {
        if (progressArc) {
            progressArc.requestPaint()
        }
    }
}