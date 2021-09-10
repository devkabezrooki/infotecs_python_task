# -*- coding: utf-8 -*-
from flask import Flask, request, json

'''
Обработка файла
'''
file = open('RU.txt', 'r', encoding='utf-8')
onstring = file.readlines()
cities = dict()

for item in onstring: #данные из файла представляются в виде словаря, ключ - id города
    key = item.split('\t')[0]
    value = item.split('\t')[1:]
    cities[key] = value

'''
Вспомогательные методы
'''
#Метод принимает id города  и возвращает данные о нем в виде списка, который 
#удобно представить в формате json
def make_json_from_id(id): 
    city = cities[id]
    return {"geonameid":id,
                       "name":city[0],
                       "asciiname":city[1],
                       "alternatenames":city[2],
                       "latitude":city[3],
                       "longitude":city[4],
                       "feature class":city[5],
                       "feature code":city[6],
                       "country code":city[7],
                       "cc2":city[8],
                       "admin1 code":city[9],
                       "admin2 code":city[10],
                       "admin3 code":city[11],
                       "admin4 code":city[12],
                       "population":city[13],
                       "elevation":city[14],
                       "dem":city[15],
                       "timezone":city[16],
                       "modification date":city[17][:10]}
       

#Метод для поиска города в третьем задании
#Принимает имя города без учета регистра
#Возвращает id города с максимальным населением из городов с искомым именем
#Если подходящих городов с одинаковым именем и населением несколько, вернется первый попавшийся 
def find_city(name):  
    key = -1
    max_population = -1
    for k, d in cities.items():
        names_list = d[2].lower().split(',')
        if name.lower() in names_list:
            if int(d[13]) > max_population:
                max_population = int(d[13])
                key = k 
    return key

'''
Реализация REST API
'''
app = Flask(__name__) #для реализации веб-приложения используется фреймворк Flask


#Первое задание
#GET-метод, принимает единственный параметр - id города
#Если введенное id обнаружено в файле, метод возвращает информацию о городе в формате json
#Если id отсутствует в файле, метод возвращает сообщение об ошибке
@app.route('/info_from_id', methods = ['GET'])
def get_info_from_id():
    geonameid = str(int(request.args.get('id')))
    if geonameid not in cities:
        return "Error! Id not found in the file"
    else:
        return json.dumps(make_json_from_id(geonameid), ensure_ascii=False, indent=2, sort_keys=False)

#Второе задание
#GET-метод, принимает два параметра: номер страницы и количество городов на ней
#Возвращает список данных о городах в формате json
#Если число городов на странице некратно количеству городов, на последней странице отобразится меньшее 
#количество (т.е. сколько городов останется с предпоследней страницы до конца)
#Если количество городов на странице неположительно, метод вернет информацию об ошибке
#При выходе за границы списка также возвращается сообщение об ошибке
@app.route('/info_from_page', methods = ['GET'])
def get_info_from_page():
    page = int(request.args.get('page'))
    page_cities_count  = int(request.args.get('count'))
    if page_cities_count <= 0:
        return "Error! Cities count must be > 0"
    if (page * page_cities_count > len(cities) and (page - 1) * page_cities_count >= len(cities)) or page <= 0:
        return "Error! Out of range"
    if page * page_cities_count >= len(cities):
        cities_id = list(cities)[(page - 1) * page_cities_count:]
    else:
        cities_id = list(cities)[(page - 1) * page_cities_count:page * page_cities_count]
    jsons = []
    for i in range(len(cities_id)):
        jsons.append(make_json_from_id(cities_id[i]))
    return json.dumps(jsons, ensure_ascii=False, indent = 3, sort_keys=False)

#Третье задание
#GET-метод, принимает названия двух городов на русском языке (без учета регистра)
#Если названия городов совпадают, метод вернет сообщение об ошибке
#Если один или оба города не обнаружен в файле, метод вернет сообщение об ошибке
#Если входные данные корректны, метод вернет данные о городах, а также информацию о том, какой из городов
#севернее, и информацию о разнице в их часовых поясах в формате json
@app.route('/cities_compare', methods = ['GET'])
def cities_compare():
    name_1 = str(request.args.get('city1'))
    name_2  = str(request.args.get('city2'))
    if name_1.lower() == name_2.lower():
        return "Error! You are trying to compare the same city"
    city_1 = find_city(name_1)
    city_2 = find_city(name_2)
    if city_1 == -1 and city_2 == -1:
        return f'Error! {name_1} and {name_2} not found in the file!'
    if city_1 == -1:
        return f'Error! {name_1} not found in the file!'
    if city_2 == -1:
        return f'Error! {name_2} not found in the file!'
    jsons = []
    jsons.append(make_json_from_id(city_1))
    jsons.append(make_json_from_id(city_2))
    if float(cities[city_1][3]) > float(cities[city_2][3]):
        jsons.append(f'Northern city: {name_1}')
    elif float(cities[city_1][3]) == float(cities[city_2][3]):
        jsons.append(f'Cities are on the same latitude')
    else:
        jsons.append(f'Northern city: {name_2}')
    if cities[city_1][16] == cities[city_2][16]:
        jsons.append("Cities are in the same timezone")
    else:
        timezones = {'Europe/Kaliningrad': 2, 'Europe/Moscow': 3, 'Europe/Samara': 4, 'Asia/Yekaterinburg': 5, 'Asia/Omsk': 6,
             'Asia/Krasnoyarsk': 7, 'Asia/Irkutsk': 8, 'Asia/Yakutsk': 9, 'Asia/Vladivostok': 10, 'Asia/Magadan': 11,
             'Asia/Kamchatka': 12}
        jsons.append(f'The difference between timezones is {abs(timezones[cities[city_1][16]] - timezones[cities[city_2][16]])} hours')
    return json.dumps(jsons, ensure_ascii=False, indent = 3, sort_keys=False)
    
    

if __name__ == '__main__':
    app.run(port = 8000) #сервис доступен по адресу http://127.0.0.1:8000/
  