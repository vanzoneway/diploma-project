# Cab Aggregator Application

Проект представляет собой распределенную микросервисную систему для агрегации поездок, включающую сервисы для управления пользователями (водителями и пассажирами), обработки поездок, начисления рейтингов, регистрации через Keycloak и систему уведомлений.

## Основные компоненты
Система состоит из следующих функциональных модулей:
- **Инфраструктурные сервисы**: API Gateway, Discovery Service (Eureka).
- **Бизнес-сервисы**: Driver, Passenger, Ride, Rating, Registration, Notification.
- **Инструменты мониторинга**: Grafana, Loki, VictoriaMetrics, Tempo, Kafka UI.
- **Хранилища**: PostgreSQL, Redis, MinIO, Kafka, Zookeeper, Keycloak.

## Предварительные требования
Для запуска системы на локальной машине необходимо иметь:
* [Docker](https://www.docker.com/get-started)
* [Docker Compose](https://docs.docker.com/compose/install/)
* JDK 21+

## Запуск проекта

Запуск всей инфраструктуры и микросервисов осуществляется из корневой директории проекта с помощью Docker Compose.

### 1. Подготовка конфигурации
Убедитесь, что в директории `docker/` настроены все необходимые переменные окружения. При необходимости создайте файл `.env` в корне проекта для передачи секретных ключей (например, `KEYCLOAK_ADMIN_PASSWORD`).

### 2. Сборка и запуск
Для сборки образов всех сервисов и запуска контейнеров выполните команду:

```bash
docker-compose -f docker/docker-compose.yml up -d --build
```

### 3. Остановка системы
Для остановки всех контейнеров и очистки сетевых ресурсов выполните:

```bash
docker-compose -f docker/docker-compose.yml down
```

Для полной очистки (включая удаление данных в томах БД и Kafka) используйте:

```bash
docker-compose -f docker/docker-compose.yml down -v
```

## Доступ к сервисам после запуска
После успешного запуска системы, следующие инструменты будут доступны для работы:

* **API Gateway (Точка входа):** `http://localhost:8080/api/v1`
* **Swagger UI (Документация API):** `http://localhost:8080/swagger-ui.html`
* **Grafana (Мониторинг):** `http://localhost:3000`
* **Kafka UI (Управление брокером):** `http://localhost:8079`
* **Keycloak (Аутентификация):** `http://localhost:8090`
* **VictoriaMetrics (Метрики):** `http://localhost:8428`

## Сборка отдельных модулей
Если требуется пересборка только одного из сервисов (например, `driver-service`), вы можете использовать Gradle из директории соответствующего сервиса:

```bash
cd driver-service
./gradlew clean build -x test
```

## Инструкция по E2E-тестированию
Для запуска сквозного (end-to-end) тестирования используйте отдельный compose-файл:

```bash
docker-compose -f docker/docker-compose-e2e.yml up -d
```
