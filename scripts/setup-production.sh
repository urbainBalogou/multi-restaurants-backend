#!/bin/bash
# Script d'installation initiale en production

set -e

echo "🎯 Installation du projet Multi-Restaurants Backend"

# Variables
PROJECT_NAME="multi-restaurants-backend"
PROJECT_DIR="/var/www/$PROJECT_NAME"
DOMAIN="your-domain.com"

# Vérifier que le script est exécuté en tant que root
if [[ $EUID -ne 0 ]]; then
   echo "❌ Ce script doit être exécuté en tant que root (sudo)"
   exit 1
fi

# Mise à jour du système
echo "📦 Mise à jour du système..."
apt update && apt upgrade -y

# Installation des dépendances système
echo "🔧 Installation des dépendances système..."
apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib \
    nginx \
    redis-server \
    git \
    supervisor \
    certbot python3-certbot-nginx

# Création du répertoire projet
echo "📁 Création du répertoire projet..."
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Clonage du projet
echo "📥 Clonage du repository..."
git clone https://github.com/votre-username/$PROJECT_NAME.git .

# Création de l'environnement virtuel
echo "🐍 Création de l'environnement virtuel Python..."
python3.11 -m venv venv
source venv/bin/activate

# Installation des dépendances Python
echo "📦 Installation des dépendances Python..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Configuration de la base de données PostgreSQL
echo "🗄️ Configuration de PostgreSQL..."
sudo -u postgres psql <<EOF
CREATE DATABASE multi_restaurants_db;
CREATE USER multi_restaurants_user WITH PASSWORD 'changeme';
ALTER ROLE multi_restaurants_user SET client_encoding TO 'utf8';
ALTER ROLE multi_restaurants_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE multi_restaurants_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE multi_restaurants_db TO multi_restaurants_user;
\q
EOF

# Copie du fichier .env
echo "⚙️ Configuration des variables d'environnement..."
cp .env.example .env
echo "⚠️ IMPORTANT: Modifiez le fichier .env avec vos vraies valeurs !"
echo "📝 nano $PROJECT_DIR/.env"

# Migrations
echo "🔄 Application des migrations..."
python manage.py migrate

# Collecte des fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput

# Création du superuser (interactif)
echo "👤 Création du superuser..."
python manage.py createsuperuser

# Configuration de Gunicorn avec systemd
echo "🚀 Configuration de Gunicorn..."
cat > /etc/systemd/system/multi-restaurants-gunicorn.service <<EOF
[Unit]
Description=multi-restaurants gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn \\
    --config $PROJECT_DIR/gunicorn_config.py \\
    multi_restaurants.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Configuration de Celery Worker avec systemd
echo "🎯 Configuration de Celery Worker..."
cat > /etc/systemd/system/multi-restaurants-celery.service <<EOF
[Unit]
Description=multi-restaurants celery worker
After=network.target redis.service

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/celery -A multi_restaurants worker -l info --detach

[Install]
WantedBy=multi-user.target
EOF

# Configuration de Celery Beat avec systemd
echo "⏰ Configuration de Celery Beat..."
cat > /etc/systemd/system/multi-restaurants-celery-beat.service <<EOF
[Unit]
Description=multi-restaurants celery beat
After=network.target redis.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/celery -A multi_restaurants beat -l info

[Install]
WantedBy=multi-user.target
EOF

# Permissions
echo "🔒 Configuration des permissions..."
chown -R www-data:www-data $PROJECT_DIR

# Démarrage des services
echo "▶️ Démarrage des services..."
systemctl daemon-reload
systemctl enable multi-restaurants-gunicorn
systemctl enable multi-restaurants-celery
systemctl enable multi-restaurants-celery-beat
systemctl enable redis-server
systemctl enable nginx

systemctl start multi-restaurants-gunicorn
systemctl start multi-restaurants-celery
systemctl start multi-restaurants-celery-beat
systemctl start redis-server

# Configuration de Nginx (déjà créée dans nginx/conf.d/app.conf)
echo "🌐 Configuration de Nginx..."
ln -sf $PROJECT_DIR/nginx/conf.d/app.conf /etc/nginx/sites-available/$PROJECT_NAME
ln -sf /etc/nginx/sites-available/$PROJECT_NAME /etc/nginx/sites-enabled/

# Test de la configuration Nginx
nginx -t

# Redémarrage de Nginx
systemctl restart nginx

# Configuration SSL avec Let's Encrypt
echo "🔐 Configuration SSL..."
echo "Voulez-vous configurer SSL avec Let's Encrypt? (y/n)"
read -r SETUP_SSL

if [[ $SETUP_SSL == "y" ]]; then
    certbot --nginx -d $DOMAIN -d www.$DOMAIN
fi

echo "✅ Installation terminée!"
echo "🌐 Votre application est accessible sur: https://$DOMAIN"
echo "🔍 Vérification des services:"
systemctl status multi-restaurants-gunicorn --no-pager
systemctl status multi-restaurants-celery --no-pager

echo "📝 N'oubliez pas de configurer:"
echo "  - Les variables d'environnement dans .env"
echo "  - Les credentials Stripe, AWS, etc."
echo "  - La configuration email SMTP"
