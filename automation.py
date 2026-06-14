"""
automation.py — Lógica de automação do Robô Reiniciador Blok.

Este módulo é responsável exclusivamente por interagir com o Smart Panel:
buscar máquinas, acionar reinícios e gerar relatórios. Não contém nenhum
código de interface gráfica, o que facilita testes e manutenção.
"""

import os
import time

import pyautogui
import keyboard

import config


class BlokAutomation:
    """
    Gerencia a automação de reinício de máquinas no sistema Blok (Smart Panel).

    Utiliza reconhecimento de imagem via PyAutoGUI para interagir com a
    interface gráfica do sistema sem necessidade de API ou integração direta.

    Exemplo de uso:
        def meu_log(msg):
            print(msg)

        automacao = BlokAutomation(callback_log=meu_log)
        automacao.executar()
    """

    def __init__(self, callback_log=None, callback_parar=None):
        """
        Inicializa a automação.

        Args:
            callback_log (callable, opcional): Função chamada para registrar
                mensagens de progresso. Recebe uma string. Padrão: print().
            callback_parar (callable, opcional): Função chamada a cada iteração
                para verificar se a execução deve ser interrompida.
                Deve retornar True para parar. Padrão: nunca para.
        """
        self._log = callback_log or print
        self._deve_parar = callback_parar or (lambda: False)

        pyautogui.useImageNotFoundException(False)
        pyautogui.PAUSE = config.PAUSA_PADRAO

        os.makedirs(config.PASTA_RELATORIOS, exist_ok=True)

    # ------------------------------------------------------------------
    # Métodos públicos
    # ------------------------------------------------------------------

    def executar(self):
        """
        Ponto de entrada principal: processa todas as máquinas e gera relatório.

        Returns:
            str | None: Caminho do arquivo de relatório gerado, ou None se a
                lista de máquinas estiver vazia ou não for encontrada.
        """
        maquinas = self._carregar_maquinas()
        if not maquinas:
            return None

        relatorio = [
            f"Início: {time.strftime('%d/%m/%Y %H:%M:%S')}",
            "-" * 40,
        ]

        time.sleep(config.PAUSA_INICIALIZACAO)

        for maquina in maquinas:
            if self._deve_parar() or keyboard.is_pressed('f10'):
                self._log("Execução interrompida pelo usuário.")
                break

            self._log(f"Processando: {maquina}")
            resultado = self._processar_maquina(maquina)

            if resultado:
                relatorio.append(resultado)

        self._log("Processo concluído.")
        return self._salvar_relatorio(relatorio)

    # ------------------------------------------------------------------
    # Métodos privados — fluxo principal
    # ------------------------------------------------------------------

    def _carregar_maquinas(self):
        """
        Lê a lista de máquinas do arquivo configurado em config.ARQUIVO_MAQUINAS.

        Returns:
            list[str]: Nomes das máquinas. Lista vazia se o arquivo não existir.
        """
        if not os.path.exists(config.ARQUIVO_MAQUINAS):
            self._log(f"ERRO: Arquivo '{config.ARQUIVO_MAQUINAS}' não encontrado!")
            return []

        with open(config.ARQUIVO_MAQUINAS, "r", encoding="utf-8") as f:
            maquinas = [linha.strip() for linha in f if linha.strip()]

        self._log(f"{len(maquinas)} máquinas carregadas.")
        return maquinas

    def _processar_maquina(self, nome):
        """
        Executa o fluxo completo de busca e reinício para uma máquina.

        Args:
            nome (str): Identificador da máquina (ex: "MQ72").

        Returns:
            str | None: Linha de resultado para o relatório, ou None se a
                máquina foi pulada por problema de interface.
        """
        if not self._abrir_caixa_pesquisa():
            self._log(f"[AVISO] Caixa de pesquisa não detectada para {nome}. Pulando...")
            return None

        self._pesquisar(nome)

        if pyautogui.locateOnScreen(config.IMAGEM_ERRO, confidence=config.CONFIANCA_ERRO):
            self._log(f"{nome} — Não localizada no sistema.")
            pyautogui.press('esc')
            time.sleep(1.0)
            return f"Máquina: {nome} - Não localizada."

        if pyautogui.locateOnScreen(config.IMAGEM_CONFIRMACAO, confidence=config.CONFIANCA_PADRAO):
            self._reiniciar()
            self._log(f"{nome} — Reiniciada com sucesso.")
            return f"Máquina: {nome} - Reiniciada com sucesso."

        self._log(f"[AVISO] {nome} — Inconsistência visual. Pulando...")
        pyautogui.press('esc')
        return f"AVISO: {nome} - Inconsistência visual."

    def _salvar_relatorio(self, linhas):
        """
        Salva o relatório de execução em um arquivo datado dentro de relatorios/.

        Usa modo 'append' para não sobrescrever execuções anteriores do mesmo dia.

        Args:
            linhas (list[str]): Linhas de conteúdo do relatório.

        Returns:
            str: Caminho completo do arquivo salvo.
        """
        nome_arquivo = f"relatorio_{time.strftime('%d-%m-%Y')}.txt"
        caminho = os.path.join(config.PASTA_RELATORIOS, nome_arquivo)

        with open(caminho, "a", encoding="utf-8") as f:
            f.write("\n".join(linhas) + "\n\n")

        self._log(f"Relatório salvo em: {caminho}")
        return caminho

    # ------------------------------------------------------------------
    # Métodos privados — interação com a tela
    # ------------------------------------------------------------------

    def _abrir_caixa_pesquisa(self):
        """
        Garante que a caixa de pesquisa do Smart Panel esteja visível.

        Estratégia:
            1. Verifica se a caixa já está aberta.
            2. Se não, tenta clicar no ícone da lupa.
            3. Se a lupa não for encontrada, usa coordenada fixa como fallback.
            4. Aguarda até MAX_TENTATIVAS_CAIXA vezes antes de desistir.

        Returns:
            bool: True se a caixa de pesquisa estiver visível e pronta.
        """
        if pyautogui.locateOnScreen(config.IMAGEM_CAIXA_PESQUISA, confidence=config.CONFIANCA_PADRAO):
            return True

        lupa = pyautogui.locateCenterOnScreen(config.IMAGEM_LUPA, confidence=config.CONFIANCA_PADRAO)
        if lupa:
            pyautogui.click(lupa)
        else:
            pyautogui.click(config.COORD_CAMPO_LOCALIZAR)

        for _ in range(config.MAX_TENTATIVAS_CAIXA):
            time.sleep(config.PAUSA_RETRY_CAIXA)
            if pyautogui.locateOnScreen(config.IMAGEM_CAIXA_PESQUISA, confidence=config.CONFIANCA_PADRAO):
                return True

        return False

    def _pesquisar(self, nome):
        """
        Digita o nome da máquina no campo de pesquisa e confirma.

        O clique acima do campo (80px) garante que a janela receba o foco
        antes de qualquer digitação, evitando que o texto vá para outro lugar.

        Args:
            nome (str): Identificador da máquina a ser pesquisada.
        """
        x, y = config.COORD_BOTAO_OK_PESQUISA
        pyautogui.click(x, y - 80)   # ativa o foco na janela
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('delete')
        pyautogui.write(nome, interval=0.05)
        pyautogui.click(x, y)
        time.sleep(config.PAUSA_APOS_PESQUISA)

    def _reiniciar(self):
        """
        Clica no botão de reinício e confirma o diálogo de confirmação.
        """
        pyautogui.click(*config.COORD_BOTAO_REINICIAR)
        time.sleep(1.5)
        pyautogui.click(*config.COORD_BOTAO_SIM_CONFIRMA)
        time.sleep(config.PAUSA_APOS_REINICIO)
