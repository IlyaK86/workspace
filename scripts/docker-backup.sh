#!/bin/bash
# =============================================================================
# DOCKER-AWARE AUTO-BACKUP
# =============================================================================
# Бэкапит workspace и config ВНУТРИ контейнера
# Работает через cron внутри Docker
# =============================================================================

set -e

BACKUP_DIR="/home/openclaw/.openclaw/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

echo "🚀 Docker Backup начался [$DATE]"

# 1. Git commit workspace
cd /home/openclaw/.openclaw/workspace
git add -A
git commit -m "Docker auto-backup $DATE" 2>/dev/null || echo "Нет изменений"
git push origin main 2>/dev/null || echo "GitHub push failed"

# 2. Создаю full backup
echo "📦 Backup workspace..."
tar -czf "$BACKUP_DIR/workspace-${DATE}.tar.gz" -C /home/openclaw/.openclaw workspace

# 3. Backup config
echo "⚙️ Backup config..."
tar -czf "$BACKUP_DIR/openclaw-config-${DATE}.tar.gz" \
    /home/openclaw/.openclaw/openclaw.json \
    /home/openclaw/.openclaw/skills \
    /home/openclaw/.openclaw/agents \
    /home/openclaw/.openclaw/telegram \
    /home/openclaw/.openclaw/cron \
    /home/openclaw/.openclaw/devices

# 4. Удаляю старые бэкапы
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +$RETENTION_DAYS -delete

# 5. Статус
echo "📊 Последние бэкапы:"
ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -3

echo "✅ Backup завершен!"
echo "📁 Файлы в: $BACKUP_DIR"
