"""
app.py — Interface gráfica do Robô Reiniciador Blok.

Este módulo cuida exclusivamente da apresentação visual: janela, botões e
terminal de log. Toda a lógica de automação fica em automation.py,
mantendo cada arquivo com uma responsabilidade única.
"""

import threading
import time

import keyboard
import customtkinter as ctk

from automation import BlokAutomation


class App(ctk.CTk):
    """
    Janela principal do Robô Reiniciador Blok.

    Fornece uma interface gráfica para iniciar, monitorar e interromper
    a automação de reinício de máquinas no Smart Panel.
    """

    def __init__(self):
        super().__init__()

        self.title("Robô Reiniciador Blok")
        self.geometry("600x600")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

        self._running = False

        self._construir_interface()
        self._registrar_hotkeys()
        self._log("Sistema pronto. Clique em INICIAR para começar.")

    # ------------------------------------------------------------------
    # Construção da interface
    # ------------------------------------------------------------------

    def _construir_interface(self):
        """Cria e posiciona todos os widgets da janela."""
        ctk.CTkLabel(
            self,
            text="ROBÔ REINICIADOR BLOK",
            font=("Roboto", 22, "bold"),
        ).pack(pady=15)

        ctk.CTkLabel(
            self,
            text="Automação de reinício de máquinas via Smart Panel",
            font=("Roboto", 12),
            text_color="#AAAAAA",
        ).pack(pady=(0, 10))

        self._btn_iniciar = ctk.CTkButton(
            self,
            text="INICIAR",
            width=200,
            height=40,
            font=("Roboto", 14, "bold"),
            fg_color="#28a745",
            hover_color="#218838",
            command=self._iniciar,
        )
        self._btn_iniciar.pack(pady=5)

        self._btn_parar = ctk.CTkButton(
            self,
            text="PARAR  (F10)",
            width=200,
            height=40,
            font=("Roboto", 14, "bold"),
            fg_color="#dc3545",
            hover_color="#c82333",
            command=self._parar,
        )
        self._btn_parar.pack(pady=5)

        self._terminal = ctk.CTkTextbox(
            self,
            width=540,
            height=380,
            font=("Consolas", 12),
            text_color="#FFFFFF",
            fg_color="#1E1E1E",
        )
        self._terminal.pack(pady=20, padx=20)

    # ------------------------------------------------------------------
    # Controle de execução
    # ------------------------------------------------------------------

    def _registrar_hotkeys(self):
        """Registra F10 como atalho global de parada de emergência."""
        keyboard.add_hotkey('f10', self._parar)

    def _iniciar(self):
        """Inicia a automação em uma thread separada para não travar a UI."""
        if self._running:
            return

        self._running = True
        self._btn_iniciar.configure(state="disabled")
        self._log("Aguarde... Iniciando em 3 segundos.")

        thread = threading.Thread(target=self._executar, daemon=True)
        thread.start()

    def _parar(self):
        """Solicita a interrupção da automação."""
        if self._running:
            self._running = False
            self._log("Parada solicitada pelo usuário...")

    def _executar(self):
        """Roda na thread secundária: instancia a automação e dispara o processo."""
        automacao = BlokAutomation(
            callback_log=self._log,
            callback_parar=lambda: not self._running,
        )
        automacao.executar()

        self._running = False
        self.after(0, self._btn_iniciar.configure, {"state": "normal"})

    # ------------------------------------------------------------------
    # Log
    # ------------------------------------------------------------------

    def _log(self, texto):
        """
        Registra uma mensagem no terminal visual com timestamp.

        Thread-safe: usa self.after() para garantir que a atualização
        do widget aconteça sempre na thread principal do Tkinter.

        Args:
            texto (str): Mensagem a ser exibida.
        """
        msg = f"[{time.strftime('%H:%M:%S')}] {texto}\n"
        self.after(0, self._inserir_no_terminal, msg)

    def _inserir_no_terminal(self, msg):
        """Insere texto no terminal (deve ser chamado na thread principal do Tkinter)."""
        self._terminal.insert("end", msg)
        self._terminal.see("end")


if __name__ == "__main__":
    app = App()
    app.mainloop()
