import subprocess

def test_syntax():
    exclude_files = ['app_service.py', 'test_up.py', 'test_predict.py', 'test_syntax.py']

    flake8_command = ["flake8", ".", "--exclude=" + ",".join(exclude_files)]

    result = subprocess.run(flake8_command, capture_output=True, text=True)

    assert result.returncode == 0, "Se encontraron errores de estilo en el código"
