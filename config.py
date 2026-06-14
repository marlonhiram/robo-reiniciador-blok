"""
config.py — Configurações centralizadas da aplicação.

Após rodar o calibrador.py, atualize as coordenadas neste arquivo.
Todos os demais módulos importam suas configurações daqui.
"""

import os
import sys

# ---------------------------------------------------------------------------
# Diretório base
# Funciona tanto ao rodar o script .py quanto o executável .exe gerado
# pelo PyInstaller (getattr verifica se está rodando como bundle).
# ---------------------------------------------------------------------------
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Caminhos de arquivos e pastas
# ---------------------------------------------------------------------------
ARQUIVO_MAQUINAS = os.path.join(BASE_DIR, "maquinas.txt")
PASTA_RELATORIOS = os.path.join(BASE_DIR, "relatorios")
PASTA_ASSETS     = os.path.join(BASE_DIR, "assets")

# ---------------------------------------------------------------------------
# Imagens de referência para reconhecimento de tela (PyAutoGUI)
# ---------------------------------------------------------------------------
IMAGEM_CAIXA_PESQUISA = os.path.join(PASTA_ASSETS, "caixa_pesquisa.png")
IMAGEM_ERRO           = os.path.join(PASTA_ASSETS, "erro.png")
IMAGEM_CONFIRMACAO    = os.path.join(PASTA_ASSETS, "confirmacao.png")
IMAGEM_LUPA           = os.path.join(PASTA_ASSETS, "lupa.png")

# ---------------------------------------------------------------------------
# Coordenadas de clique — atualize com os valores do calibrador.py
# ---------------------------------------------------------------------------
COORD_CAMPO_LOCALIZAR   = (273, 64)
COORD_BOTAO_OK_PESQUISA = (217, 229)
COORD_BOTAO_REINICIAR   = (409, 328)
COORD_BOTAO_SIM_CONFIRMA = (883, 549)

# ---------------------------------------------------------------------------
# Tempos de espera (em segundos)
# ---------------------------------------------------------------------------
PAUSA_PADRAO         = 0.5   # Pausa global entre ações do PyAutoGUI
PAUSA_INICIALIZACAO  = 3.0   # Aguarda antes de começar (tempo para o usuário focar na janela certa)
PAUSA_APOS_PESQUISA  = 3.5   # Aguarda o Smart Panel filtrar o resultado
PAUSA_APOS_REINICIO  = 3.0   # Aguarda o sistema processar o comando de reinício
PAUSA_RETRY_CAIXA    = 0.5   # Intervalo entre tentativas de detectar a caixa de pesquisa

# ---------------------------------------------------------------------------
# Parâmetros de reconhecimento de imagem
# ---------------------------------------------------------------------------
MAX_TENTATIVAS_CAIXA = 5    # Número máximo de tentativas para localizar a caixa de pesquisa
CONFIANCA_PADRAO     = 0.8  # Confiança mínima para correspondência de imagem (0.0 a 1.0)
CONFIANCA_ERRO       = 0.7  # Confiança usada na detecção da tela de erro (mais tolerante)
