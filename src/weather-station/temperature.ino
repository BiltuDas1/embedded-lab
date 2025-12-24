#include <DHT11.h>
#include <ESP8266WiFi.h>
#include <ESPAsyncWebServer.h>
#include <ESPAsyncTCP.h>

DHT11 dht11(D1);
const char *ssid = "ByteSpeed_30";
const char *password = "pendrive";

AsyncWebServer server(80);
AsyncWebSocket ws("/ws");  // WebSocket endpoint


// Function to send sensor data via WebSocket
void sendSensorData() {
  int temperature = 0;
  int humidity = 0;
  int result = dht11.readTemperatureHumidity(temperature, humidity);
  String json;

  if (result == 0) {
    json = "{\"temperature\": " + String(temperature) + ", \"humidity\": " + String(humidity) + "}";
  } else {
    // Print error message based on the error code.
    Serial.println(DHT11::getErrorString(result));
    json = "{\"temperature\": null, \"humidity\": null}";
  }
  ws.textAll(json);  // Broadcast data to all clients
}

// WebSocket event handler
void onWebSocketEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len) {
  if (type == WS_EVT_CONNECT) {
    Serial.printf("WebSocket Client %u connected\n", client->id());
  } else if (type == WS_EVT_DISCONNECT) {
    Serial.printf("WebSocket Client %u disconnected\n", client->id());
  }
}

// Serve HTML page
const char htmlPage[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <title>ESP8266 (DHT11)</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
</head>
<body>
  <script>
    function reboot() {
      fetch(window.location.origin + "/reboot")
    }
  </script>
  <h2>Temperature: <span id="temp">Loading...</span></h2>
  <h2>Humidity: <span id="hum">Loading...</span></h2>
  <p>Next update in <span id="timeout">5</span> seconds</p>
  <button onclick="reboot()">Reboot</button>
  <script>
    let socket = new WebSocket("ws://" + window.location.hostname + "/ws");
    socket.onmessage = function(event) {
      let data = JSON.parse(event.data);
      if (data.temperature != null) {
        document.getElementById("temp").innerHTML = data.temperature + "&deg;C";
      } else {
        document.getElementById("temp").innerText = "Not Available";
      }
      if (data.humidity != null) {
        document.getElementById("hum").innerHTML = data.humidity + "%";
      } else {
        document.getElementById("hum").innerText = "Not Available";
      }

      let seconds = 5;
      setInterval(() => {
        if (seconds < 0) {
          return;
        }
        document.getElementById("timeout").innerText = seconds;
        seconds--;
      }, 1000);
    };
    window.addEventListener("beforeunload", () => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.close();
      }
    });
  </script>
</body>
</html>
)rawliteral";

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  dht11.setDelay(1000);
  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send_P(200, "text/html", htmlPage);
  });

  server.on("/reboot", HTTP_GET, [](AsyncWebServerRequest *request) {
    request->send(200, "text/plain", "");
    ESP.restart();
  });

  ws.onEvent(onWebSocketEvent);
  server.addHandler(&ws);

  server.begin();
}

void loop() {
  // put your main code here, to run repeatedly:
  ws.cleanupClients();
  sendSensorData(); // Send data to clients
  delay(5000);
}
