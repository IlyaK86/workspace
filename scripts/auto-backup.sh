#!/bin/bash
# Автоматический бэкап workspace и config

BACKUP_DIR="/home/openclaw/backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_DIR"

# Бэкап workspace
echo "📦 Бэкап workspace..."
tar -czf "$BACKUP_DIR/workspace-${DATE}.tar.gz" /home/openclaw/.openclaw/workspace/

# Бэкап config
echo "⚙️  Бэкап config..."
tar -czf "$BACKUP_DIR/openclaw-config-${DATE}.tar.gz" /home/openclaw/.openclaw/{openclaw.json,skills,agents,telegram,cron,devices}

# Бэкап на GitHub
echo "🔧 Бэкап на GitHub..."
cd /home/openclaw/.openclaw/workspace
git add -A
git commit -m "Auto-backup $DATE" 2>/dev/null || echo "No changes"
git push origin main 2>/dev/null

echo "✅ Бэкап completed!"
echo "Файлы в: $BACKUP_DIR"
