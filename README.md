# comics-publisher-xkcd
Публикация комиксов xkcd в социальной сети Вконтакте


# Публикация комикса xkcd в социальной сети Вконтакте
Программа выбирает случайный комикс [xkcd] (https://xkcd.com) из коллекции и публикует его на стене вашей группы с описанием от автора.

# Как установить
Для работы необходимо зарегистрировать приложение Вконтакте, получить access_token, указать тип публикуемого файла, от чьего имени публиковать посты и id группы.

Данные находятся в специальном .env файле. Документация и примеры доступны на странице проекта [repl.it](https://repl.it/site/docs/repls/secret-keys).
В файле 4 переменных:
Ключ доступа — access_token
Тип публикуемого контента — attachment_type
От кого публиковать — owner_id
Куда публиковать — group_id

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть конфликт с Python2) для установки зависимостей:
```sh
pip install -r requirements.txt
```

# API Вконтакте
[Ссылка на API] (https://vk.com/dev)
[Описание процедуры получения access_token] (https://vk.com/dev/implicit_flow_user)
[Описание синтаксиса запросов к API] (https://vk.com/dev/api_requests)

Применяемые методы:
[groups.get] (https://vk.com/dev/groups.get)
[photos.getWallUploadServer] (https://vk.com/dev/photos.getWallUploadServer)
[photos.saveWallPhoto] (https://vk.com/dev/photos.saveWallPhoto)
[wall.post] (https://vk.com/dev/wall.post)

# Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.
