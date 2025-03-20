from django.contrib.gis.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class BusinessLocation(models.Model):
    name = models.CharField('Nome', max_length=200)
    description = models.TextField('Descrição', blank=True)
    address = models.CharField('Endereço', max_length=500)
    city = models.CharField('Cidade', max_length=100)
    state = models.CharField('Estado', max_length=2)
    postal_code = models.CharField('CEP', max_length=8)
    phone = models.CharField('Telefone', max_length=20, blank=True)
    email = models.EmailField('E-mail', blank=True)
    website = models.URLField('Website', blank=True)
    
    # Campos de localização
    location = models.PointField('Localização')
    radius = models.IntegerField(
        'Raio de Atuação (km)',
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text='Raio de atuação em quilômetros'
    )
    coverage_area = models.PolygonField('Área de Cobertura', null=True, blank=True)
    
    # Campos de negócio
    business_type = models.CharField('Tipo de Negócio', max_length=100)
    opening_hours = models.JSONField('Horário de Funcionamento', default=dict)
    is_active = models.BooleanField('Ativo', default=True)
    
    # Campos de métricas
    customer_count = models.IntegerField('Número de Clientes', default=0)
    revenue = models.DecimalField('Faturamento', max_digits=12, decimal_places=2, default=0)
    
    # Campos de auditoria
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)
    
    class Meta:
        verbose_name = 'Localização de Negócio'
        verbose_name_plural = 'Localizações de Negócios'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} - {self.city}/{self.state}"
    
    def save(self, *args, **kwargs):
        # Aqui você pode adicionar lógica para calcular a área de cobertura
        # baseada no ponto e raio de atuação
        super().save(*args, **kwargs)
    
    @property
    def coordinates(self):
        """Retorna as coordenadas no formato [longitude, latitude]"""
        return [self.location.x, self.location.y] 