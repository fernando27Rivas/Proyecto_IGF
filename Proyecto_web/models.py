# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator

#No se Implemento esto del estado de la visita
Visita_CHOICES = (
    ( 1, 'Solicitada'),
    ( 2, 'Aprobada'),
    ( 3 ,'En proceso'),#Se esta llevando a cabo en el momento
    ( 4 ,'Finalizada'),
)

Vehiculo_CHOICES = (
    ( 1, 'Disponible'),
    ( 2, 'Asignado'),
    ( 3 ,'Mantenimiento'),
    ( 4 ,'Inactivo'),
)

Choices=(
    ('Liviana','Liviana'),
    ('Particular','Particular'),
    ('Pesada','Pesada'),
    ('Pesada-T','Pesada-T'),
)
class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=10,blank=False,null=False)
    estado = models.SmallIntegerField('Estado Vehiculo',choices=Vehiculo_CHOICES,default=1)
    proximo_mantenimiento = models.DateField(null=False,blank=False)
    color = models.CharField(max_length=10, blank=True, null=True)
    id_unidad = models.ForeignKey('UnidadOrganizacional', models.DO_NOTHING, db_column='id_unidad', blank=False, null=False)
    vehiculo = models.Manager()

    def __str__(self):
        return self.placa

    class Meta:
        managed = False
        db_table = 'vehiculo'
        ordering = ["id_vehiculo"]


class UnidadOrganizacional(models.Model):
    id_unidad_organizacional = models.AutoField(primary_key=True)
    unidad_padre = models.ForeignKey('self', models.DO_NOTHING, db_column='unidad_padre',null=True,blank=True)
    nombre = models.CharField(max_length=50)
    departamento = models.CharField(max_length=30)
    activa = models.NullBooleanField(null=False, blank=False,default=True)
    tiene_transporte = models.NullBooleanField(null=False, blank=False,default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'unidad_organizacional'


class Proveedor(models.Model):
    id_proveedor = models.AutoField('Proveedor',primary_key=True)
    nombre = models.CharField(max_length=50,blank=False,null=False)
    id_unidad = models.ForeignKey('UnidadOrganizacional', models.DO_NOTHING, db_column='id_unidad', blank=False, null=False)

    def __str__(self):
        return self.nombre

    class Meta:
        managed = False
        db_table = 'proveedor'

class Mantenimiento(models.Model):
    id_mantenimento = models.AutoField(primary_key=True)
    tipo = models.BooleanField('Tipo',blank=False,null=False)
    descripcion = models.CharField(max_length=100)
    costo = models.FloatField(blank=False, null=False, validators = [MinValueValidator(0)])
    fecha_actual = models.DateField('Fecha Mantenimiento')
    proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='id_proveedor', blank=True, null=True)
    id_vehiculo = models.ForeignKey('Vehiculo', models.DO_NOTHING, db_column='id_vehiculo', blank=False, null=False)

    def __str__(self):
        return '{} {}'.format( self.fecha_actual,self.id_vehiculo.placa)

    class Meta:
        managed = False
        db_table = 'mantenimiento'



class Usuario(models.Model):
    id_usuari=models.AutoField(primary_key=True,db_column='id')
    id_user = models.OneToOneField(User, null=True, db_column='id_user',)
    id_unidad = models.ForeignKey('UnidadOrganizacional', models.DO_NOTHING, db_column='id_unidad')
    def __str__(self):
        return '{} {}'.format(self.id_user.get_username(), self.id_unidad.nombre)

    class Meta:
        managed = False
        db_table = 'usuario'


class Conductor(models.Model):
    id_conductor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=25, null=False, blank=False)
    apellido = models.CharField(max_length=25, null=False, blank=False)
    fecha_nacimiento = models.DateField(blank=False,null=False)
    numero_telefono=models.CharField( max_length=9, help_text='Formato: XXXX-XXXX')
    id_unidad = models.ForeignKey('UnidadOrganizacional', models.DO_NOTHING, db_column='id_unidad')
    licencia=models.CharField( max_length=10,choices=Choices )

    def __str__(self):
        return self.nombre

    class Meta:
       managed = False
       db_table = 'conductor'


class Visita(models.Model):
    id_visita = models.AutoField(primary_key=True)
    fecha_solicitud = models.DateField(auto_now_add=True)
    id_vehiculo = models.ForeignKey(Vehiculo, models.DO_NOTHING, db_column='id_vehiculo', blank=True, null=True)
    fecha_inicio = models.DateTimeField(blank=False, null=True)
    fecha_fin = models.DateTimeField(blank=False, null=True)
    id_unidad = models.ForeignKey(UnidadOrganizacional, models.DO_NOTHING, db_column='id_unidad')
    estado = models.SmallIntegerField()
    destino = models.CharField('Destino viaje', max_length=100,null=False,blank=False)
    id_conductor=models.ForeignKey("Conductor",db_column='id_conductor',null=True,blank=True)
    user = models.OneToOneField(User, null=True,db_column='id_user', help_text='Usuario relacionado')

    def __str__(self):
        return '{} {}'.format( self.id_vehiculo,self.fecha_solicitud)

    class Meta:
        managed = False
        db_table = 'visita'

class Incidencia(models.Model):
    id_incidencia = models.AutoField(primary_key=True)
    fecha = models.DateField('Fecha Incidencia',blank=False, null=False)
    causa = models.CharField(max_length=75, blank=False, null=True)
    consecuencia = models.CharField(max_length=100, blank=False, null=False)
    id_vehiculo = models.ForeignKey('Vehiculo', models.DO_NOTHING, db_column='id_vehiculo', blank=False, null=False)
    id_visita = models.ForeignKey('Visita', models.DO_NOTHING, db_column='id_visita', blank=False, null=False)
    id_mantenimiento=models.ForeignKey('Mantenimiento', models.DO_NOTHING, db_column='id_mantenimiento', blank=True, null=True)

    def __str__(self):
        return '{} {}'.format( self.id_vehiculo.placa,self.fecha)

    class Meta:
        managed = False
        db_table = 'incidencia'