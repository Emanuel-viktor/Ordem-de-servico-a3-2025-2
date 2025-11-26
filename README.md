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

### **Visual Studio Code**
Editor de código utilizado para escrever, organizar e executar o projeto.

![VS Code](https://code.visualstudio.com/assets/images/code-stable.png)
