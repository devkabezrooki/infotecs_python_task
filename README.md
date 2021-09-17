# infotecs_python_task
Тестовое задание для стажера на позицию «Программист на языке Python» в Infotecs Academy
# Текст задания:
Реализовать HTTP-сервер для предоставления информации по географическим объектам.
Данные взять из географической базы данных GeoNames, по ссылке: http://download.geonames.org/export/dump/RU.zip
Реализованный сервер должен предоставлять REST API сервис со следующими методами:
1.	Метод принимает идентификатор geonameid и возвращает информацию о городе.
2.	Метод принимает страницу и количество отображаемых на странице городов и возвращает список городов с их информацией. 
3.	Метод принимает названия двух городов (на русском языке) и получает информацию о найденных городах, а также дополнительно: какой из них расположен севернее и одинаковая ли у них временная зона (когда несколько городов имеют одно и то же название, разрешать неоднозначность выбирая город с большим населением; если население совпадает, брать первый попавшийся)

**Дополнительное задание:** 
•	Для 3-его метода показывать пользователю не только факт различия временных зон, но и на сколько часов они различаются.

# Описание реализации:
Для выполнения задания использовался Python 3.9.6 и фреймворк Flask 2.0.1 для реализации веб-интерфейса.

Данные о городах считываются из файла **RU.txt** и хранятся в виде словаря, в котором ключами являются id городов.

Скрипт можно запустить через консоль следующим образом: python script.py

После этого по адресу 127.0.0.1 и порту 8000 можно обращаться к описанным ниже методам.

Для удобства представления данных о городах в формате json был реализован метод **make_json_from_id(id)**, который принимает id города и возвращает данные о нем в виде словаря со структурой json следующего вида:
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
## Первое задание:
Первый метод доступен по адресу:
```
http://127.0.0.1:8000/info_from_id?id=id
```
GET-метод, принимает единственный параметр - целочисленное id города.
Если введенное id обнаружено в файле, метод возвращает информацию о городе в формате json.
Если id отсутствует в файле, метод возвращает сообщение об ошибке.

## Второе задание:
Второй метод доступен по адресу:
```
http://127.0.0.1:8000/info_from_page?page=page&count=count
```
GET-метод, принимает два целочисленных параметра: номер страницы и количество городов на ней.
Возвращает список данных о городах в формате json.
Если число городов на странице некратно количеству городов, на последней странице отобразится меньшее  количество (т.е. сколько городов останется с предпоследней страницы до конца).
Если количество городов на странице неположительно, метод вернет информацию об ошибке.
При выходе за границы списка городов также возвращается сообщение об ошибке.

## Третье задание:
Для выполнения третьего задания был реализован вспомогательный метод **find_city(name)**, который принимает в качестве входного параметра имя города без учета регистра и возвращает id города с максимальным населением из городов с искомым именем. Если подходящих городов с одинаковым именем и населением несколько, вернется первый попавшийся.
Также для третьего задания было реализовано доп. задание.
Третий метод доступен по адресу:
```
http://127.0.0.1:8000/cities_compare?city1=name1&city2=name2
```
GET-метод, принимает названия двух городов на русском языке (без учета регистра).
Если названия городов совпадают, метод вернет сообщение об ошибке.
Если один или оба города не обнаружены в файле, метод вернет соответствующее сообщение об ошибке.
Если входные данные корректны, метод вернет данные о городах, а также информацию о том, какой из городов севернее, и информацию о разнице в их часовых поясах в формате json.
