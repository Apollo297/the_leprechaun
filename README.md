# The_leprechaun

**Описание проекта:**

Финансовый ассистент — это веб-приложение, которое позволяет пользователям управлять своими личными финансами. Система предлагает функционал для отслеживания доходов и расходов, а также анализ финансового состояния через различные отчеты и диаграммы. Приложение поддерживает работу с несколькими валютами и актуальными валютными курсами. 💰🍀

## Основные функции

- Ведение личного бюджета
  - Отслеживание доходов и расходов
  - Анализ финансов с помощью отчетов и диаграмм

- Многовалютность
  - Управление накоплениями в разных валютах
  - Автоматическое обновление курсов валют

- Цели накоплений
  - Создание финансовых целей
  - Отслеживание срока до их достижения

- Планирование
  - Установка повторяющихся транзакций на выбранные промежутки времени

- История операций
  - Просмотр и фильтрация операций за выбранный промежуток времени

**Цель проекта:**

Проект "Лепрекон" создан с целью помочь пользователям эффективно управлять своими финансами, осуществлять контроль доходов и расходов, а также достигать своих финансовых целей.</br> Я стремлюсь предоставить интуитивно понятный и мощный инструмент для управления личными финансами, который поможет пользователям достичь финансовой стабильности и благополучия.


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
python3 -m venv env
```
```python
source env/bin/activate
```
Установить зависимости из файла requirements.txt:
```python
python3 -m pip install --upgrade pip
```
```python
pip install -r requirements.txt
```
Выполнить миграции:
```python
python3 manage.py migrate
```
Создать суперпользователя (если необходимо):
```python
python manage.py createsuperuser
```
Запустить проект:
```python
python3 manage.py runserver
```
