![embed](https://github.com/user-attachments/assets/f99bf311-dca1-45c0-a7ee-05036b452afc)

Exemplo demonstrativo para o uso da `lib-embed` no transações com TEF.

## Instalação

### Requisitos

É necessário ter o Python 3 instalado em sua máquina.

#### Dependências 
- python3-tk
- python3-pip
- Pillow (via pip)
- python-dotenv (via pip)

### Equipamentos

É obrigatório ter um pinpad para realizar seus testes.

### Clonar

```git
git clone git@github.com:embed-labs/example-lib-embed-python-tef.git
```

### Configurações 

Acessar o diretório, modificar o arquivo .env.example, renomeando para .env e colocando os valores passados pelo time de integração

```
cd example-lib-embed-python-xml
mv .env.example .env
```

Feito isso, executar o programa com python

```
python3 embed_example.py
```

## API

### Fluxos
Vamos definir o fluxo que deve ser seguido para que sua implementação seja realizada seguindo as melhores práticas no uso da nossa API

![geral](https://github.com/user-attachments/assets/16ca412b-4104-453f-aed8-c69d92c445fd)
![tef-credito](https://github.com/user-attachments/assets/26bec95a-4059-46a0-ab3d-f5d84ec36dba)
![tef-debito](https://github.com/user-attachments/assets/98c90120-893e-4511-9a86-5795b9a18116)
![tef-cancelar](https://github.com/user-attachments/assets/969b0d51-05f8-42aa-9b8f-97f6e5e93c39)
![tef-reimprimir](https://github.com/user-attachments/assets/aafa1d13-64e4-46dc-9912-f7626d5dfb5d)

### Métodos

#### 1. Configurar 

Este método realiza a configuração do produto, para este caso TEF

##### 1.1. Assinatura

```c++
char* embed_configurar(char* input);
```

##### 1.2. Parâmetros

Aqui estão as definições para _input_ e _output_ para este método

###### 1.2.1. Input

Pode ser parametrizado de duas maneiras:

1. JSON
```json
{
    "configs": {
        "produto": "tef",                                        
        "sub_produto": "1",                                       
        "infos": {
            "timeout": "300",
            "codigo_ativacao": "",      // gerado pelo time de integração
            "token_autorizacao": "",    // gerado pelo time de integração
            "nome_app": "",
            "versao_app": "",
            "texto_pinpad": "",
        }
    }
}
```
2. Metaparâmetro (obedecendo a sequência)
```c
"tef;1;300;codigo_ativacao;token_autorizacao;nome_app;versao_app;texto_pinpad"
```

###### 1.2.2. Output

O retorno para este método consiste em um Json (sempre), no seguinte formato:

```json
{
  "codigo": 0,
  "mensagem": "Sucesso"
}
```

#### 2. Iniciar

Este método realiza a inicialização do produto, para este caso TEF

##### 2.1. Assinatura

```c++
char* embed_iniciar(char* input);
```

##### 2.2. Parâmetros

Aqui estão as definições para _input_ e _output_ para este método.

###### 2.2.1. Input

Pode ser parametrizado de duas maneiras:

1. JSON
```json
{
    "iniciar": {
        "operacao": "tef"
    }
}
```
2. Metaparâmetro
```c
"tef"
```

###### 2.2.2. Output

O retorno para este método consiste em um JSON (sempre), no seguinte formato:

```json
{
    "codigo": 0,
    "mensagem": "Sucesso",
    "resultado": {
        "status_code": 1,
        "status_message": "iniciado"
    }
}
```

#### 3. Processar

Este método realiza o processamento de transações TEF

##### 3.1. Assinatura

```c++
char* embed_processar(char* input);
```

##### 3.2. Parâmetros

Aqui estão as definições para _input_ e _output_ para este método.

###### 3.2.1. Input

Temos cinco modalidades de processamento que podem ser realizadas:
1. crédito
2. débito
3. cancelar
4. reimprimir
5. abortar (transação atual)
6. get_status (transação atual)

Estas modalidades podem ser parametrizadas de duas formas:

1. JSON
```json
// Crédito
{
    "processar": {
        "operacao": "credito",          // credito 
        "valor": "",                    // em centavos (se R$ 1,00 logo 100)
        "parcelas": "",                 // 1 a 99 (se a vista logo 1)
        "financiamento": "",            // 0 - a vista; 1 - estabelecimento; 2 - administradora
    }
}
// Débito
{
    "processar": {
        "operacao": "débito",           // debito
        "valor": ""                     // em centavos (se R$ 1,00 logo 100)
    }
}
// Cancelar
{
    "processar": {
        "operacao": "cancelar",         // cancelar 
        "valor": "",                    // em centavos (se R$ 1,00 logo 100)
        "data": "",                     // no formato DDMMAAAA  
        "nsu": "",                      // igual está no comprovante recebido com 9 caracteres
    }
}
// Reimprimir
{
    "processar": {
        "operacao": "reimprimir",       // reimprimir 
        "valor": "",                    // em centavos (se R$ 1,00 logo 100)
        "data": "",                     // no formato DDMMAAAA  
        "nsu": "",                      // igual está no comprovante recebido com 9 caracteres
    }
}
// Abortar 
{
    "processar": {
        "operacao": "abortar"           // abortar 
    }
}
// Get Status
{
    "processar": {
        "operacao": "get_status"
    }
}
```
2. Metaparâmetro (obedecendo a sequência)
```c
// Crédito
"credito;valor;parcelas;financiamento"
// Débito
"debito;valor"
// Cancelar
"cancelar;valor;data;nsu"
// Reimprimir
"reimprimir;valor;data;nsu"
// Abortar 
"abortar"
// Get Status
"get_status"
```
###### 3.2.2. Output

O retorno para este método consiste em um JSON (sempre), no seguinte formato:

```json
{
    "codigo": 0,
    "mensagem": "Sucesso",
    "resultado": {
        "status_code": 1,
        "status_message": "iniciado"
    }
}
```

#### 4. Finalizar

Este método realiza a finalização de transações TEF

##### 4.1. Assinatura

```c++
char* embed_finalizar(char* input);
```

##### 4.2. Parâmetros

Aqui estão as definições para os _inputs_ e _output_ para este método.

###### 4.2.1. Input

Pode ser parametrizado de duas maneiras:

1. JSON
```json
{
    "finalizar": {
        "operacao": "confirmar",
        "valor": ""                     // 0 - não (desfaz); 1 - sim (confirmar)
    }
}
```
2. Metaparâmetro
```c
"confirmar;valor"
```

###### 4.2.2. Output



#### 5. Obter Valor

Este método responsável por buscar um valor contido em uma chave ou objeto de um JSON válido. 

##### 5.1. Assinatura

```c++
char* embed_obter_valor(char* json, char* key);
```

##### 5.2. Parâmetros

Aqui estão as definições para os _inputs_ e _output_ para este método.

###### 5.2.1. Input

Deve ser informado sempre um String com conteúdo JSON.

```json
// Json
{
    "key1": "value1",
    "key2": {
        "key21": "value21",
        "key22": "value22",
        "key23": "value23",
        "key24": "value24",
        "key25": "value25"
    }
}
```
```c
// Key
"key2.key25"
```

###### 5.2.2. Output

Será um String com valor informado em _key_ se conter em _json_ 

```c
// Value
"value25"
```

### Retornos 

Os possíveis retornos para os métodos utilizando o produto TEF conforme as tabelas abaixo

| codigo | mensagem |
| - | - |
| 0 | Sucesso | 
| -1 | Erro |
| -2 | Deserialize |
| -3 | ProviderError |
| -4 | FileNotFound |
| -31 | TefError |
| -32 | TefMissingParameter |
| -33 | TefInvalidOperation |
| -34 | TefInputBadFormat |
| -34 | TefTransactionError |

| status_code | status_message |
| - | - |
| -1 | erro |
| 0 | finalizado |
| 1 | processando |

### Dados da Transação

Ao finalizar com sucesso a propriedade _result_ além de retornar _status_code_ e _status_message_, contém outros dados da transação conforme a tabela abaixo

| Chave | Descrição |
| - | - |
| tipo_cartao | Modalidade de pagamento (débito ou crédito) |
| valor | Valor do pagamento realizado em centavos |
| parcelas | Quantidade de parcelas (para débito sempre o valor será 1) |
| financiamento | Tipo de financiamento do pagamento (à vista, estabelecimento ou administradora) |
| data_hora | Data/hora do pagamento realizado|
| bandeira | Bandeira do cartão que realizou o pagamento |
| aid | AID do cartão utilizado |
| nsu | Número sequencial único (utilizado para realizar o cancelamento) |
| via_loja | Cupom para realização de impressão com os dados para estabelecimento |
| via_cliente | Cupom para realização de impressão com os dados para cliente |
| numero_cartao | Número do cartão utilizado no pagamento com máscara |
| codigo_autorizacao | Código da autorização do pagamento |
