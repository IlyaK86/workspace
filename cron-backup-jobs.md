# =============================================================================
# CRON JOBS FOR AUTOMATIC BACKUPS
# =============================================================================
# Добавь эти строки в /etc/cron.d/openclaw-backups или через crontab -e
# =============================================================================

# Ежедневные бэкапы в 2:00 и 14:00 UTC
0 2 * * * /home/openclaw/.openclaw/workspace/scripts/full-backup.sh >> /home/openclaw/backups/cron.log 2>&1
0 14 * * * /home/openclaw/.openclaw/workspace/scripts/full-backup.sh >> /home/openclaw/backups/cron.log 2>&1

# Ежечасные бэкапы в каждую минуту на 5 
*/5 * * * * /home/openclaw/.openclaw/workspace/scripts/full-backup.sh >> /home/openclaw/backups/cron.log 2>&1

# Недельные бэкапы каждый понедельник в 3:00
0 3 * * 1 /home/openclaw/.openclaw/workspace/scripts/full-backup.sh >> /home/openclaw/backups/cron.log 2>&1

# Ежемесячные полные бэкапы 1 числа в 4:00
0 4 1 * * /home/openclaw/.openclaw/workspace/scripts/full-backup.sh >> /home/openclaw/backups/cron.log 2>&1

# =============================================================================
# УСТАНОВКА CRON:
# =============================================================================
# 1. crontab -e
# 2. Добавь строки выше
# 3. Или создай файл /etc/cron.d/openclaw-backups с правами 644
# =============================================================================
