import sys
import random
import string
import sqlite3
import os
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QPushButton, QLineEdit, QLabel, 
                               QComboBox, QDialog, QTableWidget, QTableWidgetItem,
                               QHeaderView, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon


class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Senhas")
        
        # Definir ícone da janela (para barra de tarefas)
        icon_path = self.get_icon_path()
        if icon_path and os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.setMinimumWidth(700)
        self.setMinimumHeight(650)
        
        # Modo atual: 'restaurante' ou 'escritorio'
        self.modo_atual = 'restaurante'
        
        # Variáveis para armazenar senha temporária antes de salvar
        self.senha_atual = None
        self.unidade_atual = None
        self.numero_unidade_atual = None
        
        # Inicializar banco de dados
        self.init_database()
        
        self.palavras_restaurante = [
            # Utensílios
            "garfo", "faca", "colher", "prato", "tigela", "panela", "frigideira",
            "espumadeira", "concha", "escumadeira", "ralador", "peneira", "fouet",
            "espatula", "pegador", "abridor", "tabua", "cortador",
            
            # Carnes e Proteínas
            "costela", "picanha", "alcatra", "maminha", "fraldinha", "cupim",
            "linguica", "bacon", "pernil", "lombo", "bisteca", "file", "patinho",
            "lagarto", "acem", "paleta", "peito", "coxa", "sobrecoxa", "asa",
            "salmao", "tilapia", "bacalhau", "camarao", "lula", "polvo", "atum",
            
            # Grãos e Cereais
            "arroz", "feijao", "lentilha", "ervilha", "milho",
            "quinoa", "aveia", "trigo", "cevada", "centeio", "farro",
            
            # Vegetais e Legumes
            "tomate", "cebola", "alho", "batata", "cenoura", "brocolis", "couve",
            "alface", "rucula", "espinafre", "abobrinha", "berinjela", "pimentao",
            "pepino", "rabanete", "nabo", "beterraba", "mandioca", "inhame",
            "chuchu", "quiabo", "vagem", "aspargo", "alcachofra", "palmito",
            
            # Temperos e Ervas
            "sal", "pimenta", "oregano", "manjericao", "tomilho", "alecrim",
            "salsa", "cebolinha", "coentro", "hortela", "louro", "cominho",
            "paprica", "curry", "canela", "gengibre", "acafrao",
            
            # Massas e Pães
            "macarrao", "espaguete", "penne", "lasanha",
            "nhoque", "pao", "baguete",
            "brioche", "torrada", "pizza", "calzone",
            
            # Laticínios
            "queijo", "mussarela", "parmesao", "gorgonzola", "brie", "provolone",
            "ricota", "requeijao", "cheddar", "leite", "creme", "manteiga",
            "iogurte", "nata", "coalhada",
            
            # Molhos e Condimentos
            "molho", "vinagrete", "pesto", "bechamel", "carbonara", "bolonhesa",
            "shoyu", "mostarda", "ketchup", "maionese", "azeite", "vinagre",
            "limao", "chimichurri",
            
            # Sobremesas e Doces
            "bolo", "torta", "pudim", "mousse", "sorvete", "brigadeiro", "beijinho",
            "trufa", "brownie", "cookie", "cupcake",
            "cheesecake", "crepe", "waffle",
            
            # Pratos e Preparações
            "risoto", "sushi", "empada", "pastel", "coxinha", "esfiha", "kibe",
            "hamburguer", "sanduiche",

            # Frutas
            "morango", "banana", "maca", "pera", "uva", "laranja",
            "abacaxi", "manga", "mamao", "melancia", "melao", "kiwi", "pessego",
            "ameixa", "cereja", "framboesa", "mirtilo", "amora", "coco", "maracuja",
            
            # Outros Ingredientes
            "ovo", "farinha", "acucar", "mel", "baunilha", "fermento",
            "amido", "gelatina", "extrato", "essencia", "corante"
        ]
        
        self.palavras_escritorio = [
            # Equipamentos e Mobiliário
            "mesa", "cadeira", "armario", "estante", "arquivo", "gaveta", "prateleira",
            "balcao", "divisoria", "painel", "quadro", "lousa", "suporte", "apoio",
            
            # Tecnologia e Informática
            "computador", "notebook", "teclado", "mouse", "monitor", "impressora",
            "scanner", "webcam", "headset", "fone", "microfone", "roteador", "modem",
            "servidor", "switch", "cabo", "pendrive", "hd", "ssd", "memoria", "cpu",
            "placa", "fonte", "cooler", "hub", "adaptador", "carregador",
            
            # Materiais de Escritório
            "papel", "caneta", "lapis", "borracha", "apontador", "regua", "tesoura",
            "cola", "fita", "grampo", "clipe", "pasta", "envelope", "etiqueta",
            "carimbo", "perfurador", "grampeador", "calculadora", "agenda", "bloco",
            "caderno", "fichario", "organizador", "porta", "caixa", "bandeja",
            
            # Documentos e Arquivos
            "relatorio", "planilha", "documento", "contrato", "proposta", "ata",
            "memorando", "oficio", "circular", "edital", "protocolo", "formulario",
            "recibo", "nota", "fatura", "boleto", "comprovante", "declaracao",
            "certidao", "atestado", "laudo", "parecer", "termo", "anexo",
            
            # Departamentos e Áreas
            "financeiro", "contabil", "fiscal", "juridico", "comercial", "vendas",
            "compras", "estoque", "logistica", "producao", "qualidade", "rh",
            "marketing", "ti", "suporte", "atendimento", "recepcao", "diretoria",
            "gerencia", "coordenacao", "supervisao", "operacao",
            
            # Ações e Processos
            "aprovar", "revisar", "assinar", "protocolar", "arquivar", "enviar",
            "receber", "conferir", "validar", "autorizar", "solicitar", "agendar",
            "registrar", "cadastrar", "atualizar", "consultar", "imprimir", "copiar",
            "digitalizar", "anexar", "encaminhar", "distribuir",
            
            # Comunicação
            "email", "mensagem", "telefone", "ramal", "ligacao", "reuniao",
            "videoconferencia", "apresentacao", "pauta", "ata", "comunicado",
            "aviso", "notificacao", "alerta", "lembrete", "convite",
            
            # Tempo e Organização
            "prazo", "deadline", "cronograma", "calendario", "horario", "turno",
            "periodo", "trimestre", "semestre", "anual", "mensal", "semanal",
            "diario", "urgente", "prioritario", "pendente", "concluido",
            
            # Recursos Humanos
            "funcionario", "colaborador", "equipe", "time", "gestor", "lider",
            "analista", "assistente", "auxiliar", "estagiario", "trainee",
            "consultor", "especialista", "coordenador", "supervisor", "gerente",
            "diretor", "presidente", "socio", "parceiro",
            
            # Financeiro
            "orcamento", "custo", "despesa", "receita", "lucro", "prejuizo",
            "investimento", "capital", "credito", "debito", "saldo", "extrato",
            "pagamento", "recebimento", "transferencia", "deposito", "saque",
            "juros", "taxa", "desconto", "multa", "parcela",
            
            # Projetos e Planejamento
            "projeto", "plano", "meta", "objetivo", "estrategia", "tatica",
            "acao", "iniciativa", "programa", "campanha", "evento", "lancamento",
            "implementacao", "execucao", "monitoramento", "avaliacao", "resultado",
            "indicador", "metrica", "kpi", "dashboard", "relatorio",
            
            # Qualidade e Processos
            "processo", "procedimento", "norma", "padrao", "diretriz", "politica",
            "manual", "guia", "tutorial", "instrucao", "orientacao", "checklist",
            "auditoria", "inspecao", "verificacao", "validacao", "certificacao",
            "conformidade", "compliance", "governanca",
            
            # Segurança e Acesso
            "senha", "login", "usuario", "acesso", "permissao", "autorizacao",
            "credencial", "token", "chave", "cadeado", "seguranca", "protecao",
            "backup", "restauracao", "criptografia", "firewall", "antivirus",
            
            # Infraestrutura
            "sala", "andar", "predio", "bloco", "ala", "setor", "area",
            "espaco", "ambiente", "instalacao", "facilidade", "recurso",
            "equipamento", "ferramenta", "utilitario", "acessorio",
            
            # Diversos
            "codigo", "numero", "referencia", "identificacao", "registro",
            "versao", "revisao", "edicao", "atualizacao", "modificacao",
            "alteracao", "correcao", "ajuste", "melhoria", "otimizacao"
        ]
        
        self.simbolos = "!@#$%&*+?"
        
        # Dicionário de unidades
        self.unidades = {
            "02 - UNIDADE": "02",
            "03 - UNIDADE": "03",
            "04 - UNIDADE": "04",
            "05 - UNIDADE": "05",
            "06 - UNIDADE": "06",
            "07 - UNIDADE": "07",
            "08 - UNIDADE": "08",
            "09 - UNIDADE": "09",
            "10 - UNIDADE": "10",
            "11 - UNIDADE": "11",
            "12 - UNIDADE": "12",
            "13 - UNIDADE": "13",
            "14 - UNIDADE": "14",
            "15 - UNIDADE": "15",
            "16 - UNIDADE": "16",
            "17 - UNIDADE": "17",
            "18 - UNIDADE": "18",
            "19 - UNIDADE": "19",
            "20 - UNIDADE": "20",
            "21 - UNIDADE": "21",
            "22 - UNIDADE": "22",
            "23 - UNIDADE": "23",
            "24 - UNIDADE": "24"
        }
        
        self.init_ui()
    
    def get_icon_path(self):
        """Retorna o caminho do ícone, funciona tanto em desenvolvimento quanto no executável"""
        if getattr(sys, 'frozen', False):
            # Executável PyInstaller
            base_path = sys._MEIPASS
        else:
            # Desenvolvimento
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(base_path, 'icon.ico')
    
    def init_database(self):
        """Inicializa o banco de dados SQLite"""
        self.conn = sqlite3.connect('senhas_geradas.db')
        self.cursor = self.conn.cursor()
        
        # Criar tabela se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS senhas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unidade TEXT NOT NULL,
                numero_unidade TEXT NOT NULL,
                senha TEXT NOT NULL UNIQUE,
                data_geracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def senha_existe(self, senha):
        """Verifica se a senha já foi gerada anteriormente"""
        self.cursor.execute('SELECT COUNT(*) FROM senhas WHERE senha = ?', (senha,))
        return self.cursor.fetchone()[0] > 0
    
    def salvar_senha(self, unidade, numero_unidade, senha):
        """Salva a senha no banco de dados"""
        try:
            self.cursor.execute('''
                INSERT INTO senhas (unidade, numero_unidade, senha)
                VALUES (?, ?, ?)
            ''', (unidade, numero_unidade, senha))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def obter_senhas_unidade(self, numero_unidade):
        """Obtém todas as senhas de uma unidade específica"""
        self.cursor.execute('''
            SELECT senha, data_geracao 
            FROM senhas 
            WHERE numero_unidade = ?
            ORDER BY data_geracao DESC
        ''', (numero_unidade,))
        return self.cursor.fetchall()
    
    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
            }
        """)
        
        # Aplicar estilo geral da janela
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
            }
        """)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)
        
        # Barra de abas superior com gradiente sutil
        tab_bar = QWidget()
        tab_bar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 #3d3d3d, stop:1 #353535);
            border-bottom: 1px solid #4a4a4a;
        """)
        tab_bar.setFixedHeight(40)
        tab_layout = QHBoxLayout()
        tab_layout.setContentsMargins(15, 0, 15, 0)
        tab_layout.setSpacing(0)
        tab_bar.setLayout(tab_layout)
        
        # Título na barra
        title = QLabel("Gerador de Senhas")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title.setStyleSheet("color: #e0e0e0; background: transparent; padding: 8px;")
        tab_layout.addWidget(title)
        tab_layout.addStretch()
        
        main_layout.addWidget(tab_bar)
        
        # Container de conteúdo
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #2b2b2b;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 25, 30, 25)
        content_layout.setSpacing(16)
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget)
        
        # Container para os botões de modo
        mode_container = QWidget()
        mode_container.setStyleSheet("background-color: #2b2b2b;")
        mode_layout = QHBoxLayout()
        mode_layout.setSpacing(12)
        mode_layout.setContentsMargins(0, 0, 0, 0)
        mode_container.setLayout(mode_layout)
        
        # Botão Restaurante
        self.btn_restaurante = QPushButton("RESTAURANTE")
        self.btn_restaurante.setMinimumHeight(52)
        self.btn_restaurante.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.btn_restaurante.setCursor(Qt.PointingHandCursor)
        self.btn_restaurante.clicked.connect(lambda: self.mudar_modo('restaurante'))
        mode_layout.addWidget(self.btn_restaurante)
        
        # Botão Escritório
        self.btn_escritorio = QPushButton("ESCRITÓRIO")
        self.btn_escritorio.setMinimumHeight(52)
        self.btn_escritorio.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.btn_escritorio.setCursor(Qt.PointingHandCursor)
        self.btn_escritorio.clicked.connect(lambda: self.mudar_modo('escritorio'))
        mode_layout.addWidget(self.btn_escritorio)
        
        content_layout.addWidget(mode_container)
        
        # Seleção de unidade (apenas para restaurante)
        self.unit_label = QLabel("Selecione a Unidade")
        self.unit_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.unit_label.setStyleSheet("color: #d0d0d0; margin-top: 8px;")
        content_layout.addWidget(self.unit_label)
        
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(self.unidades.keys())
        self.unit_combo.setCurrentIndex(13)  # Padrão: 15 - GUARANI
        self.unit_combo.setMinimumHeight(45)
        self.unit_combo.setFont(QFont("Segoe UI", 10))
        self.unit_combo.setCursor(Qt.PointingHandCursor)
        self.unit_combo.setStyleSheet("""
            QComboBox {
                border: 1px solid #4a4a4a;
                border-radius: 5px;
                padding: 10px 12px;
                background-color: #1e1e1e;
                color: #d0d0d0;
            }
            QComboBox:hover {
                background-color: #252525;
                border: 1px solid #5cb85c;
            }
            QComboBox:focus {
                border: 1px solid #5cb85c;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #b8b8b8;
                margin-right: 12px;
            }
            QComboBox QAbstractItemView {
                border: 1px solid #4a4a4a;
                border-radius: 5px;
                background-color: #1e1e1e;
                color: #d0d0d0;
                selection-background-color: #5cb85c;
                selection-color: #ffffff;
                padding: 5px;
                outline: none;
            }
            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border-radius: 3px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #2a2a2a;
            }
        """)
        self.unit_combo.currentTextChanged.connect(self.generate_password)
        content_layout.addWidget(self.unit_combo)
        
        # Botão gerar (estilo verde como no print)
        self.generate_button = QPushButton("GERAR NOVA SENHA")
        self.generate_button.setMinimumHeight(48)
        self.generate_button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.generate_button.setCursor(Qt.PointingHandCursor)
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #5cb85c;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                letter-spacing: 0.5px;
            }
            QPushButton:hover {
                background-color: #6ec96e;
            }
            QPushButton:pressed {
                background-color: #4cae4c;
            }
        """)
        self.generate_button.clicked.connect(self.generate_password)
        content_layout.addWidget(self.generate_button)
        
        # Campo de senha gerada
        password_label = QLabel("Senha Gerada")
        password_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        password_label.setStyleSheet("color: #d0d0d0; margin-top: 8px;")
        content_layout.addWidget(password_label)
        
        self.password_field = QLineEdit()
        self.password_field.setReadOnly(True)
        self.password_field.setMinimumHeight(55)
        self.password_field.setAlignment(Qt.AlignCenter)
        self.password_field.setFont(QFont("Consolas", 16, QFont.Bold))
        # Desabilitar seleção de texto e menu de contexto
        self.password_field.setContextMenuPolicy(Qt.NoContextMenu)
        self.password_field.setFocusPolicy(Qt.NoFocus)
        self.password_field.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.password_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4a4a4a;
                border-radius: 6px;
                padding: 10px;
                background-color: #1a1a1a;
                color: #5cb85c;
                letter-spacing: 2px;
            }
        """)
        # Sobrescrever eventos de mouse para impedir seleção
        self.password_field.mousePressEvent = lambda event: None
        self.password_field.mouseMoveEvent = lambda event: None
        self.password_field.mouseDoubleClickEvent = lambda event: None
        content_layout.addWidget(self.password_field)
        
        # Botão copiar
        self.copy_button = QPushButton("Copiar para Área de Transferência")
        self.copy_button.setMinimumHeight(46)
        self.copy_button.setFont(QFont("Segoe UI", 10))
        self.copy_button.setCursor(Qt.PointingHandCursor)
        self.copy_button.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: #d0d0d0;
                border: 1px solid #4a4a4a;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #252525;
                border: 1px solid #5cb85c;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
            QPushButton:disabled {
                background-color: #1e1e1e;
                color: #5a5a5a;
                border-color: #3a3a3a;
            }
        """)
        self.copy_button.clicked.connect(self.copy_password)
        self.copy_button.setEnabled(False)
        content_layout.addWidget(self.copy_button)
        
        # Botão visualizar senhas
        self.view_button = QPushButton("Visualizar Senhas da Unidade")
        self.view_button.setMinimumHeight(46)
        self.view_button.setFont(QFont("Segoe UI", 10))
        self.view_button.setCursor(Qt.PointingHandCursor)
        self.view_button.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: #d0d0d0;
                border: 1px solid #4a4a4a;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #252525;
                border: 1px solid #5cb85c;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
        """)
        self.view_button.clicked.connect(self.show_passwords_dialog)
        content_layout.addWidget(self.view_button)
        
        # Status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setMinimumHeight(35)
        self.status_label.setStyleSheet("color: #5cb85c;")
        content_layout.addWidget(self.status_label)
        
        content_layout.addStretch()
        
        # Rodapé
        self.footer = QLabel("Padrão: Palavra + Símbolo + Palavra + Número")
        self.footer.setAlignment(Qt.AlignCenter)
        self.footer.setFont(QFont("Segoe UI", 9))
        self.footer.setStyleSheet("color: #7a7a7a; padding: 5px;")
        content_layout.addWidget(self.footer)
        
        # Atualizar interface para o modo inicial
        self.atualizar_interface_modo()
        
        # Gerar senha inicial
        self.generate_password()
    
    def mudar_modo(self, modo):
        """Alterna entre modo restaurante e escritório"""
        self.modo_atual = modo
        self.atualizar_interface_modo()
        self.generate_password()
    
    def atualizar_interface_modo(self):
        """Atualiza a interface baseado no modo selecionado"""
        if self.modo_atual == 'restaurante':
            # Estilo botão restaurante ativo
            self.btn_restaurante.setStyleSheet("""
                QPushButton {
                    background-color: #5cb85c;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 11pt;
                    padding: 12px;
                    letter-spacing: 0.5px;
                }
                QPushButton:hover {
                    background-color: #6ec96e;
                }
                QPushButton:pressed {
                    background-color: #4cae4c;
                }
            """)
            # Estilo botão escritório inativo
            self.btn_escritorio.setStyleSheet("""
                QPushButton {
                    background-color: #1e1e1e;
                    color: #b8b8b8;
                    border: 1px solid #4a4a4a;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 11pt;
                    padding: 12px;
                    letter-spacing: 0.5px;
                }
                QPushButton:hover {
                    background-color: #252525;
                    border: 1px solid #5cb85c;
                }
                QPushButton:pressed {
                    background-color: #1a1a1a;
                }
            """)
            # Mostrar seleção de unidade
            self.unit_label.show()
            self.unit_combo.show()
            # Atualizar textos
            self.generate_button.setText("GERAR NOVA SENHA DE RESTAURANTE")
            self.view_button.setText("Visualizar Senhas da Unidade")
            self.footer.setText("Padrão: Palavra + Símbolo + Palavra + Número da Unidade")
        else:  # escritorio
            # Estilo botão escritório ativo
            self.btn_escritorio.setStyleSheet("""
                QPushButton {
                    background-color: #5cb85c;
                    color: #ffffff;
                    border: none;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 11pt;
                    padding: 12px;
                    letter-spacing: 0.5px;
                }
                QPushButton:hover {
                    background-color: #6ec96e;
                }
                QPushButton:pressed {
                    background-color: #4cae4c;
                }
            """)
            # Estilo botão restaurante inativo
            self.btn_restaurante.setStyleSheet("""
                QPushButton {
                    background-color: #1e1e1e;
                    color: #b8b8b8;
                    border: 1px solid #4a4a4a;
                    border-radius: 6px;
                    font-weight: bold;
                    font-size: 11pt;
                    padding: 12px;
                    letter-spacing: 0.5px;
                }
                QPushButton:hover {
                    background-color: #252525;
                    border: 1px solid #5cb85c;
                }
                QPushButton:pressed {
                    background-color: #1a1a1a;
                }
            """)
            # Esconder seleção de unidade
            self.unit_label.hide()
            self.unit_combo.hide()
            # Atualizar textos
            self.generate_button.setText("GERAR NOVA SENHA DE ESCRITÓRIO")
            self.view_button.setText("Visualizar Senhas de Escritório")
            self.footer.setText("Padrão: Palavra + Símbolo + Palavra + Número Aleatório (00-99)")
    
    def generate_password(self):
        """Gera uma senha seguindo o padrão: palavra + símbolo + palavra + número"""
        max_tentativas = 100
        tentativa = 0
        
        # Seleciona a lista de palavras baseada no modo
        if self.modo_atual == 'restaurante':
            palavras = self.palavras_restaurante
            # Pega informações da unidade selecionada
            unidade_selecionada = self.unit_combo.currentText()
            numero_unidade = self.unidades[unidade_selecionada]
        else:  # escritorio
            palavras = self.palavras_escritorio
            # Gera número aleatório de 00 a 99
            numero_unidade = f"{random.randint(0, 99):02d}"
            unidade_selecionada = f"ESCRITÓRIO-{numero_unidade}"
        
        while tentativa < max_tentativas:
            # Seleciona duas palavras aleatórias da lista apropriada
            palavra1 = random.choice(palavras)
            palavra2 = random.choice(palavras)
            
            # Capitaliza a primeira letra de cada palavra
            palavra1 = palavra1.capitalize()
            palavra2 = palavra2.capitalize()
            
            # Seleciona um símbolo aleatório
            simbolo = random.choice(self.simbolos)
            
            # Monta a senha
            senha = f"{palavra1}{simbolo}{palavra2}{numero_unidade}"
            
            # Verifica se a senha já existe
            if not self.senha_existe(senha):
                # Armazena informações da senha para salvar depois
                self.senha_atual = senha
                self.unidade_atual = unidade_selecionada
                self.numero_unidade_atual = numero_unidade
                
                # Exibe a senha
                self.password_field.setText(senha)
                self.copy_button.setEnabled(True)
                self.status_label.setText("Nova senha gerada! Clique em 'Copiar' para salvar.")
                self.status_label.setStyleSheet("color: #5cb85c; font-weight: bold;")
                return
            
            tentativa += 1
        
        # Se não conseguiu gerar uma senha única após várias tentativas
        self.status_label.setText("Não foi possível gerar uma senha única. Tente novamente.")
        self.status_label.setStyleSheet("color: #d9534f; font-weight: bold;")
    
    def show_passwords_dialog(self):
        """Mostra um diálogo com todas as senhas da unidade selecionada ou escritório"""
        if self.modo_atual == 'restaurante':
            unidade_selecionada = self.unit_combo.currentText()
            numero_unidade = self.unidades[unidade_selecionada]
            senhas = self.obter_senhas_unidade(numero_unidade)
            titulo = unidade_selecionada
        else:  # escritorio
            # Para escritório, mostra todas as senhas que começam com "ESCRITÓRIO-"
            senhas = self.obter_senhas_escritorio()
            titulo = "ESCRITÓRIO"
        
        dialog = PasswordListDialog(titulo, senhas, self)
        dialog.exec()
    
    def obter_senhas_escritorio(self):
        """Obtém todas as senhas de escritório"""
        self.cursor.execute('''
            SELECT senha, data_geracao 
            FROM senhas 
            WHERE unidade LIKE 'ESCRITÓRIO-%'
            ORDER BY data_geracao DESC
        ''')
        return self.cursor.fetchall()
    
    def copy_password(self):
        """Copia a senha para a área de transferência e salva no banco de dados"""
        password = self.password_field.text()
        if password:
            # Salva a senha no banco de dados
            if hasattr(self, 'senha_atual') and hasattr(self, 'unidade_atual') and hasattr(self, 'numero_unidade_atual'):
                if self.salvar_senha(self.unidade_atual, self.numero_unidade_atual, self.senha_atual):
                    # Copia para área de transferência
                    clipboard = QApplication.clipboard()
                    clipboard.setText(password)
                    self.status_label.setText("Senha copiada e salva com sucesso!")
                    self.status_label.setStyleSheet("color: #5cb85c; font-weight: bold;")
                    
                    # Limpa as variáveis temporárias
                    delattr(self, 'senha_atual')
                    delattr(self, 'unidade_atual')
                    delattr(self, 'numero_unidade_atual')
                else:
                    self.status_label.setText("Erro ao salvar senha no banco de dados.")
                    self.status_label.setStyleSheet("color: #d9534f; font-weight: bold;")
            else:
                # Se não há senha atual (já foi copiada antes), apenas copia
                clipboard = QApplication.clipboard()
                clipboard.setText(password)
                self.status_label.setText("Senha copiada!")
                self.status_label.setStyleSheet("color: #5cb85c; font-weight: bold;")
    
    def closeEvent(self, event):
        """Fecha a conexão com o banco de dados ao fechar a aplicação"""
        self.conn.close()
        event.accept()


class PasswordListDialog(QDialog):
    """Diálogo para exibir todas as senhas de uma unidade"""
    def __init__(self, unidade, senhas, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Senhas Geradas - {unidade}")
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
        
        self.unidade = unidade
        self.senhas = senhas
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        
        # Estilo do diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #d0d0d0;
            }
            QTableWidget {
                background-color: #1e1e1e;
                color: #d0d0d0;
                border: 1px solid #4a4a4a;
                border-radius: 5px;
                gridline-color: #3a3a3a;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #3a3a3a;
            }
            QTableWidget::item:selected {
                background-color: #5cb85c;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #1a1a1a;
                color: #d0d0d0;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #5cb85c;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton {
                background-color: #5cb85c;
                color: #ffffff;
                border: none;
                border-radius: 5px;
                padding: 10px 18px;
                font-weight: bold;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #6ec96e;
            }
            QPushButton:pressed {
                background-color: #4cae4c;
            }
        """)
        
        # Barra de título com gradiente
        title_bar = QWidget()
        title_bar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                       stop:0 #3d3d3d, stop:1 #353535);
            border-bottom: 1px solid #4a4a4a;
        """)
        title_bar.setFixedHeight(40)
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(15, 0, 15, 0)
        title_bar.setLayout(title_layout)
        
        # Título
        title = QLabel(f"Senhas Geradas - {self.unidade}")
        title.setFont(QFont("Segoe UI", 11, QFont.Bold))
        title.setStyleSheet("color: #e0e0e0; background: transparent;")
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        layout.addWidget(title_bar)
        
        # Container de conteúdo
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #2b2b2b;")
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        content_widget.setLayout(content_layout)
        layout.addWidget(content_widget)
        
        # Contador
        count_label = QLabel(f"Total de senhas: {len(self.senhas)}")
        count_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        count_label.setStyleSheet("color: #7a7a7a; margin-bottom: 5px;")
        content_layout.addWidget(count_label)
        
        if not self.senhas:
            # Mensagem quando não há senhas
            no_data_label = QLabel("Nenhuma senha foi gerada para esta unidade ainda.")
            no_data_label.setFont(QFont("Segoe UI", 10))
            no_data_label.setAlignment(Qt.AlignCenter)
            no_data_label.setStyleSheet("color: #7a7a7a; padding: 50px;")
            content_layout.addWidget(no_data_label)
        else:
            # Tabela de senhas
            self.table = QTableWidget()
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["#", "Senha", "Data de Geração"])
            self.table.setRowCount(len(self.senhas))
            self.table.setEditTriggers(QTableWidget.NoEditTriggers)
            self.table.setSelectionBehavior(QTableWidget.SelectRows)
            self.table.setSelectionMode(QTableWidget.SingleSelection)
            
            # Configurar largura das colunas
            header = self.table.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.Stretch)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            
            # Preencher tabela
            for i, (senha, data_geracao) in enumerate(self.senhas):
                # Número
                num_item = QTableWidgetItem(str(i + 1))
                num_item.setTextAlignment(Qt.AlignCenter)
                num_item.setFont(QFont("Segoe UI", 9))
                self.table.setItem(i, 0, num_item)
                
                # Senha
                senha_item = QTableWidgetItem(senha)
                senha_item.setFont(QFont("Consolas", 11, QFont.Bold))
                senha_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, 1, senha_item)
                
                # Data
                try:
                    # Formatar data
                    data_obj = datetime.strptime(data_geracao, "%Y-%m-%d %H:%M:%S")
                    data_formatada = data_obj.strftime("%d/%m/%Y %H:%M")
                except:
                    data_formatada = data_geracao
                
                data_item = QTableWidgetItem(data_formatada)
                data_item.setFont(QFont("Segoe UI", 9))
                data_item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(i, 2, data_item)
            
            # Ajustar altura das linhas
            self.table.verticalHeader().setDefaultSectionSize(40)
            self.table.verticalHeader().setVisible(False)
            
            content_layout.addWidget(self.table)
            
            # Botão copiar senha selecionada
            copy_button = QPushButton("Copiar Senha Selecionada")
            copy_button.setMinimumHeight(45)
            copy_button.clicked.connect(self.copy_selected_password)
            content_layout.addWidget(copy_button)
        
        # Botão fechar
        close_button = QPushButton("Fechar")
        close_button.setMinimumHeight(45)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #1e1e1e;
                color: #d0d0d0;
                border: 1px solid #4a4a4a;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #252525;
                border: 1px solid #5cb85c;
            }
            QPushButton:pressed {
                background-color: #1a1a1a;
            }
        """)
        close_button.clicked.connect(self.accept)
        content_layout.addWidget(close_button)
    
    def copy_selected_password(self):
        """Copia a senha selecionada para a área de transferência"""
        if hasattr(self, 'table'):
            selected_rows = self.table.selectedIndexes()
            if selected_rows:
                row = selected_rows[0].row()
                senha = self.table.item(row, 1).text()
                clipboard = QApplication.clipboard()
                clipboard.setText(senha)
                
                # Mostrar mensagem de confirmação
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Sucesso")
                msg.setText("Senha copiada com sucesso!")
                msg.setStyleSheet("""
                    QMessageBox {
                        background-color: #2b2b2b;
                    }
                    QMessageBox QLabel {
                        color: #d0d0d0;
                        font-size: 10pt;
                    }
                    QPushButton {
                        background-color: #5cb85c;
                        color: #ffffff;
                        border: none;
                        border-radius: 5px;
                        padding: 8px 20px;
                        font-weight: bold;
                        min-width: 80px;
                    }
                    QPushButton:hover {
                        background-color: #6ec96e;
                    }
                """)
                msg.exec()


def main():
    app = QApplication(sys.argv)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
