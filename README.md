
# 🍕 Sistema de Gerenciamento de Pedidos de Pizza

##  Descrição do Projeto

Este projeto consiste no desenvolvimento de um sistema web simples, implementado com o framework Flask, destinado ao gerenciamento de pedidos de pizza. A aplicação possibilita a realização das principais operações de CRUD (Create, Read, Update, Delete), permitindo que o usuário adicione, visualize, edite e exclua pedidos realizados por clientes. Para o armazenamento dos dados, utiliza-se um banco de dados relacional SQLite, proporcionando uma solução leve e eficaz para o controle das informações.

---

##  Instruções de Execução

### Pré-requisitos

- Python 3 instalado
- Bibliotecas Flask e SQLAlchemy

### Instalação

1. Clone ou baixe este repositório.
2. Acesse a pasta do projeto no terminal.
3. Instale os requisitos:

```bash
pip install flask flask_sqlalchemy
```

4. Execute o aplicativo:

```bash
python app.py
```

5. Acesse no navegador:

```
http://127.0.0.1:5000
```

---

##  Tecnologias Utilizadas

- **Python 3**
- **Flask** – Framework web
- **Flask-SQLAlchemy** – ORM para banco de dados
- **SQLite** – Banco de dados local
- **HTML/CSS** – Templates renderizados com Jinja2

---

## 📁 Estrutura dos Arquivos

```
projeto_pizza/
│
├── app.py                    # Arquivo principal da aplicação Flask
├── pedidos.db                # Banco de dados SQLite
│
├── templates/                # Templates HTML
│   ├── index.html            # Página principal com lista de pedidos
│   ├── editar.html           # Formulário para editar um pedido
│   ├── login.html            # Página de login
│   ├── registro.html         # Página de registro
│
├── static/
│   └── style.css             # Estilo da interface
```

---

##  Observações

- As páginas de login e registro existem mas ainda não estão funcionais.
- O banco de dados é criado automaticamente ao iniciar o app.
- Ideal para fins didáticos ou para expandir funcionalidades futuras (API, autenticação, etc).

## Participantes
---
- Guilherme Humberto
- Ian Gabriel
- Gabriela Simeao
---
