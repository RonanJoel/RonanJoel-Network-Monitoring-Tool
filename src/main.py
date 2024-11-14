import time
import psutil
from scapy.all import sniff
from influxdb import InfluxDBClient
from alertas import send_email_alert, check_alerts  # Asegúrate de tener estos métodos definidos en tu módulo 'alertas'

# Configurar InfluxDB
client = InfluxDBClient(host='localhost', port=8086)
client.create_database('network_monitoring')
client.switch_database('network_monitoring')

# Función para capturar paquetes
def packet_callback(packet):
    print(f"Paquete capturado: {packet.summary()}")

# Función para guardar datos en InfluxDB
def save_to_influxdb(cpu_usage, memory_usage):
    json_body = [
        {
            "measurement": "system_metrics",
            "fields": {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage
            }
        }
    ]
    client.write_points(json_body)

# Monitoreo de tráfico de red
def monitor_traffic():
    print("Monitoreando tráfico de red... Presiona Ctrl+C para detener.")
    sniff(prn=packet_callback, store=0)  # Captura paquetes

# Monitoreo de recursos del sistema (CPU, Memoria)
def monitor_system_resources():
    print("Monitoreando recursos del sistema...")
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        print(f"Uso de CPU: {cpu_usage}% | Memoria: {memory_info.percent}%")
        save_to_influxdb(cpu_usage, memory_info.percent)  # Guardar en InfluxDB
        check_alerts(cpu_usage, memory_info.percent)  # Verificar alertas
        time.sleep(1)

if __name__ == "__main__":
    try:
        # Elegir qué monitoreo ejecutar (puedes elegir tráfico o recursos)
        monitor_traffic()  # Para monitorear el tráfico de red
        # monitor_system_resources()  # Para monitorear los recursos del sistema
    except KeyboardInterrupt:
        print("\nMonitoreo detenido.")
