import uuid
from django.db import models


class Categoria(models.Model):
    nome = models.CharField(
        verbose_name="Nome", max_length=100, unique=True, null=False, blank=False, help_text="Nome da categoria")

    def __str__(self):
        return self.nome


class Padaria(models.Model):
    nome = models.CharField(
        verbose_name="Nome", max_length=100, unique=True, null=False, blank=False, help_text="Nome da padaria")
    descricao = models.TextField(
        verbose_name="Descrição", null=True, blank=True, help_text="Descrição da padaria")
    cestas = models.ManyToManyField(
        'Cesta', verbose_name="Cestas", help_text="Cestas da padaria", related_name="padarias")

    def __str__(self):
        return self.nome


class Produto(models.Model):
    nome = models.CharField(
        verbose_name="Nome", max_length=100, unique=True, null=False, blank=False, help_text="Nome do produto")
    descricao = models.TextField(
        verbose_name="Descrição", null=True, blank=True, help_text="Descrição do produto")
    preco = models.DecimalField(
        verbose_name="Preço", max_digits=10, decimal_places=2, null=False, blank=False, help_text="Preço do produto")
    categoria = models.ForeignKey(
        Categoria, on_delete=models.SET_NULL, verbose_name="Categoria", null=True, help_text="Categoria do produto")

    def __str__(self):
        return self.nome


class Cesta(models.Model):

    class Niveis(models.TextChoices):
        BASICO = 'B', 'Básico'
        MEDIO = 'M', 'Médio'
        PREMIUM = 'P', 'Premium'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(
        verbose_name="Nome", max_length=100, unique=True, null=False, blank=False, help_text="Nome da cesta")
    descricao = models.TextField(
        verbose_name="Descrição", null=True, blank=True, help_text="Descrição da cesta")
    preco = models.DecimalField(
        verbose_name="Preço", max_digits=10, decimal_places=2, null=False, blank=False, help_text="Preço da cesta")
    produtos = models.ManyToManyField(
        Produto, verbose_name="Produtos", help_text="Produtos da cesta", related_name="cestas")
    nivel = models.CharField(
        verbose_name="Nível", max_length=1, choices=Niveis.choices, default=Niveis.BASICO, help_text="Nível da cesta")

    def __str__(self):
        return self.nome


class Endereco(models.Model):
    rua = models.CharField(
        verbose_name="Rua", max_length=100, null=False, blank=False, help_text="Rua do endereço")
    numero = models.CharField(
        verbose_name="Número", max_length=10, null=False, blank=False, help_text="Número do endereço")
    complemento = models.CharField(
        verbose_name="Complemento", max_length=100, null=True, blank=True, help_text="Complemento do endereço")
    bairro = models.CharField(
        verbose_name="Bairro", max_length=100, null=True, blank=True, help_text="Bairro do endereço")
    cidade = models.CharField(
        verbose_name="Cidade", max_length=100, null=False, blank=False, help_text="Cidade do endereço")
    estado = models.CharField(
        verbose_name="Estado", max_length=2, null=False, blank=False, help_text="Estado do endereço")
    cep = models.CharField(
        verbose_name="CEP", max_length=8, null=False, blank=False, help_text="CEP do endereço")
    padaria = models.OneToOneField(
        Padaria, on_delete=models.CASCADE, verbose_name="Padaria", null=False, help_text="Padaria do endereço", related_name="endereco"
    )

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"

class Assinatura(models.Model):
    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE, verbose_name="Usuário", null=False, help_text="Usuário da assinatura", related_name="assinatura")
    cesta = models.OneToOneField(
        Cesta, on_delete=models.CASCADE, verbose_name="Cesta", null=False, help_text="Cesta da assinatura", related_name="assinatura")
    data_inicio = models.DateField("Data de início", null=False, blank=False, help_text="Data de início da assinatura", auto_now_add=True)
    observacao = models.TextField("Observação", null=True, blank=True, help_text="Observação da assinatura")
