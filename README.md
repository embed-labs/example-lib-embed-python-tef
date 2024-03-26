# example-lib-embed-python-tef

Exemplo demonstrativo para o uso da `lib-embed` no transações com TEF.

## Instalação

### Requisitos

É necessário ter o Python 3 instalado em sua máquina.

### Clonar

```git
git clone git@github.com:org-dev-embed/example-lib-embed-python-tef.git
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

#### Geral
```mermaid
graph TD;
    A(1 - embed_configurar) -->B(2 - embed_iniciar);    
    B --> C(3 - embed_processar);
    C --> D{4 - embed_processar};
    D --> |processando|D;
    D --> E(5 - embed_finalizar);
```

#### Transações

1. Crédito
```mermaid
flowchart TD;
    cred1(embed_iniciar\ninput = tef) -- result.status_code ==  0 --> cred2(embed_processar\ninput = credito;10000;1;0);
    cred2 -- result.status_code ==  0 --> cred3(embed_processar\ninput = get_status);
    cred3 -- result.status_code ==  1 --> cred3;
    cred3 -- result.status_code ==  0 --> cred4(embed_finalizar\ninput = confirmar;1);
```
2. Débito
```mermaid
flowchart TD;
    deb1(embed_iniciar\ninput = tef) -- result.status_code ==  0 --> deb2(embed_processar\ninput = debito;1);
    deb2 -- result.status_code ==  0 --> deb3(embed_processar\ninput = get_status);
    deb3 -- result.status_code ==  1 --> deb3;
    deb3 -- result.status_code ==  0 --> deb4(embed_finalizar\ninput = confirmar;1);
```
3. Cancelar
```mermaid
flowchart TD;
    canc1(embed_iniciar\ninput = tef) -- result.status_code ==  0 --> canc2(embed_processar\ninput = cancelar;10000;22032024;000000078);
    canc2 -- result.status_code ==  0 --> canc3(embed_processar\ninput = get_status);
    canc3 -- result.status_code ==  1 --> canc3;
    canc3 -- result.status_code ==  0 --> canc4(embed_finalizar\ninput = confirmar;1);
```

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
            "senha_adm": "",            // somente para linux
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
// windows
"tef;1;300;;codigo_ativacao;token_autorizacao;nome_app;versao_app;texto_pinpad"
// linux
"tef;1;300;senha_adm;codigo_ativacao;token_autorizacao;nome_app;versao_app;texto_pinpad"
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
4. abortar (transação atual)
5. get_status (transação atual)

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