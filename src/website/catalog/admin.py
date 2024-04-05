from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import Registrator, Price, TeamMember

admin.site.empty_value_display = "Нет данных"


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'title', 'contact', 'photo', 'sex')
    search_fields = ('name', 'title', 'contact', 'sex')


admin.site.register(TeamMember, TeamMemberAdmin)


class PriceRegistratorInline(admin.TabularInline):
    model = Price
    readonly_fields = ("last_change_at", "parse_at",)
    fields = ("last_change_at", "parse_at", "domain",
              "price_reg", "reg_status", "price_prolong", "prolong_status", "price_change", "change_status")
    extra = 1
    min_num = 1

    @admin.display(description="Дата парсинга")
    def parse_at(self, obj):
        return obj.parse.date.strftime("%m/%d/%Y, %H:%M:%S")

    @admin.display(description="Последнее изменение")
    def last_change_at(self, obj):
        return obj.updated_at.strftime("%m/%d/%Y, %H:%M:%S")


@admin.register(Registrator)
class RegistratorAdmin(admin.ModelAdmin):
    inlines = (PriceRegistratorInline, )
    list_display = ("name", "website", "city", "price")
    list_filter = ("city",)

    @admin.display(description="Цены регистрации")
    def price(self, obj):
        return list(obj.price_set.values_list("price_reg", flat=True))[-3:]


admin.site.site_title = "Администрирование Ecodomen"
admin.site.site_header = "Администрирование Ecodomen"

admin.site.unregister(Group)
admin.site.unregister(User)
