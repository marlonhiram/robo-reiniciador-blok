# **AUTOMATIZAR PROCESSOS DE TI**



**Passo 1: Instalação das Bibliotecas**

	**pip install pyautogui keyboard opencv-python**





#### **Passo 2: Preparar as Imagens (Os "Olhos" do Script)**



Salve estas 3 imagens na mesma pasta do seu script Python:



erro.png: Print da frase "Não encontrado".



confirmacao.png: Print do trecho com o IP que aparece logo abaixo da busca.



botao\_reiniciar.png: Print do ícone verde de reiniciar (o sol/engrenagem).





#### **O Script Final (Com Limpeza de Campo)**



##### Este código já trata a limpeza manual do campo de pesquisa caso a máquina anterior não tenha sido encontrada.

&nbsp;	import pyautogui

import time

import os



\# --- 1. CONFIGURAÇÕES ---

ARQUIVO\_MAQUINAS = "maquinas.txt"

SENHA\_SMARTPANEL = "SUA\_SENHA\_AQUI"



\# --- 2. COORDENADAS (Preencha com o Calibrador) ---

COORD\_MENU\_SMARTPANEL = (0, 0)

COORD\_CAMPO\_SENHA = (0, 0)

COORD\_OK\_SENHA = (0, 0)

COORD\_LUPA = (0, 0)

COORD\_CAMPO\_LOCALIZAR = (0, 0)

COORD\_BOTAO\_SIM\_CONFIRMA = (0, 0)



def carregar\_maquinas():

&nbsp;   if not os.path.exists(ARQUIVO\_MAQUINAS):

&nbsp;       print(f"Erro: O arquivo {ARQUIVO\_MAQUINAS} não foi encontrado!")

&nbsp;       return \[]

&nbsp;   with open(ARQUIVO\_MAQUINAS, "r") as f:

&nbsp;       return \[linha.strip() for linha in f if linha.strip()]



def iniciar\_automacao():

&nbsp;   maquinas = carregar\_maquinas()

&nbsp;   if not maquinas:

&nbsp;       return



&nbsp;   print(f"Iniciando automação para {len(maquinas)} máquinas em 5s...")

&nbsp;   time.sleep(5)



&nbsp;   # LOGIN INICIAL

&nbsp;   pyautogui.hotkey('ctrl', 'shift', 'f7')

&nbsp;   time.sleep(2)

&nbsp;   pyautogui.click(COORD\_MENU\_SMARTPANEL)

&nbsp;   time.sleep(1)

&nbsp;   pyautogui.click(COORD\_CAMPO\_SENHA)

&nbsp;   pyautogui.write(SENHA\_SMARTPANEL)

&nbsp;   pyautogui.click(COORD\_OK\_SENHA)

&nbsp;   time.sleep(2)



&nbsp;   for maquina in maquinas:

&nbsp;       print(f"Processando: {maquina}")

&nbsp;       

&nbsp;       # BUSCA

&nbsp;       pyautogui.click(COORD\_LUPA)

&nbsp;       time.sleep(0.5)

&nbsp;       pyautogui.click(COORD\_CAMPO\_LOCALIZAR)

&nbsp;       pyautogui.hotkey('ctrl', 'a'); pyautogui.press('delete') # Limpeza de garantia

&nbsp;       pyautogui.write(maquina)

&nbsp;       time.sleep(2)



&nbsp;       # TESTE 1: NÃO ENCONTRADO

&nbsp;       if pyautogui.locateOnScreen('erro.png', confidence=0.8):

&nbsp;           print(f"X {maquina} não encontrada. Limpando busca...")

&nbsp;           pyautogui.click(COORD\_CAMPO\_LOCALIZAR)

&nbsp;           pyautogui.hotkey('ctrl', 'a'); pyautogui.press('delete')

&nbsp;           pyautogui.press('esc')

&nbsp;           continue



&nbsp;       # TESTE 2: CONFIRMAÇÃO VISUAL (IP/NOME)

&nbsp;       if pyautogui.locateOnScreen('confirmacao.png', confidence=0.8):

&nbsp;           print(f"✅ {maquina} confirmada!")

&nbsp;           botao = pyautogui.locateCenterOnScreen('botao\_reiniciar.png', confidence=0.8)

&nbsp;           if botao:

&nbsp;               pyautogui.click(botao)

&nbsp;               time.sleep(1)

&nbsp;               pyautogui.click(COORD\_BOTAO\_SIM\_CONFIRMA)

&nbsp;               time.sleep(2)

&nbsp;       else:

&nbsp;           print(f"⚠️ {maquina} sem confirmação visual.")

&nbsp;           pyautogui.press('esc')



&nbsp;   print("--- FIM DO PROCESSO ---")



if \_\_name\_\_ == "\_\_main\_\_":

&nbsp;   iniciar\_automacao()





## **Calibrador de Coordenadas (Rode este primeiro)**



&nbsp;	import pyautogui

import time



def pegar\_pontos():

&nbsp;   pontos = \[

&nbsp;       "Opção 'Smartpanel' no menu inicial", 

&nbsp;       "Campo de Senha", 

&nbsp;       "Botão OK da Senha", 

&nbsp;       "Ícone da Lupa", 

&nbsp;       "Campo de texto 'Localizar PC'", 

&nbsp;       "Botão 'SIM' (confirmação final)"

&nbsp;   ]

&nbsp;   for p in pontos:

&nbsp;       print(f"\\nColoque o mouse em: {p}")

&nbsp;       for i in range(5, 0, -1):

&nbsp;           print(f"{i}...", end=" ", flush=True)

&nbsp;           time.sleep(1)

&nbsp;       print(f"\\nCOORDENADA: {pyautogui.position()}")



pegar\_pontos()



## **1. O Arquivo de Máquinas (maquinas.txt)**

**Crie um arquivo chamado maquinas.txt na mesma pasta do seu script. Dentro dele, coloque os nomes das máquinas, um por linha, assim:**

**MQ75**

**MQ76**

**MQ77**

**MQ100**

























