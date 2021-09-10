# infotecs_python_task
Тестовое задание для стажера на позицию «Программист на языке Python» в Infotecs Academy
## Текст задания:
Реализовать HTTP-сервер для предоставления информации по географическим объектам.
Данные взять из географической базы данных GeoNames, по ссылке: http://download.geonames.org/export/dump/RU.zip
Реализованный сервер должен предоставлять REST API сервис со следующими методами:
1.	Метод принимает идентификатор geonameid и возвращает информацию о городе.
2.	Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией. 
3.	Метод принимает названия двух городов (на русском языке) и получает информацию о найденных городах, а также дополнительно: какой из них расположен севернее и одинаковая ли у них временная зона (когда несколько городов имеют одно и то же название, разрешать неоднозначность выбирая город с большим населением; если население совпадает, брать первый попавшийся)

**Дополнительное задание:** 
•	Для 3-его метода показывать пользователю не только факт различия временных зон, но и на сколько часов они различаются.
## Описание реализации:
Для выполнения задания использовался Python 3.9.6 и фреймворк Flask 2.0.1 для реализации веб-интерфейса.

Данные о городах считываются из файла **RU.txt** и хранятся в виде словаря, в котором ключами являются id городов.

Для удобства представления данных о городах в формате json был реализован метод **make_json_from_id(id)**, который принимает id города и возвращает данные о нем в виде словаря, который в последствии легко преобразовать в json следующего вида:
```json
"geonameid": id,
"name": name,
"asciiname": asciiname,
"alternatenames": alternatenames,
"latitude": latitude,
"longitude": longitude,
"feature class": feature class,
"feature code": feature code,
"country code": country code,
"cc2": cc2,
"admin1 code": admin1 code,
"admin2 code": admin2 code,
"admin3 code": admin3 code,
"admin4 code": admin4 code,
"population": population,
"elevation": elevation,
"dem": dem,
"timezone": timezone,
"modification date": modification date
```

