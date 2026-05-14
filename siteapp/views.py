from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
# AJUSTE: Importado o modelo EnderecoImovel para salvar a localização junto com a Casa
from core.models import Casa, Usuario, FotosImovel, EnderecoImovel 

def logout_view(request):
    logout(request)
    return redirect('login') 


def login_view(request):
    if request.method == "POST":
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        
        if usuario == 'bragatto' and senha == '123456':
            return redirect('home')  
        else:
            return render(request, 'login.html', {
                'erro': 'Usuário ou senha invalidos'
            })

    return render(request, 'login.html')

def home_view(request):
    return render(request, 'home.html') 


# CORREÇÃO DA BUSCA: Filtra por Tipo de Imóvel e Valor Máximo, trazendo o endereço junto
def buscar_imoveis_view(request):
    tipo_imovel = request.GET.get('tipo_imovel')
    valor_maximo = request.GET.get('valor_maximo')
    
    # select_related traz o endereço do MySQL junto com o imóvel, evitando erros na tela
    imoveis = Casa.objects.all().select_related('endereco')
    
    # Se o usuário escolheu um tipo específico (e não a opção "Todos")
    if tipo_imovel and tipo_imovel != "Todos":
        # Filtra no banco pelo nome que começa com o tipo selecionado (Ex: "Casa - ...")
        imoveis = imoveis.filter(nome__istartswith=tipo_imovel)
    
    # Filtro por preço limite
    if valor_maximo:
        try:
            valor_limpo = str(valor_maximo).replace('R$', '').replace('.', '').replace(',', '.').strip()
            preco_limite = float(valor_limpo)
            imoveis = imoveis.filter(valor_original__lte=preco_limite)
        except ValueError:
            pass

    return render(request, 'buscar_imoveis.html', {'imoveis': imoveis})

def cadastro_proprietario_view(request):
    return render(request, 'cadastro_proprietario.html')    


# GESTÃO DE CADASTRO COM LOCALIZAÇÃO POR CEP AUTOMÁTICO E FOTOS
def cadastro_imoveis_view(request):
    if request.method == "POST":
        tipo = request.POST.get('tipo_imovel')
        valor_da_tela = request.POST.get('valor_imovel') 
        
        # AJUSTE: Captura os novos dados de localização preenchidos automaticamente na tela
        cep = request.POST.get('cep')
        logradouro = request.POST.get('logradouro')
        numero = request.POST.get('numero')
        bairro = request.POST.get('bairro')
        cidade = request.POST.get('cidade')
        estado = request.POST.get('estado')

        foto_principal = request.FILES.get('foto_principal')
        fotos_galeria = request.FILES.getlist('fotos_galeria')
        
        if valor_da_tela:
            try:
                valor_limpo = str(valor_da_tela).replace('R$', '').replace('.', '').replace(',', '.').strip()
                valor_final = float(valor_limpo)
            except ValueError:
                valor_final = 0.00
        else:
            valor_final = 0.00

        usuario_teste = Usuario.objects.first()

        # Salva o imóvel principal (Ajustado o campo nome para herdar o logradouro e número de forma limpa)
        nova_casa = Casa.objects.create(
            nome=f"{tipo} - {logradouro}, {numero}",
            valor_original=valor_final,
            status="disponivel",  # Mantendo o padrão minúsculo do choices do seu models.py
            user=usuario_teste,
            foto_principal=foto_principal,
            area_terreno=200.0,       
            area_construcao=100.0,
            numero_dormitorios=2,
            numero_suites=0
        )
        
        # AJUSTE: Cria a linha correspondente na tabela EnderecoImovel apontando para o imóvel acima
        EnderecoImovel.objects.create(
            cep=cep,
            logradouro=logradouro,
            numero=numero,
            bairro=bairro,
            localidade=cidade,         # Guarda a Cidade no campo localidade do seu modelo
            sigla_federacao=estado,    # Guarda o Estado na sigla_federacao
            imovel=nova_casa           # Faz o vínculo OneToOne com a casa criada
        )
        
        # Vincula as imagens adicionais da galeria
        for foto in fotos_galeria:
            FotosImovel.objects.create(
                imovel=nova_casa,
                caminho=foto      
            )
            
        return redirect('home')

    return render(request, 'cadastro_imoveis.html')

def cadastro_comprador_view(request):
    return render(request, 'cadastro_comprador.html')
