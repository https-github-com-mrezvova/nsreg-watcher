
Как известно на чтение и разбор кода уходит больше времени чем на само программирование. Если код написан понятно и однообразно, новым участникам будет проще влиться в работу. Давайте поможем друг другу и ускорим чтение и понимание кода. Для этого необходимо придерживаться некоторых общих рекомендаций.

# Описание комитов

Использовать единый стиль и язык комитов.
```bash
feat: Add awesome feature.
----------------------
fix: Fix some bug.
----------------------
docs: Edit documentation.
```

- `build` - Сборка проекта или изменения внешних зависимостей.
- `ci` - Настройка CI и работа со скриптами.
- `docs` - Обновление документации.
- `feat` - Добавление нового функционала.
- `fix` - Исправление ошибок.
- `perf` - Изменения направленные на улучшение производительности.
- `refactor` - Правки кода без исправления ошибок или добавления новых функций.
- `revert` - Откат на предыдущие коммиты.
- `style` - Правки по кодстайлу (табы, отступы, точки, запятые и т.д.).
- `test` - Добавление тестов.


# Форматирование кода
Форматер [black](https://black.readthedocs.io/en/stable/)

Установка [локально](https://black.readthedocs.io/en/stable/getting_started.html#installation) для каждого проекта в его виртуальное окружение.

Настройте максимальную длину строки в 79 символов согласно [pep8](https://peps.python.org/pep-0008/#maximum-line-length)

### Аргументы для настройки Black
- #### VSCode:

Файл `settings.json`

```
"python.formatting.blackArgs": [
    "--line-length",
    "79",
```

- #### PyCharm:
В настройках "Tools -> Black" установить параметр:

Settings: `-l 79`


# Оформление кода и документации
- Ознакомится с хорошим, подробным гайдом: [Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md#google-python-style-guide)

- Не использовать комментарии вместо докстрингов и наоборот.

```python
ПЛОХО:

class User:
    # Супер класс для супер юзера
    # Без него эта программа не будет так хороша
    def __init__(self):
        ...
```

```python
ХОРОШО:

class User:
    """Супер класс для супер юзера

    Без него эта программа не будет так хороша
    """

    def __init__(self):
        ...
```

- Не использовать встрочные комментариев.

```python
ПЛОХО:

class Parser(models.Model):
    ...
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Assuming the use of Django's default user model
    ...
```
```python
ХОРОШО:

class Parser(models.Model):
    ...
    # Assuming the use of Django's default user model
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    ...
```

- Использовать единый стиль и язык оформления документации и комментариев.
- Использовать построчные переводы каретки like black code style.
Это позволяет при чтении выделять блоки кода, декомпозировать их и читать поблочно, выделяя ключевые части и анализируя их работу.

### Пример описания полей модели:
```python
ПЛОХО:

class TeamMember(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("Имя", max_length=255)
    title = models.CharField("Роль", max_length=255)
    contact = models.CharField("https://github.com/", max_length=255, null=True, blank=True)
    photo = models.ImageField("Фото", upload_to='pictures/', null=True, blank=True)
```

```python
ХОРОШО:

class TeamMember(models.Model):
    id = models.AutoField(
        primary_key=True,
    )
    name = models.CharField(
        verbose_name="Имя",
        max_length=255,
    )
    title = models.CharField(
        verbose_name="Роль",
        max_length=255,
    )
    photo = models.ImageField(
        verbose_name="Фото",
        upload_to="pictures/",
        null=True,
        blank=True,
    )
```

### Пример описания url:
```python
ПЛОХО:

urlpatterns = [
    path("", views.registrator_list, name="registrator_list"),
    path("list/", views.registrator_list, name="registrator_list"),
    path("partner/<int:id>/",views.registrator_details,name="registrator_details"),
    path("admin/", admin.site.urls),
    path("about-us/", views.about, name="about-us"),
]
```

```python
ХОРОШО:

urlpatterns = [
    path(
        "",
        views.registrator_list,
        name="registrator_list",
    ),
    path(
        "list/",
        views.registrator_list,
        name="registrator_list",
    ),
    path(
        "partner/<int:id>/",
        views.registrator_details,
        name="registrator_details",
    ),
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "about-us/",
        views.about,
        name="about-us",
    ),
]
```
- Не засорять проект закомментированными кусками кода.
- Комментарии имеющие характер напоминания о действиях с кодом, отмечать тегом `TODO:` В любой IDE есть плагины для быстрого поиска, анализа и работы с такими комментариями, а про обычный комментарий без тега, можно и забыть.
```python
# TODO: Fix the code.
def bad_func()
    ...
```
- Использовать одинаковый стиль кавычек. Black с этим поможет.
