# Тестовое задание Газпром МКС

______________________________________

### Данная работа представляет собой приложение "Кабельный журнал" c графическим интерфейсом

<p align="left">
<img src="https://img.shields.io/badge/python_3.10-3670A0?style=flat-square&logo=python&logoColor=ffdd54" alt="Python 3.10">
<img src="https://img.shields.io/badge/Streamlit-red?style=flat-square" alt="Streamlit">
<img src="https://img.shields.io/badge/SQLite-%2307405e.svg?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
</p>

______________________________________
**Приложение реализует учет кабельных линий,
которыми подключены АРМ (автоматизированные рабочие места)
сотрудников к ЛВС (локальной вычислительной сети) компании**

Приложение реализует такие возможности как:

1) Справочники:
    - Кабельный журнал (№ розетки, № порта, № порта на патчпанели,
      Длина, ФИО, подразделение, имя АРМ, IP адрес АРМ, MAC адрес АРМ)
    - Сотрудники (фамилия, имя, отчество, подразделение)
    - Подразделения (название подразделения)
    - Серверные (номер серверной)
    - АРМ (имя, IP адрес, MAC адрес)
2) Чтение и запись используя SQL базу данных
3) CRUD для всех справочников, вынесенный в блок **"Панель администратора"** для каждого из справочников
4) Доступ к CRUD защищен паролем

______________________________________
**Используемый стек**

- Язык программирования: `Python 3.10`
- Фреймворк приложения: `Streamlit 1.25.0`
- База данных: `SQLite`
- ORM для базы данных: `SQLAlchemy 2.0.19`
- Библиотека управления миграциями: `alembic 1.11.1`
- Библиотека для работы с окружением: `python-dotenv 1.0.0`

______________________________________
**Структура проекта**

- `dao/`: папка с файлами DataAccessObject для работы с базой данных
- `dao/models`: папка с файлами моделей для базы данных
- `dao/utils`: папка с файлами утилитами
- `database/`: папка с базой данных и файлом с настройками подключения
- `migration/`: папка с миграциями для работы Alembic
- `pages/`: папка со страницами для Streamlit
- `services`: папка с файлами Service для работы с базой данных
- `.env`: файл с настройками окружения
- `alembic.ini`: файл для настройки Alembic
- `main.py`: главный файл для запуска приложения
- `pyproject.toml`: файл для установки зависимостей через Poetry

______________________________________
**Установка и запуск приложения**

1) Установите при необходимости зависимости в окружение через poetry
   ```sh
   poetry install
   ```

2) Переименуйте `.env.sample` в `.env` и присвойте необходимые значения переменным:
    - ADMIN_PASSWORD

3) При необходимости создайте базу данных и примените начальную миграцию
   ```sh
   alembic upgrade head
   ```

4) Запустите локальное приложение
   ```sh
   streamlit run .\main.py
   ```
   