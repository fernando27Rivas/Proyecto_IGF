# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10, blank=True, null=True)
    estado = models.SmallIntegerField(blank=True, null=True)
    primer_mantenimiento = models.DateField(blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'vehiculo'


class Visita(models.Model):
    id_visita = models.AutoField(primary_key=True)
    fecha = models.DateField(blank=True, null=True)
    id_vehiculo = models.ForeignKey(Vehiculo, models.DO_NOTHING, db_column='id_vehiculo', blank=True, null=True)
    hora_inicio = models.TimeField(blank=True, null=True)
    hora_fin = models.TimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'visita'

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    tipo = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proveedor'


class UnidadOrganizacional(models.Model):
    id_unidad_organizacional = models.AutoField(primary_key=True)
    unidad_padre = models.SmallIntegerField(blank=True, null=True)
    unidad_hija = models.SmallIntegerField(blank=True, null=True)
    id_vehiculo = models.ForeignKey('Vehiculo', models.DO_NOTHING, db_column='id_vehiculo', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'unidad_organizacional'

class Incidencia(models.Model):
    id_incidencia = models.AutoField(primary_key=True)
    fecha_mantenimiento = models.DateField(blank=True, null=True)
    causa = models.CharField(max_length=75, blank=True, null=True)
    consecuencia = models.CharField(max_length=100, blank=True, null=True)
    id_vehiculo = models.ForeignKey('Vehiculo', models.DO_NOTHING, db_column='id_vehiculo', blank=True, null=True)
    id_visita = models.ForeignKey('Visita', models.DO_NOTHING, db_column='id_visita', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'incidencia'


class Mantenimiento(models.Model):
    id_mantenimento = models.AutoField(primary_key=True)
    tipo = models.SmallIntegerField(blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    costo = models.FloatField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    id_proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='id_proveedor', blank=True, null=True)
    id_incidencia = models.ForeignKey('Incidencia', models.DO_NOTHING, db_column='id_incidencia', blank=True, null=True)
    id_vehiculo = models.ForeignKey('Vehiculo', models.DO_NOTHING, db_column='id_vehiculo', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mantenimiento'






