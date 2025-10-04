# Guide de déploiement - LogiSuiEl V4

## 🚀 Déploiement en production

Ce guide vous aide à déployer LogiSuiEl en production.

## ⚠️ Prérequis de sécurité

Avant le déploiement, **modifier ces paramètres critiques**:

### Backend (`backend/app/core/config.py`)

```python
SECRET_KEY = "CHANGEZ-CETTE-CLE-AVEC-UNE-VALEUR-ALEATOIRE-LONGUE"
DATABASE_URL = "postgresql://user:password@localhost/logisuiel"  # PostgreSQL recommandé
BACKEND_CORS_ORIGINS = ["https://votre-domaine.com"]
```

### Génération d'une clé secrète sécurisée

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Créer de nouveaux comptes admin

```python
# Dans backend/app/seed.py, modifier:
admin_user = User(
    username="votre_admin",  # CHANGER
    email="admin@votre-domaine.com",
    hashed_password=get_password_hash("mot_de_passe_fort_123!"),  # CHANGER
    role=Role.ADMIN,
    is_active=True
)
```

## 🐳 Déploiement avec Docker (Recommandé)

### Dockerfile Backend

Créer `backend/Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Dockerfile Frontend

Créer `frontend/Dockerfile`:

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

Créer `docker-compose.yml` à la racine:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: logisuiel
      POSTGRES_USER: logisuiel_user
      POSTGRES_PASSWORD: changeme_secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - logisuiel

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://logisuiel_user:changeme_secure_password@db:5432/logisuiel
      SECRET_KEY: your-secret-key-here
    depends_on:
      - db
    networks:
      - logisuiel

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - logisuiel

volumes:
  postgres_data:

networks:
  logisuiel:
```

### Démarrer avec Docker Compose

```bash
docker-compose up -d
```

## 🖥️ Déploiement manuel

### Backend (avec Gunicorn)

```bash
cd backend

# Installer Gunicorn
pip install gunicorn

# Démarrer avec Gunicorn
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Frontend (avec Nginx)

```bash
cd frontend

# Build de production
npm run build

# Les fichiers sont dans dist/
# Configurer Nginx pour servir dist/
```

Configuration Nginx (`/etc/nginx/sites-available/logisuiel`):

```nginx
server {
    listen 80;
    server_name votre-domaine.com;

    # Frontend
    location / {
        root /var/www/logisuiel/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔒 HTTPS avec Let's Encrypt

```bash
# Installer Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtenir un certificat
sudo certbot --nginx -d votre-domaine.com

# Renouvellement automatique (déjà configuré)
sudo certbot renew --dry-run
```

## 📊 Base de données PostgreSQL

### Installation

```bash
sudo apt-get install postgresql postgresql-contrib
```

### Configuration

```bash
sudo -u postgres psql

CREATE DATABASE logisuiel;
CREATE USER logisuiel_user WITH PASSWORD 'votre_mot_de_passe_securise';
GRANT ALL PRIVILEGES ON DATABASE logisuiel TO logisuiel_user;
\q
```

### Migration depuis SQLite

```bash
# Exporter depuis SQLite
sqlite3 logisuiel.db .dump > dump.sql

# Importer dans PostgreSQL (après adaptation du SQL)
psql -U logisuiel_user -d logisuiel -f dump.sql
```

## 🔍 Monitoring et Logs

### Logs Backend

```bash
# Avec systemd
sudo journalctl -u logisuiel-backend -f
```

### Logs Frontend (Nginx)

```bash
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

## 🔄 Sauvegarde

### Script de sauvegarde automatique

Créer `/root/backup-logisuiel.sh`:

```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/logisuiel"

# Sauvegarde PostgreSQL
pg_dump -U logisuiel_user logisuiel > $BACKUP_DIR/db_$DATE.sql

# Compression
gzip $BACKUP_DIR/db_$DATE.sql

# Garder seulement les 30 derniers jours
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +30 -delete
```

### Crontab pour sauvegarde quotidienne

```bash
crontab -e

# Ajouter:
0 2 * * * /root/backup-logisuiel.sh
```

## 🚀 Optimisations de performance

### Backend
- Utiliser un cache Redis pour les sessions
- Activer la compression gzip
- Configurer le nombre de workers Gunicorn selon CPU

### Frontend
- Activer la compression Nginx (gzip)
- Configurer le cache des assets statiques
- Utiliser un CDN pour les fichiers statiques

### Base de données
- Créer des index sur les colonnes fréquemment requêtées
- Configurer `pg_stat_statements` pour surveiller les requêtes
- Ajuster `shared_buffers` et `work_mem` selon la RAM

## 📝 Checklist de déploiement

- [ ] Changer SECRET_KEY
- [ ] Changer mots de passe admin
- [ ] Configurer PostgreSQL
- [ ] Configurer CORS
- [ ] Activer HTTPS
- [ ] Configurer les sauvegardes
- [ ] Tester l'authentification
- [ ] Tester les imports CSV/ICS
- [ ] Configurer le monitoring
- [ ] Documenter l'architecture
- [ ] Former les utilisateurs

## 🆘 Support

En cas de problème, consulter les logs et ouvrir une issue sur GitHub avec:
- Version de l'application
- Logs d'erreur
- Configuration (sans mots de passe!)
