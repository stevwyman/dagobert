# Project Dagobert

## setting up the environment

```sh
python3 -m venv ~/development/dagobert-env/
. ~/development/dagobert-env/bin/activate

brew install mysql-client pkg-config
export PKG_CONFIG_PATH="$(brew --prefix)/opt/mysql-client/lib/pkgconfig"

pip install -r requirements.txt

python -m django --version
```

```sh
django-admin startproject alpha .
```

now you can check if your project is working http://127.0.0.1:8000

### creating the app

we can now add the 

inside this project alpha, we can now create an app - beta

```sh
python manage.py startapp beta
```

```sh
podman compose --file compose-dev.yaml up --detach
```

python manage.py migrate

docker build -t stevwyman/market_analysis:local .

podman build -t dagobert:local .

### database details

command: --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci --max-connections=1000