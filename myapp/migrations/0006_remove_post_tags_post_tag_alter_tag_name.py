# Generated by Django 4.2 on 2023-05-13 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_tag_post_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='tags',
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(max_length=200, to='myapp.tag', verbose_name='タグ'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=50, verbose_name='タグ'),
        ),
    ]