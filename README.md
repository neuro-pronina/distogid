# distogid

Веб‑приложение для врачей для анализа видео пациентов с цервикальной дистонией. 
Интерфейс реализован на [Streamlit](https://streamlit.io) и поддерживает простой
пароль для доступа.

## Возможности
- загрузка видео пациента (10–30 сек);
- анализ траектории головы (демо или через OpenFace);
- отображение графиков ориентации;
- генерация отчёта в PDF и выгрузка данных в JSON.

## Подготовка
Проект использует переменные окружения:

- `STREAMLIT_PASSWORD` – пароль для входа;
- `DISTOGID_DEMO` – `1` (по умолчанию) включает демо‑режим, `0` – реальный анализ
  через OpenFace;
- `DOMAIN` – домен для Caddy и Let's Encrypt.

## Запуск локально
```bash
docker compose -f docker-compose.prod.yml up --build
```
После сборки приложение будет доступно по адресу http://localhost:8501 (через Caddy).
Все загруженные видео и отчёты сохраняются в том `data/`.

## Деплой на VPS
1. Укажите DNS записи на ваш сервер.
2. Задайте переменную `DOMAIN`, например `export DOMAIN=distogid.example.com`.
3. Запустите:
   ```bash
   STREAMLIT_PASSWORD=секрет \
   DOMAIN=distogid.example.com \
   docker compose -f docker-compose.prod.yml up -d --build
   ```
   Caddy автоматически получит сертификат Let's Encrypt.

## Режимы анализа
- **Демо** – используется по умолчанию. Генерируются синтетические данные, структура отчёта соответствует реальной.
- **Реальный анализ** – установите `DISTOGID_DEMO=0`. В контейнере будет запущен `OpenFace FeatureExtraction` по пути `/opt/OpenFace/build/bin/FeatureExtraction`.

## Структура
- `app.py` – Streamlit фронтенд;
- `analysis.py` – модуль анализа видео;
- `reports.py` – генерация PDF отчёта;
- `data/` – хранение загруженных файлов и отчётов;
- `Dockerfile`, `docker-compose.prod.yml`, `Caddyfile` – инфраструктура.

## Лицензия
MIT
