#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# /*********************************************************************************
# * Projeto:   S.I.G.M.A. (Sistema Inteligente de Gerenciamento e Mapeamento de Arquivos)
# * Autor:     Carlos Henrique Tourinho Santana
# * GitHub:    https://github.com/henriquetourinho/S.I.G.M.A
# * Versão:    1.0
# * Data:      18 de junho de 2025
# *
# * Descrição:
# * O S.I.G.M.A. é uma plataforma avançada de busca e análise de arquivos locais,
# * desenvolvida em Python com uma interface gráfica moderna construída com PySide6.
# * O sistema evoluiu de um simples script para uma ferramenta robusta, capaz
# * de realizar buscas complexas baseadas em múltiplos metadados e com uma
# * arquitetura preparada para futuras expansões com inteligência artificial e
# * visualização de dados.
# *
# * Funcionalidades Principais:
# * - Interface Gráfica Intuitiva: Permite que usuários de todos os níveis
# * realizem buscas complexas sem a necessidade de linha de comando.
# * - Busca Multi-Critério: Filtra arquivos por nome, extensão, classificação
# * (tipo), tamanho, data de modificação, proprietário e permissões.
# * - Desempenho Assíncrono: A interface permanece responsiva e funcional
# * mesmo durante buscas intensivas em diretórios grandes.
# * - Personalização de Créditos: Rodapé customizável com informações do autor
# * e links para portfólios profissionais.
# * - Preparado para o Futuro: A arquitetura modular com abas foi projetada
# * para incorporar facilmente novas funcionalidades como mapas de calor de
# * disco, grafos de relação de arquivos e detecção semântica.
# * - Portátil e Robusto: Escrito em Python para ser compatível com múltiplos
# * sistemas e com tratamento de erros para garantir estabilidade.
# *********************************************************************************/

import sys
import os
import stat
import threading
import pwd
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QFileDialog, QLabel, QStatusBar, QGroupBox, QComboBox, QSpinBox, QCheckBox
)
from PySide6.QtCore import Qt, Signal, QObject

# Adicione esta linha para resolver o problema de rodar como root
os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--no-sandbox'

FILE_CATEGORIES = {
    "Qualquer tipo": [], "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "Documentos": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".odt", ".ods", ".odp", ".txt", ".rtf"],
    "Vídeos": [".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv"], "Áudio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
}

class AbortFlag:
    def __init__(self): self._should_abort = False
    def set(self): self._should_abort = True
    def is_set(self): return self._should_abort

class WorkerSignals(QObject):
    found = Signal(dict)
    finished = Signal()
    status = Signal(str)

class AdvancedSearchApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S.I.G.M.A. – Sistema Inteligente de Gerenciamento e Mapeamento de Arquivos")
        self.setGeometry(100, 100, 1024, 768)
        self.search_thread = None
        self.abort_flag = None
        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        
        basic_search_group=QGroupBox("Busca Básica");basic_layout=QGridLayout();self.name_input=QLineEdit();self.name_input.setPlaceholderText("Parte do nome do arquivo");basic_layout.addWidget(QLabel("Nome:"),0,0);basic_layout.addWidget(self.name_input,0,1,1,3);self.ext_input=QLineEdit();self.ext_input.setPlaceholderText("Extensão (ex: pdf)");basic_layout.addWidget(QLabel("Extensão:"),1,0);basic_layout.addWidget(self.ext_input,1,1,1,3);self.dir_input=QLineEdit(os.path.expanduser("~"));browse_button=QPushButton("Procurar...");browse_button.clicked.connect(self.browse_directory);basic_layout.addWidget(QLabel("Buscar em:"),2,0);basic_layout.addWidget(self.dir_input,2,1,1,2);basic_layout.addWidget(browse_button,2,3);basic_search_group.setLayout(basic_layout);main_layout.addWidget(basic_search_group)
        advanced_group=QGroupBox("Opções Avançadas");advanced_group.setCheckable(True);advanced_group.setChecked(False);advanced_layout=QGridLayout();advanced_layout.addWidget(QLabel("Classificação:"),0,0);self.category_combo=QComboBox();self.category_combo.addItems(FILE_CATEGORIES.keys());advanced_layout.addWidget(self.category_combo,0,1,1,3);advanced_layout.addWidget(QLabel("Tamanho:"),1,0);self.size_min_spinbox=QSpinBox();self.size_min_spinbox.setRange(0,99999);self.size_min_unit=QComboBox();self.size_min_unit.addItems(["Bytes","KB","MB","GB"]);self.size_min_unit.setCurrentText("MB");self.size_max_spinbox=QSpinBox();self.size_max_spinbox.setRange(0,99999);self.size_max_unit=QComboBox();self.size_max_unit.addItems(["Bytes","KB","MB","GB"]);self.size_max_unit.setCurrentText("MB");size_layout=QHBoxLayout();size_layout.addWidget(QLabel("Mínimo:"));size_layout.addWidget(self.size_min_spinbox);size_layout.addWidget(self.size_min_unit);size_layout.addStretch();size_layout.addWidget(QLabel("Máximo:"));size_layout.addWidget(self.size_max_spinbox);size_layout.addWidget(self.size_max_unit);advanced_layout.addLayout(size_layout,2,0,1,4);advanced_layout.addWidget(QLabel("Permissões:"),3,0);self.perm_readonly_check=QCheckBox("Apenas Leitura");self.perm_executable_check=QCheckBox("Executável");advanced_layout.addWidget(self.perm_readonly_check,3,1);advanced_layout.addWidget(self.perm_executable_check,3,2);advanced_group.setLayout(advanced_layout);main_layout.addWidget(advanced_group);self.advanced_group=advanced_group
        action_buttons_layout=QHBoxLayout();self.search_button=QPushButton("Buscar");self.search_button.clicked.connect(self.start_search);self.abort_button=QPushButton("Abortar");self.abort_button.clicked.connect(self.abort_search);self.abort_button.setEnabled(False);action_buttons_layout.addStretch();action_buttons_layout.addWidget(self.search_button);action_buttons_layout.addWidget(self.abort_button);action_buttons_layout.addStretch();main_layout.addLayout(action_buttons_layout)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(6)
        self.results_table.setHorizontalHeaderLabels(["Caminho Completo do Arquivo", "Tamanho", "Permissões", "Extensão", "Proprietário", "Última Modificação"])
        header = self.results_table.horizontalHeader();header.setSectionResizeMode(0, QHeaderView.Stretch);header.setSectionResizeMode(1, QHeaderView.ResizeToContents);header.setSectionResizeMode(2, QHeaderView.ResizeToContents);header.setSectionResizeMode(3, QHeaderView.ResizeToContents);header.setSectionResizeMode(4, QHeaderView.ResizeToContents);header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.results_table.doubleClicked.connect(self.open_file_location);self.results_table.setEditTriggers(QTableWidget.NoEditTriggers);self.results_table.setSelectionBehavior(QTableWidget.SelectRows)
        main_layout.addWidget(self.results_table)
        
        credits_layout = QHBoxLayout()
        # TODO: Substituir 'seu-email-aqui@dominio.com' pelo email correto
        credit_text = """
        <a href='https://github.com/henriquetourinho/S.I.G.M.A'><b>S.I.G.M.A.</b></a> | Criado por Carlos Henrique Tourinho Santana | 
        <a href='https://wiki.debian.org/henriquetourinho'>Wiki Debian</a> | 
        <a href='https://br.linkedin.com/in/carloshenriquetourinhosantana'>LinkedIn</a> | 
        <a href='https://github.com/henriquetourinho'>GitHub Pessoal</a> | 
        <a href='mailto:seu-email-aqui@dominio.com'>Email</a>
        """
        credits_label = QLabel(credit_text)
        credits_label.setTextFormat(Qt.RichText)
        credits_label.setOpenExternalLinks(True)
        credits_label.setAlignment(Qt.AlignCenter)
        credits_layout.addWidget(credits_label)
        main_layout.addLayout(credits_layout)
        
        self.setCentralWidget(main_widget)
        self.setStatusBar(QStatusBar())

    def browse_directory(self): directory = QFileDialog.getExistingDirectory(self, "Selecione um Diretório", self.dir_input.text()); (self.dir_input.setText(directory) if directory else None)
    def abort_search(self): (self.statusBar().showMessage("Abortando a busca..."), self.abort_flag.set()) if self.abort_flag else None
    def _format_size(self, size_bytes):
        if size_bytes < 1024: return f"{size_bytes} B"
        elif size_bytes < 1024**2: return f"{size_bytes/1024:.1f} KB"
        elif size_bytes < 1024**3: return f"{size_bytes/1024**2:.1f} MB"
        else: return f"{size_bytes/1024**3:.1f} GB"
    def _convert_size_to_bytes(self, v, u): return v*1024 if u=="KB" else v*1024**2 if u=="MB" else v*1024**3 if u=="GB" else v
    def start_search(self):
        criteria = {"name": self.name_input.text().strip(), "ext": self.ext_input.text().strip().replace(".", ""), "dir": self.dir_input.text().strip(), "advanced_enabled": self.advanced_group.isChecked(),}
        if criteria["advanced_enabled"]:
            criteria["category"] = self.category_combo.currentText(); min_v,max_v = self.size_min_spinbox.value(),self.size_max_spinbox.value()
            criteria["min_size"] = self._convert_size_to_bytes(min_v, self.size_min_unit.currentText()) if min_v > 0 else -1
            criteria["max_size"] = self._convert_size_to_bytes(max_v, self.size_max_unit.currentText()) if max_v > 0 else -1
            criteria["perm_readonly"] = self.perm_readonly_check.isChecked(); criteria["perm_executable"] = self.perm_executable_check.isChecked()
        if not criteria["name"] and not criteria["ext"] and not criteria["advanced_enabled"]: self.statusBar().showMessage("Erro: Forneça ao menos um critério de busca."); return
        self.search_button.setEnabled(False); self.abort_button.setEnabled(True); self.results_table.setRowCount(0); self.statusBar().showMessage(f"Buscando em {criteria['dir']}...")
        self.abort_flag = AbortFlag(); self.worker_signals = WorkerSignals(); self.worker_signals.found.connect(self.add_result); self.worker_signals.finished.connect(self.finish_search)
        self.search_thread = threading.Thread(target=self.run_search, args=(criteria, self.worker_signals, self.abort_flag)); self.search_thread.start()
    def run_search(self, criteria, signals, abort_flag):
        category_extensions = FILE_CATEGORIES.get(criteria.get("category", "Qualquer tipo"), [])
        try:
            for root, _, files in os.walk(criteria["dir"], onerror=lambda e: None):
                if abort_flag.is_set(): break
                for filename in files:
                    if abort_flag.is_set(): break
                    full_path = os.path.join(root, filename)
                    if criteria["name"] and criteria["name"].lower() not in filename.lower(): continue
                    file_ext = os.path.splitext(filename)[1]
                    if criteria["ext"] and not file_ext.lower() == f".{criteria['ext'].lower()}": continue
                    if criteria["advanced_enabled"]:
                        if category_extensions and file_ext.lower() not in category_extensions: continue
                        try:
                            file_stat_filter = os.stat(full_path)
                            if criteria["min_size"] != -1 and file_stat_filter.st_size < criteria["min_size"]: continue
                            if criteria["max_size"] != -1 and file_stat_filter.st_size > criteria["max_size"]: continue
                            if criteria["perm_readonly"] and os.access(full_path, os.W_OK): continue
                            if criteria["perm_executable"] and not os.access(full_path, os.X_OK): continue
                        except (FileNotFoundError, PermissionError): continue
                    try:
                        final_stat = os.stat(full_path)
                        try: owner = pwd.getpwuid(final_stat.st_uid).pw_name
                        except KeyError: owner = str(final_stat.st_uid)
                        mod_time = datetime.fromtimestamp(final_stat.st_mtime).strftime('%d/%m/%Y %H:%M')
                        result_data = {"full_path": full_path, "size": self._format_size(final_stat.st_size), "permissions": stat.filemode(final_stat.st_mode), "ext": file_ext, "owner": owner, "modified": mod_time}
                        signals.found.emit(result_data)
                    except (FileNotFoundError, PermissionError): continue
        except Exception: pass
        finally: signals.finished.emit()
    def add_result(self, file_data):
        row_position = self.results_table.rowCount()
        self.results_table.insertRow(row_position)
        path_item=QTableWidgetItem(file_data["full_path"]); size_item=QTableWidgetItem(file_data["size"]); perms_item=QTableWidgetItem(file_data["permissions"]); ext_item=QTableWidgetItem(file_data["ext"]); owner_item=QTableWidgetItem(file_data["owner"]); modified_item=QTableWidgetItem(file_data["modified"])
        size_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter); perms_item.setTextAlignment(Qt.AlignCenter); owner_item.setTextAlignment(Qt.AlignCenter); modified_item.setTextAlignment(Qt.AlignCenter)
        self.results_table.setItem(row_position, 0, path_item); self.results_table.setItem(row_position, 1, size_item); self.results_table.setItem(row_position, 2, perms_item); self.results_table.setItem(row_position, 3, ext_item); self.results_table.setItem(row_position, 4, owner_item); self.results_table.setItem(row_position, 5, modified_item)
    def open_file_location(self, mi):
        item = self.results_table.item(mi.row(), 0)
        if item:
            directory = os.path.dirname(item.text())
            try: os.system(f'xdg-open "{directory}"')
            except Exception as e: self.statusBar().showMessage(f"Não foi possível abrir a pasta: {e}")
    def finish_search(self):
        total_found = self.results_table.rowCount()
        if self.abort_flag and self.abort_flag.is_set(): self.statusBar().showMessage(f"Busca abortada. {total_found} arquivos encontrados.")
        else: self.statusBar().showMessage(f"Busca concluída. {total_found} arquivos encontrados.")
        self.search_button.setEnabled(True); self.abort_button.setEnabled(False); self.search_thread = None; self.abort_flag = None

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdvancedSearchApp()
    window.show()
    sys.exit(app.exec())