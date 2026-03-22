#!/bin/bash
# =============================================================================
# Ручной запуск бэкапа
# =============================================================================

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/openclaw/.openclaw/backups"

mkdir -p "$BACKUP_DIR"

echo "🚀 Запуск ручного бэкапа..."

# Git commit + push
cd /home/openclaw/.openclaw/workspace
git add -A
git commit -m "Manual backup $DATE" 2>/dev/null || echo "Нет изменений"
git push origin main 2>/dev/null || echo "GitHub не доступен"

# Архива workspace
tar -czf "$BACKUP_DIR/workspace-${DATE}.tar.gz" -C /home/openclaw/.openclaw workspace

# Архива config
tar -czf "$BACKUP_DIR/config-${DATE}.tar.gz" \
    /home/openclaw/.openclaw/openclaw.json \
    /home/openclaw/.openclaw/skills \
    /home/openclaw/.openclaw/agents \
    /home/openclaw/.openclaw/telegram \
    /home/openclaw/.openclaw/cron \
    /home/openclaw/.openclaw/devices

echo "✅ Бэкапы созданы в: $BACKUP_DIR"
ls -lh "$BACKUP_DIR"
