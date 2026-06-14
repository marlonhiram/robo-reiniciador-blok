# Robô Reiniciador Blok

> Automação de reinício de máquinas no Smart Panel (sistema Blok) via reconhecimento de imagem.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-informational?logo=windows)
![Status](https://img.shields.io/badge/Status-Em%20produção-success)

---

## Sobre o projeto

Este projeto nasceu de uma necessidade real do dia a dia: reiniciar dezenas de máquinas
manualmente no sistema **Blok Smart Panel** é uma tarefa repetitiva que consome tempo
e está sujeita a erros humanos.

O robô automatiza esse processo completo:

1. Lê uma lista de máquinas de um arquivo de texto
2. Busca cada máquina no Smart Panel via reconhecimento de imagem
3. Aciona o reinício e confirma o diálogo de segurança
4. Gera um relatório diário com o status de cada máquina processada

O tempo de execução para reiniciar 14 máquinas caiu de aproximadamente **20 minutos**
de trabalho manual para **execução autônoma**, sem intervenção do operador.

---

## Demonstração

> *Adicione aqui um GIF ou screenshot da interface em funcionamento.*

---

## Tecnologias utilizadas

| Biblioteca | Versão | Uso |
|---|---|---|
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | 5.2.2 | Interface gráfica moderna (tema escuro) |
| [PyAutoGUI](https://pyautogui.readthedocs.io) | 0.9.54 | Controle de mouse, teclado e reconhecimento de tela |
| [keyboard](https://github.com/boppreh/keyboard) | 0.13.5 | Atalho global de parada de emergência (F10) |
| [PyInstaller](https://pyinstaller.org) | 6.3.0 | Empacotamento como executável `.exe` |

---

## Estrutura do projeto

```
robo-reiniciador-blok/
├── app.py               # Interface gráfica (apenas UI)
├── automation.py        # Lógica de automação (apenas o robô)
├── config.py            # Configurações centralizadas (coordenadas, caminhos, tempos)
├── calibrador.py        # Utilitário para capturar coordenadas de tela
├── maquinas.example.txt # Modelo do arquivo de lista de máquinas
├── requirements.txt     # Dependências do projeto
├── assets/              # Imagens de referência para reconhecimento de tela
│   ├── caixa_pesquisa.png
│   ├── confirmacao.png
│   ├── erro.png
│   ├── lupa.png
│   └── botao_reiniciar.png
└── relatorios/          # Relatórios gerados automaticamente (ignorado pelo Git)
```

### Por que essa separação?

| Arquivo | Responsabilidade |
|---|---|
| `app.py` | Só sabe mostrar janelas e reagir a cliques |
| `automation.py` | Só sabe interagir com o Smart Panel |
| `config.py` | Centraliza tudo que pode mudar (coordenadas, tempos, caminhos) |

Essa separação segue o princípio **SRP (Single Responsibility Principle)**: cada arquivo
tem uma única razão para ser modificado. Se a interface mudar, só `app.py` é tocado.
Se as coordenadas mudarem (troca de monitor, por exemplo), só `config.py` é editado.

---

## Pré-requisitos

- Windows 10 ou superior
- Python 3.10+
- Smart Panel (Blok) instalado e acessível

---

## Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/marlonhiram/robo-reiniciador-blok.git
cd robo-reiniciador-blok

# 2. Crie e ative um ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt
```

---

## Configuração

### 1. Lista de máquinas

Copie o arquivo de exemplo e preencha com os identificadores das suas máquinas:

```bash
copy maquinas.example.txt maquinas.txt
```

Edite `maquinas.txt` com um identificador por linha:

```
MQ72
MQ07
MQ96
```

### 2. Calibração de coordenadas

As coordenadas de clique variam conforme resolução e posição da janela. Execute o
calibrador para capturar os valores corretos para sua tela:

```bash
python calibrador.py
```

O script guia você passo a passo. Ao final, copie os valores gerados para `config.py`.

---

## Como usar

```bash
python app.py
```

1. Abra o Smart Panel e deixe-o visível na tela
2. Clique em **INICIAR** na interface do robô
3. Aguarde 3 segundos (tempo para focar na janela correta)
4. O robô processa cada máquina e exibe o status no terminal interno
5. Para interromper a qualquer momento: botão **PARAR** ou tecla **F10**

O relatório do dia é salvo automaticamente em `relatorios/relatorio_DD-MM-AAAA.txt`.

---

## Gerar executável (.exe)

Para distribuir o programa sem precisar instalar Python:

```bash
pyinstaller --noconsole --onefile --add-data "assets;assets" app.py
```

O executável será gerado em `dist/app.exe`. Copie junto com as pastas `assets/`
e o arquivo `maquinas.txt`.

---

## Funcionamento interno

```
INICIAR
  │
  ├─► Carrega maquinas.txt
  │
  └─► Para cada máquina:
        │
        ├─► Abre caixa de pesquisa (por imagem ou coordenada)
        ├─► Digita o nome e confirma a busca
        │
        ├─► Detecta resultado na tela:
        │     ├─► [erro.png]        → registra "Não localizada" e avança
        │     ├─► [confirmacao.png] → clica em Reiniciar → clica em SIM
        │     └─► [nenhum]         → registra "Inconsistência visual" e avança
        │
        └─► Salva resultado no relatório do dia
```

---

## Decisões técnicas

**Por que PyAutoGUI e não uma integração via API?**
O Smart Panel não disponibiliza API pública. A automação via reconhecimento de imagem
foi a única abordagem viável sem acesso ao código-fonte do sistema.

**Por que threading?**
A automação leva vários segundos por máquina. Rodar tudo na thread principal travaria
a interface gráfica. A thread secundária mantém a UI responsiva durante todo o processo.

**Por que `self.after()` no log?**
Tkinter não é thread-safe: atualizar widgets de uma thread secundária pode causar
crashes imprevisíveis. O método `after()` agenda a atualização na thread principal,
tornando o log seguro independentemente de onde foi chamado.

---

## Autor

Desenvolvido por **Marlon Hiram De Almeida**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Marlon%20Hiram-blue?logo=linkedin)](https://www.linkedin.com/in/marlon-hiram-de-almeida-17244a239/)
[![GitHub](https://img.shields.io/badge/GitHub-marlonhiram-black?logo=github)](https://github.com/marlonhiram)
