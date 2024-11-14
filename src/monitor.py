import psutil
import time
from scapy.all import sniff

# Función para capturar paquetes
def packet_callback(packet):
    print(f"Paquete capturado: {packet.summary()}")

# Monitorear tráfico de red
def monitor_traffic():
    print("Monitoreando tráfico de red... Presiona Ctrl+C para detener.")
    sniff(prn=packet_callback, store=0)  # Captura paquetes

# Monitoreo de recursos (CPU, Memoria)
def monitor_system_resources():
    print("Monitoreando recursos del sistema...")
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        print(f"Uso de CPU: {cpu_usage}% | Memoria: {memory_info.percent}%")
        time.sleep(1)  # Actualiza cada segundo

if __name__ == "__main__":
    # Aquí puedes elegir cuál funcionalidad ejecutar
    try:
        monitor_traffic()  # Monitoreo de tráfico
        # monitor_system_resources()  # Alternativamente, puedes monitorear los recursos del sistema
    except KeyboardInterrupt:
        print("\nMonitoreo detenido.")
