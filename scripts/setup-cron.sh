#!/bin/bash
# =============================================================================
# Установка crontab внутри Docker
# =============================================================================

echo "📅 Установка cron_jobs..."

# Создаю crontab для пользователя openclaw
cat > /tmp/openclaw-cron << 'EOF'
# =============================================================================
# AUTOMATIC BACKUPS - Docker
# =============================================================================
# Каждые 4 часа (для экономии ресурсов)
0 */4 * * * /home/openclaw/.openclaw/workspace/scripts/docker-backup.sh >> /home/openclaw/.openclaw/backups/cron.log 2>&1

# Каждый час (если нужно чаще)
0 * * * * /home/openclaw/.openclaw/workspace/scripts/docker-backup.sh >> /home/openclaw/.openclaw/backups/cron.log 2>&1
EOF

# Добавляю cron
crontab /tmp/openclaw-cron

echo "✅ Cron установлен!"
echo "Проверь: crontab -l"
