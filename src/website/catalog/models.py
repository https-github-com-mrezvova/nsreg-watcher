from django.db import models


class Registrator(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField("Наименование", max_length=255)
    nic_handle1 = models.TextField()
    nic_handle2 = models.TextField()
    website = models.TextField("Сайт")
    city = models.CharField("Город", max_length=255)

    def __str__(self):
        return f'{self.id}: {self.name}'

    @staticmethod
    def get_registrator(id):
        return Registrator.objects.get(id=id)

    class Meta:
        verbose_name = 'Регистратор'
        verbose_name_plural = 'Регистраторы'
        app_label = 'catalog'


class ParseHistory(models.Model):
    id = models.BigAutoField(primary_key=True)
    date = models.DateTimeField("Дата парсинга", auto_now=True)

    def __str__(self):
        return str(self.date)

    class Meta:
        app_label = 'catalog'


class Price(models.Model):
    DOMAINS = [
            ("ru", "Ru"),
    ]
    VALID_CHOICES = [
        ("V", "valid"),
        ("A", "absent"),
    ]
    id = models.BigAutoField(primary_key=True)
    registrator = models.ForeignKey(Registrator, on_delete=models.CASCADE)
    domain = models.CharField("Домен", max_length=10, choices=DOMAINS)
    parse = models.ForeignKey(ParseHistory, on_delete=models.CASCADE, null=True)
    price_reg = models.DecimalField("Регистрация", max_digits=10, decimal_places=2)
    price_prolong = models.DecimalField("Продление", max_digits=10, decimal_places=2)
    price_change = models.DecimalField("Перенос", max_digits=10, decimal_places=2)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True, null=True)
    updated_at = models.DateTimeField("Дата изменения", auto_now=True, null=True)
    reg_status = models.CharField("Статус", max_length=1, choices=VALID_CHOICES, default="V")
    prolong_status = models.CharField("Статус", max_length=1, choices=VALID_CHOICES, default="V")
    change_status = models.CharField("Статус", max_length=1, choices=VALID_CHOICES, default="V")

    def __str__(self):
        return f'{self.id}: {self.price_reg}, {self.price_prolong}, {self.price_change}'

    class Meta:
        verbose_name = 'Цена'
        verbose_name_plural = 'Цены'
        app_label = 'catalog'


class Parser(models.Model):
    id = models.BigAutoField(primary_key=True)
    registrator = models.ForeignKey(Registrator, on_delete=models.CASCADE)
    # Assuming the use of Django's default user model
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    contributor_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f'{self.id}: {self.contributor_name}'

    class Meta:
        app_label = 'catalog'


class ParseError(models.Model):
    id = models.BigAutoField(primary_key=True)
    parse = models.ForeignKey(ParseHistory, on_delete=models.CASCADE)
    parser = models.ForeignKey(Parser, on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f'{self.id}: {self.message}'

    class Meta:
        app_label = 'catalog'


class TeamMember(models.Model):
    GENDER_CHOICES = [
        ('M', 'М'),
        ('F', 'Ж'),
    ]

    id = models.AutoField(primary_key=True)
    name = models.CharField("Имя", max_length=255)
    title = models.CharField("Роль", max_length=255)
    contact = models.CharField("https://github.com/", max_length=255, null=True, blank=True)
    photo = models.ImageField("Фото", upload_to='pictures/', null=True, blank=True)
    sex = models.CharField("Пол", max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.name

    def get_avatar(self):
        if not self.photo:
            if self.sex == 'M':
                return 'pictures/no-photo-employee-male-with-backgroud.png'
            elif self.sex == 'F':
                return 'pictures/no-photo-employee-female-with-backgroud.png'
        else:
            return f'pictures/{self.photo.url.split("/")[-1]}'

    def get_contact_url(self):
        if self.contact is None:
            return "#"
        return f'https:///github.com/{self.contact}'

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
        app_label = 'catalog'
