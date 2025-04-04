# Практика 5. Прикладной уровень

## Программирование сокетов.

### A. Почта и SMTP (7 баллов)

### 1. Почтовый клиент (2 балла)
Напишите программу для отправки электронной почты получателю, адрес
которого задается параметром. Адрес отправителя может быть постоянным. Программа
должна поддерживать два формата сообщений: **txt** и **html**. Используйте готовые
библиотеки для работы с почтой, т.е. в этом задании **не** предполагается общение с smtp
сервером через сокеты напрямую.

Приложите скриншоты полученных сообщений (для обоих форматов).

#### Демонстрация работы
файл A1.py

txt

![image](https://github.com/user-attachments/assets/bcb5aa55-8cce-4db7-8e06-6e318e47ad5b)

html

![image](https://github.com/user-attachments/assets/54334b6b-f1e9-4ad8-9a98-b80ebdfb79d0)


### 2. SMTP-клиент (3 балла)
Разработайте простой почтовый клиент, который отправляет текстовые сообщения
электронной почты произвольному получателю. Программа должна соединиться с
почтовым сервером, используя протокол SMTP, и передать ему сообщение.
Не используйте встроенные методы для отправки почты, которые есть в большинстве
современных платформ. Вместо этого реализуйте свое решение на сокетах с передачей
сообщений почтовому серверу.

Сделайте скриншоты полученных сообщений.

#### Демонстрация работы
файл A2.py

txt

![image](https://github.com/user-attachments/assets/f375f11e-783f-451c-ba1e-60969ca17d17)

html

![image](https://github.com/user-attachments/assets/fb6f2072-e919-4c00-8be6-28e391c6eac5)

### 3. SMTP-клиент: бинарные данные (2 балла)
Модифицируйте ваш SMTP-клиент из предыдущего задания так, чтобы теперь он мог
отправлять письма с изображениями (бинарными данными).

Сделайте скриншот, подтверждающий получение почтового сообщения с картинкой.

#### Демонстрация работы
файл A3.py

txt

![image](https://github.com/user-attachments/assets/71f16eb4-58cc-4b24-8b58-fe4f5e631966)

html

![image](https://github.com/user-attachments/assets/0828deef-7915-4659-9777-96084ec8fbf3)

---

_Многие почтовые серверы используют ssl, что может вызвать трудности при работе с ними из
ваших приложений. Можете использовать для тестов smtp сервер СПбГУ: mail.spbu.ru, 25_

### Б. Удаленный запуск команд (3 балла)
Напишите программу для запуска команд (или приложений) на удаленном хосте с помощью TCP сокетов.

Например, вы можете с клиента дать команду серверу запустить приложение Калькулятор или
Paint (на стороне сервера). Или запустить консольное приложение/утилиту с указанными
параметрами. Однако запущенное приложение **должно** выводить какую-либо информацию на
консоль или передавать свой статус после запуска, который должен быть отправлен обратно
клиенту. Продемонстрируйте работу вашей программы, приложив скриншот.

Например, удаленно запускается команда `ping yandex.ru`. Результат этой команды (запущенной на
сервере) отправляется обратно клиенту.

#### Демонстрация работы
файлы B_server.py и B_client.py

![image](https://github.com/user-attachments/assets/bf802597-bdea-4132-8a6d-2f55a4f0c2ed)

![image](https://github.com/user-attachments/assets/86ba453e-a410-41e2-96c5-9b0b9fbd1110)

### В. Широковещательная рассылка через UDP (2 балла)
Реализуйте сервер (веб-службу) и клиента с использованием интерфейса Socket API, которая:
- работает по протоколу UDP
- каждую секунду рассылает широковещательно всем клиентам свое текущее время
- клиент службы выводит на консоль сообщаемое ему время

#### Демонстрация работы
файлы C_server.py и C_client.py

![image](https://github.com/user-attachments/assets/3272996e-6c22-4668-9bf3-17253e89d8da)

## Задачи

### Задача 1 (2 балла)
Рассмотрим короткую, $10$-метровую линию связи, по которой отправитель может передавать
данные со скоростью $150$ бит/с в обоих направлениях. Предположим, что пакеты, содержащие
данные, имеют размер $100000$ бит, а пакеты, содержащие только управляющую информацию
(например, флаг подтверждения или информацию рукопожатия) – $200$ бит. Предположим, что у
нас $10$ параллельных соединений, и каждому предоставлено $1/10$ полосы пропускания канала
связи. Также допустим, что используется протокол HTTP, и предположим, что каждый
загруженный объект имеет размер $100$ Кбит, и что исходный объект содержит $10$ ссылок на другие
объекты того же отправителя. Будем считать, что скорость распространения сигнала равна
скорости света ($300 \cdot 10^6$ м/с).
1. Вычислите общее время, необходимое для получения всех объектов при параллельных
непостоянных HTTP-соединениях
2. Вычислите общее время для постоянных HTTP-соединений. Ожидается ли существенное
преимущество по сравнению со случаем непостоянного соединения?

#### Решение
$$d_{\text{передачи}} = \frac{L}{R} = \frac{100000}{150} = 666.667 c$$
$$d_{\text{распространения}} = \frac{d}{s} = \frac{10}{300 × 10^6}$$
$$T = \frac{200}{150} = 1.33 c$$

**1. параллельное непостоянное соединение**

а) запрос первого объекта:

$$3 \cdot (T + d_{\text{распространения}}) + (d_{\text{передачи}} + d_{\text{распространения}}) =$$
$$= 3 \cdot (1.33 + d_{\text{распространения}}) + (666.667 + d_{\text{распространения}}) =$$
$$= 4 + 3 \cdot d_{\text{распространения}} + 666.667 + d_{\text{распространения}} = 670.667 + 4 \cdot d_{\text{распространения}}$$

б) параллельно оставшиеся:

$$3 \cdot (\dfrac{200}{15} + d_{\text{распространения}}) + (\dfrac{100000}{15} + d_{\text{распространения}}) =$$
$$= 3 \cdot (13.333 + d_{\text{распространения}}) + (6666.667 + d_{\text{распространения}}) =$$
$$= 40 + 3 \cdot d_{\text{распространения}} + 6666.667 + d_{\text{распространения}} = 6706.667 + 4 \cdot d_{\text{распространения}}$$

в) в итоге:

$$670.667 + 4 \cdot d_{\text{распространения}} + 6706.667 + 4 \cdot d_{\text{распространения}} = 7377.334 + 8 \cdot d_{\text{распространения}}$$

**2. постоянное соединение**

а) запрос первого объекта:

$$3 \cdot (T + d_{\text{распространения}}) + (d_{\text{передачи}} + d_{\text{распространения}}) =$$
$$= 3 \cdot (1.33 + d_{\text{распространения}}) + (666.667 + d_{\text{распространения}}) =$$
$$= 4 + 3 \cdot d_{\text{распространения}} + 666.667 + d_{\text{распространения}} = 670.667 + 4 \cdot d_{\text{распространения}}$$

б) загрузка 10 объектов (без установки соединения):

$$10 \cdot (\dfrac{200}{150} + d_{\text{распространения}} + \dfrac{100000}{150} + d_{\text{распространения}}) =$$
$$= 10 \cdot (1.33 + d_{\text{распространения}} + 666.667 + d_{\text{распространения}}) =$$
$$= 10 \cdot (668 + 2 \cdot d_{\text{распространения}}) = 6680 + 20  \cdot d_{\text{распространения}}$$

в) в итоге:

$$670.667 + 4 \cdot d_{\text{распространения}} + 6680 + 20  \cdot d_{\text{распространения}} = 7350.667 + 24 \cdot d_{\text{распространения}}$$

**3. посчитаем разницу:**

$$7377.334 + 8 \cdot d_{\text{распространения}} - 7350.667 + 24 \cdot d_{\text{распространения}} = 26.667 - 16 \cdot d_{\text{распространения}}$$

(прям существенного преимущества получается нет)

### Задача 2 (3 балла)
Рассмотрим раздачу файла размером $F = 15$ Гбит $N$ пирам. Сервер имеет скорость отдачи $u_s = 30$
Мбит/с, а каждый узел имеет скорость загрузки $d_i = 2$ Мбит/с и скорость отдачи $u$. Для $N = 10$, $100$
и $1000$ и для $u = 300$ Кбит/с, $700$ Кбит/с и $2$ Мбит/с подготовьте график минимального времени
раздачи для всех сочетаний $N$ и $u$ для вариантов клиент-серверной и одноранговой раздачи.

#### Решение
![image](https://github.com/user-attachments/assets/6159199d-e741-4ae2-97bf-96de0e337243)

### Задача 3 (3 балла)
Рассмотрим клиент-серверную раздачу файла размером $F$ бит $N$ пирам, при которой сервер
способен отдавать одновременно данные множеству пиров – каждому с различной скоростью,
но общая скорость отдачи при этом не превышает значения $u_s$. Схема раздачи непрерывная.
1. Предположим, что $\dfrac{u_s}{N} \le d_{min}$.
   При какой схеме общее время раздачи будет составлять $\dfrac{N F}{u_s}$?
2. Предположим, что $\dfrac{u_s}{N} \ge d_{min}$. 
   При какой схеме общее время раздачи будет составлять  $\dfrac{F}{d_{min}}$?
3. Докажите, что минимальное время раздачи описывается формулой $\max\left(\dfrac{N F}{u_s}, \dfrac{F}{d_{min}}\right)$?

#### Решение
**1. Случай: $\dfrac{u_s}{N} \le d_{min}$**

Если каждому пиру данные передаются со скоростью $\dfrac{u_s}{N}$, то:

а) так как по условию $\dfrac{u_s}{N} \le d_{min}$, все пиры могут принимать данные с этой скоростью

б) полный объем данных $F$ передается каждому пиру за время:

$D = \dfrac{F}{v} = \dfrac{NF}{u_s}$

в) таким образом, общее время раздачи составляет $\dfrac{NF}{u_s}$

**2. Случай: $\dfrac{u_s}{N} \ge d_{min}$**

Если каждому пиру данные передаются со скоростью $d_{min}$, то:

а) сервер может раздавать данные со скоростью $N d_{min}$, что не превышает $u_s$ по условию

б) минимальная скорость загрузки среди всех пиров равна $d_{min}$, значит, каждый пир получит все данные за время:

$D = \dfrac{F}{d_{min}}$

в) таким образом, общее время раздачи составляет $\dfrac{F}{d_{min}}$

**3. доказательство минимального времени раздачи**

а) пусть $D_{c-s}$ — минимальное время раздачи

б) Очевидно, что:
- сервер не может отправить все данные быстрее, чем за $\dfrac{N F}{u_s}$.
- клиенты не могут получить все данные быстрее, чем за $\dfrac{F}{d_{min}}$

Следовательно,

$D_{c-s} \geq \max\left(\dfrac{N F}{u_s}, \dfrac{F}{d_{min}}\right)$


в) теперь докажем, что можно достичь этого времени в двух случаях:

- если $\dfrac{u_s}{N} \le d_{min}$, по пункту (1) раздача возможна за $\dfrac{N F}{u_s}$, и в этом случае:

$\max\left(\dfrac{N F}{u_s}, \dfrac{F}{d_{min}}\right) = \dfrac{NF}{u_s}$

- если $\dfrac{u_s}{N} \ge d_{min}$, по пункту (2) раздача возможна за $\dfrac{F}{d_{min}}$, и в этом случае:

$D_{c-s} = \max\left(\dfrac{N F}{u_s}, \dfrac{F}{d_{min}}\right)$

г) таким образом, минимальное время раздачи действительно описывается формулой:

$\max\left(\dfrac{N F}{u_s}, \dfrac{F}{d_{min}}\right)$
