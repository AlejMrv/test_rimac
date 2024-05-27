import subprocess
import time
import requests

def test_docker_build_and_run():

    build_process = subprocess.run(["docker", "build", "-t", "model_service", "."]
                                   , capture_output=True
                                   , text=True)

    #build_process.wait()
    assert build_process.returncode == 0, f"La construccion de la imagen Docker fallo"


    subprocess.run(["docker", "run", "-d", "-p", "8080:8080", "model_service"]
                   , capture_output=True
                   , text=True)

    # Esperar hasta que el contenedor este en funcionamiento
    container_running = False
    for _ in range(10): 
        time.sleep(1) 
        ps_result = subprocess.run(["docker", "ps"]
                                   , capture_output=True
                                   , text=True)
        if "model_service" in ps_result.stdout:
            container_running = True
            break

    assert container_running, "El contenedor Docker no se inicio correctamente"


    # Esperar a que el contenedor esté completamente en funcionamiento
    time.sleep(3) 

    response = requests.get("http://localhost:8080/")
    assert response.status_code == 200, "El servicio no esta en funcionamiento"
