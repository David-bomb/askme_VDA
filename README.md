# askme_VDA

## ДЗ№1
Все страницы прописаны в папке <a href="https://github.com/David-bomb/askme_VDA/edit/main/templates/">templates</a>

Все ресурсы (в том числе и bootstrap) расположены в папке <a href="https://github.com/David-bomb/askme_VDA/edit/main/tratic/">static</a>

## ДЗ№2
Была реализована маршрутизация. Все элементы лежат в подпапках директории <a href="https://github.com/David-bomb/askme_VDA/tree/main/templates">templates</a>, а точнее:

1) <a href="https://github.com/David-bomb/askme_VDA/tree/main/templates/components"> components</a> для компонентов страниц
2) <a href="https://github.com/David-bomb/askme_VDA/tree/main/templates/layouts"> layouts</a> для шаблонов страниц

Стоит обратить внимание, что в проекте есть два файла с URL:
1) <a href="https://github.com/David-bomb/askme_VDA/blob/main/app/urls.py">url.py</a> для всего проекта в целом
2) <a href="https://github.com/David-bomb/askme_VDA/blob/main/askme_VDA/urls.py">url.py</a> для приложения app

## ДЗ№3
Было реализовано взаимодействие с БД, работа осуществляется по средствам PostgreSQL. 

Основные изменения связанные с БД:
1) Были созданы <a href="https://github.com/David-bomb/askme_VDA/tree/main/app/models.py">модели</a> миграций
2) Заполнение БД осуществлялось через скрипт <a href="https://github.com/David-bomb/askme_VDA/tree/main/app/management/commands/delete_db.py">delete_db.py</a> и <a href="https://github.com/David-bomb/askme_VDA/tree/main/app/management/commands/fill_db.py">fill_db.py</a> 
3) Были изменены шаблоны страниц так, чтобы они обрабатывали значения уже полученные из БД. Имитация загрузки данных из БД была заменена на реальную загрузку в файле <a href="https://github.com/David-bomb/askme_VDA/tree/main/app/views.py">views.py</a>

Также для подгрузки данных популярных тегов был написан контекстный процессор popular_tags, для кастомных контекстных процессоров был создан отдельный файл <a href="https://github.com/David-bomb/askme_VDA/blob/main/app/context_processor.py">context_processor.py</a>

## ДЗ№4
Была реализована система авторазации, входа в аккаунт, редактирования профиля. Также авторизованным пользователям дана возможность задавать вопросы и отвечать на них.

1) Все формы (авторизация, вход, настройки, задавание вопроса, ответ на вопрос) находятся в <a href="https://github.com/David-bomb/askme_VDA/tree/main/app/forms.py">forms.py</a>
2) Навигационная панель также изменяется в зависимости от юзера: авторизован он или нет. "Шапка" для авторизированного пользователя находится <a href="https://github.com/David-bomb/askme_VDA/tree/main/templates/components/base_reg_nav.html">здесь</a>
