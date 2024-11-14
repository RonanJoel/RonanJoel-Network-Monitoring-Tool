import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración del servidor SMTP
def send_email_alert(subject, body):
    from_email = "tu_email@gmail.com"
    to_email = "destinatario_email@example.com"
    password = "tu_password"
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Correo de alerta enviado")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Función para verificar el uso y enviar alertas si es necesario
def check_alerts(cpu_usage, memory_usage):
    if cpu_usage > 80:
        send_email_alert("Alerta de CPU", f"El uso de CPU ha superado el 80%. Valor actual: {cpu_usage}%")
    if memory_usage > 80:
        send_email_alert("Alerta de Memoria", f"El uso de memoria ha superado el 80%. Valor actual: {memory_usage}%")

# Modificar monitoreo de recursos para incluir alertas
def monitor_system_resources():
    print("Monitoreando recursos del sistema...")
    while True:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_info = psutil.virtual_memory()
        print(f"Uso de CPU: {cpu_usage}% | Memoria: {memory_info.percent}%")
        save_to_influxdb(cpu_usage, memory_info.percent)  # Guardar en InfluxDB
        check_alerts(cpu_usage, memory_info.percent)  # Verificar alertas
        time.sleep(1)
