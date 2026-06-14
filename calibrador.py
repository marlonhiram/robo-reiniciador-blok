"""
calibrador.py — Utilitário de calibração de coordenadas de tela.

Execute este script para capturar as coordenadas corretas de cada elemento
do Smart Panel na sua máquina. Após a calibração, copie os valores exibidos
para as constantes COORD_* dentro do arquivo config.py.

Uso:
    python calibrador.py

Para cada ponto, posicione o cursor sobre o elemento indicado e aguarde
a contagem regressiva. A coordenada será impressa automaticamente.
"""

import time
import pyautogui


PONTOS_DE_CALIBRACAO = [
    ("Campo 'Localizar PC'",                  "COORD_CAMPO_LOCALIZAR"),
    ("Botão 'OK' da Pesquisa",                "COORD_BOTAO_OK_PESQUISA"),
    ("Ícone do SOL (Reiniciar) da máquina",   "COORD_BOTAO_REINICIAR"),
    ("Botão 'SIM' da confirmação de reinício","COORD_BOTAO_SIM_CONFIRMA"),
]

CONTAGEM_REGRESSIVA = 5   # segundos para posicionar o cursor


def capturar_coordenada(descricao):
    """
    Exibe uma contagem regressiva e retorna a posição do cursor ao final.

    Args:
        descricao (str): Nome do elemento que o usuário deve mirar.

    Returns:
        tuple[int, int]: Coordenadas (x, y) do cursor no momento da captura.
    """
    print(f"\n  Posicione o cursor sobre: {descricao}")
    for i in range(CONTAGEM_REGRESSIVA, 0, -1):
        print(f"  {i}...", end=" ", flush=True)
        time.sleep(1)
    coordenada = pyautogui.position()
    print(f"\n  Capturado: {coordenada}")
    return coordenada


def calibrar():
    """
    Executa a calibração completa e exibe o bloco de configuração pronto para copiar.

    Ao final, imprime um trecho de código Python formatado que pode ser colado
    diretamente no arquivo config.py.
    """
    print("=" * 50)
    print("   CALIBRADOR DE COORDENADAS — BLOK REINICIADOR")
    print("=" * 50)
    print("\nInstruções:")
    print("  1. Abra o Smart Panel e deixe-o visível na tela.")
    print("  2. Para cada ponto abaixo, mova o cursor até o")
    print("     elemento indicado e aguarde a contagem.")
    print()

    resultados = {}
    for descricao, constante in PONTOS_DE_CALIBRACAO:
        resultados[constante] = capturar_coordenada(descricao)

    print("\n" + "=" * 50)
    print("  CALIBRAÇÃO CONCLUÍDA!")
    print("  Copie o bloco abaixo para o arquivo config.py:")
    print("=" * 50)
    print()
    for constante, coord in resultados.items():
        print(f"{constante} = {tuple(coord)}")
    print()


if __name__ == "__main__":
    calibrar()
