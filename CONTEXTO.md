# CONTEXTO DO PROJETO — Robô Reiniciador Blok
> Última atualização: 2026-06-14

---

## 1. Visão Geral

Aplicação desktop Windows que automatiza o reinício de máquinas no sistema **Blok Smart Panel**. O operador mantém uma lista de identificadores de máquinas em `maquinas.txt`; o robô percorre cada entrada, localiza a máquina na interface do Smart Panel via reconhecimento de imagem, aciona o reinício e confirma o diálogo de segurança. Ao final, gera um relatório datado com o status de cada máquina processada.

Primeiro projeto Python do autor. Desenvolvido para uso interno em ambiente industrial.

---

## 2. Contas e Serviços

N/A — nenhum serviço externo, nenhuma conta de plataforma.

---

## 3. Stack Técnica

| Tecnologia | Versão | Função |
|---|---|---|
| Python | 3.10+ | Linguagem principal |
| CustomTkinter | 5.2.2 | Interface gráfica (tema escuro) |
| PyAutoGUI | 0.9.54 | Controle de mouse/teclado e reconhecimento de tela por imagem |
| keyboard | 0.13.5 | Registro de hotkey global (F10) |
| PyInstaller | 6.3.0 | Empacotamento como executável `.exe` |

**Fixas e não substituíveis neste projeto:** PyAutoGUI (única abordagem viável sem API do Smart Panel), CustomTkinter (escolha da UI já consolidada no projeto), Windows (PyAutoGUI + keyboard dependem de ambiente Windows).

---

## 4. Variáveis de Ambiente

N/A — todas as configurações ficam em `config.py`. Não há `.env`.

---

## 5. Arquitetura e Design de Sistema

Aplicação desktop monolítica com separação de responsabilidades em três módulos:

- **`app.py`** — camada de apresentação. Conhece a UI, não conhece PyAutoGUI.
- **`automation.py`** — camada de automação. Conhece PyAutoGUI, não conhece Tkinter.
- **`config.py`** — camada de configuração. Centraliza coordenadas, caminhos e tempos; é o único arquivo a editar após calibração ou mudança de ambiente.

`app.py` instancia `BlokAutomation` passando dois callbacks: `callback_log` (para exibir mensagens na UI de forma thread-safe via `self.after()`) e `callback_parar` (para que a automação consulte o estado de `_running` sem acoplar à UI).

A automação roda em thread daemon separada para não travar a interface. Atualizações de widgets Tkinter são sempre agendadas via `self.after(0, ...)` — nunca chamadas diretamente da thread secundária.

---

## 6. Banco de Dados

N/A — sem banco de dados. Persistência limitada a:
- `maquinas.txt` — lista de entrada (leitura)
- `relatorios/relatorio_DD-MM-AAAA.txt` — saída em append diário

---

## 7. Autenticação e Permissões

N/A — aplicação local sem autenticação.

---

## 8. Integrações Externas

N/A — sem chamadas a APIs ou serviços externos.

O Smart Panel (Blok) **não é uma integração via API**: a comunicação ocorre exclusivamente por reconhecimento de imagem e simulação de mouse/teclado via PyAutoGUI. O Smart Panel é tratado como uma caixa preta visual.

---

## 9. Estrutura de Pastas

```
automacao/
├── app.py                  # Interface gráfica (UI apenas)
├── automation.py           # Lógica de automação (BlokAutomation)
├── config.py               # Configurações centralizadas
├── calibrador.py           # Utilitário de captura de coordenadas
├── maquinas.txt            # Lista de máquinas (gitignored — dados da empresa)
├── maquinas.example.txt    # Modelo de maquinas.txt para o repositório
├── requirements.txt        # Dependências pip
├── .gitignore
├── README.md
├── CONTEXTO.md
├── assets/                 # Imagens de referência para reconhecimento de tela
│   ├── caixa_pesquisa.png
│   ├── confirmacao.png
│   ├── erro.png
│   ├── lupa.png
│   └── botao_reiniciar.png
└── relatorios/             # Relatórios gerados (gitignored)
    └── relatorio_DD-MM-AAAA.txt
```

Arquivos removidos (eram versões antigas/quebradas): `interface_blok.py`, `interface_blok - Copia.py`, `blok_automation_v1.py`.

---

## 10. Fluxos Implementados

### Fluxo principal — reinício em lote

1. Usuário clica em **INICIAR** (ou é bloqueado se `_running` já for True)
2. Thread daemon é iniciada; UI permanece responsiva
3. `BlokAutomation.executar()` aguarda 3s (tempo de foco do operador)
4. Para cada máquina em `maquinas.txt`:
   - Verifica F10 e `callback_parar()` — interrompe se positivo
   - Chama `_abrir_caixa_pesquisa()`:
     - Se `caixa_pesquisa.png` já visível → continua
     - Se não → tenta clicar em `lupa.png`; fallback para `COORD_CAMPO_LOCALIZAR`
     - Aguarda até `MAX_TENTATIVAS_CAIXA` × `PAUSA_RETRY_CAIXA` segundos
   - Chama `_pesquisar(nome)`: foca janela clicando 80px acima do OK, limpa campo, digita, confirma
   - Aguarda `PAUSA_APOS_PESQUISA` segundos
   - Detecta resultado:
     - `erro.png` → registra "Não localizada", pressiona ESC
     - `confirmacao.png` → chama `_reiniciar()` (clica SOL → aguarda → clica SIM)
     - Nenhum → registra "Inconsistência visual", pressiona ESC
5. `_salvar_relatorio()` — append em `relatorios/relatorio_DD-MM-AAAA.txt`
6. `_running = False`; botão INICIAR reabilitado via `self.after()`

### Fluxo de parada de emergência

- Botão **PARAR** na UI → seta `_running = False`
- Tecla **F10** (hotkey global registrada no `__init__`) → chama `_parar()` → mesma ação
- A parada só ocorre no início de cada iteração de máquina (não interrompe uma ação PyAutoGUI em curso)

### Calibração de coordenadas

- `calibrador.py` guia o operador por 4 pontos da tela com contagem regressiva de 5s
- Imprime bloco de código pronto para colar em `config.py`
- Executado manualmente sempre que houver mudança de resolução ou layout do Smart Panel

---

## 11. Contratos de Interface

### `BlokAutomation.__init__(callback_log, callback_parar)`

```
callback_log:   (str) -> None   — chamado para cada mensagem de progresso
callback_parar: ()   -> bool    — retorna True quando a execução deve parar
```

Ambos são opcionais; defaults são `print` e `lambda: False`.

### `BlokAutomation.executar()`

```
Retorna: str | None
  str  — caminho absoluto do relatório gerado
  None — se maquinas.txt não existe ou está vazio
```

---

## 12. Ambiente, Deploy e CI/CD

**Desenvolvimento local:**
```bash
pip install -r requirements.txt
python app.py
```

**Geração do executável:**
```bash
pyinstaller --noconsole --onefile --add-data "assets;assets" app.py
# Saída: dist/app.exe
# Copiar junto: assets/, maquinas.txt
```

O módulo `config.py` detecta automaticamente se está rodando como `.py` ou como `.exe` via `getattr(sys, 'frozen', False)` e ajusta `BASE_DIR` para `os.path.dirname(sys.executable)`.

Sem CI/CD — deploy manual via cópia do `.exe` para a máquina do operador.

---

## 13. Middleware e Interceptors

N/A

---

## 14. Riscos e Limitações Conhecidas

- **Dependência de resolução de tela:** coordenadas e imagens de referência são capturadas para uma resolução e posição de janela específicas. Qualquer mudança exige nova calibração.
- **Sem interrupção mid-ação:** F10 e botão PARAR são verificados apenas entre máquinas. Se o PyAutoGUI estiver no meio de uma espera longa (ex: `PAUSA_APOS_PESQUISA = 3.5s`), a parada aguarda o término dessa espera.
- **Sem retry em falha de rede/sistema:** se o Smart Panel travar durante o processo, o robô registra "Inconsistência visual" e avança para a próxima máquina sem tentar novamente.
- **Confiança de imagem fixa:** os valores de `CONFIANCA_PADRAO` e `CONFIANCA_ERRO` em `config.py` foram ajustados empiricamente; variações de tema visual ou DPI do sistema podem exigir ajuste.
- **Relatório em append:** múltiplas execuções no mesmo dia acumulam no mesmo arquivo. Comportamento intencional, mas pode gerar confusão se o operador não souber.

---

## 15. Pendências Abertas

- Preencher dados pessoais no `README.md`: `[Seu Nome]`, `seu-usuario`, `seu-perfil` (LinkedIn e GitHub)
- Inicializar repositório Git e publicar no GitHub
- Adicionar screenshot ou GIF da interface em funcionamento na seção "Demonstração" do README
- Verificar versões exatas das dependências instaladas no ambiente de produção e atualizar `requirements.txt` se necessário (`pip freeze`)
