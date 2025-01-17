from django.contrib import admin


from import_export.admin import ImportExportModelAdmin, ImportMixin
from import_export import resources, widgets
from import_export.fields import Field
from .models import *

from .custom_sales_table import sales_row_coll_converter


class BillboardsResources(resources.ModelResource):
    id = Field(attribute='id', column_name='ID билборда')
    city = Field(attribute='city', column_name='Город')
    surface_type = Field(attribute='surface_type', column_name='Тип поверхности')
    lighting = Field(attribute='lighting', column_name='Освещение')
    address = Field(attribute='address', column_name='Адрес')
    latitude = Field(attribute='latitude', column_name='Широта')
    longitude = Field(attribute='longitude', column_name='Долгота')
    product_restrictions = Field(attribute='product_restrictions', column_name='Ограничения по продукту')
    district = Field(attribute='district', column_name='Городской округ')
    permission = Field(attribute='permission', column_name='Разрешение ПО', widget=widgets.DateWidget(format='%d.%m.%Y'))

    class Meta:
        model = Billboards
        exclude = ('date_create', 'date_update')
        skip_unchanged = True


class BillboardsAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in Billboards._meta.fields]
    resource_class = BillboardsResources


admin.site.register(Billboards, BillboardsAdmin)


class SidesResources(resources.ModelResource):
    billboard = Field(attribute='billboard', column_name='ID билборда', widget=widgets.ForeignKeyWidget(model=Billboards))
    internal_code = Field(attribute='internal_code', column_name='Вн. код')
    side = Field(attribute='side', column_name='Сторона')
    price = Field(attribute='price', column_name='Прайс с НДС')
    installation_price = Field(attribute='installation_price', column_name='Монтаж. Прайс с НДС')
    plywood_price = Field(attribute='plywood_price', column_name='Переклейка. Прайс с НДС')
    photo_or_scheme = Field(attribute='photo_or_scheme', column_name='Фото/схема')
    digital_views = Field(attribute='digital_views', column_name='Диджитал кол-во показов')
    media_material = Field(attribute='media_material', column_name='Материал носителя')
    technical_requirements = Field(attribute='technical_requirements', column_name='Тех. требования')
    note = Field(attribute='note', column_name='Примечание')

    class Meta:
        model = Sides
        import_id_fields = ('internal_code',)
        exclude = ('date_create', 'date_update')
        fields = ('billboard',)
        skip_unchanged = True


class SidesAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in Sides._meta.fields if field.name != 'id']
    resource_class = SidesResources
    search_fields = ['internal_code', 'billboard__city', 'billboard__address']


admin.site.register(Sides, SidesAdmin)


class ESPARResources(resources.ModelResource):
    id = Field(attribute='id', column_name='ID записи ЕСПАР')
    billboard = Field(attribute='billboard', column_name='ID билборда', widget=widgets.ForeignKeyWidget(model=Billboards))
    side = Field(attribute='side', column_name='Вн. код стороны', widget=widgets.ForeignKeyWidget(model=Sides))
    ESPAR_code = Field(attribute='ESPAR_code', column_name='Код ЭСПАР')
    GRP = Field(attribute='GRP', column_name='GRP')
    OTS = Field(attribute='OTS', column_name='OTS')

    class Meta:
        model = ESPAR
        exclude = ('date_create', 'date_update')
        fields = ('billboard', 'side')
        skip_unchanged = True


class ESPARAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in ESPAR._meta.fields if field.name != 'id']
    resource_class = ESPARResources


admin.site.register(ESPAR, ESPARAdmin)


class SalesResources(resources.ModelResource):
    id = Field(attribute='id', column_name='ID продажи')
    billboard = Field(attribute='billboard', column_name='ID билборда', widget=widgets.ForeignKeyWidget(model=Billboards))
    side = Field(attribute='side', column_name='Вн. код стороны', widget=widgets.ForeignKeyWidget(model=Sides))
    year = Field(attribute='year', column_name='Год')
    month = Field(attribute='month', column_name='Месяц')
    status = Field(attribute='status', column_name='Статус')

    class Meta:
        model = Sales
        exclude = ('date_create', 'date_update')
        fields = ('billboard', 'side')
        skip_unchanged = True

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        sales_row_coll_converter(dataset)



class SalesAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in Sales._meta.fields if field.name != 'id']
    list_filter = ['year', 'month', 'status']
    resource_class = SalesResources


admin.site.register(Sales, SalesAdmin)




