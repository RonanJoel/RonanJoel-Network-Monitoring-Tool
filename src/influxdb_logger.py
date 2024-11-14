from influxdb import InfluxDBClient

# Configura el cliente de InfluxDB
client = InfluxDBClient(host='localhost', port=8086)
client.create_database('network_monitoring')
client.switch_database('network_monitoring')

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

# Modificar el monitoreo de recursos para guardar en la base de datos
def monitor_system_resources():
    print("Monitoreando recursos del sistema...")
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        print(f"Uso de CPU: {cpu_usage}% | Memoria: {memory_info.percent}%")
        save_to_influxdb(cpu_usage, memory_info.percent)  # Guardar en InfluxDB
        time.sleep(1)

if __name__ == "__main__":
    try:
        monitor_system_resources()  # Empieza a monitorear y guardar los datos
    except KeyboardInterrupt:
        print("\nMonitoreo detenido.")

