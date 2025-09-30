# Project_template

Это шаблон для решения проектной работы. Структура этого файла повторяет структуру заданий. Заполняйте его по мере работы над решением.

# Задание 1. Анализ и планирование

<aside>

Чтобы составить документ с описанием текущей архитектуры приложения, можно часть информации взять из описания компании и условия задания. Это нормально.

</aside

### 1. Описание функциональности монолитного приложения

**Управление отоплением:**

На данный момент система управления отоплением не реализована


**Мониторинг температуры:**

Пользователи могут подключать / изменять / удалять датчики, получать информацию о текущем состоянии датчика (активность, текущее значение, тип и проч.). 
На данный момент система представлена в виде единого сервиса датчиков, реализовано базовое обращение к системе контроля температуры (но поскольку она пока не реализована, берутся данные из датчиков). Система датчиков хранит в себе полную информацию о датчиках, в т.ч. их текущее значение; через неё же обновляется значение датчиков. 


### 2. Анализ архитектуры монолитного приложения

- Язык программирования: Go
- База данных: PostgreSQL
- Архитектура: Монолитная, все компоненты системы (обработка запросов, бизнес-логика, работа с данными) находятся в рамках одного приложения. Есть не имплементированный интерфейс сервиса температуры.
- Взаимодействие: Синхронное, запросы обрабатываются последовательно.
- Масштабируемость: Ограничена, так как монолит сложно масштабировать по частям.
- Развертывание: Требует остановки всего приложения.
- Инфраструктура: Приложение упаковано в docker-compose вместе с БД

### 3. Определение доменов и границы контекстов
На данный момент в системе реализован только один домен (As-Is):
Домен умного дома
 - Поддомен датчиков
	- Контекст управления датчиками (подключение, отключение)
	- Контекст получения информации с датчиков
	- Контекст обновления значения датчика

Конечная цель проекта (To-Be):

### DDD (To‑Be): домены и границы контекстов

- Ядро (Core) — управление умным домом:
  - Реестр устройств и ввод в эксплуатацию (provisioning): каталог устройств, привязка к дому/«семье», паринг/закрепление владения.
  - Телеметрия и события: приём, нормализация и хранение телеметрии; публикация событий.
  - Команды и управление: синхронные/асинхронные команды к устройствам с гарантиями доставки и идемпотентностью.
  - Автоматизация и сцены: правила, триггеры, расписания; реакция на события телеметрии.
  - Прошивки/OTA (опционально для MVP): обновления, поэтапный выпуск/откат, совместимость.

- Аутентификация и доступ (IAM/тенантность):
  - Пользователи, «семьи»/домохозяйства, роли и доступ к устройствам; учётные данные устройств; мульти‑тенантность.

- Вспомогательные домены:
  - Жизненный цикл устройств: регистрация/конфигурация, замена/деактивация, диагностика.
  - Уведомления и оповещения: e‑mail/SMS/push/webhooks; политики эскалации.
  - Поддержка пользователей: база знаний, тикеты, доступ только для чтения к устройствам и журналам.
  - Наблюдаемость и диагностика: здоровье устройств и платформы, аудит.

- Универсальные (generic) домены:
  - Маркетинг.
  - Аналитика (продуктовая/бизнес; не путать с телеметрией в ядре).
  - Электронная коммерция (e‑commerce).
  - Биллинг и подписки: планы, тарифы, квоты, учёт потребления и платежи.


### **4. Проблемы монолитного решения**

- Сложно масштабировать
- Нет разбиения на домены, для исправления приходится держать в голове большой контекст
- Невозможно "таргетно" адаптировать нагрузку
- Весь сервис (в т.ч. БД хостятся на одной машине)

Проблемы, не связанные с монолитом:
- Запросы отрабатывают синхронно, при большой нагрузке сильно возрастёт задержка
- Данные о датчиках обновляются по запросу в эндпоинт, то есть датчики не хранят в себе информацию о своём состоянии, не ясен источник истины

### 5. Визуализация контекста системы — диаграмма С4

Добавьте сюда диаграмму контекста в модели C4.

Чтобы добавить ссылку в файл Readme.md, нужно использовать синтаксис Markdown. Это делают так:

[Context schema As-Is](https://plantuml.com/plantuml/png/RL9DRzf04BtxLqmvKIc4IqyzfQAbFIHL18bwZ8RT0O-q7zRic2R_lhCsTH3XXkVvVRo7xugYQ1z3ewo1OCrwptk2LKvAhmhV6G-2iMaqTw0PTbarH_0iv9HpQffFd5peFVKIe5NjojVbKl3lxO6rxNTz8N5LA-cjot6vOOVYys-cZi9ozMNn633fyyFzCc9H4Zkzh7BiSggChWPh7abAJlCgTGEp3HNs1ixizpVe1Wm27paTW1DeIz1cUtVs-JzHoRM97MCoofefU7YQJgEC8r7UCtde9E-f5Ak60OIA9Icy2mJxB8DuJel2IkPL54D0vMowrYtoGBCSDu39GqIklJ4v8-sXH1IrQ970qv4T5KlORD-AKfp_GOc_QkhnsJBLorW4od2hGKVKb1CUp6UqCKlDKXyBfPBbJFVbnwlENU28IlKVbHos9DNSn5RZ7Ku0d93gyzIo-4M7ec_WGkuzb16iynpPLpEXc9N0N3eIr5xg93PI71Qn3ATgOwY76faY9PqQRWS0tX7OJaKtX66X76aorXOL-iwZKZat0jpbNi-hDniAfu_buwm_IS7r8fGcpaLiOvz_CPSIip5lcHn7nkLhrqUVhKbTI-LYjKlxwvDzZF9yckDwaJjAle_X7m00)


[Context schema To-Be](https://www.plantuml.com/plantuml/png/TP9FInjH5CNt-HIlMKM8pgQhhgGYT5516akNaZ-Z6Jf_mimRgfH2a_xfegNINLULwhAR61qTdPY0d-2-RzHpUEg4a2XXPjwxzvnxV_Uk9xePwpJmAq-yiEsd7LTrjUubpnmdRhvRs_TqDssbYHkter2xeLvhHu7JyviXSrOJtV6zbhFnT7MRHw-tNZf1Cz5kZAFT3MOSwBKUrIlRRfn4OOrITLMLOvb8ONx85PuZ6Pg1PFokykvKfkQZ36M4aoF9p42PJpAMM_DTnaeka37chxho8AhTTZVqsbupPFe9Khx8hUHoKxstGj8Dn7wQRx3XJQOaLpW_Ctqfe7ufESkmTx0pVJD03HEvvfkCIgyaxVMYM5FuhqmOXVGBQwTaIY_yPqY-X6S-Kq5vEbGiXrPeQa02TVQLeu1pA4teAJa3uLjf789eiFiyIiDECpwiWRxUY-B0AXU4PpxB1DfZAD_zanFp2uKKm7LzZ-kkgAweznM5FwjMQqUnkr00pPVuBIrpD3yMoPQIGi1Oyhgo4yLlB1aZA5DNJ6V7T6AFSeNdLzwXqm-FlMuUw5hBytqltBUWSufJZEpEa5UG7ueu1oE6_94p5eSxpCGY1WAxM62U4KN-C9yfzV1s0zCPnp3ItjwXDUIeHWnJb8Lx7pWBvj1kSpLeUhxJs6eulJJfajb8CikwfCRXlNBz-vr_8FuRrjEPxI_NhZQFdgSWsGSXVWr9KV8LLl1YPsUx0GFgpwu_NPOklRDiu-SKooMdtC8DTfRiQobaUxS2CxCydfbAFZyJIEIF4iuRjzMDehS9j4gfSaYd2valobvtmquQ-Fy1)


# Задание 2. Проектирование микросервисной архитектуры

В этом задании вам нужно предоставить только диаграммы в модели C4. Мы не просим вас отдельно описывать получившиеся микросервисы и то, как вы определили взаимодействия между компонентами To-Be системы. Если вы правильно подготовите диаграммы C4, они и так это покажут.

**Диаграмма контейнеров (Containers)**

[Containers schema](https://plantuml.com/plantuml/png/dLNDRjj64BxhAROwqO1YNdhgAOeJD2sYLWrTv1XGqYOYoX-1N3OrYWAHdDG75KbJ56rH56YT77BeHMubbxP-3EG9bg_G9-atovKeKrI3sB3DvN3d-sPdlfcz7Wax5B7dLjvp_BORTpZh2j6BFZ3Dq7wq-z0HtRWLHpni1xxWljXj1vxPSssVVAv5ekCwBNFl_MjDCdtUk6DwTYHu2DFzFNZOZi_3tHxXLuGZNCxaSVfKJkHCZfWybmivJmTuFPDpEKaVu_ql9Y_aL8xIGVf4Bc2QfKFsva_vCdr17zAXF6DoZ8spDzDAfSd3AF0D2h36gl9tsAVfT_8V0W86eEczIjzUoGkWZM2Vfiz1Dc3fOTe73R6UqOfS45Z2y8ltR-4yboDyJ-00UtLdoITuk-ixRSVs2Vabq9vYQoBFgpeAH7WEdcVf4K3eouH0OJz9-x0VobFOGAU_RKQISqLnhnU4We2FvO9smNsSqL6kY6kiadSApYIF8BTckPuI5UKxot92QKmGmj_0MYZMXBQ2kM8Te8ZU_Hj1x7ViyC10mSM38FGKzkNg07jBTQexxEiAmyzA28OTYoumwdWmYuTVEcrEyTxUts-oUlCZ5ViVSeAG4fsG4Sg0z9iWNP1PpcliutlxDKR9eYEPHASs7yeBcFiaBaW0rIgGUu4Vk8uAmF8WUdOxy3XhQEjw7CpuCDYfwjA218Wac4m9EdEKWYFAM0bJs-l0UI_mFDllR3tehvGc9O5nEeG4SdrIcOWAHkoO8wipdLNwAzBTR1cT5W2RGIGUXjpwx0x1txrves5LjpQ5JDPpLIkS2Dy6coVVEESZJhptU8lLUxsgNXfMivubxmUud_px-0LLZV2Wt2SmGU7GRLbG9HHUq79S3hI6MYo9d4yji-vtmi3fAAhVgBN0Gv1ph2TWeA2LR4xp7jnE-yrAzRU-4WQUlNhF0VG-LZoqHHnoNJbLnPKwPi34oLJs3kcfI9WYFi_a2y4OghJph8Wxe5lZyWFXF3Z8s3wXjTEsXHFuKP7FQbZcBSzsNBCPHrs80qUOP92vPgXzxt9NZyIiGlANj5yykiw8eJ1ETfOy5lnpTvtzjo10bIK8wpDosNg5EPpNPLrzQWONqF8fk0xrOzdyCWcV31GNIVV_0jC3INwFsWtqT4oWKaBIesTh9E_egvmp7zMkyZNswmIOoEb8Nj3KosuhDB6cq-TzHo-QGDhX9oNBENPESGlaCyS4n5WBUB4wW4xbEbuEk9xxrw0T04bTfFtC2_-Vwz1AviUpPJOsJfPtc_mPaBf-c46R_PKEo_fhA_9wRybNPVt2ZCjjbUlOn3Jh1i4NaKQrumt4OtcYOqLG8reguBEQlfZf9jUNyFZI44gFS9pXAajqcLA9D1EwzWhIr7werCRjKhenprBfFMSMBha2X1uDLmbJkswFj6JlrOEzplrExBd_0G00)

**Диаграмма компонентов (Components)**

[Auth component](https://plantuml.com/plantuml/png/fLPDRnjL5DtFhtXavKXDPyEALHst4g0OcJYbosWyyx177S-CthnfYH1IdHGAIgL2rHM85YGaM3eGjwvTEt_XpZ_Y7ddiyVXr36gpSDx7k-VSZtkkVIFHZj9fFx0-y4CtI3qfUbh7oKUshPpxrxk-xgMTD97AZK8jGttTZVfs73WXRFOIxGL-nsvykDV2qUtcWTrt4YqL7nqteduSXR29WMzfNmTIqCyqfpTqnPyp6j4iEytEHJtLFT6MwfxlIijgC9NZXrBLtC1d-sjYfu655lKuJdPuUqTsx6RKyGE97Jrbe0j1Oy70SxgWCKspnpJZzKZGLVO01xnv2JvUuv2tUFEA__zDm-oKHhn_ihDhMUqJ3g1_VEihNGiZxNzvKezz9laCQzzrj1-5YQYtFW7pnqT7BVnlDzlshRxZ1tOhJNeYEsFG4LqI8fqkM05UH7QpK_CwRDYA4jrLiltv0M0ER-utsrZGSxh8Vc2_dWZwYPw9sjiTfl4raGruzOPli3xB7j68xsRPEKV9ZuTiEEOdurrcB-YFzwCqz1nrKdCuyqouNe2TNV6r9VXlLS2QabtOgYW8f8AZikidMZb8Hd6ndX7wZTtw1znSu0Viy7T8WU1CmFyvNystLQ5CxtZURMx1aWiuQ3gXqvLzVbBXn3Eq0mqPV5hK_frSqD5T6POSEC991UyBeA8QArO6djC4MnfoEQVWvuiPryN8TI9rYQdb9CdzI7c7kAbW_9qkECtpR82GXbY-DOnxKd57bz2_m57Us5l2kUG8kAaP-ILTbeIKFOA6xKNg-CL3cYDAWpkHRgfyVGAzv4kW7_WTnPreBxiFX7znipn44AZ9Wegx-ri6_vx6c-USIBWpMckp8jjuQlQJwyeaoOD5zw_luS2wBozoFk1FQ8WnW_3e5JxNAundQBFNDcOEkavW1401F12kKFV3_Nh3h7W-PZmdrb9jZ9hyT5aEiHY4sDAFZ3vagbEu9cWYsCaPKeHF7WbdmfXPJFsDPHtAO3LPIygkrEsIliq09ND3cHMggn9QDR8fEFfbAHfEy5Q1LO8QsgeIJYM28Q2jyf1x-58mf66WRrJ1wm3sJpRBWUnYb6UFOOqlZ5sO5hFntSoDDBydzwQqwDV_9nK0--5Uh2BOLpbNZ90ywqk_W5EMwQTtZWnCW9hpTLD-z9o3pzqYG37183kdAHhCfWbuGPKxQNJ4VmFILKN7lCunDn3MVuVGqvN8aKhpfqP9hpR_Kkf5qLr4NmHlbFiFnffaWzNyN9HyeGk4QfS7Qj45PWAgGJ5I87oMxQ0o2NXPmD-GePVsWty1)

[Commands component](https://plantuml.com/plantuml/png/jLPDRzj64BthLsnzKW0xlFJKKnovG094g6kbwD6Wo4LCW1y4kMfh50Nig6qE2ffR0nH5WnOeUcMTi9BbMFaBmt_KDrbnIP6C1QEe3kBkSFUzcJSpkxoNAZjHay3lVUI5ZZznfJXHAau_iQp4_lhk4q-TJCQJL2PE52ePghjE55YnRuUyPozLhk-DhS77UuTi-cBuo0hiLCa4fkD15CHHo7jYnkyfJ_bIq2-qehVq3l_NbDDryRIO2ImDxD0L8vbyvJcornk0pVP2cVGTtmF4hjWPl1-8_JXETp3zKewjOJJsVCape5xHOertJaiU2tfNd65m1Qf_-1KjYXSxTtgZKtWO77_wZUe7KHZv2148em0wY0TH8CLmRMNW1uyV7uhzmuSyfZye1reEztFGd36Ue8MWDvHX_WnS80Q3yVvWt7V7s7aOfUf98aUVFsASeuFxmn4FwETY2fXhokXAO2yBas7wPbS0-vn50jzrwVkkmEACxSHlCnDHHNXyFvg4hfsSzft01KD3s9qxujkUmC_afk_e5OoGHBul4zxLj9LAy9D-fTTWNj45-mN1PtGfQ4uPv9wozXkHmBjDljGvaUu4c1kC8sFjvdm57NIyPyoinvHRHemLBQrYofdW3Ect7NBH9HngU1Gb84zLOgke5lndDIkxK2h8tlm6u2Lgu1nPPueVEGyVJbckbz6Y9ORdIWpHLyufS1zMingR6UegBtxYGWCPOirr8nLFTU5pLjWdMbYKiO4NGPI_kJS-d8Yw_4t2F-4ue8oYODQLZnfuZS3E1DDNBSRbKFoWou6xubcBrdOScQR0tdy_MEUxoVjAvnaCh7IcMpcZ2y7D8egfbXvBBdd41M6n7cOAwLk9Djq-A8-KuOR1j7irfR-0PghfNCkB_nSwknOcZHD1fsOkO5bnFbXwhCfQEYGoZbY68tvwA39FfanvO2jRQ6rqogjUAcQtEHTsRwoHuZay-gxNEvA-EMAxZWBw7LnppYNliUYYc1dw1PiskhsObYAE05_7RhTz6xsxcpLDLo_dTJBDrev0rzjDDSKeNhWN9n6lNFjj_FslMDrUrHk_3RUbkxSx_F_HTCHIFpzlTpgs69YYSHwtcdPRJt8z8X1Ui-HNvXxH0JJnoZaZlwIC4ycGdSXQBc1Z-Zrcq90NQ5KDJsSOPRjh3XP3rtHESnJwLV4SG01Ze6rIRScvCTRxozoNqx9IQzTaTLhZ-NPRVPbOpEtG0RG5ebKpBwlFXzQDmgVyvYapwuIl5VjDFYxr7SgNHIVCUgSxRjIQHVCgTRmJNtFOSa-6xYJm_mK0)

[Sensors monolith](https://plantuml.com/plantuml/png/jLHDJzjA5DtxLypBof40RzxghGZXILGYKagekaIECm9BjiSQZzkYgX8GzQC22QbgLQaBKDj5jm65OX8-_iBCF-gvav00iTGLICHtPdpFEVVSErxCb2zL7aVEFs4IH7c7iosbqkm_pvF-ouNDK6tbxJpZCX29uebQ24JifP6VKCvyfZfHsFRg_yutQUjPOzMB_KnnYQsDkeXJaL1EIlYE2bN4cVwch_Mbli7lbJxJLsRFxBDM315iHSISDKGY8h0o5syLUAV0iwU7vW1npnmoiuUqWUcQZtQfJ_MPsJ6xkZ27LSUfGwOV9bowGHI2UuvLwZPWjJJDAbW-vssl8TfXn6a5EKDGM2406L3Cz8tPGJ24njzqHDYC95iPvtYUWXiwi3wiL9qcbvb8NCM3hIGCGZyXu1_GzTRg7rYY8tq2Wg7f0hCW03eZie81y0GhWXqIdzr7XRlGj8Fj2uhqwPGfozDKI4Mmt_KrlGNO_eZC2iMYJxw02oLP_cE2WeBBKK89FaaPLON_IwJJQO5q-DhQHblZZVzVAHVFj9Q6m5n7nAMlSibPhVc4Q5RMrvkLSVdKPX91Ne4DJwkDMMC7s7r7wCob4sZlqs1KGJRfuNBRxRG1rXIPsfIyzNILeDUMbnejo_7pOGMwDrTIWUtH57LZIUH9nvVRRZoUDM2LJ62bobux37-JGNOpdcH2PYj-qecufBHx6_SC-ABxDBzcNrymFQ1n7siTaZeq0ETap7jTq36rzm6RcjhRul95673oV6QJsEw4-YlSl1ar6sRCji7ibxLXXbtoL6HaDpr39MJ8xVrPzfNFQa70CxlKd-zKKTWHAc_06yTPuz7aMivOgOz6CYTp0VdtBEe1iF1cqH5Vt3hV0f6bcTx5nwQQNCP7vta0VziW_Si2sA-6fy-f-x1yrnmGGfZCfrBOPbKjoZYhq_vR9jssQYbnwLpgO_jvx59bAEAWVFIwPQDNghECPFhbqP_q5O0_a7QwN-VJcR_r3JYBFEdaSVG7)


**Диаграмма кода (Code)**

[Command service code](https://plantuml.com/plantuml/png/bLNTQXj76BtVfnXofQIEIMz5C55NsrRKaOraqTwLyUmNQ_7iZDYPTNv2m8wXLuNUfD37C8bD7F_Khp3x2dsIdj6ivDtAK2S2wPlp_P-S6JypbXUsp6LaCok9kG_kt9suJzKXlg_mEM7kmltjJc7yS_Y1nJhFkKhPc8g3J50KcVrCpNZ1SoOaDwPdRP7jbfO6GgjnzeROaqQ8cV9KlypK7dl1fK7sF8Tj5IaLx6t4s3VQcuEqooQJGTy3eY1kAVtkzGhKirqsK9XVMO_2iANfXcBZ-S73MKhvJ5jIulLFX2A3rdbUBgo4rCtCsAVrXXlUnTEqFdP4Zg7gmyCkEz1P6hsB8b9btcmvts8x6VO7mnzW9RyayMGdsF7My-tDP2VnEtpV6sp2UBTWO2ocb9QI0WccFZLvq2zLcnZmlBT7HPVj1CDZfFYk90JjQYs9AuyfUcL7fMgorQPbMyjCW9anAggz_s5a9hdg1Fyg7pwLAq5o4R6OjmwutRUUEQnRh4md2gsQ0zaifpTQKHFBJ8oepiFbiilgIv6-RIpJf2ubhzqcmeNDsYtdWYLB1LXupcTFWsUjZjXeAgvkTwkvWamfRPlHeY39VPDbsrezhVIWds7oCxx7yOz9VmAPm1vDXiEWel4aZfEaVwUAUaAGCR5Mjj2otfwhv1M9qb87CLbke1UzJogU7zPOcuerrYRYBd8R5wX-1EfEKnBxFPMEo02cplxgRLjZHkWPeRh_kIqUE8DbxfVMrb8xE0npm6L9BGLPEIRHPPco2-93kNdyrgYVZ1gK_mg-bmsQX8NgfMbVHR1DYylIqCTK8t2gPUfZ0uwY-1VUkqUF7xC7twwlFtgm56oNrM_lcVlapgl3wjYTLU-ZnUiGKfxS9wNkiRw-SST_698GUkHkyB1VLh-xp__jytLfaK8OmusUMgPVj5K87jnVgpdLKVK7SzVkX5N7rI5y7t4u2tzghk7sq2K-Py7fgvmY7pat0V4UH9y7uCHzPBu52lWazyLT0RjYrNl4NW10fuZ0bf-qddTNMwjpF_3gfhxVd-XuxXDzrrFKEAsEqUCIu0N0tq057FLKdz4EA7un6rYAMC1kiDuHF1xrStecF8TmNQFGbzkXdi4gS_al)

# Задание 3. Разработка ER-диаграммы

[ER Diagram](https://plantuml.com/plantuml/png/jLR1RXit4BtlLmnoiHn8wLq8uW1j0WG9WZQ0pWArEzAovP82oRNhH0Li5sXHkCSUUketk6bKgAcS_WBt5_ebdQLOhhIorAHmR40WPqOpRzxmaNfeBDEsB4HYkHK8Zrxqt1ktS5Vkj-gCFfVqVmL_d_q4xfVgt5sxT-wrkwuktHogy-hRweVQHAiBjm3oB_noxfRLPP8SmATQdHXuh9G5gIopN4aOAqrL4e5Z2rQ1vfFSGiOrfhKxoNc6a7AT2apCLrnEcMO522xHdauHbBQvIXAK1FSKxkIgD9WhaPaxm0mqMtYL0Dm5dlLXC7Zo6To___dJ1m_8rklHXsG5zi7YrvOsgKPcCHioIoPU835IJEtBv9kc36NLgmf-jJyv5eoBLNRo39u_-MBmo7kdkPAXx15j9qADc1Xg9O8HuC3ddrbCSybJpkJCbDEfqXy0SzYYf6KBqBrr3V_ZfwlExl7CGxtRKDaAY_OG6vhUx4ATI6gZm6AqgnkMPJVq0f4mw0I8tGqaXrHnhU4CZtcAgqR3UlzithyhEctD4IbKXgAP7C6rfOdUCTV52TCuF2O6kP8ny7rcPb0Q5GvNMDzI2u6H67Rauu9r5LJFoYr9qx-xUNK1xjVgihgeVWGI_clIyJklzwNN-v8IaXops7KfkTr9YL0finzAXKM11Lfzwic8kxrq1CuskGZ6PfQcVSoEcIXflB8iKFEK3CnQpKUbHGhzqYWvEjeOKffZLefmqkBkjWP5SjalHy8scL18SoYX7fqk9V49Co9NoGJ2VgFN8mgJfH1i9D1F8Su4ujzwXF_kIoMRiu-ozX2saL82MLr7acTuGx5zSmOefzb_dO1K5GMJuUOAcuybXsqr9117snPDiCV0sEReTEVGMDeeWBR-8KDB0U64RQj6eoc53MvFfj8QXLTIWxjvK_ultGVm8cGrEPyQwAJ-dHuhPG-JXZYOpNezzIhUh7t8cTds1xNjzaVoGaHIqnIzxGUg3wjtmqDhPziNdoG1w3QkL4dBk3H9C8M8vexnMPWfDLAQY3U4nPD8KHEKg9b54ujjnrYc9sXDRBFb3pEZGb9P33-0rFXVkF5EknSFx8rtzFF1isTT2YRhkVlJBS2zSLVa-TujtDkRRl0_4fGPr3NRbMF3TRgVtJLbchktrNc_yNJMTTPTlm4ETwQDxBRILfUVkBy8wna1N5JV4Lw2IQip_-FogbwxURyMU9EY4-_vBbYpisQaUQkapnVTdSXjDuZmSDE_TX6iF2lDTJOLkORZ8QtAGlm3)

# Задание 4. Создание и документирование API

### 1. Тип API

Укажите, какой тип API вы будете использовать для взаимодействия микросервисов. Объясните своё решение.

### 2. Документация API

Здесь приложите ссылки на документацию API для микросервисов, которые вы спроектировали в первой части проектной работы. Для документирования используйте Swagger/OpenAPI или AsyncAPI.

# Задание 5. Работа с docker и docker-compose

Перейдите в apps.

Там находится приложение-монолит для работы с датчиками температуры. В README.md описано как запустить решение.

Вам нужно:

1) сделать простое приложение temperature-api на любом удобном для вас языке программирования, которое при запросе /temperature?location= будет отдавать рандомное значение температуры.

Locations - название комнаты, sensorId - идентификатор названия комнаты

```
	// If no location is provided, use a default based on sensor ID
	if location == "" {
		switch sensorID {
		case "1":
			location = "Living Room"
		case "2":
			location = "Bedroom"
		case "3":
			location = "Kitchen"
		default:
			location = "Unknown"
		}
	}

	// If no sensor ID is provided, generate one based on location
	if sensorID == "" {
		switch location {
		case "Living Room":
			sensorID = "1"
		case "Bedroom":
			sensorID = "2"
		case "Kitchen":
			sensorID = "3"
		default:
			sensorID = "0"
		}
	}
```

2) Приложение следует упаковать в Docker и добавить в docker-compose. Порт по умолчанию должен быть 8081

3) Кроме того для smart_home приложения требуется база данных - добавьте в docker-compose файл настройки для запуска postgres с указанием скрипта инициализации ./smart_home/init.sql

Для проверки можно использовать Postman коллекцию smarthome-api.postman_collection.json и вызвать:

- Create Sensor
- Get All Sensors

Должно при каждом вызове отображаться разное значение температуры

Ревьюер будет проверять точно так же.


# **Задание 6. Разработка MVP**

Необходимо создать новые микросервисы и обеспечить их интеграции с существующим монолитом для плавного перехода к микросервисной архитектуре. 

### **Что нужно сделать**

1. Создайте новые микросервисы для управления телеметрией и устройствами (с простейшей логикой), которые будут интегрированы с существующим монолитным приложением. Каждый микросервис на своем ООП языке.
2. Обеспечьте взаимодействие между микросервисами и монолитом (при желании с помощью брокера сообщений), чтобы постепенно перенести функциональность из монолита в микросервисы. 

В результате у вас должны быть созданы Dockerfiles и docker-compose для запуска микросервисов. 