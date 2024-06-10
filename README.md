# The_leprechaun

**Описание проекта:**

Финансовый ассистент — это веб-приложение, которое позволяет пользователям управлять своими личными финансами. Система предлагает функционал для отслеживания доходов и расходов, а также анализ финансового состояния через различные отчеты и диаграммы. Приложение поддерживает работу с несколькими валютами и актуальными валютными курсами. 💰🍀

## Основные функции

- Ведение личного бюджета
  - Отслеживание доходов и расходов

- Многовалютность
  - Управление накоплениями в разных валютах

- Цели накоплений
  - Создание финансовых целей
  - Отслеживание прогресса

- История операций
  - Просмотр и фильтрация операций за выбранный промежуток времени
  - Возможность скачать файл с историей транзакций


**Цель проекта:**

Проект "Лепрекон" создан с целью помочь пользователям эффективно управлять своими финансами, осуществлять контроль доходов и расходов, а также достигать своих финансовых целей.</br> Я стремлюсь предоставить интуитивно понятный инструмент для управления личными финансами, который поможет пользователям достичь финансовой стабильности и благополучия.

![Screenshot_1](https://github.com/Apollo297/the_leprechaun/assets/138869794/b4d3f7bc-c0ec-452e-95e1-d4bb1b4280d4)
---
![Screenshot_2](https://github.com/Apollo297/the_leprechaun/assets/138869794/83428550-c15b-41d9-815a-639df6df32b4)
---
![Screenshot_3](https://github.com/Apollo297/the_leprechaun/assets/138869794/34858d9b-4711-491b-bec6-3138d7236c56)
---
![Screenshot_4](https://github.com/Apollo297/the_leprechaun/assets/138869794/c76080e1-aab3-4161-a514-1c2d00da39e0)
---
![Screenshot_5](https://github.com/Apollo297/the_leprechaun/assets/138869794/7383263d-779d-4438-b6b5-91cac0f2dea3)
---
![Screenshot_6](https://github.com/Apollo297/the_leprechaun/assets/138869794/54e56bb1-040d-479a-a8b7-5b12fa04e35a)
---

| Адрес | Описание |
|-------------|-------------|
| 127.0.0.1   | Главная страница   |
| 127.0.0.1/admin/   | Панель администратора  |

### Используемые технологии:
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![image](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![image](https://img.shields.io/badge/VSCode-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![image](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)
![image](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white)

## Установка:

Если Python не установлен, скачайте и установите его с [официального сайта](https://www.python.org/downloads/).

### Системные требования

- **Версия Python**: 3.9 или выше
- **Операционная система**: Windows / macOS / Linux

Клонировать репозиторий и перейти в него в командной строке:
```python
git clone git@github.com:Apollo297/the_leprechaun.git
```
```python
cd the_leprechaun
```
Cоздать и активировать виртуальное окружение:
```python
python -m venv env
```
```python
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```python
python -m pip install --upgrade pip
```
```python
pip install -r requirements.txt
```
Создать файл .env и заполнить его своими данными:
```
POSTGRES_USER=[имя_пользователя_базы]
POSTGRES_PASSWORD=[пароль_к_базе]
POSTGRES_DB= [имя_базы_данных]
DB_PORT=[порт_соединения_к_базе]
DB_HOST=[db]
SECRET_KEY=[ключ]
DEBUG=[значение]
```

**Установите PostgreSQL с [официального сайта](https://www.postgresql.org/download/windows/).**</br>
Откройте командную строку Windows (Cmd) или PowerShell.
Запустите psql
```cmd
psql -U postgres
```
Вас попросят ввести пароль для пользователя PostgreSQL.</br>
Выполните команды: После входа в psql, вы можете выполнять следующие команды одну за другой.</br>
```sql
CREATE DATABASE <имя_базы_данных>;
```
```sql
CREATE ROLE <имя_пользователя_базы> with password '<пароль_к_базе>';
```
```sql
ALTER ROLE "<имя_пользователя_базы>" WITH LOGIN;
```
```sql
GRANT ALL PRIVILEGES ON DATABASE "<имя_базы_данных>" to <имя_пользователя_базы>;
```
```sql
ALTER USER <имя_пользователя_базы> CREATEDB;
```
```sql
\c <имя_базы_данных>
```
```sql
GRANT ALL ON schema public TO <имя_пользователя_базы>;
```
Выполнить миграции:
```python
python manage.py migrate
```
Создать суперпользователя:
```python
python manage.py createsuperuser
```
Запустить проект:
```python
python manage.py runserver
```
**Автор: Нечепуренко Алексей**
