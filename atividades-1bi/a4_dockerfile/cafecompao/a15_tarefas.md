## A15 - Edit e Delete

### Resumo dos Conceitos Importantes

- Editar e deletar são operações básicas de manipulação de dados em um banco de dados. O Django possui suporte nativo para essas operações através do ORM.
- Nessa tarefa vamos criar as views, rotas e templates para criar, editar e deletar uma Assinatura de cesta de café da manhã para o usuário logado.
- O primeiro passo é criar o model de Assinatura que vai representar a assinatura do usuário. Esse model deve ter os campos de `user`, `cesta`, `observacao` e `data_inicio`. O campo `user` deve ser uma chave estrangeira para o model `User` e o campo `cesta` deve ser uma chave estrangeira para o model `Cesta`. Os campos `data_inicio` deve ser do tipo `DateField`. 

### Model Assinatura

- No arquivo `padarias/models.py` criar o model `Assinatura` 

```python

class Assinatura(models.Model):
    user = models.OneToOneField(
        'auth.User', on_delete=models.CASCADE, verbose_name="Usuário", null=False, help_text="Usuário da assinatura", related_name="assinatura")
    cesta = models.OneToOneField(
        Cesta, on_delete=models.CASCADE, verbose_name="Cesta", null=False, help_text="Cesta da assinatura", related_name="assinatura")
    data_inicio = models.DateField("Data de início", null=False, blank=False, help_text="Data de início da assinatura", auto_now_add=True)
    observacao = models.TextField("Observação", null=True, blank=True, help_text="Observação da assinatura")

```

- Criar a migração para o model `Assinatura` com o comando `python manage.py makemigrations` e aplicar a migração com o comando `python manage.py migrate`

### Create e Update de Assinatura

- No arquivo `padarias/views.py` criar a view `assinatura_create` para criar uma nova assinatura e a view `assinatura_update` para atualização de uma assinatura.  Caso o usuário esteja logado, deve carregar todas as cestas do banco de dados e exibir, basear no protótipo `prototipo/dash_assinatura_update.html`.
- Criar as views no arquivo `padarias/views.py`

```python
# importar model Assinatura
from .models import Padaria, Cesta, Assinatura

@login_required
def assinatura_create(request):
    if request.method == 'POST':
        cesta_id = request.POST.get('cesta')
        observacoes = request.POST.get('observacoes')
        cesta = get_object_or_404(Cesta, id=cesta_id)
        assinatura = Assinatura.objects.create(user=request.user, cesta=cesta, observacao=observacoes)
        messages.success(request, 'Assinatura criada com sucesso!')
        return redirect('dashboard_main')
    cestas = Cesta.objects.all()
    return render(request, 'assinaturas/create.html', {'cestas': cestas})

@login_required
def assinatura_update(request):
    assinatura = get_object_or_404(Assinatura, user=request.user)
    if request.method == 'POST':
        cesta_id = request.POST.get('cesta')
        observacoes = request.POST.get('observacoes')
        cesta = get_object_or_404(Cesta, id=cesta_id)
        assinatura.cesta = cesta
        assinatura.observacao = observacoes
        assinatura.save()
        messages.success(request, 'Assinatura atualizada com sucesso!')
        return redirect('dashboard_main')
    cestas = Cesta.objects.all()
    return render(request, 'assinaturas/update.html', {'assinatura': assinatura, 'cestas': cestas})

```

- Criar as rotas em `urls.py`

```python	
urlpatterns = [
    ...
    path('assinaturas/create/', padarias_views.assinatura_create, name='assinatura_create'),
    path('assinaturas/update/', padarias_views.assinatura_update, name='assinatura_update'),
    ...
] 
```

- Criar os templates para criação e atualização de assinatura
- Criar o arquivo `templates/assinaturas/create.html`

```html
{% extends 'dashboard/base_logged.html' %}
{% load static %}

{% block title %}Criar Assinatura - Café com Pão{% endblock %}

{% block dashboard_content %}
  <h1 class="text-2xl my-4">Criar Assinatura</h1>
  <form action="{% url 'assinatura_create' %}" method="post" class="space-y-4">
    {% csrf_token %}
    <div>
      <label for="cesta" class="block text-sm font-medium text-gray-700">Escolha a cesta:</label>
      <select id="cesta" name="cesta" class="select select-bordered w-full max-w-xs">
        {% for cesta in cestas %}
          <option value="{{ cesta.id }}">{{ cesta.nome }}</option>
        {% endfor %}
      </select>
    </div>
    <div>
      <label for="observacoes" class="block text-sm font-medium text-gray-700">Observações:</label>
      <textarea id="observacoes" name="observacoes" rows="4" class="textarea textarea-bordered w-full" placeholder="Digite suas observações aqui..."></textarea>
    </div>
    <div class="flex space-x-4">
      <button type="submit" class="btn btn-primary">Confirmar Assinatura</button>
      <a href="{% url 'dashboard_main' %}" class="btn btn-secondary">Cancelar</a>
    </div>
  </form>
{% endblock %}
```

- Criar arquivo `templates/assinaturas/update.html`

```html
{% extends 'dashboard/base_logged.html' %}
{% load static %}

{% block title %}Alterar Assinatura - Café com Pão{% endblock %}

{% block dashboard_content %}
  <h1 class="text-2xl my-4">Alterar Assinatura</h1>
  <form action="{% url 'assinatura_update' %}" method="post" class="space-y-4">
    {% csrf_token %}
    <div>
      <label for="cesta" class="block text-sm font-medium text-gray-700">Escolha a nova cesta:</label>
      <select id="cesta" name="cesta" class="select select-bordered w-full max-w-xs">
        {% for cesta in cestas %}
          <option value="{{ cesta.id }}" {% if cesta.id == assinatura.cesta.id %}selected{% endif %}>{{ cesta.nome }}</option>
        {% endfor %}
      </select>
    </div>
    <div>
      <label for="observacoes" class="block text-sm font-medium text-gray-700">Observações:</label>
      <textarea id="observacoes" name="observacoes" rows="4" class="textarea textarea-bordered w-full" placeholder="Digite suas observações aqui...">{{ assinatura.observacao }}</textarea>
    </div>
    <div class="flex space-x-4">
      <button type="submit" class="btn btn-primary">Confirmar Alteração</button>
      <a href="{% url 'dashboard_main' %}" class="btn btn-secondary">Cancelar</a>
    </div>
  </form>
{% endblock %}
```

### Delete de Assinatura

- Vamos criar a view, rota e template para cancelar uma assinatura
- Criar a view `assinatura_delete` em `padarias/views.py`

```python
@login_required
def assinatura_delete(request):
    assinatura = get_object_or_404(Assinatura, user=request.user)
    if request.method == 'POST':
        assinatura.delete()
        messages.success(request, 'Assinatura cancelada com sucesso!')
        return redirect('dashboard_main')
    return render(request, 'assinaturas/delete.html', {'assinatura': assinatura})
```

- Criar a rota em `urls.py`

```python
urlpatterns = [
    ...
    path('assinaturas/delete/', padarias_views.assinatura_delete, name='assinatura_delete'),
    ...
]
```

- Usar como base o protótipo `prototipo/dash_assinatura_delete.html`
- Criar arquivo `templates/assinaturas/delete.html`

```html
{% extends 'dashboard/base_logged.html' %}
{% load static %}

{% block title %}Cancelar Assinatura - Café com Pão{% endblock %}

{% block dashboard_content %}
  <div class="">
    <h2 class="text-xl font-bold">Plano Atual</h2>
    <p>Cesta: <span class="font-medium">{{ assinatura.cesta.nome }}</span></p>
    <p>Valor: <span class="font-medium">R$ {{ assinatura.cesta.preco }}</span></p>
    <p>Data de Início: <span class="font-medium">{{ assinatura.data_inicio }}</span></p>
    <div class="mt-6">
      <p class="text-lg">Ops! 😅</p>
      <p class="text-lg">Tem certeza de que quer dar tchau para as delícias matinais do Café com Pão?</p>
      <p class="mt-4">Se mudar de ideia, estamos aqui para te receber de volta com pães quentinhos e cafés especiais. 🥐</p>
    </div>
    <form action="{% url 'assinatura_delete' %}" method="post" class="flex space-x-4 mt-6">
      {% csrf_token %}
      <button type="submit" class="btn btn-primary">Confirmar Cancelamento</button>
      <a href="{% url 'dashboard_main' %}" class="btn btn-secondary">Voltar ao Menu Principal</a>
    </form>
  </div>
{% endblock %}
```


### Atualizar Menu da Área Logada

- Atualizar o template `templates/components/left_menu.html` para incluir o link para a página de criar assinatura e alterar assinatura

```html
<nav class="menu bg-base-200 w-56 p-4">
  <ul>
    <li>
      <a href="{% url 'dashboard_main' %}">
        <i class="bi bi-person"></i>
        Minha Conta
      </a>
    </li>
    {% if user.assinatura %}
    <li>
      <a href="{% url 'assinatura_update' %}">
        <i class="bi bi-pencil-square"></i>
        Alterar Assinatura
      </a>
    </li>
    <li>
      <a href="{% url 'assinatura_delete' %}">
        <i class="bi bi-x-circle"></i>
        Cancelar Assinatura
      </a>
    </li>
    {% else %}
    <li>
      <a href="{% url 'assinatura_create' %}">
        <i class="bi bi-credit-card"></i>
        Assinatura
      </a>
    </li>
    {% endif %}
    <li>
      <form action="{% url 'logout' %}" method="post" class="w-full block">
        {% csrf_token %}
        <button type="submit" class="w-full block text-left cursor-pointer">
          <i class="bi bi-box-arrow-right mr-2"></i>
          Sair
        </button>
      </form>
    </li>
  </ul>
</nav>
```

### Atividade

- Reproduzir os passos acima
Desafio:
- Criar um model de Perfil para cadastrar outras informações importantes do Usuário
- Perfil tem relacionamento 1-1 com User
- Cadastrar algumas informações como: telefone, endereço, CPF, data de nascimento, etc
- Criar uma view para editar o perfil do usuário logado
- Criar rota e template para editar o perfil do usuário logado
- Exibir os dados do perfil na área logada

