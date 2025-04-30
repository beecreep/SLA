
# 🧠 Guia definitivo do Erick para rodar o projeto Flask

## 🚨 Pré-requisitos

- Python 3.x instalado
- Git e terminal funcional (não adianta ser o cmd do Windows pré-2000)
- Um mínimo de bom senso pra não rodar `pip` fora do `.venv`

---

## ⚙️ Passo a passo

### 1. 🔥 Remover o ambiente virtual antigo (se existir)
```bash
rm -rf .venv
```
> Remove de forma recursiva e forçada. Sem dó.

---

### 2. 🧪 Criar novo ambiente virtual
```bash
python3 -m venv .venv
```
> Isso gera a pasta `.venv` com os binários corretos do Python.

---

### 3. 🚀 Ativar o `.venv`

- **No Windows:**
```bash
source .venv/Scripts/activate
```

- **No Linux/macOS:**
```bash
source .venv/bin/activate
```

---

### 4. 📦 Instalar as dependências do projeto

- Se já tiver o `requirements.txt`:
```bash
pip install -r requirements.txt
```

- Ou manualmente (caso você goste de sofrer):
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv
python -m ensurepip --upgrade 
pip install flask-migrate
pip install flask-login
pip install python-dotenv
```

---

### 5. 🧾 Atualizar ou recriar o `requirements.txt` (se adicionar libs novas)
```bash
pip freeze > requirements.txt
```

---

### 6. 🧼 Desfazer besteira: desinstalar tudo (caso tenha feito cagada fora do `.venv`)
```bash
pip uninstall -r requirements.txt -y
```
> `-r` lê o arquivo. `-y` confirma que sim, você fez bobagem.

---

### 7. 🧨 Caso o `.venv` esteja amaldiçoado:
```bash
rm -rf .venv
# E volta pro passo 2
```

---

### 8. 🏁 Rodar o projeto
```bash
python app.py
```
> Copie o IP que aparecer (tipo `http://127.0.0.1:5000`) e cole no navegador.

---

## 🧠 Resumo do Projeto

```bash
python app.py
```

- Roda o servidor Flask
- Interface web interativa
- Integração com banco de dados
- Front bonitão na medida do possível

---

> 💡 Dica de ouro: se aparecer `ModuleNotFoundError`, você **não ativou o .venv** ou **não instalou as dependências**. Pare de culpar o Python.
