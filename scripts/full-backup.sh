#!/bin/bash
# =============================================================================
# AUTOMATIC BACKUP SCRIPT
# =============================================================================
# Делает бэкапы workspace и config в local и на GitHub
# Работает через cron каждые 4 часа + по требованию
# =============================================================================

set -e  # Exit on error

BACKUP_DIR="/home/openclaw/backups"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30  # Удалять бэкапы старше этого срока

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR${NC} $1" >&2
}

# Создаем директорию
mkdir -p "$BACKUP_DIR"

log "🚀 Начинаю бэкап..."

# =============================================================================
# 1. Бэкап workspace (Git)
# =============================================================================
log "📦 Бэкап workspace (Git)..."
cd /home/openclaw/.openclaw/workspace || {
    error "Workspace не найден"
    exit 1
}

# Коммитируем изменения
git add -A
git commit -m "Auto-backup $(date '+%Y-%m-%d %H:%M') - $(hostname)" 2>/dev/null || {
    echo "📝 Нет изменений для коммита"
}

# Push на GitHub
if git push origin main 2>/dev/null; then
    log "✅ Workspace успешно запушен на GitHub"
else
    error "GitHub push failed"
fi

# =============================================================================
# 2. Создаю полный бэкап workspace
# =============================================================================
log "📦 Создаю полный бэкап workspace..."
tar -czf "$BACKUP_DIR/workspace-${DATE}.tar.gz" -C /home/openclaw/.openclaw workspace 2>/dev/null

if [ -f "$BACKUP_DIR/workspace-${DATE}.tar.gz" ]; then
    SIZE=$(du -h "$BACKUP_DIR/workspace-${DATE}.tar.gz" | cut -f1)
    log "✅ Бэкап workspace создан: $SIZE"
else
    error "Не удалось создать бэкап workspace"
fi

# =============================================================================
# 3. Бэкап config и settings
# =============================================================================
log "⚙️  Бэкап config и settings..."
tar -czf "$BACKUP_DIR/openclaw-config-${DATE}.tar.gz" \
    /home/openclaw/.openclaw/openclaw.json \
    /home/openclaw/.openclaw/skills \
    /home/openclaw/.openclaw/agents \
    /home/openclaw/.openclaw/telegram \
    /home/openclaw/.openclaw/cron \
    /home/openclaw/.openclaw/devices 2>/dev/null

if [ -f "$BACKUP_DIR/openclaw-config-${DATE}.tar.gz" ]; then
    SIZE=$(du -h "$BACKUP_DIR/openclaw-config-${DATE}.tar.gz" | cut -f1)
    log "✅ Бэкап config создан: $SIZE"
else
    error "Не удалось создать бэкап config"
fi

# =============================================================================
# 4. Создаю snapshot workspace (клон)
# =============================================================================
log "📋 Создаю snapshot workspace..."
if [ -f "$BACKUP_DIR/workspace-${DATE}.tar.gz" ]; then
    BACKUP_WORKSPACE="$BACKUP_DIR/workspace-backup-$(date +%Y%m%d_%H%M%S)"
    tar -xzf "$BACKUP_DIR/workspace-${DATE}.tar.gz" -C "$BACKUP_WORKSPACE" 2>/dev/null
    log "✅ Workspace snapshot в: $BACKUP_WORKSPACE"
fi

# =============================================================================
# 5. Чистю старые бэкапы (старше RETENTION_DAYS)
# =============================================================================
log "🧹 Чистю старые бэкапы > ${RETENTION_DAYS} дней..."
find "$BACKUP_DIR" -name "*.tar.gz" -type f -mtime +$RETENTION_DAYS -delete 2>/dev/null || true
OLD_COUNT=$(find "$BACKUP_DIR" -name "*.old.gz" -type f 2>/dev/null | wc -l)
log "✅ Старых бэкапов: $OLD_COUNT"

# =============================================================================
# 6. Проверяю последние бэкапы
# =============================================================================
log "📊 Статус бэкапов:"
ls -lh "$BACKUP_DIR"/*.tar.gz 2>/dev/null | tail -5 || echo "Бэкапы пока нет"

echo ""
log "✅ ВСЕ БЭКАПЫ ЗАВЕРШЕНЫ!"
log "📁 Все бэкапы в: $BACKUP_DIR"
log "🔗 GitHub: https://github.com/IlyaK86/workspace"
