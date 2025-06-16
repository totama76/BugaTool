import QtQuick 2.15

Item {
    id: root
    
    property real value: 0
    property real minValue: 0
    property real maxValue: 100
    property real size: 200
    property color backgroundColor: "#34495E"
    property color foregroundColor: "#3498DB"
    property color dangerColor: "#E74C3C"
    property color textColor: "#ECF0F1"
    
    width: size
    height: size
    
    // Fondo del gauge
    Rectangle {
        id: background
        anchors.fill: parent
        color: "transparent"
        border.color: backgroundColor
        border.width: 8
        radius: width / 2
        
        // Líneas de marcas
        Repeater {
            model: 11
            
            Rectangle {
                width: 2
                height: 15
                color: root.textColor
                opacity: 0.7
                
                property real angle: (index / 10) * 240 - 120
                
                transform: [
                    Rotation {
                        origin.x: 1
                        origin.y: height
                        angle: parent.angle
                    }
                ]
                
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: parent.top
                anchors.topMargin: 4
            }
        }
    }
    
    // Arco de progreso
    Canvas {
        id: progressArc
        anchors.fill: parent
        
        onPaint: {
            var ctx = getContext("2d");
            ctx.reset();
            
            var centerX = width / 2;
            var centerY = height / 2;
            var radius = (width - 20) / 2;
            
            // Calcular ángulo basado en el valor
            var normalizedValue = (root.value - root.minValue) / (root.maxValue - root.minValue);
            var angle = normalizedValue * 240 * Math.PI / 180;
            var startAngle = -120 * Math.PI / 180;
            
            // Dibujar arco de progreso
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, startAngle, startAngle + angle);
            ctx.lineWidth = 8;
            ctx.strokeStyle = root.value > (root.maxValue * 0.8) ? root.dangerColor : root.foregroundColor;
            ctx.stroke();
        }
        
        Connections {
            target: root
            function onValueChanged() { progressArc.requestPaint(); }
        }
    }
    
    // Aguja central
    Rectangle {
        id: needle
        width: 4
        height: root.size * 0.35
        color: root.value > (root.maxValue * 0.8) ? root.dangerColor : root.foregroundColor
        radius: 2
        
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.verticalCenter
        anchors.bottomMargin: -2
        
        transformOrigin: Item.Bottom
        
        rotation: {
            var normalizedValue = (root.value - root.minValue) / (root.maxValue - root.minValue);
            return -120 + (normalizedValue * 240);
        }
        
        Behavior on rotation {
            NumberAnimation { duration: 500; easing.type: Easing.OutQuad }
        }
    }
    
    // Centro del gauge
    Rectangle {
        width: 12
        height: 12
        radius: 6
        color: root.textColor
        anchors.centerIn: parent
    }
    
    // Texto del valor
    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: parent.height * 0.25
        
        text: root.value.toFixed(1)
        font.pixelSize: root.size * 0.12
        font.bold: true
        color: root.textColor
        horizontalAlignment: Text.AlignHCenter
    }
}