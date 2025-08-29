from django.db import models


class Feedback(models.Model):
    nome = models.CharField("Nome", max_length=100)
    email = models.EmailField("Email")
    assunto = models.CharField("Assunto", max_length=100)
    avaliacao = models.PositiveSmallIntegerField("Avaliação", default=1)
    mensagem = models.TextField("Mensagem", blank=True, null=True)
    telefone = models.CharField("Telefone", max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Feedback de {self.nome} ({self.email})"


class Categoria(models.Model):
    nome = models.CharField(
        verbose_name="Nome", max_length=100, unique=True, null=False, blank=False, help_text="Nome da categoria")

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


class Padaria(models.Model):
    nome = models.CharField(
        verbose_name="Nome", max_length=100, unique=True, null=False, blank=False, help_text="Nome da padaria")
    descricao = models.TextField(
        verbose_name="Descrição", null=True, blank=True, help_text="Descrição da padaria")
    cestas = models.ManyToManyField(
        'Cesta', verbose_name="Cestas", help_text="Cestas da padaria", related_name="padarias")
    imagem = models.ImageField(
        verbose_name="Imagem", upload_to="padarias", null=True, blank=True, help_text="Imagem da padaria")
    telefone = models.CharField(
        verbose_name="Telefone", max_length=20, null=True, blank=True, help_text="Telefone da padaria")
    email = models.EmailField(
        verbose_name="E-mail", null=True, blank=True, help_text="E-mail da padaria")

    def __str__(self):
        return self.nome


class Cesta(models.Model):

    class Niveis(models.TextChoices):
        BASICO = 'B', 'Básico'
        MEDIO = 'M', 'Médio'
        PREMIUM = 'P', 'Premium'

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
    imagem = models.ImageField(
        verbose_name="Imagem", upload_to="cestas", null=True, blank=True, help_text="Imagem da cesta")

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
        Padaria, on_delete=models.CASCADE, verbose_name="Padaria", null=True, help_text="Padaria do endereço", related_name="endereco"
    )

    def __str__(self):
        return f"{self.rua}, {self.numero} - {self.cidade}/{self.estado}"
