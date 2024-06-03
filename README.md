# ngreg-watcher

[![ecodomen.ru](https://img.shields.io/website?url=https%3A%2F%2Fecodomen.ru%2F)](https://ecodomen.ru/)
[![flake8 linter](https://github.com/ecodomen/nsreg-watcher/actions/workflows/linter.yml/badge.svg)](https://github.com/ecodomen/nsreg-watcher/actions/workflows/linter.yml)
[![deploy and build](https://github.com/ecodomen/nsreg-watcher/actions/workflows/deploy.yml/badge.svg)](https://github.com/ecodomen/nsreg-watcher/actions/workflows/deploy.yml)

[![License MIT](https://img.shields.io/badge/licence-MIT-%3A%2F%2F)](https://opensource.org/license/mit/)
[![Code style black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Python versions](https://img.shields.io/badge/python-_3.10_|_3.11_-blue)](https://www.python.org/)
[![Django versions](https://img.shields.io/badge/django-4.1-blue?logo=django)](https://www.djangoproject.com/)
[![Postgres version](https://img.shields.io/badge/PSQL-14_|_15_|_16-blue?logo=postgresql)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?logo=nginx&logoColor=white)](https://nginx.org/)
[![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?logo=redis&logoColor=white)](https://redis.io/)
[![Telegram](https://img.shields.io/badge/telegram-blue.svg?logo=telegram&logoColor=white)](https://core.telegram.org/bots/api)

# Установка и запуск

### 💡 Необходимо для запуска

>- [Python 3.9 - 3.11](https://www.python.org/downloads/) (python-pip, python-dev)
>- [Docker](https://docs.docker.com/engine/install/)
>- [PostgreSQL](https://www.postgresql.org/download/). Возможен запуск [PostgresSQL в Docker](#база-данных)
>- Для работы Telegram bot необходимо [создать](https://core.telegram.org/bots#how-do-i-create-a-bot) бата и получить
   bot token

### Установка

Клонировать репозиторий:

```shell
git clone git@github.com:ecodomen/nsreg-watcher.git
```

Перейти в директорию проекта:

```shell
cd nsreg-watcher
```

Создать виртуальное окружение.

- Если версии Python, установленная в системе по умолчанию, соответствует [требованиям](#-необходимо-для-запуска),
  выполнить:

```shell
python3 -m venv env
```

- или указать версию Python явно:

```shell
python3.11 -m venv env
```

Активировать виртуальное окружение:

```shell
source env/bin/activate
```

Обновить pip:

```shell
pip install pip -U
```

Установить зависимости:

```shell
pip install -r requirements.txt
```

В корневой директории проекта создать файл `.env` и заполнить его по шаблону [.env.template](.env.template)

### База данных

- Использование локальной СУБД PostgreSQL.
    - Создать базу данных:
   ```shell
   createdb -U postgres -h localhost -p 5432 nsreg
   ```

- Запуск PostgresSQL в Docker.
    - Экспортировать переменные окружения:
   ```shell
   export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
   ```
    - выполнить запуск сервисов:
   ```shell
   sudo docker compose up -d
   ```

Выполнить миграции:

```shell
python src/website/manage.py migrate
```

### Запуск

Запустить dev сервер Django:

```shell
python src/website/manage.py runserver
```

В новом окне терминала перейти в директорию проекта:

```shell
cd <PATH>/nsreg-watcher
```

Выполнить скрипт для запуска scrapy:

```shell
sh runspiders.sh
```

Дождаться завершения парсинга.

# Создание спайдера

В [папке](src/grabber/nsreg/spiders) нужно создать новый парсер с обязательным
нэймингом "nsreg_sitename"

Посмотрите [пример парсера](src/grabber/nsreg/spiders/nsreg_domainshop.py) с использованием композиции:

По аналогии пишете имена, ссылки в классе вашего Спайдера. site_name нужно найти на сайте регистратора:

```python
class NsregDomainshopSpider(scrapy.Spider):
    name = "nsreg_domainshop.py"
    start_urls = ["https://domainshop.ru/services/"]
    allowed_domains = ("domainshop.ru")
    site_names = ("ООО «Лавка доменов»",)
```

Подбираете путь к ценам: покупка домена, продление, перенос. Например:

```
'price_reg': '/html/body/div/div[2]/div/div/div/div/div[3]/div/div/div/div/table/tbody/tr[1]/td[2]/div/text()'
```

Пути можно посмотреть на сайте и скопировать. Могут возникнуть проблемы с тем, что скопированный путь неправильный --
тогда нужно исследовать его самому

Подбираете регулярное выражение (поможет сайт Regex):

```python
regex=r"([0-9]+[.,\s])?руб"
```

```python
# -*- coding: utf-8 -*-
import scrapy

from ..base_site_spider import BaseSpiderComponent


# Пример спайдера для одного сайта
class NsregDomainshopSpider(scrapy.Spider):
    name = "nsreg_domainshop.py"
    start_urls = ["https://domainshop.ru/services/"]
    allowed_domains = ("domainshop.ru")
    # в site_names важно поставить запятую, иначе scrapy вместо целого названия вставит одну букву
    site_names = ("ООО «Лавка доменов»",)

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.component = BaseSpiderComponent(
            start_urls=self.start_urls,
            allowed_domains=self.allowed_domains,
            site_names=self.site_names,
            regex=r"([0-9]+[.,\s])?руб",
            path={
                'price_reg': '/html/body/div/div[2]/div/div/div/div/div[3]/div/div/div/div/table/tbody/tr[1]/td[2]/div/text()',
                'price_prolong': '/html/body/div/div[2]/div/div/div/div/div[3]/div/div/div/div/table/tbody/tr[4]/td[2]/div/p/text()',
                'price_change': '/html/body/div/div[2]/div/div/div/div/div[3]/div/div/div/div/table/tbody/tr[7]/td[2]/div/text()'
            }
        )

    # Метод для обработки ответов на запросы
    def parse(self, response):
        # Применение метода parse компонента BaseSpiderComponent
        return self.component.parse(response)
```

Если вам требуется добавить разные регулярные выражения для каждого из полей, то в поле regex записывается такой dict:

```python
regex = {
    'price_reg': 'your_regex1',
    'price_prolong': 'your_regex2',
    'price_change': 'your_regex3'
}
```

В сложных случаях, когда требуется пройтись по разным страницам внутри сайта, вам необходимо переписать функцию parse.
Для прохода по разным страницам лучше всего добавить соответствующую функцию:

```python
from nsreg.items import NsregItem()
EMPTY_PRICE = {
    'price_reg': None,
    'price_prolong': None,
    'price_change': None,
}

...

def parse_price_change(self, response):
        price_change = response.xpath(self.component.path['price_change']).get()
        price_change = find_price(, price_change)

        item = NsregItem()
        item['name'] = "ООО «Ваш ООО»"
        price = item.get('price', EMPTY_PRICE)
        price['price_change'] = price_change
        item['price'] = price
        price['price_change'] = price_change
        item['price'] = price

        yield item
```

А также вызвать ее из функции parse:

```python
def parse(self, response):
    price_reg = response.xpath(self.pathreg).get()
    price_reg = self.find_price(self.regex_reg, price_reg)

    price_prolong = response.xpath(self.pathprolong).get()
    price_prolong = self.find_price(self.regex_prolong, price_prolong)

    yield scrapy.Request('https://2domains.ru/domains/transfer', callback=self.parse_price_change)

    site_name = self.site_names[0]

    item = NsregItem()
    item['name'] = site_name
    price = item.get('price', EMPTY_PRICE)
    price['price_reg'] = price_reg
    price['price_change'] = price_change
    item['price'] = price
```