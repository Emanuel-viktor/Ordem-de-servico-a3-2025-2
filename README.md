# 🧾 Documento de Requisitos do Sistema  
## Sistema de Gestão de Clientes e Ordens de Serviço

---

## 👥 **Autores do Projeto**

| Nome | RA |
|------|------|
| Maiquel Brassiani | 13623110385 |
| João Victor Gabriel Rodrigues de Lima | 1362312519 |
| Roberto Carlos da Silva Figueiredo | 1362318889 |
| Emanuel Viktor de Souza Bezerra | 1362416509 |
| Tiago Anderson Fernandes Filho | 1362314424 |
| João Pedro Firmo Lira da Costa | 1362316447 |

---

## 🏷️ Nome do Projeto

**Sistema de Gestão de Clientes e Ordens de Serviço**

---
🌐 GitHub Pages
https://emanuel-viktor.github.io/Ordem-de-servico-a3-2025-2/

## 📘 1. Introdução

### 1.1 Propósito  
Este documento descreve os **requisitos funcionais e não funcionais** do sistema de gestão de clientes, técnicos e ordens de serviço (O.S.).  
Serve como referência para desenvolvimento, validação e manutenção.

### 1.2 Escopo  
O sistema permitirá:

- Cadastro de clientes  
- Cadastro de técnicos  
- Abertura e gerenciamento de Ordens de Serviço  
- Consulta de relatórios e histórico  

### 1.3 Definições, Acrônimos e Abreviações

| Termo | Definição |
|-------|-----------|
| CPF | Cadastro de Pessoa Física |
| CNPJ | Cadastro Nacional da Pessoa Jurídica |
| O.S. | Ordem de Serviço |
| CRUD | Create, Read, Update e Delete |
| PDF | Formato de documento portátil |

---

## ⚙️ 2. Descrição Geral

### 2.1 Perspectiva do Produto  
Aplicação em **Python** com banco local.  
Foco em simplicidade, produtividade e expansão futura.

### 2.2 Funcionalidades Principais

- Cadastro de clientes  
- Cadastro de técnicos  
- Abertura e atualização de O.S.  
- Relatórios  
- Histórico de atendimentos  

### 2.3 Restrições

- CPF/CNPJ não podem ser duplicados  
- Número de O.S. gerado automaticamente  
- Campos obrigatórios validados  

### 2.4 Suposições e Dependências

- Usuário tem acesso ao sistema  
- Informações fornecidas são reais  
- Python instalado no ambiente  

---

## 🧩 3. Requisitos Funcionais

| Código | Requisito | Descrição | Prioridade |
|--------|-----------|-----------|-----------|
| RF001 | Cadastro de Cliente | Cadastrar clientes com todos os campos obrigatórios. | Alta |
| RF002 | Cadastro de Técnico | Registrar técnicos com informações completas. | Alta |
| RF003 | Abertura de O.S. | Criar O.S. vinculada a cliente e técnico. | Alta |
| RF004 | Atualização de Status | Atualizar status da O.S. | Alta |
| RF005 | Consulta de Histórico | Exibir histórico de atendimentos do cliente. | Média |
| RF006 | Checklist de Segurança | Registrar checklist obrigatório antes do serviço. | Média |
| RF007 | Materiais/Equipamentos | Registrar materiais usados. | Baixa |

---

## 🧱 4. Requisitos Não Funcionais

| Código | Requisito | Descrição | Prioridade |
|--------|-----------|-----------|-----------|
| RNF001 | Usabilidade | Interface simples e intuitiva. | Alta |
| RNF002 | Segurança | Proteção de dados sensíveis. | Alta |
| RNF003 | Desempenho | Respostas rápidas nas operações. | Média |
| RNF004 | Confiabilidade | Evitar duplicidade e garantir integridade. | Alta |
| RNF005 | Portabilidade | Deve rodar em qualquer ambiente com Python. | Média |

---

## 🗄️ 5. Modelo de Dados

### Tabela: **clientes**
- id  
- nome_razao  
- tipo_pessoa  
- cpf_cnpj  
- cep  
- endereco_completo  
- ponto_referencia  
- email  
- telefone1  
- telefone2  
- responsavel_nome  
- responsavel_cpf  
- responsavel_whatsapp  
- telefone_porteiro  
- observacoes  
- data_cadastro  
- status  
- modalidade_atendimento  

### Tabela: **tecnicos**
- id  
- nome_completo  
- cpf  
- rg  
- telefone  
- email_corporativo  

### Tabela: **ordens_servico**
- id  
- numero_os  
- cliente_id  
- tipo_os  
- data_abertura  
- horario_previsto  
- endereco_execucao  
- relato_cliente  
- descricao_detalhada  
- tecnico_responsavel  
- prioridade  
- canal_origem  
- equipamentos  
- status  
- checklist  
- materiais  
- observacoes_finais  
- data_encerramento  

---

## 🎯 6. Histórias de Usuário

- Como **administrador**, desejo cadastrar clientes.  
- Como **técnico**, desejo visualizar minhas O.S.  
- Como **cliente**, desejo ter meus dados registrados corretamente.  

---

## 💻 7. Requisitos de Interface

- Tela de cadastro de clientes  
- Tela de cadastro de técnicos  
- Tela de abertura de O.S.  
- Filtros por período, prioridade e status  

---

## 🔐 8. Requisitos de Segurança

- Validação de CPF/CNPJ  
- Proteção de dados sensíveis  
- Logs de alterações  

---



## 👨‍💻 9. Autores

Projeto acadêmico — Engenharia de Software  
**Aluno responsável pela compilação:** *Emanuel Viktor*

---

## 🧪 10. Planos de Teste

### Ferramenta Utilizada:
| Ferramenta | Finalidade |
|-----------|------------|
| **pytest** | Execução de testes automatizados unitários e funcionais |

### Comando para execução:
``bash
pytest -v

## 🛠 Tecnologias Utilizadas

### **Python**
Linguagem principal usada para desenvolver e executar os testes automatizados.

![Python](https://www.python.org/static/community_logos/python-logo.png)

---

## ⚙️ 11. Passo a passo — Principais Funções 

Esta seção descreve, de forma prática, o fluxo e os passos realizados pelas principais funções do sistema. Útil para desenvolvedores que vão ler ou estender o código.

### 11.1 `cadastrar_cliente()`
1. Exibe o cabeçalho de cadastro no console.  
2. Solicita ao usuário os campos obrigatórios (nome, tipo de pessoa, CNPJ/CPF) e opcionais (endereço, telefones, observações).  
3. Monta o endereço completo com rua, número, bairro, cidade e estado.  
4. Preenche a `data_cadastro` com a data/hora atual.  
5. Valida que campos obrigatórios não estejam vazios (loop até preenchimento).  
6. Insere o registro na tabela `clientes` do banco SQLite.  
7. Exibe mensagem de sucesso ao final.

### 11.2 `listar_clientes(retornar=False)`
1. Abre conexão com o banco e busca os clientes (id, nome, documento, endereço, email, telefone, status).  
2. Se não houver clientes, imprime mensagem informativa.  
3. Caso haja, imprime uma lista formatada com os dados principais.  
4. Se `retornar=True`, devolve a lista de linhas para uso por outras funções (ex.: seleção em menus).

### 11.3 `cadastrar_tecnico()`
1. Solicita campos do técnico: nome, CPF, RG, telefone, email.  
2. Garante que o nome seja preenchido (campo obrigatório).  
3. Insere o técnico na tabela `tecnicos` do banco.  
4. Mostra confirmação de cadastro.

### 11.4 `abrir_os()`
1. Mostra lista de clientes disponíveis (consulta à tabela `clientes`) e pede que o usuário selecione um cliente.  
2. Recupera o `endereco_execucao` automaticamente do cadastro do cliente selecionado.  
3. Solicita os dados da O.S.: tipo, data de agendamento (padrão: hoje), horário previsto, título e descrição.  
4. Exibe lista de técnicos (se houver) para possível atribuição; permite deixar sem técnico (atribuir depois).  
5. Solicita prioridade, canal de origem, equipamentos, checklist e informações de fotos/assinaturas (opcionais).  
6. Gera um `numero_os` único chamando `gerar_numero_os(cur)` — formato com data + sufixo incremental.  
7. Insere a nova O.S. na tabela `os` com `status` inicial (padrão: "Aberta") e `data_abertura` atual.  
8. Exibe o número da O.S. criada como confirmação.

### 11.5 `listar_os(retornar=False)`
1. Faz join entre `os`, `clientes` e `tecnicos` para obter informações legíveis (número, cliente, tipo, data, status, técnico).  
2. Se não houver O.S., informa ao usuário.  
3. Caso exista, imprime cada ordem com campos principais.  
4. Retorna a lista quando `retornar=True` para uso em outras rotinas.

### 11.6 `fechar_os()`
1. Lista O.S. existentes e solicita ao usuário o ID da O.S. que deseja encerrar.  
2. Recupera a `data_abertura` armazenada na O.S. (se houver).  
3. Calcula `tempo_execucao_min` (diferença entre agora e `data_abertura`, em minutos) quando possível.  
4. Atualiza o registro da O.S. definindo `status = "Concluída"`, grava `data_encerramento` e `tempo_execucao_min`.  
5. Persiste a alteração no banco e confirma a operação.

### 11.7 `export_csv_todas_os(path="export_os.csv")`
1. Realiza consulta completa das O.S. com nomes de cliente e técnico (JOIN).  
2. Abre/Cria o arquivo CSV no caminho informado.  
3. Escreve a primeira linha com os nomes das colunas (cabeçalho).  
4. Percorre todos os registros e grava cada linha no CSV.  
5. Fecha o arquivo e informa quantas O.S. foram exportadas e o caminho do arquivo.

---

# 📏 12. Métricas e Estimativas

Esta seção apresenta as métricas e a técnica de estimativa utilizadas para o planejamento e acompanhamento do desenvolvimento do Sistema de Gestão de Clientes e Ordens de Serviço.

---

## **12.1 Métrica 1 — Produtividade do Desenvolvimento (LOC/hora)**  
A métrica de produtividade mede quantas linhas de código são produzidas por hora, permitindo acompanhar o ritmo do desenvolvimento.

**Aplicação no projeto:**  
Durante a implementação da função **abrir_os()**, foram desenvolvidas cerca de 150 linhas de código em 4 horas de trabalho, resultando em:

**➡️ Produtividade média: 37,5 LOC/h**

---

## **12.2 Métrica 2 — Taxa de Defeitos (bugs por funcionalidade)**  
A Taxa de Defeitos mede a qualidade do software com base na quantidade de erros encontrados durante os testes.

**Aplicação no projeto:**  
Na primeira bateria de testes com **pytest**, foram registrados 4 defeitos em 2 funcionalidades principais (cadastro e listagem), resultando em:

**➡️ Taxa de defeitos: 2 bugs por funcionalidade**

---

## **12.3 Técnica de Estimativa — Planning Poker**  
O Planning Poker utiliza a sequência de Fibonacci (1, 2, 3, 5, 8, 13…) para estimar o esforço e complexidade das tarefas, considerando riscos e incertezas.

**Aplicação no projeto:**  
Para a funcionalidade **fechar_os()**, que envolve cálculos, validações e atualização de status:

- Estimativas sugeridas pelos membros: **3, 5 e 8 pontos**  
- Após discussão técnica:

**➡️ Estimativa final definida: 5 pontos**

---


### Dica rápida para leitura do código
- As funções seguem o padrão: abrir conexão → executar SELECT/INSERT/UPDATE → commit → fechar conexão.  
- Funções que imprimem listas normalmente têm a opção `retornar=True` para obter os dados e reutilizá-los em outros fluxos (por exemplo, seleção de ID no menu).  
- Validações básicas (campos obrigatórios) são feitas no input com `while` até o usuário preencher.

> Essas instruções servem como guia inicial para entender o fluxo do sistema e modificá-lo. Se quiser, gero diagrama de sequência para `abrir_os()` e `fechar_os()` para facilitar a implementação visual.

