from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
# IMPORTANTE: Importa os modelos da sua API core (adicionado Usuario para o vínculo)
from core.models import Casa, Usuario 

def logout_view(request):
    logout(request)
    return redirect('login') # Redireciona para a página de login após o logout


def login_view(request):
    if request.method == "POST":
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        # LOGIN FIXO verificação (você pode mudar depois)
        
        if usuario == 'bragatto' and senha == '123456':
            return redirect('home')  # Redireciona para a página home
        else:
            return render(request, 'login.html', {
                'erro': 'Usuário ou senha inválidos'
            })

    return render(request, 'login.html')

def home_view(request):
    return render(request, 'home.html') 


# CORREÇÃO DA BUSCA: Processa o valor enviado pelo formulário e filtra o banco
def buscar_imoveis_view(request):
    tipo_imovel = request.GET.get('tipo_imovel')
    valor_maximo = request.GET.get('valor_maximo')
    
    # Começa trazendo todas as casas por padrão
    imoveis = Casa.objects.all()
    
    # Se o usuário digitou um valor máximo na busca
    if valor_maximo:
        try:
            # Limpa pontos e vírgulas (Ex: "R$ 350.000,00" vira 350000.00)
            valor_limpo = str(valor_maximo).replace('R$', '').replace('.', '').replace(',', '.').strip()
            preco_limite = float(valor_limpo)
            
            # Filtra no banco apenas imóveis com valor_original menor ou igual ao digitado
            imoveis = imoveis.filter(valor_original__lte=preco_limite)
        except ValueError:
            # Se o usuário digitar letras por erro, não quebra o sistema
            pass

    # Envia a lista de imóveis filtrados de volta para o seu HTML buscar_imoveis.html
    return render(request, 'buscar_imoveis.html', {'imoveis': imoveis})

def cadastro_proprietario_view(request):
    return render(request, 'cadastro_proprietario.html')    

# GESTÃO DE CADASTRO COM LIMPEZA DE MÁSCARA MONETÁRIA
def cadastro_imoveis_view(request):
    if request.method == "POST":
        tipo = request.POST.get('tipo_imovel')
        endereco = request.POST.get('endereco')
        valor_da_tela = request.POST.get('valor_imovel') # Pega o valor formatado (ex: "R$ 420.000,00")
        
        if valor_da_tela:
            try:
                # O Python remove a máscara visual para salvar como número decimal puro (420000.00)
                valor_limpo = str(valor_da_tela).replace('R$', '').replace('.', '').replace(',', '.').strip()
                valor_final = float(valor_limpo)
            except ValueError:
                valor_final = 0.00
        else:
            valor_final = 0.00

        # Seleciona o usuário de testes para não quebrar a restrição NOT NULL da chave estrangeira
        usuario_teste = Usuario.objects.first()

        # Cria o registro definitivo da Casa no banco de dados SQLite
        Casa.objects.create(
            nome=f"{tipo} - {endereco}",
            valor_original=valor_final,
            status="Disponível",
            user=usuario_teste,
            area_terreno=200.0,       # Valores fictícios padrão para evitar restrições NOT NULL do banco
            area_construcao=100.0,
            numero_dormitorios=2,
            numero_suites=0
        )
        return redirect('home')

    return render(request, 'cadastro_imoveis.html')

def cadastro_comprador_view(request):
    return render(request, 'cadastro_comprador.html')
