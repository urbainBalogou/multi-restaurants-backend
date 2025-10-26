#!/bin/bash
# Script de déploiement production

set -e

echo "🚀 Démarrage du déploiement..."

# Variables
PROJECT_DIR="/var/www/multi-restaurants-backend"
VENV_DIR="$PROJECT_DIR/venv"

# Backup de la base de données
echo "📦 Backup de la base de données..."
python manage.py dumpdata --natural-foreign --natural-primary \
    --exclude=contenttypes --exclude=auth.Permission \
    --indent 2 > backup_$(date +%Y%m%d_%H%M%S).json

# Pull du code
echo "📥 Récupération du code..."
git pull origin main

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source $VENV_DIR/bin/activate

# Installation des dépendances
echo "📦 Installation des dépendances..."
pip install -r requirements.txt --upgrade

# Migrations
echo "🗄️ Application des migrations..."
python manage.py migrate --noinput

# Collecte des fichiers statiques
echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --clear

# Redémarrage des services
echo "🔄 Redémarrage des services..."
sudo systemctl restart multi-restaurants-gunicorn
sudo systemctl restart multi-restaurants-celery
sudo systemctl restart multi-restaurants-celery-beat
sudo systemctl restart nginx

echo "✅ Déploiement terminé avec succès!"
echo "🔍 Vérification de l'état des services..."
sudo systemctl status multi-restaurants-gunicorn --no-pager
