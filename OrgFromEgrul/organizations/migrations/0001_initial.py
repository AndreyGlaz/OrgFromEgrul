# Generated by Django 3.0.7 on 2020-06-14 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationEgrul',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=1000, verbose_name='Наименование')),
                ('short_name', models.CharField(blank=True, max_length=1000, verbose_name='Краткое наименование')),
                ('inn', models.CharField(blank=True, max_length=255, verbose_name='ИНН')),
                ('kpp', models.CharField(blank=True, max_length=255, verbose_name='КПП')),
                ('ogrn', models.CharField(blank=True, max_length=255, verbose_name='ОГРН')),
                ('okpo', models.CharField(blank=True, max_length=255, verbose_name='ОКПО')),
                ('okato', models.CharField(blank=True, max_length=255, verbose_name='ОКАТО')),
                ('index', models.CharField(blank=True, max_length=255, verbose_name='Почтовый индекс')),
                ('locality', models.CharField(blank=True, max_length=255, verbose_name='Город')),
                ('street', models.CharField(blank=True, max_length=255, verbose_name='Улица')),
                ('house', models.CharField(blank=True, max_length=255, verbose_name='Номер дома')),
                ('building', models.CharField(blank=True, max_length=255, verbose_name='Строение')),
                ('supervisor_name', models.CharField(blank=True, max_length=255, verbose_name='Имя руководителя')),
                ('supervisor_surname', models.CharField(blank=True, max_length=255, verbose_name='Фамилия руководителя')),
                ('supervisor_patronymic', models.CharField(blank=True, max_length=255, verbose_name='Отчество руководителя')),
                ('supervisor_post', models.CharField(blank=True, max_length=255, verbose_name='Должность руководителя')),
                ('okopf', models.CharField(blank=True, max_length=255, verbose_name='ОКОПФ')),
                ('okfs', models.CharField(blank=True, max_length=255, verbose_name='ОКФС')),
                ('region', models.CharField(blank=True, max_length=255, verbose_name='Регион')),
                ('okogu', models.CharField(blank=True, max_length=255, verbose_name='ОКОГУ')),
            ],
            options={
                'verbose_name': 'Организация из егрюл',
                'verbose_name_plural': 'Организация из егрюл',
            },
        ),
    ]