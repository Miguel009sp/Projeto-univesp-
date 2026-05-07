# Projeto Universidade

Olá Pessoal!!!

Este é um projeto desenvolvido como parte das atividades da **Univesp (Universidade Virtual do Estado de São Paulo)**. 
O objetivo deste repositório é hospedar o código-fonte do framework utilizado para o desenvolvimento da nossa aplicação.

## 🚀 Tecnologias Utilizadas

*   **Python**: Linguagem de programação principal.
*   **Django**: Framework web para o backend.
*   **SQLite**: Banco de dados padrão utilizado no desenvolvimento.

## 📂 Estrutura do Projeto

*   `essencial/`: Configurações principais do sistema.
*   `projeto/`: Pasta de configurações do Django.
*   `siteapp/`: Aplicativo principal com as funcionalidades do site.
*   `manage.py`: Script de gerenciamento do Django.

## 🛠️ Como rodar o projeto localmente

Para rodar este projeto na sua máquina, siga os passos abaixo:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   ```
2. **Entre na pasta do projeto:**
   ```bash
   cd Projeto-universidade
   ```

3. **Crie um ambiente virtual (opcional mais recomendado):** 
```python
python -m venv venv
source venv/Scripts/activate  # No Windows
(env) pip install -r requirements # instala as bibliotecas do projeto
```

4. **Inicie o servidor**
```bash
python manage.py runserver
```

# Como utilizar a API
#### 1. **Raiz da API**
http://localhost:8000/api/ <br>
Nessa URL você pode ver quais endpoints podem ser acessados:
```json
   {
      "terrenos": "http://127.0.0.1:8000/api/terrenos/",
      "casas": "http://127.0.0.1:8000/api/casas/",
      "salas-comerciais": "http://127.0.0.1:8000/api/salas-comerciais/",
      "galpoes-comerciais": "http://127.0.0.1:8000/api/galpoes-comerciais/",
      "sitios": "http://127.0.0.1:8000/api/sitios/",
      "chacaras": "http://127.0.0.1:8000/api/chacaras/",
      "apartamentos": "http://127.0.0.1:8000/api/apartamentos/",
      "vendas": "http://127.0.0.1:8000/api/vendas/",
      "fotos-imovel": "http://127.0.0.1:8000/api/fotos-imovel/"
   }
```

#### 1.1. **Demais urls**
Além das urls da raiz, há também
- `http://127.0.0.1:8000/api/token/` <br> (responsável por pegar o token JWT para autenticar o usuário)
- `http://127.0.0.1:8000/api/token/refresh/` <br> (responsável por pegar o refresh token para o usuário)
- `http://127.0.0.1:8000/api/pessoa-fisica` <br>
(cadastro e listagem de pessoas físicas)
- `http://127.0.0.1:8000/api/pessoa-juridica` <br>
(cadastro e listagem de pessoas juridicas)
- `http://127.0.0.1:8000/api/usuarios` <br>
(lista todos os usuários cadastrados no sistema sem distinção entre pessoa física e jurídica)
- `http://127.0.0.1:8000/api/telefones` <br>
(cadastro e listagem dos telefones dos usuários)
- `http://127.0.0.1:8000/api/enderecos-usuario` <br>
(cadastro e listagem dos endereços dos usuários)

#### 1.2 **Detalhe nas urls:**
As urls da raiz possuem métodos http juntos, por exemplo:
ao acessar `http://127.0.0.1:8000/api/vendas/`, é possível por padrão utilizar o método `POST` para registrar uma venda no banco de dados e `GET` para listar todas as vendas no banco de dados. Porém se adicionar o `id` de alguma venda existente no final do endpoint `http://127.0.0.1:8000/api/vendas/[vendaId]`, mais métodos podem ser acessados, como o `DELETE`, `PUT`, `PATCH` e o `GET` de um só elemento.
As urls da raiz são feitas utilizando o recurso `ModelViewSet` que conseguem agrupar vários tipos de requisição em uma só view.
As [demais urls](README.md#11-demais-urls) são feitas usando `ListCreateAPIView`, sendo possível utilizar só os métodos `POST` e `GET`.

#### 2 **Criando usuário:**
Acesse o endpoint `/api/pessoa-fisica` ou `/api/pessoa-juridica` conforme necessário. Campos gerais:
- `Usuário:` Login exclusivo do usuário, `ex: user1224`. **Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas. SEM ESPAÇOS.**
- `Nome:` Nome do usuário, `ex: Carlos Silva`. 
- `Senha:` Senha do perfil.
- `Endereço de email:` Email do usuário, `ex: email@gmail.com`.
- `Role:` Nível de permissão do usuário no sistema, `ex: o ADMIN tem controle total no sistema`.
- `Foto:` Foto de perfil do usuário.

Demais campos: 
1. **Pessoa física:**
   - `cpf:` Cadastro de pessoa física
   - `rg:` Número da carteira de identifdade
2. **Pessoa Jurídica:**
   - `cnpj:` Cadastro Nacional de Pessoa Jurídica
   - `nome_empresa:` Nome da empresa do usuário
   - `nome_comercial:` Nome comercial do usuário

**OBS:** Nenhum desses campos têm validação.

#### 2.1 **Logando o usuário:**
Acesse o endpoint `/api/token/`. Preencha os campos:
- `Username:` Login exclusivo do usuário, `ex: user1224`
- `Senha:` Senha do perfil.

Exemplo resposta:
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc3ODIwNzA0NCwiaWF0IjoxNzc4MTIwNjQ0LCJqdGkiOiI4ZDViZWM5MzZiZjM0ZDQ1YmVkNGVhOGNjM2ZlMmFhMiIsInVzZXJfaWQiOiIxIn0.4IXfEyYD4Sth5EyZ59UljjZhH63CCTpnbJeJBMKX4U4",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzc4MTI0MjQ0LCJpYXQiOjE3NzgxMjA2NDQsImp0aSI6IjNjYzE5NTQ2Mzk3NjQzNzhiNmRlZmUzMzlkYjcxNTA0IiwidXNlcl9pZCI6IjEifQ.dBF4YsRH5deL3Ekg6-Uvr_BoXi0fXItZJJIMhirru04"
}
```
O token que é usado na aplicação é o `access`. Para fazer login, basta copiar o token e colar em seu devido lugar como `Bearer`.
Após o token expirar, será necessário fazer login novamente.

#### 3 **Cadastro de imóvel:**
Acesse o endpoint do tipo de imóvel que deseja cadastrar. Nesse exemplo, será utilizado o `/api/terrenos`. Note que ao acessar a url, já é possível ver a listagem de terrenos (caso haja algum no banco de dados). Preencha os campos:
- `Bairro:` Bairro que o imóvel é localizado, `ex: Manhattan`
- `Logradouro:` Logradouro do imóvel, `ex: Fifth Avenue`
- `Número:` Número do imóvel
- `Complemento`
- `CEP`
- `Localidade:` Cidade do endereço, `ex: New York City`
- `Sigla`
- `Nome:` Nome que aparecerá no anúncio do imóvel, `ex: Apartamento à venda com 78m², 3 quartos e sem vaga`
- `Descrição`
- `Foto principal:` Foto de destaque do imóvel. As demais fotos são cadastradas no endpoint `/api/fotos-imovel`.
- `Valor original:` Valor que se pede pelo imóvel.
- `Status:` Se o imóvel está oculto para visualizações, ou já foi vendido ou está disponível.
- `Metragem:` Metragem do terreno **campo específico do terreno. Demais tipos de imóveis terão outros campos**.
- `User:` Usuário que está vendendo o terreno.

#### 3.1 **Atualizar imóvel:**
Utilizando ainda 'terreno' como exemplo, acesse o endpoint `/api/terrenos/[id do terreno]`. Ao adicionar o id do terreno no endpoint, é possível utilizar tanto o `PUT` quanto o `PATCH` para atualizar as informações do determinado terreno. Os campos existentes serão retornados com seus valores. Depois disso, troque os valores necessários. 

#### 4 **Cadastrar vendas:**
Acesse o endpoint `/api/vendas/`. Preencha os campos:
- `Preço pedido:` preço que o dono do imóvel pede para a compra
- `Preço final:` preço final da venda que foi acordado
- `Data fechamento:` Data em que a venda foi finalizada.
- `Observações`
- `Status:` se a venda foi finalizada, cancelada ou está sendo executada/
- `Imovel:` qual imóvel que está sendo vendido
- `Comprador:` usuário que está comprando
- `Vendedor:` usuário que está vendendo


✒️ Autores
**Miguel Fonseca- Desenvolvedor Principal - Miguel009sp**
