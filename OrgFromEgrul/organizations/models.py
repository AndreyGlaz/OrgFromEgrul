from django.db import models


class OrganizationEgrul(models.Model):
    """
    Абстрактная модель для организации (OrganizationEgrul; OrganizationHistory)
    """
    name = models.CharField('Наименование', max_length=1000, blank=True)
    short_name = models.CharField('Краткое наименование', max_length=1000, blank=True)
    inn = models.CharField('ИНН', max_length=255, blank=True)
    kpp = models.CharField('КПП', max_length=255, blank=True)
    ogrn = models.CharField('ОГРН', max_length=255, blank=True)
    okpo = models.CharField('ОКПО', max_length=255, blank=True)
    okato = models.CharField('ОКАТО', max_length=255, blank=True)
    index = models.CharField('Почтовый индекс', max_length=255, blank=True)
    locality = models.CharField('Город', max_length=255, blank=True)
    street = models.CharField('Улица', max_length=255, blank=True)
    house = models.CharField('Номер дома', max_length=255, blank=True)
    building = models.CharField('Строение', max_length=255, blank=True)

    supervisor_name = models.CharField('Имя руководителя', max_length=255, blank=True)
    supervisor_surname = models.CharField('Фамилия руководителя', max_length=255, blank=True)
    supervisor_patronymic = models.CharField('Отчество руководителя', max_length=255, blank=True)
    supervisor_post = models.CharField('Должность руководителя', max_length=255, blank=True)

    okopf = models.CharField('ОКОПФ', max_length=255, blank=True)
    okfs = models.CharField('ОКФС', max_length=255, blank=True)
    region = models.CharField('Регион', max_length=255, blank=True)
    okogu = models.CharField('ОКОГУ', max_length=255, blank=True)

    # Новые поля необходимо добавлять в абстрактную модель OrganizationAbstract (кроме связей ManyToManyField)
    class Meta:
        verbose_name = 'Организация из егрюл'
        verbose_name_plural = 'Организация из егрюл'
