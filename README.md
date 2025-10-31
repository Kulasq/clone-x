# 🐦 Clone X - Twitter Clone

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-brightgreen.svg)](https://djangoproject.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com)

Clone X é uma rede social inspirada no Twitter, desenvolvida com Django e Bootstrap.  
Compartilhe ideias, interaja em tempo real e descubra o que está acontecendo agora.

---

## ✨ Funcionalidades

### 🔐 Autenticação & Perfil
- **Registro e Login** — Sistema seguro de autenticação  
- **Perfil Personalizável** — Foto, biografia, localização e website  
- **Alteração de Senha** — Interface segura para atualização de credenciais  
- **Exclusão de Conta** — Remoção completa dos dados do usuário  

### 📱 Feed & Conteúdo
- **Feed Personalizado** — Posts de usuários que você segue + seus próprios posts  
- **Criação de Posts** — Texto (até 280 caracteres) + imagens  
- **Paginação** — Navegação suave entre páginas de posts  
- **Upload de Imagens** — Otimização automática (máx. 800×400px)  

### 💬 Interações Sociais
- **Sistema de Likes** — Curta posts com atualização em tempo real (AJAX)  
- **Comentários** — Adicione comentários aos posts  
- **Seguir/Deixar de Seguir** — Conecte-se com outros usuários  
- **Busca de Usuários** — Encontre pessoas por nome ou username  

### 🎨 Interface
- **Design Responsivo** — Funciona perfeitamente em desktop e mobile  
- **Experiência Fluida** — AJAX para ações sem refresh de página  
- **Bootstrap 5** — Interface moderna e acessível  
- **Upload Otimizado** — Redimensionamento automático de imagens  

---

## 🚀 Demonstração

**Acesse a aplicação:** [Em breve no PythonAnywhere](#)

**Credenciais de Teste:**
- Usuário: `demo`  
- Senha: `demopassword123`

---

## 🛠️ Tecnologias

- **Backend:** Django 4.2, Python 3.8+  
- **Frontend:** Bootstrap 5.3, JavaScript Vanilla  
- **Banco de Dados:** SQLite (desenvolvimento) / PostgreSQL (produção)  
- **Armazenamento:** Sistema de arquivos local / AWS S3 (produção)  
- **Deploy:** Heroku, Railway ou PythonAnywhere  

---

## 🗂️ Estrutura do Projeto

```
clone-x/
├── users/              # App de autenticação e perfis  
├── posts/              # App de postagens e interações  
├── core/               # Configurações principais do Django  
   ├── static/          # Arquivos estáticos (CSS, JS, imagens)                
   └── templates/       # Templates HTML  
├── manage.py           # Script principal do Django  
├── requirements.txt    # Dependências do projeto  
└── .env.example        # Exemplo de variáveis de ambiente
```

---

## 📦 Instalação e Uso

### Pré-requisitos
- Python 3.8 ou superior  
- pip (gerenciador de pacotes Python)  
- virtualenv (recomendado)  

### 🏃‍♂️ Executando Localmente

1. **Clone o repositório**
   ```bash
   git clone https://github.com/Kulasq/clone-x.git
   cd clone-x
   ```

2. **Configure o ambiente virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` com suas configurações locais.

5. **Execute as migrações**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crie um superusuário (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Execute o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```

8. **Acesse a aplicação**
   ```
   http://localhost:8000
   ```

---

## ⚙️ Configuração

### Variáveis de Ambiente (.env)
```
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Para Produção
```
DEBUG=False
SECRET_KEY=sua-chave-secreta-muito-longa
DATABASE_URL=postgres://usuario:senha@host:porta/nome_do_banco
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
```

---

## 🧪 Testando

### Executar testes
```bash
python manage.py test
```

### Verificar cobertura de testes
```bash
coverage run manage.py test
coverage report
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas!  
1. Faça um fork do projeto  
2. Crie uma branch com sua feature (`git checkout -b feature/nova-feature`)  
3. Faça commit das alterações (`git commit -m 'Adiciona nova feature'`)  
4. Envie para o repositório (`git push origin feature/nova-feature`)  
5. Abra um Pull Request

---

## 📝 Licença

Este projeto está sob a licença **MIT**.  
Consulte o arquivo [LICENSE](LICENSE) para mais informações.

---

Feito com por [@Kulasq](https://github.com/Kulasq)
