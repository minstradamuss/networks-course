# Практика 4. Прикладной уровень

## Программирование сокетов: Прокси-сервер
Разработайте прокси-сервер для проксирования веб-страниц. 
Приложите скрины, демонстрирующие работу прокси-сервера. 

### Запуск прокси-сервера
Запустите свой прокси-сервер из командной строки, а затем запросите веб-страницу с помощью
вашего браузера. Направьте запросы на прокси-сервер, используя свой IP-адрес и номер порта.
Например, http://localhost:8888/www.google.com

_(*) Вы должны заменить стоящий здесь 8888 на номер порта в серверном коде, 
то есть тот, на котором прокси-сервер слушает запросы._

Вы можете также настроить непосредственно веб-браузер на использование вашего прокси сервера. 
В настройках браузера вам нужно будет указать адрес прокси-сервера и номер порта,
который вы использовали при запуске прокси-сервера (опционально).

### А. Прокси-сервер без кеширования (4 балла)
1. Разработайте свой прокси-сервер для проксирования http GET запросов от клиента веб-серверу 
   с журналированием проксируемых HTTP-запросов. В файле журнала сохраняется
   краткая информация о проксируемых запросах (URL и код ответа). Кеширование в этом
   задании не требуется. **(2 балла)**
2. Добавьте в ваш прокси-сервер обработку ошибок. Отсутствие обработчика ошибок может
   вызвать проблемы. Особенно, когда клиент запрашивает объект, который не доступен, так
   как ответ 404 Not Found, как правило, не имеет тела, а прокси-сервер предполагает, что
   тело есть и пытается прочитать его. **(1 балл)**
3. Простой прокси-сервер поддерживает только метод GET протокола HTTP. Добавьте
   поддержку метода POST. В запросах теперь будет использоваться также тело запроса
   (body). Для вызова POST запросов вы можете использовать Postman. **(1 балл)**

Приложите скрины или логи работы сервера.

#### Демонстрация работы

![image](https://github.com/user-attachments/assets/c884b9e6-11b2-427d-859a-2cf8f67ec4ca)

![image](https://github.com/user-attachments/assets/586b662b-41b0-43b3-adfa-18ade863b056)

![image](https://github.com/user-attachments/assets/3a72cfc8-31db-4191-8e44-4f0b0af3abce)


### Б. Прокси-сервер с кешированием (4 балла)
Когда прокси-сервер получает запрос, он проверяет, есть ли запрашиваемый объект в кэше, и,
если да, то возвращает объект из кэша без соединения с веб-сервером. Если объекта в кэше нет,
прокси-сервер извлекает его с веб-сервера обычным GET запросом, возвращает клиенту и
кэширует копию для будущих запросов.

Для проверки того, прокис объект в кеше или нет, необходимо использовать условный GET
запрос. В таком случае вам необходимо указывать в заголовке запроса значение для If-Modified-Since и If-None-Match. 
Подробности можно найти [тут](https://ruturajv.wordpress.com/2005/12/27/conditional-get-request).

Будем считать, что кеш-память прокси-сервера хранится на его жестком диске. Ваш прокси-сервер
должен уметь записывать ответы в кеш и извлекать данные из кеша (т.е. с диска) в случае
попадания в кэш при запросе. Для этого необходимо реализовать некоторую внутреннюю
структуру данных, чтобы отслеживать, какие объекты закешированы.

Приложите скрины или логи, из которых понятно, что ответ на повторный запрос был взят из кэша.

#### Демонстрация работы
![image](https://github.com/user-attachments/assets/53c44659-735f-4732-bd29-dc9f64287e0c)

![image](https://github.com/user-attachments/assets/f4586c36-37b4-49bd-ab48-7ecd1955631b)

кэш хранится у меня в папке с таким путем: C:\Users\User\Source\Repos\networks-course\lab04\cache

### В. Черный список (2 балла)
Прокси-сервер отслеживает страницы и не пускает на те, которые попадают в черный список. Вместо
этого прокси-сервер отправляет предупреждение, что страница заблокирована. Список доменов
и/или URL-адресов для блокировки по черному списку задается в **конфигурационном файле**.

Приложите скрины или логи запроса из черного списка.

#### Демонстрация работы
![image](https://github.com/user-attachments/assets/072eb1df-7e1b-46ad-b970-09259630bf40)

![image](https://github.com/user-attachments/assets/f130068f-b166-4be1-8814-1ee6758fce54)

![image](https://github.com/user-attachments/assets/d28dfac5-5fad-47a7-9129-237364e30472)

## Wireshark. Работа с DNS
Для каждого задания в этой секции приложите скрин с подтверждением ваших ответов.

### А. Утилита nslookup (1 балл)

#### Вопросы
1. Выполните nslookup, чтобы получить IP-адрес какого-либо веб-сервера в Азии
   - 54.222.60.218
     
![image](https://github.com/user-attachments/assets/ba4d95ed-bea5-42f7-89a9-2836751359e4)

2. Выполните nslookup, чтобы определить авторитетные DNS-серверы для какого-либо университета в Европе
   - получилось только так
     
![image](https://github.com/user-attachments/assets/8ba4755f-4467-423c-9122-c69ab21f11fe)

3. Используя nslookup, найдите веб-сервер, имеющий несколько IP-адресов. Сколько IP-адресов имеет веб-сервер вашего учебного заведения?
   - 205.251.242.103, 54.239.28.85, 52.94.236.248
     
![image](https://github.com/user-attachments/assets/6fcd2370-8bb7-4a99-bfc7-8bfad61d81c5)

   - 1
     
![image](https://github.com/user-attachments/assets/95a18121-651f-4ef4-b551-e06079032824)

### Б. DNS-трассировка www.ietf.org (3 балла)

#### Подготовка
1. Используйте ipconfig для очистки кэша DNS на вашем компьютере.
2. Откройте браузер и очистите его кэш (для Chrome можете использовать сочетание клавиш
   CTRL+Shift+Del).
3. Запустите Wireshark и введите `ip.addr == ваш_IP_адрес` в строке фильтра, где значение
   ваш_IP_адрес вы можете получить, используя утилиту ipconfig. Данный фильтр позволит
   нам отбросить все пакеты, не относящиеся к вашему хосту. Запустите процесс захвата пакетов в Wireshark.
4. Зайдите на страницу www.ietf.org в браузере.
5. Остановите захват пакетов.

#### Вопросы
1. Найдите DNS-запрос и ответ на него. С использованием какого транспортного протокола
   они отправлены?
   - TCP

![image](https://github.com/user-attachments/assets/634fbdc9-9cc8-4e20-bbc8-f43ff5b787d4)

2. Какой порт назначения у запроса DNS?
   - 53
3. На какой IP-адрес отправлен DNS-запрос? Используйте ipconfig для определения IP-адреса
   вашего локального DNS-сервера. Одинаковы ли эти два адреса?
   - 192.168.01
   - да

![image](https://github.com/user-attachments/assets/0de2fce2-5d34-448e-9ab3-71e50d8594d6)

4. Проанализируйте сообщение-запрос DNS. Запись какого типа запрашивается? Содержатся
   ли в запросе какие-нибудь «ответы»?
   - type A
   - нет

![image](https://github.com/user-attachments/assets/76f5ac18-3af4-4e1a-8560-1766c26af7ca)

5. Проанализируйте ответное сообщение DNS. Сколько в нем «ответов»? Что содержится в
   каждом?
   - 2
   - IP-адреса

![image](https://github.com/user-attachments/assets/541c79b8-de55-4f0d-a9c7-094e91c27b88)

6. Посмотрите на последующий TCP-пакет с флагом SYN, отправленный вашим компьютером.
   Соответствует ли IP-адрес назначения пакета с SYN одному из адресов, приведенных в
   ответном сообщении DNS?
   - да

![image](https://github.com/user-attachments/assets/865b5247-6707-40cc-a6ba-568d4b9931c5)

7. Веб-страница содержит изображения. Выполняет ли хост новые запросы DNS перед
   загрузкой этих изображений?
   - да, на static.ietf.org и analytics.ietf.org

### В. DNS-трассировка www.spbu.ru (2 балла)

#### Подготовка
1. Запустите захват пакетов с тем же фильтром `ip.addr == ваш_IP_адрес`
2. Выполните команду nslookup для сервера www.spbu.ru
3. Остановите захват
4. Вы увидите несколько пар запрос-ответ DNS. Найдите последнюю пару, все вопросы будут относиться к ней
   
#### Вопросы
1. Каков порт назначения в запросе DNS? Какой порт источника в DNS-ответе?
   - 53
   - 53

![image](https://github.com/user-attachments/assets/85262f72-f836-4c51-b620-dbbf81faf91b)

2. На какой IP-адрес отправлен DNS-запрос? Совпадает ли он с адресом локального DNS-сервера, установленного по умолчанию?
   - 192.168.0.1
   - да
3. Проанализируйте сообщение-запрос DNS. Запись какого типа запрашивается? Содержатся
   ли в запросе какие-нибудь «ответы»?
   - type A
   - нет

![image](https://github.com/user-attachments/assets/4b461505-176d-4838-8481-f62a5918ebdd)

4. Проанализируйте ответное сообщение DNS. Сколько в нем «ответов»? Что содержится в каждом?
   - 2
   - CNAME spbu.ru, IP-адрес

![image](https://github.com/user-attachments/assets/75974231-8ff7-4b1e-8ee5-414a8ccf12fc)

### Г. DNS-трассировка nslookup –type=NS (1 балл)
Повторите все шаги по предварительной подготовке из Задания B, но теперь для команды `nslookup –type=NS spbu.ru`

#### Вопросы
1. На какой IP-адрес отправлен DNS-запрос? Совпадает ли он с адресом локального DNS-сервера, установленного по умолчанию?
   - 192.168.0.1
   - да
2. Проанализируйте сообщение-запрос DNS. Запись какого типа запрашивается? Содержатся ли в запросе какие-нибудь «ответы»?
   - type NS
   - нет

![image](https://github.com/user-attachments/assets/85d52a1d-ddbe-4c1a-90e3-e2b588eb0b47)

3. Проанализируйте ответное сообщение DNS. Имена каких DNS-серверов университета в
   нем содержатся? А есть ли их адреса в этом ответе?
   - ns7.spbu.ru, ns.pu.ru, ns2.pu.ru
   - нет

![image](https://github.com/user-attachments/assets/5093caa0-5006-4a4e-82da-271e6509aaf6)

### Д. DNS-трассировка nslookup www.spbu.ru ns2.pu.ru (1 балл)
Снова повторите все шаги по предварительной подготовке из Задания B, но теперь для команды `nslookup www.spbu.ru ns2.pu.ru`.
Запись `nslookup host_name dns_server` означает, что запрос на разрешение доменного имени `host_name` пойдёт к `dns_server`.
Если параметр `dns_server` не задан, то запрос идёт к DNS-серверу по умолчанию (например, к локальному).

#### Вопросы
1. На какой IP-адрес отправлен DNS-запрос? Совпадает ли он с адресом локального DNS-сервера, установленного по умолчанию? 
   Если нет, то какому хосту он принадлежит?
   - 195.70.196.210
   - ns2.pu.ru

![image](https://github.com/user-attachments/assets/c9f8c7f3-af49-4679-b6c8-e427b29274c5)

2. Проанализируйте сообщение-запрос DNS. Запись какого типа запрашивается? Содержатся
   ли в запросе какие-нибудь «ответы»?
   - type A
   - нет

![image](https://github.com/user-attachments/assets/5d442d51-f40e-47ad-bda9-495c694723c9)

3. Проанализируйте ответное сообщение DNS. Сколько в нем «ответов»? Что содержится в
   каждом?
   - 2
   - CNAME spbu.ru, IP-адрес

![image](https://github.com/user-attachments/assets/d865a936-346c-4274-bea3-0de947b3baab)

### Е. Сервисы whois (2 балла)
1. Что такое база данных whois?
   - База данных WHOIS - это база данных, содержащая информацию о доменных именах, владельцах доменов и их контактных данных.
2. Используя различные сервисы whois в Интернете, получите имена любых двух DNS-серверов. 
   Какие сервисы вы при этом использовали?
   - ns1.yandex.ru, ns2.yandex.ru (https://www.nic.ru/whois/?searchWord=ya.ru)
     
![image](https://github.com/user-attachments/assets/ab173490-1462-48ff-8ca0-167ac43a477b)

   - ns1.google.com, ns2.google.com, ns3.google.com, ns4.google.com (http://www.whois-service.ru/)
     
![image](https://github.com/user-attachments/assets/109115fc-bdf4-41cc-830a-7524676ec920)
![image](https://github.com/user-attachments/assets/d35d1a24-0c58-4da9-a0d0-423707f73b1f)

3. Используйте команду nslookup на локальном хосте, чтобы послать запросы трем конкретным
   серверам DNS (по аналогии с Заданием Д): вашему локальному серверу DNS и двум DNS-серверам,
   найденным в предыдущей части.
   
![image](https://github.com/user-attachments/assets/82be9e08-6640-423e-b1da-89a16f5345c3)

![image](https://github.com/user-attachments/assets/dbbc5709-9b94-40cf-92c2-e67988cb95dd)
