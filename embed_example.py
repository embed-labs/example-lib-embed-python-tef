# python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------------------
# imports

from libembed import configurar, iniciar, processar, finalizar, obter_valor
import json
import os
import warnings
from dotenv import load_dotenv
from threading import Thread
from tkinter import (
    Button,
    Tk,
    Label,
    Frame,
    Text,
    StringVar,
    Scrollbar,
    VERTICAL,
    NSEW,
    NS,
    W,
    FLAT,
    SUNKEN,
    END,
    RAISED,
)

warnings.filterwarnings("ignore", category=DeprecationWarning)

# --------------------------------------------------------------------------------------------

LARGE_FONT_STYLE = ("Roboto", 12, "bold")  # brandon, musc, montserrat, coco goose
SMALL_FONT_STYLE = ("Roboto", 11, "bold")
BUTTON_FONT_STYLE = ("Roboto", 9)
COLOR_BG_FRAME = "#000000"  # Dark purple
COLOR_BG_LABEL = "#000000"  # Dark purple
COLOR_FG_LABEL = "#80ff80"  # White
COLOR_BG_ENTRY = "#000000"  # Dark gray
COLOR_BG_BUTTON = "#80ff80"  # Light purple
COLOR_FG_BUTTON = "#000000"  # White
COLOR_BG_BUTTON_DISABLED = "#80ff80"
COLOR_FG_BUTTON_DISABLED = "#666666"

# =========================================
# | =========  PÁGINA PRINCIPAL ========= |
# =========================================


class TefApp:
    # =========================================
    # | ===========  BEGIN LAYOUT =========== |
    # =========================================
    def __init__(self, root):
        self.root = root
        self.root.title("Demo TEF")
        self.root.resizable(width=False, height=False)
        self.root.minsize(700, 400)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame = self.create_main_frame()
        self.value_frame = self.create_value_frame()
        self.operator_frame = self.create_operator_frame()
        self.logs_frame = self.create_logs_frame()
        self.labels = self.create_labels()
        self.buttons = self.create_buttons()
        self.logs_text = self.create_logs_text()
        self.buttons["btn_abortar"]["state"] = "disabled"

    def create_main_frame(self):
        frame = Frame(self.root, bg=COLOR_BG_FRAME, borderwidth=2, border=10)
        frame.grid(column=0, row=0, sticky=NSEW, padx=(5, 5), pady=(5, 5))
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        return frame

    def create_value_frame(self):
        frame = Frame(self.main_frame, bg=COLOR_BG_FRAME, borderwidth=2)
        frame.grid(column=0, row=0, sticky=NSEW, padx=(1, 1), pady=(1, 1))
        return frame

    def create_operator_frame(self):
        frame = Frame(self.main_frame, bg=COLOR_BG_FRAME, borderwidth=2)
        frame.grid(column=0, row=1, sticky=NSEW, padx=(1, 1), pady=(1, 1))
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.rowconfigure(3, weight=1)
        frame.rowconfigure(4, weight=1)
        return frame

    def create_logs_frame(self):
        frame = Frame(self.main_frame, bg=COLOR_BG_FRAME, borderwidth=2)
        frame.grid(column=1, row=0, rowspan=2, sticky=NS, padx=(1, 1), pady=(1, 1))
        return frame

    def create_labels(self):
        self.lbl_value_text = StringVar()
        self.lbl_value_text.set("")
        lbl_value = Label(
            self.value_frame,
            text="TEF",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_value.grid(column=0, row=0, sticky=W, pady=(0, 0))

        lbl_operator_title = Label(
            self.operator_frame,
            text="Operador",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_operator_title.grid(column=0, row=0, columnspan=2, sticky=W, pady=(10, 0))

        lbl_logs = Label(
            self.logs_frame,
            text="Logs Exemplos",
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=LARGE_FONT_STYLE,
        )
        lbl_logs.grid(column=0, row=0, sticky=W, pady=(10, 0))

        self.lbl_operator_text = StringVar()
        self.lbl_operator_text.set("Status")
        lbl_operator = Label(
            self.operator_frame,
            textvariable=self.lbl_operator_text,
            relief=FLAT,
            bg=COLOR_BG_LABEL,
            fg=COLOR_FG_LABEL,
            font=SMALL_FONT_STYLE,
        )
        lbl_operator.grid(column=0, row=1, columnspan=2, sticky=W, pady=(10, 0))

        return lbl_operator

    def create_buttons(self):
        btns = {}

        btns["btn_config"] = Button(
            self.value_frame,
            text="Configurar",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            disabledforeground=COLOR_FG_BUTTON_DISABLED,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.configurar,
        )
        btns["btn_config"].grid(column=0, row=1, columnspan=4, padx=5, pady=5, sticky=NSEW)

        btns["btn_debito"] = Button(
            self.value_frame,
            text="Debito",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            disabledforeground=COLOR_FG_BUTTON_DISABLED,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.pagamento_debito,
        )
        btns["btn_debito"].grid(column=0, row=2, columnspan=2, padx=5, pady=5, sticky=NSEW)

        btns["btn_credito"] = Button(
            self.value_frame,
            text="Credito",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            disabledforeground=COLOR_FG_BUTTON_DISABLED,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.pagamento_credito,
        )
        btns["btn_credito"].grid(column=2, row=2, columnspan=2, padx=5, pady=5, sticky=NSEW)

        btns["btn_confirmar"] = Button(
            self.value_frame,
            text="Confirmar",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            disabledforeground=COLOR_FG_BUTTON_DISABLED,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.confirmar,
        )
        btns["btn_confirmar"].grid(column=0, row=3, columnspan=2, padx=5, pady=5, sticky=NSEW)

        btns["btn_desfazer"] = Button(
            self.value_frame,
            text="Desfazer",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            disabledforeground=COLOR_FG_BUTTON_DISABLED,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.desfazer,
        )
        btns["btn_desfazer"].grid(column=2, row=3, columnspan=2, padx=5, pady=5, sticky=NSEW)

        btns["btn_cancelar"] = Button(
            self.value_frame,
            text="Cancelar",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            disabledforeground=COLOR_FG_BUTTON_DISABLED,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.pagamento_cancelar,
        )
        btns["btn_cancelar"].grid(column=0, row=4, columnspan=4, padx=5, pady=5, sticky=NSEW)

        btns["btn_abortar"] = Button(
            self.operator_frame,
            text="Abortar",
            relief=RAISED,
            bg=COLOR_BG_BUTTON,
            fg=COLOR_FG_BUTTON,
            disabledforeground=COLOR_FG_BUTTON_DISABLED,
            font=SMALL_FONT_STYLE,
            borderwidth=1,
            width=17,
            command=self.abortar,
        )
        btns["btn_abortar"].grid(column=2, row=4, columnspan=2, padx=5, pady=5, sticky=NSEW)
        
        return btns

    def create_logs_text(self):
        self.logs = StringVar()
        logs_entry = Text(
            self.logs_frame,
            relief=SUNKEN,
            bg=COLOR_BG_ENTRY,
            fg=COLOR_FG_LABEL,
            width=60,
        )
        logs_entry.grid(column=0, row=1, sticky=NS, padx=(10, 0), pady=(10, 20))
        logs_entry.insert(END, "")

        sb_ver = Scrollbar(self.logs_frame, orient=VERTICAL)
        sb_ver.grid(column=1, row=1, sticky=NS, pady=(10, 20))

        logs_entry.config(yscrollcommand=sb_ver.set)
        sb_ver.config(command=logs_entry.yview)
        return logs_entry

    def write_logs(self, logs: str, div=True):
        if div:
            logs = "\n=======================================\n" + logs
        self.logs_text.insert(END, logs)
        self.logs_text.yview(END)
        self.root.update()

    # =======================================
    # | ===========  END LAYOUT =========== |
    # =======================================

    # =======================================
    # | ==============  TEF  ============== |
    # =======================================
    def error(self):
        self.lbl_operator_text.set("aconteceu algum erro na operacao")

    def configurar(self):
        result = self.e_configurar()
        self.lbl_operator_text.set(result)
        self.root.update()

    def pagamento_debito(self):
        self.buttons["btn_config"]["state"] = "active"
        self.buttons["btn_debito"]["state"] = "active"
        self.buttons["btn_credito"]["state"] = "active"
        self.buttons["btn_abortar"]["state"] = "active"
        self.buttons["btn_cancelar"]["state"] = "active"
        self.running = True
        self.process_thread = Thread(target=self.debito)
        self.process_thread.start()

    def pagamento_credito(self):
        self.buttons["btn_config"]["state"] = "active"
        self.buttons["btn_debito"]["state"] = "active"
        self.buttons["btn_credito"]["state"] = "active"
        self.buttons["btn_abortar"]["state"] = "active"
        self.buttons["btn_cancelar"]["state"] = "active"
        self.running = True
        self.process_thread = Thread(target=self.credito)
        self.process_thread.start()

    def abortar(self):
        self.buttons["btn_config"]["state"] = "active"
        self.buttons["btn_debito"]["state"] = "active"
        self.buttons["btn_credito"]["state"] = "active"
        self.buttons["btn_abortar"]["state"] = "active"
        self.buttons["btn_cancelar"]["state"] = "active"
        self.lbl_operator_text.set("operação abortada")
        self.running = True
        self.process_thread = Thread(target=self.e_abortar)
        self.process_thread.start()

    def confirmar(self):
        self.buttons["btn_config"]["state"] = "active"
        self.buttons["btn_debito"]["state"] = "active"
        self.buttons["btn_credito"]["state"] = "active"
        self.buttons["btn_abortar"]["state"] = "active"
        self.buttons["btn_cancelar"]["state"] = "active"
        self.lbl_operator_text.set("operação abortada")
        self.running = True
        self.process_thread = Thread(target=self.e_finalizar("1"))
        self.process_thread.start()

    def desfazer(self):
        self.buttons["btn_config"]["state"] = "active"
        self.buttons["btn_debito"]["state"] = "active"
        self.buttons["btn_credito"]["state"] = "active"
        self.buttons["btn_abortar"]["state"] = "active"
        self.buttons["btn_cancelar"]["state"] = "active"
        self.lbl_operator_text.set("operação abortar")
        self.running = True
        self.process_thread = Thread(target=self.e_finalizar("0"))
        self.process_thread.start()

    def pagamento_cancelar(self):
        self.buttons["btn_config"]["state"] = "active"
        self.buttons["btn_debito"]["state"] = "active"
        self.buttons["btn_credito"]["state"] = "active"
        self.buttons["btn_abortar"]["state"] = "active"
        self.buttons["btn_cancelar"]["state"] = "active"
        self.lbl_operator_text.set("operação cancelar")
        self.running = True
        self.process_thread = Thread(target=self.cancelar())
        self.process_thread.start()

    def debito(self):
        if "Sucesso" not in self.e_iniciar():
            return self.error()
        
        if "Sucesso" not in self.e_debito():
            return self.error()
        
        while self.running:
            result = self.e_status() 
            self.lbl_operator_text.set(f"Result: {result}")
            self.root.update()
            if "-1" in result:
                self.error()
                break
            if "0" in result:
                break

        self.root.update()

    def credito(self):
        if "Sucesso" not in self.e_iniciar():
            return self.error()
        if "Sucesso" not in self.e_credito():
            return self.error()
        while self.running:
            result = self.e_status() 
            self.lbl_operator_text.set(f"Result: {result}")
            self.root.update()
            if "-1" in result:
                self.error()
                break
            if "0" in result:
                break

        self.root.update()

    def cancelar(self):
        if "Sucesso" not in self.e_iniciar():
            return self.error()
        if "Sucesso" not in self.e_cancelar():
            return self.error()
        while self.running:
            result = self.e_status() 
            self.lbl_operator_text.set(f"Result: {result}")
            self.root.update()
            if "-1" in result:
                self.error()
                break
            if "0" in result:
                break

        self.root.update()

    def e_configurar(self):
        self.lbl_operator_text.set("configurando produto tef")
        
        load_dotenv()

        PRODUTO = "tef"                         
        TIMEOUT = os.getenv('TIMEOUT')          
        SUB_PRODUTO = os.getenv('SUB_PRODUTO')  
        CODIGO_ATIVACAO = os.getenv('CODIGO_ATIVACAO')
        NOME_APP = os.getenv('APP_NOME')
        VERSAO_APP = os.getenv('APP_VERSAO')
        TEXTO_PINPAD = os.getenv('TEXTO_PINPAD')

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON 
        input_data = {
            "configs": {
                "produto": PRODUTO,                                        
                "sub_produto": SUB_PRODUTO,                                       
                "infos": {
                    "timeout": TIMEOUT,
                    "codigo_ativacao": CODIGO_ATIVACAO,
                    "nome_app": NOME_APP,
                    "versao_app": VERSAO_APP,
                    "texto_pinpad": TEXTO_PINPAD,
                }
            }
        }
        input_json = json.dumps(input_data)
        res = configurar(input_json)

        # META PARAMETROS
        # input_data = f"{PRODUTO};{SUB_PRODUTO};{TIMEOUT};{CODIGO_ATIVACAO};{NOME_APP};{VERSAO_APP};{TEXTO_PINPAD}"
        # res = configurar(input_data)

        self.write_logs("CONFIGURAR")
        self.write_logs(res)

        result = obter_valor(res, "mensagem")
        return result

    def e_iniciar(self):
        self.lbl_operator_text.set("iniciando tef")

        OPERACAO = "tef" # produto que será executado (atual pos)

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON
        # input_data = {
        #     "iniciar": {
        #         "operacao": OPERACAO
        #     }
        # }
        # input_json = json.dumps(input_data)
        # res = iniciar(input_json)

        # META PARAMETROS
        res = iniciar(OPERACAO)

        self.write_logs("INICIAR")
        self.write_logs(res)

        return res

    def e_debito(self):
        self.lbl_operator_text.set("transacao débito de 19,00 reais")

        OPERACAO    = 'debito'      
        VALOR       = "1900"        

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON 
        input_data = {
            "processar": {
                "operacao": OPERACAO,       # debito
                "valor": VALOR              # valor sempre em centavos
            }
        }
        input_json = json.dumps(input_data)
        res = processar(input_json)

        # META PARAMETROS
        # input_data = f"{OPERACAO};{VALOR}"
        # res = processar(input_data)

        self.write_logs("PROCESSAR")
        self.write_logs(res)
        
        status_code = obter_valor(res, "resultado.status_code")
        message = obter_valor(res, "resultado.status_message")

        if status_code == "1":
            self.lbl_operator_text.set(message)
            self.root.update()
        else:
            print("error in response ")
            self.lbl_operator_text.set("Ocorreu algum erro")

        message = obter_valor(res, "mensagem")
        return message

    def e_credito(self):
        self.lbl_operator_text.set("transacao crédito de 1,00 reais")

        OPERACAO        = 'credito'     
        VALOR           = "100"       
        PARCELAS        = "1"           
        FINANCIAMENTO   = "0"           

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON 
        # input_data = {
        #     "processar": {
        #         "operacao": OPERACAO,           # credito 
        #         "valor": VALOR,                 # em centavos
        #         "parcelas": PARCELAS,           # 1 a 99
        #         "financiamento": FINANCIAMENTO, # 0 - a vista; 1 - estabelecimento; 2 - administradora
        #     }
        # }
        # input_json = json.dumps(input_data)
        # res = processar(input_json)

        # META PARAMETROS
        input_data = f"{OPERACAO};{VALOR};{PARCELAS};{FINANCIAMENTO}"
        res = processar(input_data)

        self.write_logs("PROCESSAR")
        self.write_logs(res)
        
        status_code = obter_valor(res, "resultado.status_code")
        message = obter_valor(res, "resultado.status_message")

        if status_code == "1":
            self.lbl_operator_text.set(message)
            self.root.update()
        else:
            print("error in response ")
            self.lbl_operator_text.set("Ocorreu algum erro")

        message = obter_valor(res, "mensagem")
        return message

    def e_status(self):
        self.lbl_operator_text.set("consultando status")

        OPERACAO = 'get_status' # obtem o status do pagamento do qrcode

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON
        input_data = {
            "processar": {
                "operacao": OPERACAO
            }
        }
        input_json = json.dumps(input_data)
        res = processar(input_json)
    
        # META PARAMETROS
        # res = processar(OPERACAO)

        self.write_logs("PROCESSAR")
        self.write_logs(res)
        
        result = obter_valor(res, "resultado.status_code")
        return result

    def e_abortar(self):
        self.lbl_operator_text.set("abortando operacao")

        OPERACAO = 'abortar' # obtem o status do pagamento do qrcode

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON
        input_data = {
            "processar": {
                "operacao": OPERACAO
            }
        }
        input_json = json.dumps(input_data)
        res = processar(input_json)
    
        # META PARAMETROS
        # res = processar(OPERACAO)

        self.write_logs("PROCESSAR")
        self.write_logs(res)
        self.root.update()

        result = obter_valor(res, "resultato.status_code")
        return result
    
    def e_cancelar(self): 
        self.lbl_operator_text.set("cancelando transação")

        OPERACAO        = 'cancelar'     
        VALOR           = "4500"       
        DATA            = "20032024"           
        NSU             = "000000060"           

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON 
        # input_data = {
        #     "processar": {
        #         "operacao": OPERACAO,           # credito 
        #         "valor": VALOR,                 # em centavos
        #         "data": DATA,                   # DDMMAAAA - 
        #         "nsu": NSU,                     # igual está no comprovante recebido com 9 caracteres
        #     }
        # }
        # input_json = json.dumps(input_data)
        # res = processar(input_json)

        # META PARAMETROS
        input_data = f"{OPERACAO};{VALOR};{DATA};{NSU}"
        res = processar(input_data)

        self.write_logs("PROCESSAR")
        self.write_logs(res)
        
        status_code = obter_valor(res, "resultado.status_code")
        message = obter_valor(res, "resultado.status_message")

        if status_code == "1":
            self.lbl_operator_text.set(message)
            self.root.update()
        else:
            print("error in response ")
            self.lbl_operator_text.set("Ocorreu algum erro")

        message = obter_valor(res, "mensagem")
        return message

    def e_finalizar(self, confirmar):
        self.lbl_operator_text.set("finalizando operacao")

        OPERACAO = 'confirmar'  # realiza a confirmação da transacao
        VALOR    = confirmar    # 1 - confirmar / 0 - desfazer

        # DESCOMENTE UMA DAS OPCOES PARA TESTAR: JSON OU META PARAMETROS

        # JSON
        input_data = {
            "finalizar": {
                "operacao": OPERACAO,
                "valor": VALOR
            }
        }
        input_json = json.dumps(input_data)
        res = finalizar(input_json)
    
        # META PARAMETROS
        # res = processar(OPERACAO)
        # input_data = f"{OPERACAO};{VALOR}"
        # res = processar(input_data)

        self.write_logs("FINALIZAR")
        self.write_logs(res)
        self.root.update()
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TefApp(Tk())
    app.run()
