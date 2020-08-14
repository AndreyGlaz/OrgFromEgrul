from django.db import models


class OrganizationEgrul(models.Model):
    """
    Абстрактная модель для организации (OrganizationEgrul; OrganizationHistory)
    """
    name = models.CharField('Наименование', max_length=1000, blank=True, null=True)
    short_name = models.CharField('Краткое наименование', max_length=1000, blank=True, null=True)
    inn = models.CharField('ИНН', max_length=255, blank=True)
    kpp = models.CharField('КПП', max_length=255, blank=True, null=True, db_index=True)
    ogrn = models.CharField('ОГРН', max_length=255, blank=True, db_index=True)
    okpo = models.CharField('ОКПО', max_length=255, blank=True, null=True)
    okato = models.CharField('ОКАТО', max_length=255, blank=True, null=True)
    index = models.CharField('Почтовый индекс', max_length=255, blank=True, null=True)
    locality = models.CharField('Город', max_length=255, blank=True, null=True)
    street = models.CharField('Улица', max_length=255, blank=True, null=True)
    house = models.CharField('Номер дома', max_length=255, blank=True, null=True)
    building = models.CharField('Строение', max_length=255, blank=True, null=True)

    supervisor_name = models.CharField('Имя руководителя', max_length=255, blank=True, null=True)
    supervisor_surname = models.CharField('Фамилия руководителя', max_length=255, blank=True, null=True)
    supervisor_patronymic = models.CharField('Отчество руководителя', max_length=255, blank=True, null=True)
    supervisor_post = models.CharField('Должность руководителя', max_length=255, blank=True, null=True)

    okopf = models.CharField('ОКОПФ', max_length=255, blank=True, null=True)
    okfs = models.CharField('ОКФС', max_length=255, blank=True, null=True)
    region = models.CharField('Регион', max_length=255, blank=True, null=True)
    okogu = models.CharField('ОКОГУ', max_length=255, blank=True, null=True)
    liquidation_date = models.CharField('Дата ликвидации', max_length=100, blank=True, null=True)

    main_company = models.ForeignKey('self', verbose_name='Основная компания',
                                     on_delete=models.CASCADE, null=True, blank=True)

    # Новые поля необходимо добавлять в абстрактную модель OrganizationAbstract (кроме связей ManyToManyField)
    class Meta:
        verbose_name = 'Организация из егрюл'
        verbose_name_plural = 'Организация из егрюл'


class SuccessfullyProcessedZip(models.Model):
    """
    Словарь для хранения уже обработанных zip
    """
    url_zip = models.CharField('Ссылка на zip файл', max_length=400, blank=True, null=True)
    date = models.DateField('Дата обработки zip', auto_now_add=True)

    class Meta:
        verbose_name = 'Обработанный zip'
        verbose_name_plural = 'Обработанные zip'
