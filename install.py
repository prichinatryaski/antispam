import subprocess
import os
import sys
import platform

class Color:
    RED   = "\033[1;31m"
    BLUE  = "\033[1;34m"
    CYAN  = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD    = "\033[;1m"
    HI_INT_WHITE = "\e[0;97m"
    REVERSE = "\033[;7m"

def system_choice():
    system = platform.system()
    if system == "Windows":
        install_docker_windows()
    elif system == "Linux":
        install_docker_linux()
    elif system == "Darwin":  # macOS
        install_docker_macos()
    elif system == "FreeBSD":
        install_docker_freebsd()
    else:
        print(f"Неподдерживаемая операционная система: {system}")
        sys.exit(1)

def insert_api():
    api_key = input("Введите ваш API ключ: ")
    with open('api_key.txt', 'w') as secret_file:
        secret_file.write(api_key)
    return 'api_key.txt'

def model_choice():
    pass

def install_docker_windows():
    sys.stdout.write("Установка Docker на Windows...")
    url = "https://desktop.docker.com/win/stable/Docker%20Desktop%20Installer.exe"
    installer_path = "DockerInstaller.exe"
    subprocess.run(["powershell", "-Command", f"Invoke-WebRequest -Uri {url} -OutFile {installer_path}"])
    subprocess.run([installer_path])
    sys.stdout.write("Docker установлен.\n")

def install_docker_linux():
    sys.stdout.write("Установка Docker на Linux...")
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "apt-transport-https", "ca-certificates", "curl", "software-properties-common"])
    subprocess.run(["curl", "-fsSL", "https://download.docker.com/linux/ubuntu/gpg", "|", "sudo", "apt-key", "add", "-"])
    subprocess.run(["sudo", "add-apt-repository", "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"])
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", "docker-ce"])
    subprocess.run(["sudo", "usermod", "-aG", "docker", os.getlogin()])
    sys.stdout.write("Docker установлен.\n")

def install_docker_macos():
    sys.stdout.write("Установка Docker на macOS...")
    url = "https://desktop.docker.com/mac/stable/Docker.dmg"
    installer_path = "Docker.dmg"
    subprocess.run(["curl", "-L", url, "-o", installer_path])
    subprocess.run(["hdiutil", "attach", installer_path])
    subprocess.run(["sudo", "cp", "-R", "/Volumes/Docker/Docker.app", "/Applications/"])
    subprocess.run(["hdiutil", "detach", "/Volumes/Docker"])
    sys.stdout.write("Docker установлен.\n")

def install_docker_freebsd():
    sys.stdout.write("Установка Docker на FreeBSD...")
    subprocess.run(["sudo", "pkg", "install", "-y", "docker"])
    subprocess.run(["sudo", "sysrc", "docker_enable=YES"])
    subprocess.run(["sudo", "service", "docker", "start"])
    sys.stdout.write("Docker установлен.\n")

def generate_dockerfile(bot_script):
    dockerfile_content = f"""
FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

ADD . /app

WORKDIR /app

CMD ["python", "{bot_script}"]
"""
    with open('Dockerfile', 'w') as dockerfile:
        dockerfile.write(dockerfile_content)

def build_and_run_docker_container(bot_script):
    # Генерируем Dockerfile
    generate_dockerfile(bot_script)

    # Создаем docker-compose.yml
    docker_compose_content = """
services:
  bot:
    build: .
    secrets:
      - api_key

secrets:
  api_key:
    file: api_key.txt
"""
    with open('docker-compose.yml', 'w') as compose_file:
        compose_file.write(docker_compose_content)

    # Постройте Docker-образ
    subprocess.run(["docker-compose", "build"])

    # Запустите Docker-контейнер
    subprocess.run(["docker-compose", "up"])

def main():
    sys.stdout.write(f'{Color.BOLD}Добро пожаловать.\n')
    sys.stdout.write('Этот скрипт поможет установить все необходимые для работы этого бота библиотеки и приложения\n')
    try:
        if not subprocess.run(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            sys.stdout.write(f"{Color.RESET}Docker не установлен. Устанавливаем Docker...\nВнимание! После установки Docker, выйдите из терминала и запустите скрипт снова.\n")
            system_choice()
    except Exception:
        sys.stdout.write("Docker не установлен. Устанавливаем Docker...\nВнимание! После установки Docker, выйдите из терминала и запустите скрипт снова.\n")
        system_choice()

    sys.stdout.write('Собираем Dockerfile\n')

    bot_script = 'main.py'  # Замените на имя вашего скрипта бота
    secret_file = insert_api()

    # Копируем содержимое default.ini в preferences.ini
    with open('default.ini', 'r') as default_file:
        default_content = default_file.read()
    with open('preferences.ini', 'w') as preferences_file:
        preferences_file.write(default_content)

    build_and_run_docker_container(bot_script)

if __name__ == '__main__':
    main()
