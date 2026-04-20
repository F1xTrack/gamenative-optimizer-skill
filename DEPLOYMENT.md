# GameNative Optimizer Deployment Guide

Этот репозиторий теперь является официальным расширением для Gemini CLI.

## 🚀 Быстрая установка
Вы можете установить все навыки и MCP-сервер одной командой:

```bash
gemini extensions install https://github.com/F1xTrack/gamenative-optimizer-skill
```

## ⚙️ После установки
Чтобы MCP-сервер заработал, необходимо создать виртуальное окружение и установить зависимости внутри папки расширения:

```bash
cd ~/.gemini/extensions/gamenative-optimizer-skill
python3 -m venv venv
./venv/bin/pip install mcp
```

## 📂 Структура расширения
- **skills/**: Набор из 6 специализированных навыков.
- **gamenative-mcp/**: Сервер для связи с Android через ADB.
- **GEMINI.md**: Базовый контекст и правила для ИИ-агента.

## 🛠 Ручная настройка (если не через расширение)
Если вы хотите использовать только MCP-сервер без установки расширения, добавьте его в `settings.json`:
```json
{
  "mcpServers": {
    "gamenative": {
      "command": "/path/to/venv/bin/python",
      "args": ["/path/to/gamenative-mcp/mcp_server.py"]
    }
  }
}
```
