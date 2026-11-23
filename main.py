import math
import os
import sys
from html import escape

import mysql.connector
from PySide6.QtCore import (
    Qt, QEvent, QRect, QRectF, QPointF, QSize, QSettings, QDate, Signal,
    Property, QPropertyAnimation, QEasingCurve
)
from PySide6.QtGui import (
    QAction, QColor, QCursor, QFont, QFontDatabase, QIcon, QPainter,
    QPainterPath, QPen, QPixmap, QPolygonF
)
from PySide6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox,
    QTabWidget, QDoubleSpinBox, QComboBox, QTableWidget,
    QTableWidgetItem, QAbstractItemView, QHeaderView, QSpinBox,
    QCheckBox, QStyledItemDelegate, QStyle, QStyleOptionViewItem,
    QFrame, QGridLayout, QDateEdit, QListWidget, QListWidgetItem,
    QScrollArea, QSizePolicy
)


# ==================================================
# DATABASE
# ==================================================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="libreria_pyside_esame"
)
cursor = db.cursor()

operatore_corrente = None


# ==================================================
# COSTANTI
# ==================================================

LARGHEZZA_PULSANTE = 120
LARGHEZZA_COLONNA = 350
LARGHEZZA_COLONNA_SCORRIMENTO = 380
ALTEZZA_SCHEDA = 190
ALTEZZA_RIGA_TABELLA = 32


# ==================================================
# FUNZIONI COMUNI
# ==================================================

# --------------------------------------------------
# Temi e colori
# --------------------------------------------------

TEMI = {
    "scuro": {
        "pulsante_bg": "#333333",
        "pulsante_testo": "#ffffff",
        "pulsante_bordo": "#4a4a4a",
        "pulsante_hover": "#444444",
        "pulsante_premuto": "#2b2b2b",
        "pulsante_dis_bg": "#2a2a2a",
        "pulsante_dis_testo": "#7a7a7a",
        "pulsante_dis_bordo": "#3a3a3a",
        "tab_bg": "#262626",
        "tab_testo": "#cccccc",
        "tab_bordo": "#3a3a3a",
        "tab_sel_bg": "#3a3a3a",
        "tab_sel_testo": "#ffffff",
        "tab_hover_bg": "#456b50",
        "tab_hover_testo": "#ffffff",
        "hover_riga": "#456b50",
        "riga_selezionata": "#5a5a5a",
        "carrello_riga": "#4d4d4d",
        "carrello_selezionata": "#757575",
        "azione_blu": "#4a86c8",
        "azione_blu_hover": "#2f64a0",
        "tabella_intestazione": "#454545",
        "tabella_intestazione_testo": "#f2f2f2",
        "tabella_bordo": "#6a6a6a",
        "tabella_griglia": "#4a4a4a",
        "riga_alterna": "#383838",
        "tabella_sfondo": "#2f2f2f",
        "scheda_sfondo": "#33465e",
        "scheda_bordo": "#7ea6d6",
        "scheda_nomi": "#FFCCB6",
        "scheda_valori": "#ffffff",
        "scheda_linea": "#6f86a3",
        "scheda_ok": "#86e09a",
        "scheda_ko": "#ff9a9a",
        "pannello_sfondo": "#3a3a3a",
        "pannello_bordo": "#d0d0d0",
        "pannello_testo": "#ffffff",
        "pannello_linea": "#6a6a6a",
        "ok": "#7fd48f",
        "ko": "#ef8a8a",
        "annulla_bg": "#e6e6e6",
        "annulla_testo": "#222222",
        "annulla_bordo": "#bdbdbd",
        "annulla_hover_bg": "#ec9c9c",
        "annulla_hover_testo": "#3b0d0d",
        "annulla_hover_bordo": "#cf7070",
        "annulla_premuto": "#d95f5f",
        "spunta_sfondo": "#2b2b2b",
        "spunta_bordo": "#d0d0d0",
        "spunta_attiva": "#3f9b5a",
        "icone": "#e0e0e0",
    },
    "chiaro": {
        "pulsante_bg": "#f3f3f3",
        "pulsante_testo": "#1f1f1f",
        "pulsante_bordo": "#c8c8c8",
        "pulsante_hover": "#e2e2e2",
        "pulsante_premuto": "#d4d4d4",
        "pulsante_dis_bg": "#ececec",
        "pulsante_dis_testo": "#9a9a9a",
        "pulsante_dis_bordo": "#dcdcdc",
        "tab_bg": "#e6e6e6",
        "tab_testo": "#444444",
        "tab_bordo": "#cfcfcf",
        "tab_sel_bg": "#ffffff",
        "tab_sel_testo": "#111111",
        "tab_hover_bg": "#bfe3c9",
        "tab_hover_testo": "#12351c",
        "hover_riga": "#d4ecda",
        "riga_selezionata": "#cfcfcf",
        "carrello_riga": "#e2e2e2",
        "carrello_selezionata": "#b9b9b9",
        "azione_blu": "#5b9bd5",
        "azione_blu_hover": "#3a77b5",
        "tabella_intestazione": "#e2e2e2",
        "tabella_intestazione_testo": "#222222",
        "tabella_bordo": "#a8a8a8",
        "tabella_griglia": "#d4d4d4",
        "riga_alterna": "#f4f4f4",
        "tabella_sfondo": "#ffffff",
        "scheda_sfondo": "#e6f0fb",
        "scheda_bordo": "#6a9bd1",
        "scheda_nomi": "#9a4a1f",
        "scheda_valori": "#1a1a1a",
        "scheda_linea": "#c4c4c4",
        "scheda_ok": "#1e7a34",
        "scheda_ko": "#b02a2a",
        "pannello_sfondo": "#f2f2f2",
        "pannello_bordo": "#9e9e9e",
        "pannello_testo": "#1a1a1a",
        "pannello_linea": "#c4c4c4",
        "ok": "#1e7a34",
        "ko": "#b02a2a",
        "annulla_bg": "#f3f3f3",
        "annulla_testo": "#1f1f1f",
        "annulla_bordo": "#c8c8c8",
        "annulla_hover_bg": "#f4a6a6",
        "annulla_hover_testo": "#3b0d0d",
        "annulla_hover_bordo": "#d98080",
        "annulla_premuto": "#ee8f8f",
        "spunta_sfondo": "#ffffff",
        "spunta_bordo": "#7a7a7a",
        "spunta_attiva": "#2e8b4f",
        "icone": "#333333",
    },
}

TEMA_CORRENTE = "scuro"
COLORI = TEMI["scuro"]
VERDE_HOVER = COLORI["hover_riga"]
COLORE_OK = COLORI["ok"]
COLORE_KO = COLORI["ko"]
STILE_GENERALE = ""
STILE_ANNULLA = ""

MODELLO_GENERALE = """
QPushButton {
    background-color: %pulsante_bg%;
    color: %pulsante_testo%;
    border: 1px solid %pulsante_bordo%;
    border-radius: 4px;
    padding: 5px 10px;
}
QPushButton:hover {
    background-color: %pulsante_hover%;
}
QPushButton:pressed {
    background-color: %pulsante_premuto%;
}
QPushButton:disabled {
    background-color: %pulsante_dis_bg%;
    color: %pulsante_dis_testo%;
    border: 1px solid %pulsante_dis_bordo%;
}
QToolButton {
    background-color: transparent;
    border: 1px solid transparent;
    border-radius: 4px;
    padding: 4px;
}
QToolButton:hover {
    background-color: %pulsante_hover%;
}
QTabBar::tab {
    background-color: %tab_bg%;
    color: %tab_testo%;
    padding: 7px 14px;
    border: 1px solid %tab_bordo%;
    border-bottom: none;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background-color: %tab_sel_bg%;
    color: %tab_sel_testo%;
}
QTabBar::tab:hover:!selected {
    background-color: %tab_hover_bg%;
    color: %tab_hover_testo%;
}
QListWidget::item {
    padding: 6px 8px;
    border-bottom: 1px solid %tab_bordo%;
}
QListWidget::item:hover {
    background-color: %hover_riga%;
}
QListWidget::item:selected {
    background-color: %riga_selezionata%;
    color: %pannello_testo%;
}
QHeaderView::section {
    background-color: %tabella_intestazione%;
    color: %tabella_intestazione_testo%;
    padding: 8px 6px;
    border: none;
    border-bottom: 2px solid %tabella_bordo%;
    border-right: 1px solid %tabella_griglia%;
    font-weight: bold;
}
QTableWidget {
    background-color: %tabella_sfondo%;
    border: 1px solid %tabella_bordo%;
}
"""

MODELLO_ANNULLA = """
QPushButton {
    background-color: %annulla_bg%;
    color: %annulla_testo%;
    border: 1px solid %annulla_bordo%;
    border-radius: 4px;
    padding: 5px 10px;
}
QPushButton:hover {
    background-color: %annulla_hover_bg%;
    color: %annulla_hover_testo%;
    border: 1px solid %annulla_hover_bordo%;
}
QPushButton:pressed {
    background-color: %annulla_premuto%;
}
"""


def applica_colori(modello):
    for chiave, valore in COLORI.items():
        modello = modello.replace(f"%{chiave}%", valore)
    return modello


def imposta_tema(nome):
    global TEMA_CORRENTE, COLORI, VERDE_HOVER, COLORE_OK, COLORE_KO
    global STILE_GENERALE, STILE_ANNULLA

    TEMA_CORRENTE = nome
    COLORI = TEMI[nome]
    VERDE_HOVER = COLORI["hover_riga"]
    COLORE_OK = COLORI["ok"]
    COLORE_KO = COLORI["ko"]
    STILE_GENERALE = applica_colori(MODELLO_GENERALE)
    STILE_ANNULLA = applica_colori(MODELLO_ANNULLA)

    app = QApplication.instance()
    try:
        schema = Qt.ColorScheme.Dark if nome == "scuro" else Qt.ColorScheme.Light
        app.styleHints().setColorScheme(schema)
    except AttributeError:
        pass
    app.setStyleSheet(STILE_GENERALE)


def leggi_tema_salvato():
    tema = QSettings("GestionaleLibreria", "Gestionale").value("tema", "scuro")
    return tema if tema in TEMI else "scuro"


def salva_tema(nome):
    QSettings("GestionaleLibreria", "Gestionale").setValue("tema", nome)


# --------------------------------------------------
# Font
# --------------------------------------------------

FAMIGLIE_FONT = [
    "Segoe UI Variable Text", "Segoe UI", "SF Pro Text",
    "Helvetica Neue", "Roboto", "Noto Sans", "Arial"
]
DIMENSIONE_FONT = 11

FAMIGLIE_FONT_TABELLE = [
    "JetBrains Mono", "Cascadia Mono", "Cascadia Code", "Consolas",
    "SF Mono", "Menlo", "DejaVu Sans Mono", "Courier New"
]
DIMENSIONE_FONT_TABELLE = 10.5


def crea_font_base():
    carattere = QFont()
    carattere.setFamilies(FAMIGLIE_FONT)
    carattere.setPointSize(DIMENSIONE_FONT)
    carattere.setStyleStrategy(QFont.PreferAntialias)
    return carattere


def crea_font_tabelle():
    carattere = QFont()
    carattere.setFamilies(FAMIGLIE_FONT_TABELLE)
    carattere.setPointSizeF(DIMENSIONE_FONT_TABELLE)
    carattere.setStyleStrategy(QFont.PreferAntialias)
    return carattere


def carica_font_tabelle():
    cartella = os.path.dirname(os.path.abspath(__file__))
    for nome in ("JetBrainsMono-Regular.ttf", "JetBrainsMono-Bold.ttf"):
        percorso = os.path.join(cartella, nome)
        if os.path.exists(percorso):
            QFontDatabase.addApplicationFont(percorso)


# --------------------------------------------------
# Utilità
# --------------------------------------------------

def conferma(parent, titolo, messaggio):
    finestra = QMessageBox(parent)
    finestra.setIcon(QMessageBox.Question)
    finestra.setWindowTitle(titolo)
    finestra.setText(messaggio)
    pulsante_si = finestra.addButton("Sì", QMessageBox.YesRole)
    pulsante_no = finestra.addButton("No", QMessageBox.NoRole)
    finestra.setDefaultButton(pulsante_no)
    finestra.exec()
    return finestra.clickedButton() == pulsante_si


def conferma_pulizia(parent):
    return conferma(parent, "Pulisci modulo", "Vuoi cancellare tutti i campi compilati?")


def spezza_parole(testo, soglia=20, passo=6):
    parole = []
    for parola in testo.split(" "):
        if len(parola) > soglia:
            parola = "\u200b".join(
                parola[i:i + passo] for i in range(0, len(parola), passo)
            )
        parole.append(parola)
    return " ".join(parole)


def da_layout(layout):
    layout.setContentsMargins(0, 0, 0, 0)
    contenitore = QWidget()
    contenitore.setLayout(layout)
    return contenitore


# --------------------------------------------------
# Campi
# --------------------------------------------------

class CampoConSuggerimento(QLineEdit):
    def __init__(self, testo):
        super().__init__()
        self.testo_predefinito = testo
        self.setPlaceholderText(testo)

    def focusInEvent(self, evento):
        self.setPlaceholderText("")
        super().focusInEvent(evento)

    def focusOutEvent(self, evento):
        if not self.text():
            self.setPlaceholderText(self.testo_predefinito)
        super().focusOutEvent(evento)

    def azzera(self):
        self.clear()
        if not self.hasFocus():
            self.setPlaceholderText(self.testo_predefinito)


# --------------------------------------------------
# Tabelle
# --------------------------------------------------

class DelegateRiga(QStyledItemDelegate):
    MARGINE = 8

    def __init__(self, tabella):
        super().__init__(tabella)
        self.tabella = tabella

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter

    def sizeHint(self, option, index):
        dimensione = super().sizeHint(option, index)
        dimensione.setWidth(dimensione.width() + 2 * self.MARGINE)
        return dimensione

    def paint(self, painter, option, index):
        opzione = QStyleOptionViewItem(option)
        cella = QRect(opzione.rect)
        selezionata = bool(opzione.state & QStyle.State_Selected)
        opzione.state = opzione.state & ~QStyle.State_MouseOver & ~QStyle.State_HasFocus

        if selezionata:
            painter.fillRect(cella, QColor(COLORI[self.tabella.chiave_selezione]))
            opzione.state = opzione.state & ~QStyle.State_Selected
        elif index.row() == self.tabella.riga_hover:
            painter.fillRect(cella, QColor(VERDE_HOVER))
        elif self.tabella.chiave_base:
            painter.fillRect(cella, QColor(COLORI[self.tabella.chiave_base]))
        elif index.row() % 2 == 1:
            painter.fillRect(cella, QColor(COLORI["riga_alterna"]))

        painter.save()
        painter.setPen(QColor(COLORI["tabella_griglia"]))
        painter.drawLine(cella.bottomLeft(), cella.bottomRight())
        painter.drawLine(cella.topRight(), cella.bottomRight())
        painter.restore()

        opzione.rect = cella.adjusted(self.MARGINE, 0, -self.MARGINE, 0)
        super().paint(painter, opzione, index)


class TabellaDati(QTableWidget):
    def __init__(self, intestazioni):
        super().__init__()
        self.riga_hover = -1
        self.chiave_base = None
        self.chiave_selezione = "riga_selezionata"

        self.setColumnCount(len(intestazioni))
        self.setHorizontalHeaderLabels(intestazioni)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(ALTEZZA_RIGA_TABELLA)
        self.setShowGrid(False)
        self.setWordWrap(False)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)
        self.horizontalHeader().setMinimumSectionSize(50)
        self.setFont(crea_font_tabelle())
        self.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(20)

        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.setItemDelegate(DelegateRiga(self))

    def imposta_riga_hover(self, riga):
        if riga != self.riga_hover:
            self.riga_hover = riga
            self.viewport().update()

    def mouseMoveEvent(self, evento):
        self.imposta_riga_hover(self.rowAt(int(evento.position().y())))
        super().mouseMoveEvent(evento)

    def wheelEvent(self, evento):
        super().wheelEvent(evento)
        posizione = self.viewport().mapFromGlobal(QCursor.pos())
        self.imposta_riga_hover(self.rowAt(posizione.y()))

    def viewportEvent(self, evento):
        if evento.type() == QEvent.Leave:
            self.imposta_riga_hover(-1)
        return super().viewportEvent(evento)


class DelegateSpunta(DelegateRiga):
    LATO = 20
    cambiata = Signal()

    def rettangolo(self, cella):
        x = cella.center().x() - self.LATO // 2
        y = cella.center().y() - self.LATO // 2
        return QRect(x, y, self.LATO, self.LATO)

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        casella = self.rettangolo(option.rect)
        spuntata = index.data(Qt.UserRole) == 1
        sfondo = COLORI["spunta_attiva"] if spuntata else COLORI["spunta_sfondo"]

        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor(COLORI["spunta_bordo"]), 2))
        painter.setBrush(QColor(sfondo))
        painter.drawRoundedRect(casella.adjusted(1, 1, -1, -1), 4, 4)

        if spuntata:
            painter.setPen(
                QPen(QColor("#ffffff"), 2.5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            )
            x, y = casella.x(), casella.y()
            painter.drawPolyline(QPolygonF([
                QPointF(x + 5, y + 10),
                QPointF(x + 9, y + 14),
                QPointF(x + 15, y + 6),
            ]))
        painter.restore()

    def editorEvent(self, evento, model, option, index):
        if evento.type() == QEvent.MouseButtonRelease and evento.button() == Qt.LeftButton:
            if self.rettangolo(option.rect).contains(evento.position().toPoint()):
                spuntata = index.data(Qt.UserRole) == 1
                model.setData(index, 0 if spuntata else 1, Qt.UserRole)
                self.cambiata.emit()
                return True
        return super().editorEvent(evento, model, option, index)


# --------------------------------------------------
# Riquadri e schede
# --------------------------------------------------

class SchedaInfo(QFrame):
    DIMENSIONE_TITOLO = 19
    DIMENSIONE_TESTO = 15

    def __init__(self, messaggio_vuoto, colonne=1, altezza_minima=0):
        super().__init__()
        self.messaggio_vuoto = messaggio_vuoto
        self.colonne = colonne
        self.setMinimumWidth(260)
        self.setMinimumHeight(altezza_minima)
        self.setObjectName("schedaInfo")

        sfondo = COLORI["scheda_sfondo"]
        bordo = COLORI["scheda_bordo"]
        self.setStyleSheet(
            f"QFrame#schedaInfo {{ background-color: {sfondo}; "
            f"border: 2px solid {bordo}; border-radius: 6px; }}"
        )

        self.etichetta_titolo = QLabel(messaggio_vuoto)
        self.etichetta_titolo.setWordWrap(True)
        self.etichetta_titolo.setStyleSheet(
            f"color: {COLORI['scheda_valori']}; "
            f"font-size: {self.DIMENSIONE_TITOLO}px; font-weight: bold;"
        )

        self.linea = QFrame()
        self.linea.setFixedHeight(1)
        self.linea.setStyleSheet(f"background-color: {COLORI['scheda_linea']};")
        self.linea.setVisible(False)

        self.griglia = QGridLayout()
        self.griglia.setHorizontalSpacing(24)
        self.griglia.setVerticalSpacing(8)
        for colonna in range(colonne):
            self.griglia.setColumnStretch(colonna, 1)

        layout = QVBoxLayout()
        layout.setContentsMargins(14, 12, 14, 14)
        layout.setSpacing(8)
        layout.addWidget(self.etichetta_titolo)
        layout.addWidget(self.linea)
        layout.addLayout(self.griglia)
        layout.addStretch()
        self.setLayout(layout)

    def svuota_righe(self):
        while self.griglia.count():
            elemento = self.griglia.takeAt(0)
            if elemento.widget():
                elemento.widget().deleteLater()

    def svuota(self, messaggio=None):
        self.svuota_righe()
        self.etichetta_titolo.setText(messaggio or self.messaggio_vuoto)
        self.linea.setVisible(False)

    def mostra(self, titolo, righe):
        self.svuota_righe()
        self.etichetta_titolo.setText(spezza_parole(titolo))
        self.linea.setVisible(True)

        colore_nomi = COLORI["scheda_nomi"]
        sostituzioni = {COLORE_OK: COLORI["scheda_ok"], COLORE_KO: COLORI["scheda_ko"]}
        per_colonna = max(1, -(-len(righe) // self.colonne))
        for numero, riga in enumerate(righe):
            nome, valore, *resto = riga
            colore = resto[0] if resto else COLORI["scheda_valori"]
            colore = sostituzioni.get(colore, colore)
            peso = "bold" if valore in ("Disponibile", "Esaurito") else "normal"

            etichetta = QLabel(
                f'<span style="color:{colore_nomi}; font-weight:bold;">'
                f'{escape(nome)}:</span> '
                f'<span style="color:{colore}; font-weight:{peso};">'
                f'{escape(spezza_parole(valore))}</span>'
            )
            etichetta.setTextFormat(Qt.RichText)
            etichetta.setWordWrap(True)
            etichetta.setStyleSheet(f"font-size: {self.DIMENSIONE_TESTO}px;")
            self.griglia.addWidget(
                etichetta, numero % per_colonna, numero // per_colonna, Qt.AlignTop
            )


class Pannello(QFrame):
    def __init__(self, titolo, contenuto, dimensione=21, espandi=True, compatto=False):
        super().__init__()
        self.setObjectName("pannello")
        sfondo = COLORI["pannello_sfondo"]
        bordo = COLORI["pannello_bordo"]
        self.setStyleSheet(
            f"QFrame#pannello {{ background-color: {sfondo}; "
            f"border: 2px solid {bordo}; border-radius: 8px; }}"
        )

        if compatto:
            dimensione = 19
            margini = (14, 10, 14, 12)
            spazio = 8
        else:
            margini = (16, 14, 16, 16)
            spazio = 10

        self.etichetta_titolo = QLabel(titolo)
        self.etichetta_titolo.setStyleSheet(
            f"color: {COLORI['pannello_testo']}; "
            f"font-size: {dimensione}px; font-weight: bold;"
        )

        linea = QFrame()
        linea.setFixedHeight(1)
        linea.setStyleSheet(f"background-color: {COLORI['pannello_linea']};")

        layout = QVBoxLayout()
        layout.setContentsMargins(*margini)
        layout.setSpacing(spazio)
        layout.addWidget(self.etichetta_titolo)
        layout.addWidget(linea)
        layout.addWidget(contenuto, 1 if espandi else 0)
        self.setLayout(layout)

        if not espandi:
            self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

    def imposta_titolo(self, testo):
        self.etichetta_titolo.setText(testo)


# --------------------------------------------------
# Icone e logo
# --------------------------------------------------

def crea_icona(disegna, colore):
    lato = 24
    pixmap = QPixmap(lato * 2, lato * 2)
    pixmap.setDevicePixelRatio(2)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    penna = QPen(QColor(colore), 2)
    penna.setCapStyle(Qt.RoundCap)
    penna.setJoinStyle(Qt.RoundJoin)
    painter.setPen(penna)
    painter.setBrush(Qt.NoBrush)
    disegna(painter, QColor(colore))
    painter.end()
    return QIcon(pixmap)


def disegna_logout(painter, colore):
    painter.drawPolyline(QPolygonF([
        QPointF(10, 4), QPointF(5, 4), QPointF(5, 20), QPointF(10, 20)
    ]))
    painter.drawLine(QPointF(9, 12), QPointF(20, 12))
    painter.drawPolyline(QPolygonF([
        QPointF(16, 8), QPointF(20, 12), QPointF(16, 16)
    ]))


def disegna_sole(painter, colore):
    painter.drawEllipse(QPointF(12, 12), 4.5, 4.5)
    for angolo in range(0, 360, 45):
        radianti = math.radians(angolo)
        seno, coseno = math.sin(radianti), math.cos(radianti)
        painter.drawLine(
            QPointF(12 + 7.5 * coseno, 12 + 7.5 * seno),
            QPointF(12 + 10 * coseno, 12 + 10 * seno)
        )


def disegna_luna(painter, colore):
    luna = QPainterPath()
    luna.addEllipse(QPointF(12, 12), 8, 8)
    taglio = QPainterPath()
    taglio.addEllipse(QPointF(16, 9), 7, 7)
    painter.setPen(Qt.NoPen)
    painter.setBrush(colore)
    painter.drawPath(luna.subtracted(taglio))


def crea_logo(lato=76):
    pixmap = QPixmap(lato * 2, lato * 2)
    pixmap.setDevicePixelRatio(2)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor(COLORI["azione_blu"]))
    painter.drawRoundedRect(QRectF(0, 0, lato, lato), lato * 0.24, lato * 0.24)

    s = lato / 72
    painter.setBrush(QColor("#ffffff"))
    painter.drawPolygon(QPolygonF([
        QPointF(36 * s, 24 * s), QPointF(18 * s, 20 * s),
        QPointF(18 * s, 50 * s), QPointF(36 * s, 54 * s)
    ]))
    painter.drawPolygon(QPolygonF([
        QPointF(36 * s, 24 * s), QPointF(54 * s, 20 * s),
        QPointF(54 * s, 50 * s), QPointF(36 * s, 54 * s)
    ]))
    painter.setPen(QPen(QColor(COLORI["azione_blu"]), 2 * s))
    painter.drawLine(QPointF(36 * s, 24 * s), QPointF(36 * s, 54 * s))
    painter.end()
    return pixmap


# --------------------------------------------------
# Interruttore del tema
# --------------------------------------------------

class InterruttoreTema(QWidget):
    cambiato = Signal(str)

    LARGHEZZA = 58
    ALTEZZA = 30
    SFONDO_CHIARO = "#bcd7f5"
    SFONDO_SCURO = "#2f3b5c"

    def __init__(self, scuro):
        super().__init__()
        self.scuro = scuro
        self.in_corso = False
        self._posizione = 1.0 if scuro else 0.0

        self.setFixedSize(self.LARGHEZZA, self.ALTEZZA)
        self.setCursor(Qt.PointingHandCursor)
        self.aggiorna_suggerimento()

        self.animazione = QPropertyAnimation(self, b"posizione", self)
        self.animazione.setDuration(240)
        self.animazione.setEasingCurve(QEasingCurve.InOutCubic)
        self.animazione.finished.connect(self.animazione_finita)

    def leggi_posizione(self):
        return self._posizione

    def scrivi_posizione(self, valore):
        self._posizione = valore
        self.update()

    posizione = Property(float, leggi_posizione, scrivi_posizione)

    def aggiorna_suggerimento(self):
        self.setToolTip("Passa al tema chiaro" if self.scuro else "Passa al tema scuro")

    def alterna(self):
        if self.in_corso:
            return

        self.in_corso = True
        self.scuro = not self.scuro
        self.aggiorna_suggerimento()
        self.animazione.setStartValue(self._posizione)
        self.animazione.setEndValue(1.0 if self.scuro else 0.0)
        self.animazione.start()

    def animazione_finita(self):
        self.in_corso = False
        self.cambiato.emit("scuro" if self.scuro else "chiaro")

    def mescola(self, chiaro, scuro, t):
        a, b = QColor(chiaro), QColor(scuro)
        return QColor(
            round(a.red() + (b.red() - a.red()) * t),
            round(a.green() + (b.green() - a.green()) * t),
            round(a.blue() + (b.blue() - a.blue()) * t),
        )

    def mousePressEvent(self, evento):
        evento.accept()

    def mouseReleaseEvent(self, evento):
        if evento.button() == Qt.LeftButton and self.rect().contains(evento.position().toPoint()):
            self.alterna()

    def paintEvent(self, evento):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        altezza = self.ALTEZZA
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.mescola(self.SFONDO_CHIARO, self.SFONDO_SCURO, self._posizione))
        painter.drawRoundedRect(
            QRectF(0, 0, self.LARGHEZZA, altezza), altezza / 2, altezza / 2
        )

        margine = 3
        diametro = altezza - 2 * margine
        corsa = self.LARGHEZZA - diametro - 2 * margine
        x = margine + corsa * self._posizione

        painter.setBrush(QColor("#ffffff"))
        painter.drawEllipse(QRectF(x, margine, diametro, diametro))

        if self._posizione < 0.5:
            disegna = disegna_sole
            colore = QColor("#d98a00")
            opacita = 1 - self._posizione * 2
        else:
            disegna = disegna_luna
            colore = QColor("#3b4a80")
            opacita = self._posizione * 2 - 1

        scala = diametro * 0.8 / 24
        painter.save()
        painter.setOpacity(opacita)
        painter.translate(
            x + diametro / 2 - 12 * scala, margine + diametro / 2 - 12 * scala
        )
        painter.scale(scala, scala)
        penna = QPen(colore, 2.2)
        penna.setCapStyle(Qt.RoundCap)
        painter.setPen(penna)
        painter.setBrush(Qt.NoBrush)
        disegna(painter, colore)
        painter.restore()


# ==================================================
# LOGIN
# ==================================================

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionale Libreria - Accesso")
        self.setFixedSize(440, 580)

        self.setStyleSheet(
            f"QLineEdit {{ background-color: {COLORI['tabella_sfondo']}; "
            f"border: 1px solid {COLORI['tabella_bordo']}; border-radius: 6px; "
            f"padding: 8px 10px; }}"
            f"QLineEdit:focus {{ border: 2px solid {COLORI['azione_blu']}; }}"
        )

        logo = QLabel()
        logo.setPixmap(crea_logo(76))
        logo.setAlignment(Qt.AlignCenter)

        titolo = QLabel("Gestionale Libreria")
        titolo.setAlignment(Qt.AlignCenter)
        titolo.setStyleSheet("font-size: 28px; font-weight: bold;")

        sottotitolo = QLabel("Accedi con il tuo account operatore")
        sottotitolo.setAlignment(Qt.AlignCenter)
        sottotitolo.setStyleSheet(f"color: {COLORI['tab_testo']}; font-size: 15px;")

        etichetta_username = QLabel("Username")
        etichetta_username.setStyleSheet("font-weight: bold;")
        self.campo_username = QLineEdit()
        self.campo_username.setPlaceholderText("Inserisci il tuo username")
        self.campo_username.setMinimumHeight(44)
        self.campo_username.returnPressed.connect(lambda: self.campo_password.setFocus())
        self.campo_username.textChanged.connect(self.nascondi_errore)

        etichetta_password = QLabel("Password")
        etichetta_password.setStyleSheet("font-weight: bold;")
        self.campo_password = QLineEdit()
        self.campo_password.setPlaceholderText("Inserisci la tua password")
        self.campo_password.setEchoMode(QLineEdit.Password)
        self.campo_password.setMinimumHeight(44)
        self.campo_password.returnPressed.connect(self.controlla_credenziali)
        self.campo_password.textChanged.connect(self.nascondi_errore)

        self.mostra_password = QCheckBox("Mostra password")
        self.mostra_password.toggled.connect(self.alterna_password)

        self.etichetta_errore = QLabel()
        self.etichetta_errore.setWordWrap(True)
        self.etichetta_errore.setStyleSheet(f"color: {COLORI['ko']}; font-weight: bold;")
        self.etichetta_errore.setVisible(False)

        self.bottone_accedi = QPushButton("Accedi")
        self.bottone_accedi.setAutoDefault(False)
        self.bottone_accedi.setDefault(False)
        self.bottone_accedi.setMinimumHeight(46)
        self.bottone_accedi.setCursor(Qt.PointingHandCursor)
        self.bottone_accedi.clicked.connect(self.controlla_credenziali)
        self.bottone_accedi.setStyleSheet(
            f"QPushButton {{ background-color: {COLORI['azione_blu']}; color: #ffffff; "
            f"border: 1px solid {COLORI['azione_blu']}; border-radius: 6px; "
            f"font-size: 16px; font-weight: bold; padding: 10px; }}"
            f"QPushButton:hover {{ background-color: {COLORI['azione_blu_hover']}; "
            f"border: 1px solid {COLORI['azione_blu_hover']}; }}"
        )

        scheda = QFrame()
        scheda.setObjectName("schedaLogin")
        scheda.setStyleSheet(
            f"QFrame#schedaLogin {{ background-color: {COLORI['pannello_sfondo']}; "
            f"border: 2px solid {COLORI['pannello_bordo']}; border-radius: 12px; }}"
        )

        layout_scheda = QVBoxLayout(scheda)
        layout_scheda.setContentsMargins(26, 24, 26, 24)
        layout_scheda.setSpacing(8)
        layout_scheda.addWidget(etichetta_username)
        layout_scheda.addWidget(self.campo_username)
        layout_scheda.addSpacing(6)
        layout_scheda.addWidget(etichetta_password)
        layout_scheda.addWidget(self.campo_password)
        layout_scheda.addWidget(self.mostra_password)
        layout_scheda.addWidget(self.etichetta_errore)
        layout_scheda.addSpacing(6)
        layout_scheda.addWidget(self.bottone_accedi)

        piede = QLabel("Accesso riservato agli operatori autorizzati")
        piede.setAlignment(Qt.AlignCenter)
        piede.setStyleSheet(f"color: {COLORI['tab_testo']}; font-size: 12px;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(36, 30, 36, 24)
        layout.addWidget(logo)
        layout.addSpacing(10)
        layout.addWidget(titolo)
        layout.addWidget(sottotitolo)
        layout.addSpacing(24)
        layout.addWidget(scheda)
        layout.addStretch()
        layout.addWidget(piede)

        self.setTabOrder(self.campo_username, self.campo_password)
        self.setTabOrder(self.campo_password, self.mostra_password)
        self.setTabOrder(self.mostra_password, self.bottone_accedi)
        self.campo_username.setFocus()

    def alterna_password(self, visibile):
        if visibile:
            self.campo_password.setEchoMode(QLineEdit.Normal)
        else:
            self.campo_password.setEchoMode(QLineEdit.Password)

    def mostra_errore(self, messaggio):
        self.etichetta_errore.setText(messaggio)
        self.etichetta_errore.setVisible(True)

    def nascondi_errore(self):
        self.etichetta_errore.setVisible(False)

    def controlla_credenziali(self):
        global operatore_corrente

        username = self.campo_username.text().strip()
        password = self.campo_password.text()

        if not username or not password:
            self.mostra_errore("Inserisci username e password.")
            return

        cursor.execute(
            "SELECT id_operatore, nome FROM operatori WHERE username = %s AND password = %s",
            (username, password)
        )
        risultato = cursor.fetchone()

        if risultato:
            operatore_corrente = risultato
            self.accept()
        else:
            self.campo_password.clear()
            self.mostra_errore("Username o password errati.")
            self.campo_password.setFocus()


# ==================================================
# LIBRI E CATEGORIE
# ==================================================

class TabLibri(QWidget):
    def __init__(self):
        super().__init__()
        self.id_selezionato = None
        self.setFocusPolicy(Qt.ClickFocus)

        self.campo_titolo = QLineEdit()
        self.campo_autore = QLineEdit()
        self.campo_isbn = QLineEdit()
        self.campo_prezzo = QDoubleSpinBox()
        self.campo_prezzo.setMaximum(9999.99)
        self.campo_prezzo.setSuffix(" €")
        self.campo_categoria = QComboBox()

        form = QFormLayout()
        form.addRow("Titolo", self.campo_titolo)
        form.addRow("Autore", self.campo_autore)
        form.addRow("ISBN", self.campo_isbn)
        form.addRow("Prezzo", self.campo_prezzo)
        form.addRow("Categoria", self.campo_categoria)

        self.bottone_aggiungi = QPushButton("Aggiungi")
        self.bottone_aggiungi.clicked.connect(self.aggiungi_libro)
        bottone_modifica = QPushButton("Modifica")
        bottone_modifica.clicked.connect(self.modifica_libro)
        bottone_elimina = QPushButton("Elimina")
        bottone_elimina.clicked.connect(self.elimina_libro)
        self.bottone_pulisci = QPushButton("Pulisci modulo")
        self.bottone_pulisci.clicked.connect(self.pulisci_modulo)
        self.bottone_annulla = QPushButton("Annulla selezione")
        self.bottone_annulla.clicked.connect(self.svuota_modulo)

        self.campo_nuova_categoria = CampoConSuggerimento("Nuova categoria")
        bottone_categoria = QPushButton("Aggiungi categoria")
        bottone_categoria.clicked.connect(self.aggiungi_categoria)

        self.campo_elimina_categoria = QComboBox()
        bottone_elimina_categoria = QPushButton("Elimina categoria")
        bottone_elimina_categoria.clicked.connect(self.elimina_categoria)

        colonna_libro = QVBoxLayout()
        colonna_libro.addLayout(form)
        colonna_libro.addSpacing(4)
        colonna_libro.addWidget(self.bottone_aggiungi)
        colonna_libro.addWidget(bottone_modifica)
        colonna_libro.addWidget(bottone_elimina)
        colonna_libro.addWidget(self.bottone_pulisci)
        colonna_libro.addWidget(self.bottone_annulla)

        colonna_categorie = QVBoxLayout()
        colonna_categorie.addWidget(self.campo_nuova_categoria)
        colonna_categorie.addWidget(bottone_categoria)
        colonna_categorie.addSpacing(10)
        colonna_categorie.addWidget(self.campo_elimina_categoria)
        colonna_categorie.addWidget(bottone_elimina_categoria)

        colonna_sinistra = QVBoxLayout()
        colonna_sinistra.addWidget(
            Pannello("Dati libro", da_layout(colonna_libro), espandi=False, compatto=True)
        )
        colonna_sinistra.addSpacing(12)
        colonna_sinistra.addWidget(
            Pannello("Categorie", da_layout(colonna_categorie), espandi=False, compatto=True)
        )
        colonna_sinistra.addStretch()

        contenitore_sinistra = da_layout(colonna_sinistra)
        contenitore_sinistra.setFixedWidth(LARGHEZZA_COLONNA)
        contenitore_sinistra.setFocusPolicy(Qt.ClickFocus)

        self.tabella = TabellaDati(["ID", "Titolo", "Autore", "ISBN", "Prezzo", "Categoria"])
        for colonna in (0, 4):
            self.tabella.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )
        self.tabella.itemSelectionChanged.connect(self.riga_selezionata)

        self.scheda = SchedaInfo("Nessun libro selezionato", colonne=2, altezza_minima=ALTEZZA_SCHEDA)

        colonna_destra = QVBoxLayout()
        colonna_destra.addWidget(Pannello("Elenco libri", self.tabella), 1)
        colonna_destra.addWidget(self.scheda)

        layout = QHBoxLayout()
        layout.addWidget(contenitore_sinistra)
        layout.addLayout(colonna_destra)
        self.setLayout(layout)

        self.carica_categorie()
        self.carica_libri()
        self.aggiorna_pulsanti()

    def aggiorna(self):
        db.commit()
        self.carica_categorie()
        self.carica_libri()
        if self.id_selezionato is not None:
            self.svuota_modulo()

    def aggiorna_pulsanti(self):
        selezionato = self.id_selezionato is not None
        self.bottone_aggiungi.setEnabled(not selezionato)
        self.bottone_pulisci.setEnabled(not selezionato)
        self.bottone_annulla.setEnabled(selezionato)
        self.bottone_annulla.setStyleSheet(STILE_ANNULLA if selezionato else "")

    def carica_categorie(self):
        corrente = self.campo_categoria.currentData()

        self.campo_categoria.clear()
        self.campo_categoria.addItem("(nessuna)", None)
        self.campo_elimina_categoria.clear()
        self.campo_elimina_categoria.addItem("Seleziona categoria", None)

        cursor.execute("SELECT id_categoria, nome FROM categorie ORDER BY nome")
        for id_categoria, nome in cursor.fetchall():
            self.campo_categoria.addItem(nome, id_categoria)
            self.campo_elimina_categoria.addItem(nome, id_categoria)

        self.campo_categoria.setCurrentIndex(
            max(self.campo_categoria.findData(corrente), 0)
        )

    def carica_libri(self):
        cursor.execute(
            "SELECT l.id_libro, l.titolo, l.autore, l.isbn, l.prezzo, c.nome "
            "FROM libri l LEFT JOIN categorie c ON l.id_categoria = c.id_categoria "
            "ORDER BY l.titolo"
        )
        righe = cursor.fetchall()

        self.tabella.setRowCount(len(righe))
        for numero, riga in enumerate(righe):
            for colonna, valore in enumerate(riga):
                if colonna == 4:
                    testo = f"{valore:.2f} €"
                else:
                    testo = "" if valore is None else str(valore)
                self.tabella.setItem(numero, colonna, QTableWidgetItem(testo))

    def riga_selezionata(self):
        selezione = self.tabella.selectedItems()
        if not selezione:
            return

        self.id_selezionato = int(self.tabella.item(selezione[0].row(), 0).text())
        cursor.execute(
            "SELECT l.titolo, l.autore, l.isbn, l.prezzo, l.id_categoria, m.copie "
            "FROM libri l LEFT JOIN magazzino m ON l.id_libro = m.id_libro "
            "WHERE l.id_libro = %s",
            (self.id_selezionato,)
        )
        titolo, autore, isbn, prezzo, id_categoria, copie = cursor.fetchone()

        self.campo_titolo.setText(titolo)
        self.campo_autore.setText(autore)
        self.campo_isbn.setText(isbn or "")
        self.campo_prezzo.setValue(float(prezzo))
        self.campo_categoria.setCurrentIndex(
            max(self.campo_categoria.findData(id_categoria), 0)
        )
        self.aggiorna_pulsanti()
        self.mostra_scheda(titolo, autore, isbn, prezzo, copie or 0)

    def mostra_scheda(self, titolo, autore, isbn, prezzo, copie):
        disponibile = copie > 0
        categoria = "-"
        if self.campo_categoria.currentIndex() > 0:
            categoria = self.campo_categoria.currentText()

        self.scheda.mostra(titolo, [
            ("Autore", autore),
            ("ISBN", isbn or "-"),
            ("Categoria", categoria),
            ("Prezzo", f"{prezzo:.2f} €"),
            ("Copie in magazzino", str(copie)),
            ("Stato", "Disponibile" if disponibile else "Esaurito",
             COLORE_OK if disponibile else COLORE_KO),
        ])

    def leggi_modulo(self):
        titolo = self.campo_titolo.text().strip()
        autore = self.campo_autore.text().strip()
        isbn = self.campo_isbn.text().strip() or None
        prezzo = self.campo_prezzo.value()
        id_categoria = self.campo_categoria.currentData()

        if not titolo or not autore:
            QMessageBox.warning(self, "Attenzione", "Titolo e autore sono obbligatori.")
            return None
        if prezzo <= 0:
            QMessageBox.warning(self, "Attenzione", "Il prezzo deve essere maggiore di zero.")
            return None
        return titolo, autore, isbn, prezzo, id_categoria

    def aggiungi_libro(self):
        dati = self.leggi_modulo()
        if dati is None:
            return

        try:
            cursor.execute(
                "INSERT INTO libri (titolo, autore, isbn, prezzo, id_categoria) "
                "VALUES (%s, %s, %s, %s, %s)",
                dati
            )
            cursor.execute(
                "INSERT INTO magazzino (id_libro, copie) VALUES (%s, 0)",
                (cursor.lastrowid,)
            )
            db.commit()
        except mysql.connector.Error as errore:
            db.rollback()
            QMessageBox.critical(self, "Errore", f"Impossibile aggiungere il libro.\n{errore}")
            return

        self.svuota_modulo()
        self.carica_libri()

    def modifica_libro(self):
        if self.id_selezionato is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona prima un libro dalla tabella.")
            return

        dati = self.leggi_modulo()
        if dati is None:
            return

        if not conferma(self, "Modifica", "Vuoi salvare le modifiche al libro selezionato?"):
            return

        try:
            cursor.execute(
                "UPDATE libri SET titolo = %s, autore = %s, isbn = %s, "
                "prezzo = %s, id_categoria = %s WHERE id_libro = %s",
                dati + (self.id_selezionato,)
            )
            db.commit()
        except mysql.connector.Error as errore:
            db.rollback()
            QMessageBox.critical(self, "Errore", f"Impossibile modificare il libro.\n{errore}")
            return

        self.svuota_modulo()
        self.carica_libri()

    def elimina_libro(self):
        if self.id_selezionato is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona prima un libro dalla tabella.")
            return

        titolo = self.campo_titolo.text().strip()
        if not conferma(self, "Elimina", f'Vuoi eliminare definitivamente il libro "{titolo}"?'):
            return

        try:
            cursor.execute("DELETE FROM magazzino WHERE id_libro = %s", (self.id_selezionato,))
            cursor.execute("DELETE FROM libri WHERE id_libro = %s", (self.id_selezionato,))
            db.commit()
        except mysql.connector.Error:
            db.rollback()
            QMessageBox.critical(
                self, "Errore",
                "Il libro non può essere eliminato perché compare in alcune vendite."
            )
            return

        self.svuota_modulo()
        self.carica_libri()

    def aggiungi_categoria(self):
        nome = self.campo_nuova_categoria.text().strip()
        if not nome:
            QMessageBox.warning(self, "Attenzione", "Inserisci il nome della categoria.")
            return

        if not conferma(self, "Nuova categoria", f'Vuoi creare la categoria "{nome}"?'):
            return

        try:
            cursor.execute("INSERT INTO categorie (nome) VALUES (%s)", (nome,))
            db.commit()
        except mysql.connector.Error:
            db.rollback()
            QMessageBox.critical(self, "Errore", "Categoria già esistente.")
            return

        self.campo_nuova_categoria.azzera()
        self.carica_categorie()

    def elimina_categoria(self):
        id_categoria = self.campo_elimina_categoria.currentData()
        if id_categoria is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona la categoria da eliminare.")
            return

        nome = self.campo_elimina_categoria.currentText()
        cursor.execute(
            "SELECT COUNT(*) FROM libri WHERE id_categoria = %s", (id_categoria,)
        )
        quantita = cursor.fetchone()[0]

        if quantita == 0:
            messaggio = f'Vuoi eliminare definitivamente la categoria "{nome}"?'
        else:
            libri = "1 libro" if quantita == 1 else f"{quantita} libri"
            messaggio = (
                f'La categoria "{nome}" è assegnata a {libri}.\n\n'
                "Se confermi, la categoria verrà eliminata e questi libri resteranno "
                'senza categoria: li troverai nella sezione "Senza categoria", '
                "dove potrai assegnarli a un'altra categoria.\n\n"
                "Vuoi continuare?"
            )

        if not conferma(self, "Elimina categoria", messaggio):
            return

        try:
            cursor.execute(
                "UPDATE libri SET id_categoria = NULL WHERE id_categoria = %s",
                (id_categoria,)
            )
            cursor.execute(
                "DELETE FROM categorie WHERE id_categoria = %s", (id_categoria,)
            )
            db.commit()
        except mysql.connector.Error as errore:
            db.rollback()
            QMessageBox.critical(
                self, "Errore", f"Impossibile eliminare la categoria.\n{errore}"
            )
            return

        self.svuota_modulo()
        self.carica_categorie()
        self.carica_libri()

    def modulo_compilato(self):
        testi = (
            self.campo_titolo.text(), self.campo_autore.text(), self.campo_isbn.text()
        )
        return (
            any(testo.strip() for testo in testi)
            or self.campo_prezzo.value() > 0
            or self.campo_categoria.currentIndex() > 0
        )

    def pulisci_modulo(self):
        if self.modulo_compilato() and conferma_pulizia(self):
            self.svuota_modulo()

    def svuota_modulo(self):
        self.setFocus()
        self.id_selezionato = None
        self.campo_titolo.clear()
        self.campo_autore.clear()
        self.campo_isbn.clear()
        self.campo_prezzo.setValue(0)
        self.campo_categoria.setCurrentIndex(0)
        self.tabella.clearSelection()
        self.scheda.svuota()
        self.aggiorna_pulsanti()


# ==================================================
# SENZA CATEGORIA
# ==================================================

class TabSenzaCategoria(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.ClickFocus)

        self.suggerimento = QLabel(
            "Clicca sul riquadro a sinistra di ogni libro per spuntarlo, "
            "poi scegli la categoria da assegnare."
        )
        self.suggerimento.setWordWrap(True)

        self.etichetta_conteggio = QLabel("Libri selezionati: 0")

        bottone_tutti = QPushButton("Seleziona tutti")
        bottone_tutti.clicked.connect(lambda: self.spunta_tutti(True))
        bottone_nessuno = QPushButton("Deseleziona")
        bottone_nessuno.clicked.connect(lambda: self.spunta_tutti(False))

        self.campo_categoria = QComboBox()
        bottone_assegna = QPushButton("Assegna categoria")
        bottone_assegna.clicked.connect(self.assegna_categoria)

        riga_spunte = QHBoxLayout()
        riga_spunte.addWidget(bottone_tutti)
        riga_spunte.addWidget(bottone_nessuno)

        colonna_assegna = QVBoxLayout()
        colonna_assegna.addWidget(self.suggerimento)
        colonna_assegna.addSpacing(10)
        colonna_assegna.addWidget(self.etichetta_conteggio)
        colonna_assegna.addSpacing(8)
        colonna_assegna.addLayout(riga_spunte)
        colonna_assegna.addSpacing(16)
        colonna_assegna.addWidget(self.campo_categoria)
        colonna_assegna.addWidget(bottone_assegna)

        colonna_sinistra = QVBoxLayout()
        colonna_sinistra.addWidget(
            Pannello("Assegnazione", da_layout(colonna_assegna), espandi=False, compatto=True)
        )
        colonna_sinistra.addStretch()

        contenitore_sinistra = da_layout(colonna_sinistra)
        contenitore_sinistra.setFixedWidth(LARGHEZZA_COLONNA)
        contenitore_sinistra.setFocusPolicy(Qt.ClickFocus)

        self.tabella = TabellaDati(["", "ID", "Titolo", "Autore", "ISBN", "Prezzo", "Copie"])
        intestazione = self.tabella.horizontalHeader()
        intestazione.setSectionResizeMode(0, QHeaderView.Fixed)
        self.tabella.setColumnWidth(0, 50)
        for colonna in (1, 5, 6):
            intestazione.setSectionResizeMode(colonna, QHeaderView.ResizeToContents)

        self.delegate_spunta = DelegateSpunta(self.tabella)
        self.tabella.setItemDelegateForColumn(0, self.delegate_spunta)
        self.delegate_spunta.cambiata.connect(self.aggiorna_conteggio)
        self.tabella.itemSelectionChanged.connect(self.riga_selezionata)

        self.scheda = SchedaInfo("Nessun libro selezionato", colonne=2, altezza_minima=ALTEZZA_SCHEDA)

        colonna_destra = QVBoxLayout()
        colonna_destra.addWidget(Pannello("Libri senza categoria", self.tabella), 1)
        colonna_destra.addWidget(self.scheda)

        layout = QHBoxLayout()
        layout.addWidget(contenitore_sinistra)
        layout.addLayout(colonna_destra)
        self.setLayout(layout)

        self.aggiorna()

    def carica_categorie(self):
        corrente = self.campo_categoria.currentData()

        self.campo_categoria.clear()
        self.campo_categoria.addItem("Seleziona categoria", None)
        cursor.execute("SELECT id_categoria, nome FROM categorie ORDER BY nome")
        for id_categoria, nome in cursor.fetchall():
            self.campo_categoria.addItem(nome, id_categoria)

        self.campo_categoria.setCurrentIndex(
            max(self.campo_categoria.findData(corrente), 0)
        )

    def aggiorna(self):
        db.commit()
        self.carica_categorie()

        cursor.execute(
            "SELECT l.id_libro, l.titolo, l.autore, l.isbn, l.prezzo, m.copie "
            "FROM libri l LEFT JOIN magazzino m ON l.id_libro = m.id_libro "
            "WHERE l.id_categoria IS NULL ORDER BY l.titolo"
        )
        righe = cursor.fetchall()

        self.tabella.clearSelection()
        self.tabella.setRowCount(len(righe))
        for numero, riga in enumerate(righe):
            casella = QTableWidgetItem()
            casella.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            casella.setData(Qt.UserRole, 0)
            self.tabella.setItem(numero, 0, casella)

            for colonna, valore in enumerate(riga, start=1):
                if colonna == 5:
                    testo = f"{valore:.2f} €"
                elif colonna == 6:
                    testo = str(valore or 0)
                else:
                    testo = "" if valore is None else str(valore)
                self.tabella.setItem(numero, colonna, QTableWidgetItem(testo))

        self.aggiorna_conteggio()
        if righe:
            self.scheda.svuota()
        else:
            self.scheda.svuota("Tutti i libri hanno una categoria")

    def spunta_tutti(self, spunta):
        for riga in range(self.tabella.rowCount()):
            self.tabella.item(riga, 0).setData(Qt.UserRole, 1 if spunta else 0)
        self.aggiorna_conteggio()

    def ids_spuntati(self):
        ids = []
        for riga in range(self.tabella.rowCount()):
            if self.tabella.item(riga, 0).data(Qt.UserRole) == 1:
                ids.append(int(self.tabella.item(riga, 1).text()))
        return ids

    def aggiorna_conteggio(self):
        self.etichetta_conteggio.setText(f"Libri selezionati: {len(self.ids_spuntati())}")

    def riga_selezionata(self):
        selezione = self.tabella.selectedItems()
        if not selezione:
            return

        id_libro = int(self.tabella.item(selezione[0].row(), 1).text())
        self.mostra_scheda(id_libro)

    def mostra_scheda(self, id_libro):
        cursor.execute(
            "SELECT l.titolo, l.autore, l.isbn, l.prezzo, m.copie "
            "FROM libri l LEFT JOIN magazzino m ON l.id_libro = m.id_libro "
            "WHERE l.id_libro = %s",
            (id_libro,)
        )
        titolo, autore, isbn, prezzo, copie = cursor.fetchone()
        copie = copie or 0
        disponibile = copie > 0

        self.scheda.mostra(titolo, [
            ("Autore", autore),
            ("ISBN", isbn or "-"),
            ("Categoria", "Nessuna"),
            ("Prezzo", f"{prezzo:.2f} €"),
            ("Copie in magazzino", str(copie)),
            ("Stato", "Disponibile" if disponibile else "Esaurito",
             COLORE_OK if disponibile else COLORE_KO),
        ])

    def assegna_categoria(self):
        ids = self.ids_spuntati()
        if not ids:
            QMessageBox.warning(self, "Attenzione", "Seleziona almeno un libro dalla tabella.")
            return

        id_categoria = self.campo_categoria.currentData()
        if id_categoria is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona la categoria da assegnare.")
            return

        nome = self.campo_categoria.currentText()
        if len(ids) == 1:
            destinatari = "al libro selezionato"
        else:
            destinatari = f"ai {len(ids)} libri selezionati"

        if not conferma(
            self, "Assegna categoria",
            f'Vuoi assegnare la categoria "{nome}" {destinatari}?'
        ):
            return

        try:
            segnaposti = ", ".join(["%s"] * len(ids))
            cursor.execute(
                f"UPDATE libri SET id_categoria = %s WHERE id_libro IN ({segnaposti})",
                [id_categoria] + ids
            )
            db.commit()
        except mysql.connector.Error as errore:
            db.rollback()
            QMessageBox.critical(
                self, "Errore", f"Impossibile assegnare la categoria.\n{errore}"
            )
            return

        self.campo_categoria.setCurrentIndex(0)
        self.aggiorna()


# ==================================================
# MAGAZZINO
# ==================================================

class TabMagazzino(QWidget):
    def __init__(self):
        super().__init__()
        self.id_selezionato = None
        self.autore_filtrato = ""
        self.titolo_filtrato = ""
        self.setFocusPolicy(Qt.ClickFocus)

        self.campo_quantita = QSpinBox()
        self.campo_quantita.setRange(0, 9999)
        self.campo_quantita.setValue(1)

        bottone_aggiungi = QPushButton("Aggiungi copie")
        bottone_aggiungi.clicked.connect(self.aggiungi_copie)
        bottone_rimuovi = QPushButton("Rimuovi copie")
        bottone_rimuovi.clicked.connect(self.rimuovi_copie)

        self.campo_autore = CampoConSuggerimento("Nome autore")
        self.campo_autore.returnPressed.connect(self.filtra_autore)
        bottone_autore = QPushButton("Filtra autore")
        bottone_autore.setFixedWidth(120)
        bottone_autore.clicked.connect(self.filtra_autore)

        self.campo_titolo = CampoConSuggerimento("Nome libro")
        self.campo_titolo.returnPressed.connect(self.filtra_titolo)
        bottone_titolo = QPushButton("Cerca titolo")
        bottone_titolo.setFixedWidth(120)
        bottone_titolo.clicked.connect(self.filtra_titolo)

        bottone_reset = QPushButton("Reset")
        bottone_reset.setFixedWidth(120)
        bottone_reset.clicked.connect(self.reset_filtri)

        self.filtro_esauriti = QCheckBox("Mostra solo libri esauriti")
        self.filtro_esauriti.stateChanged.connect(lambda: self.aggiorna())

        form = QFormLayout()
        form.addRow("Quantità", self.campo_quantita)

        riga_autore = QHBoxLayout()
        riga_autore.addWidget(self.campo_autore)
        riga_autore.addWidget(bottone_autore)

        riga_titolo = QHBoxLayout()
        riga_titolo.addWidget(self.campo_titolo)
        riga_titolo.addWidget(bottone_titolo)

        riga_reset = QHBoxLayout()
        riga_reset.addStretch()
        riga_reset.addWidget(bottone_reset)

        colonna_copie = QVBoxLayout()
        colonna_copie.addLayout(form)
        colonna_copie.addSpacing(4)
        colonna_copie.addWidget(bottone_aggiungi)
        colonna_copie.addWidget(bottone_rimuovi)

        colonna_ricerca = QVBoxLayout()
        colonna_ricerca.addLayout(riga_autore)
        colonna_ricerca.addSpacing(8)
        colonna_ricerca.addLayout(riga_titolo)
        colonna_ricerca.addSpacing(8)
        colonna_ricerca.addLayout(riga_reset)
        colonna_ricerca.addSpacing(10)
        colonna_ricerca.addWidget(self.filtro_esauriti)

        colonna_sinistra = QVBoxLayout()
        colonna_sinistra.addWidget(
            Pannello("Gestione copie", da_layout(colonna_copie), espandi=False, compatto=True)
        )
        colonna_sinistra.addSpacing(12)
        colonna_sinistra.addWidget(
            Pannello("Ricerca", da_layout(colonna_ricerca), espandi=False, compatto=True)
        )
        colonna_sinistra.addStretch()

        contenitore_sinistra = da_layout(colonna_sinistra)
        contenitore_sinistra.setFixedWidth(LARGHEZZA_COLONNA)
        contenitore_sinistra.setFocusPolicy(Qt.ClickFocus)

        self.tabella = TabellaDati(["ID", "Titolo", "Autore", "Copie"])
        for colonna in (0, 3):
            self.tabella.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )
        self.tabella.itemSelectionChanged.connect(self.riga_selezionata)

        self.scheda = SchedaInfo("Nessun libro selezionato", colonne=2, altezza_minima=ALTEZZA_SCHEDA)

        colonna_destra = QVBoxLayout()
        colonna_destra.addWidget(Pannello("Magazzino", self.tabella), 1)
        colonna_destra.addWidget(self.scheda)

        layout = QHBoxLayout()
        layout.addWidget(contenitore_sinistra)
        layout.addLayout(colonna_destra)
        self.setLayout(layout)

        self.aggiorna()

    def aggiorna(self):
        db.commit()

        query = (
            "SELECT l.id_libro, l.titolo, l.autore, m.copie "
            "FROM libri l JOIN magazzino m ON l.id_libro = m.id_libro "
        )
        condizioni = []
        parametri = []

        if self.filtro_esauriti.isChecked():
            condizioni.append("m.copie = 0")
        if self.autore_filtrato:
            condizioni.append("l.autore LIKE %s")
            parametri.append(f"%{self.autore_filtrato}%")
        if self.titolo_filtrato:
            condizioni.append("l.titolo LIKE %s")
            parametri.append(f"%{self.titolo_filtrato}%")

        if condizioni:
            query += "WHERE " + " AND ".join(condizioni) + " "
        query += "ORDER BY l.titolo"

        cursor.execute(query, parametri)
        righe = cursor.fetchall()

        self.tabella.setRowCount(len(righe))
        trovato = False
        for numero, riga in enumerate(righe):
            for colonna, valore in enumerate(riga):
                self.tabella.setItem(numero, colonna, QTableWidgetItem(str(valore)))
            if riga[0] == self.id_selezionato:
                self.tabella.selectRow(numero)
                trovato = True

        if trovato:
            self.mostra_scheda()
        else:
            self.id_selezionato = None
            self.scheda.svuota()

    def filtra_autore(self):
        self.autore_filtrato = self.campo_autore.text().strip()
        self.aggiorna()

    def filtra_titolo(self):
        self.titolo_filtrato = self.campo_titolo.text().strip()
        self.aggiorna()

    def reset_filtri(self):
        self.setFocus()
        self.campo_autore.azzera()
        self.campo_titolo.azzera()
        self.autore_filtrato = ""
        self.titolo_filtrato = ""
        self.id_selezionato = None
        self.tabella.clearSelection()
        self.aggiorna()

    def riga_selezionata(self):
        selezione = self.tabella.selectedItems()
        if not selezione:
            return

        self.id_selezionato = int(self.tabella.item(selezione[0].row(), 0).text())
        self.mostra_scheda()

    def mostra_scheda(self):
        cursor.execute(
            "SELECT l.titolo, l.autore, l.isbn, c.nome, l.prezzo, m.copie "
            "FROM libri l "
            "JOIN magazzino m ON l.id_libro = m.id_libro "
            "LEFT JOIN categorie c ON l.id_categoria = c.id_categoria "
            "WHERE l.id_libro = %s",
            (self.id_selezionato,)
        )
        titolo, autore, isbn, categoria, prezzo, copie = cursor.fetchone()
        disponibile = copie > 0

        self.scheda.mostra(titolo, [
            ("Autore", autore),
            ("ISBN", isbn or "-"),
            ("Categoria", categoria or "-"),
            ("Prezzo", f"{prezzo:.2f} €"),
            ("Copie in magazzino", str(copie)),
            ("Valore a magazzino", f"{prezzo * copie:.2f} €"),
            ("Stato", "Disponibile" if disponibile else "Esaurito",
             COLORE_OK if disponibile else COLORE_KO),
        ])

    def controlla_selezione(self):
        if self.id_selezionato is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona prima un libro dalla tabella.")
            return False
        return True

    def copie_attuali(self):
        cursor.execute(
            "SELECT copie FROM magazzino WHERE id_libro = %s",
            (self.id_selezionato,)
        )
        return cursor.fetchone()[0]

    def aggiungi_copie(self):
        if not self.controlla_selezione():
            return

        quantita = self.campo_quantita.value()
        if quantita == 0:
            QMessageBox.warning(self, "Attenzione", "Inserisci una quantità maggiore di zero.")
            return

        cursor.execute(
            "UPDATE magazzino SET copie = copie + %s WHERE id_libro = %s",
            (quantita, self.id_selezionato)
        )
        db.commit()
        self.aggiorna()

    def rimuovi_copie(self):
        if not self.controlla_selezione():
            return

        quantita = self.campo_quantita.value()
        if quantita == 0:
            QMessageBox.warning(self, "Attenzione", "Inserisci una quantità maggiore di zero.")
            return

        disponibili = self.copie_attuali()
        if quantita > disponibili:
            QMessageBox.warning(
                self, "Attenzione",
                f"Copie insufficienti: ne sono disponibili {disponibili}."
            )
            return

        cursor.execute(
            "UPDATE magazzino SET copie = copie - %s WHERE id_libro = %s",
            (quantita, self.id_selezionato)
        )
        db.commit()
        self.aggiorna()


# ==================================================
# CONTATTI
# ==================================================

class TabContatti(QWidget):
    def __init__(self):
        super().__init__()
        self.id_selezionato = None
        self.testo_cercato = ""
        self.setFocusPolicy(Qt.ClickFocus)

        self.campo_ricerca = CampoConSuggerimento("Cerca persona")
        self.campo_ricerca.returnPressed.connect(self.cerca)
        bottone_cerca = QPushButton("Cerca")
        bottone_cerca.setFixedWidth(120)
        bottone_cerca.clicked.connect(self.cerca)

        bottone_reset = QPushButton("Reset")
        bottone_reset.setFixedWidth(120)
        bottone_reset.clicked.connect(self.reset_ricerca)

        self.campo_nome = QLineEdit()
        self.campo_cognome = QLineEdit()
        self.campo_indirizzo = QLineEdit()
        self.campo_citta = QLineEdit()
        self.campo_cap = QLineEdit()
        self.campo_cap.setMaxLength(10)
        self.campo_telefono = QLineEdit()
        self.campo_email = QLineEdit()
        self.campi = (
            self.campo_nome, self.campo_cognome, self.campo_indirizzo,
            self.campo_citta, self.campo_cap, self.campo_telefono, self.campo_email
        )

        form = QFormLayout()
        form.addRow("Nome", self.campo_nome)
        form.addRow("Cognome", self.campo_cognome)
        form.addRow("Indirizzo", self.campo_indirizzo)
        form.addRow("Città", self.campo_citta)
        form.addRow("CAP", self.campo_cap)
        form.addRow("Telefono", self.campo_telefono)
        form.addRow("Email", self.campo_email)

        bottone_modifica = QPushButton("Modifica")
        bottone_modifica.clicked.connect(self.modifica_contatto)
        bottone_elimina = QPushButton("Elimina")
        bottone_elimina.clicked.connect(self.elimina_contatto)
        self.bottone_pulisci = QPushButton("Pulisci modulo")
        self.bottone_pulisci.clicked.connect(self.pulisci_modulo)
        self.bottone_annulla = QPushButton("Annulla selezione")
        self.bottone_annulla.clicked.connect(self.svuota_modulo)

        riga_ricerca = QHBoxLayout()
        riga_ricerca.addWidget(self.campo_ricerca)
        riga_ricerca.addWidget(bottone_cerca)

        riga_reset = QHBoxLayout()
        riga_reset.addStretch()
        riga_reset.addWidget(bottone_reset)

        colonna_ricerca = QVBoxLayout()
        colonna_ricerca.addLayout(riga_ricerca)
        colonna_ricerca.addSpacing(8)
        colonna_ricerca.addLayout(riga_reset)

        colonna_dati = QVBoxLayout()
        colonna_dati.addLayout(form)
        colonna_dati.addSpacing(4)
        colonna_dati.addWidget(bottone_modifica)
        colonna_dati.addWidget(bottone_elimina)
        colonna_dati.addWidget(self.bottone_pulisci)
        colonna_dati.addWidget(self.bottone_annulla)

        colonna_sinistra = QVBoxLayout()
        colonna_sinistra.addWidget(
            Pannello("Ricerca", da_layout(colonna_ricerca), espandi=False, compatto=True)
        )
        colonna_sinistra.addSpacing(12)
        colonna_sinistra.addWidget(
            Pannello("Dati contatto", da_layout(colonna_dati), espandi=False, compatto=True)
        )
        colonna_sinistra.addStretch()

        contenitore_sinistra = da_layout(colonna_sinistra)
        contenitore_sinistra.setFixedWidth(LARGHEZZA_COLONNA)
        contenitore_sinistra.setFocusPolicy(Qt.ClickFocus)

        self.tabella = TabellaDati(
            ["ID", "Nome", "Cognome", "Indirizzo", "Città", "CAP", "Telefono", "Email"]
        )
        for colonna in (0, 5):
            self.tabella.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )
        self.tabella.itemSelectionChanged.connect(self.riga_selezionata)

        self.scheda = SchedaInfo("Nessun contatto selezionato", colonne=2, altezza_minima=ALTEZZA_SCHEDA)

        colonna_destra = QVBoxLayout()
        colonna_destra.addWidget(Pannello("Rubrica contatti", self.tabella), 1)
        colonna_destra.addWidget(self.scheda)

        layout = QHBoxLayout()
        layout.addWidget(contenitore_sinistra)
        layout.addLayout(colonna_destra)
        self.setLayout(layout)

        self.aggiorna()
        self.aggiorna_pulsanti()

    def aggiorna_pulsanti(self):
        selezionato = self.id_selezionato is not None
        self.bottone_pulisci.setEnabled(not selezionato)
        self.bottone_annulla.setEnabled(selezionato)
        self.bottone_annulla.setStyleSheet(STILE_ANNULLA if selezionato else "")

    def aggiorna(self):
        db.commit()

        query = (
            "SELECT id_utente, nome, cognome, indirizzo, citta, cap, telefono, email "
            "FROM utenti "
        )
        parametri = []

        if self.testo_cercato:
            query += (
                "WHERE (CONCAT(nome, ' ', cognome) LIKE %s "
                "OR CONCAT(cognome, ' ', nome) LIKE %s "
                "OR telefono LIKE %s OR email LIKE %s) "
            )
            parametri.extend([f"%{self.testo_cercato}%"] * 4)
        query += "ORDER BY cognome, nome"

        cursor.execute(query, parametri)
        righe = cursor.fetchall()

        self.tabella.setRowCount(len(righe))
        trovato = False
        for numero, riga in enumerate(righe):
            for colonna, valore in enumerate(riga):
                testo = "" if valore is None else str(valore)
                self.tabella.setItem(numero, colonna, QTableWidgetItem(testo))
            if riga[0] == self.id_selezionato:
                self.tabella.selectRow(numero)
                trovato = True

        if trovato:
            self.mostra_scheda()
        elif self.id_selezionato is not None:
            self.svuota_modulo()

    def cerca(self):
        self.testo_cercato = self.campo_ricerca.text().strip()
        self.aggiorna()

    def azzera_ricerca(self):
        self.campo_ricerca.azzera()
        self.testo_cercato = ""

    def reset_ricerca(self):
        self.svuota_modulo()
        self.azzera_ricerca()
        self.aggiorna()

    def riga_selezionata(self):
        selezione = self.tabella.selectedItems()
        if not selezione:
            return

        self.id_selezionato = int(self.tabella.item(selezione[0].row(), 0).text())
        cursor.execute(
            "SELECT nome, cognome, indirizzo, citta, cap, telefono, email "
            "FROM utenti WHERE id_utente = %s",
            (self.id_selezionato,)
        )
        for campo, valore in zip(self.campi, cursor.fetchone()):
            campo.setText(valore or "")
        self.aggiorna_pulsanti()
        self.mostra_scheda()

    def mostra_scheda(self):
        cursor.execute(
            "SELECT nome, cognome, indirizzo, citta, cap, telefono, email "
            "FROM utenti WHERE id_utente = %s",
            (self.id_selezionato,)
        )
        nome, cognome, indirizzo, citta, cap, telefono, email = cursor.fetchone()

        cursor.execute(
            "SELECT COUNT(DISTINCT v.id_vendita), "
            "COALESCE(SUM(d.quantita * d.prezzo_unitario), 0), MAX(v.data_vendita) "
            "FROM vendite v LEFT JOIN vendite_dettagli d ON v.id_vendita = d.id_vendita "
            "WHERE v.id_utente = %s",
            (self.id_selezionato,)
        )
        acquisti, totale, ultimo = cursor.fetchone()
        ultimo = ultimo.strftime("%d/%m/%Y") if ultimo else "-"

        self.scheda.mostra(f"{nome} {cognome}", [
            ("Indirizzo", indirizzo or "-"),
            ("Città", citta or "-"),
            ("CAP", cap or "-"),
            ("Telefono", telefono),
            ("Email", email),
            ("Acquisti effettuati", str(acquisti)),
            ("Totale speso", f"{totale:.2f} €"),
            ("Ultimo acquisto", ultimo),
        ])

    def leggi_modulo(self):
        nome = self.campo_nome.text().strip()
        cognome = self.campo_cognome.text().strip()
        indirizzo = self.campo_indirizzo.text().strip() or None
        citta = self.campo_citta.text().strip() or None
        cap = self.campo_cap.text().strip() or None
        telefono = self.campo_telefono.text().strip()
        email = self.campo_email.text().strip()

        if not nome or not cognome or not telefono or not email:
            QMessageBox.warning(
                self, "Attenzione",
                "Nome, cognome, telefono ed email sono obbligatori."
            )
            return None
        if not all(c.isdigit() or c in "+- " for c in telefono):
            QMessageBox.warning(self, "Attenzione", "Il telefono può contenere solo cifre, spazi, + e -.")
            return None
        if "@" not in email or "." not in email:
            QMessageBox.warning(self, "Attenzione", "L'indirizzo email non è valido.")
            return None
        return nome, cognome, indirizzo, citta, cap, telefono, email

    def modifica_contatto(self):
        if self.id_selezionato is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona prima un contatto dalla tabella.")
            return

        dati = self.leggi_modulo()
        if dati is None:
            return

        if not conferma(self, "Modifica", "Vuoi salvare le modifiche al contatto selezionato?"):
            return

        try:
            cursor.execute(
                "UPDATE utenti SET nome = %s, cognome = %s, indirizzo = %s, citta = %s, "
                "cap = %s, telefono = %s, email = %s WHERE id_utente = %s",
                dati + (self.id_selezionato,)
            )
            db.commit()
        except mysql.connector.Error as errore:
            db.rollback()
            QMessageBox.critical(self, "Errore", f"Impossibile modificare il contatto.\n{errore}")
            return

        self.svuota_modulo()
        self.aggiorna()

    def elimina_contatto(self):
        if self.id_selezionato is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona prima un contatto dalla tabella.")
            return

        nominativo = f"{self.campo_nome.text().strip()} {self.campo_cognome.text().strip()}"
        if not conferma(self, "Elimina", f'Vuoi eliminare definitivamente il contatto "{nominativo}"?'):
            return

        try:
            cursor.execute("DELETE FROM utenti WHERE id_utente = %s", (self.id_selezionato,))
            db.commit()
        except mysql.connector.Error:
            db.rollback()
            QMessageBox.critical(
                self, "Errore",
                "Il contatto non può essere eliminato perché ha acquisti registrati."
            )
            return

        self.svuota_modulo()
        self.aggiorna()

    def modulo_compilato(self):
        return any(campo.text().strip() for campo in self.campi)

    def pulisci_modulo(self):
        if self.modulo_compilato() and conferma_pulizia(self):
            self.svuota_modulo()

    def svuota_modulo(self):
        self.setFocus()
        self.id_selezionato = None
        for campo in self.campi:
            campo.clear()
        self.tabella.clearSelection()
        self.scheda.svuota()
        self.aggiorna_pulsanti()


# ==================================================
# CERCA LIBRI
# ==================================================

class TabCercaLibri(QWidget):
    def __init__(self):
        super().__init__()
        self.id_selezionato = None
        self.testo_cercato = ""
        self.setFocusPolicy(Qt.ClickFocus)

        self.campo_ricerca = CampoConSuggerimento("Titolo, autore o ISBN")
        self.campo_ricerca.returnPressed.connect(self.cerca)
        bottone_cerca = QPushButton("Cerca")
        bottone_cerca.setFixedWidth(120)
        bottone_cerca.clicked.connect(self.cerca)

        bottone_reset = QPushButton("Reset")
        bottone_reset.setFixedWidth(120)
        bottone_reset.clicked.connect(self.reset_ricerca)

        self.filtro_disponibili = QCheckBox("Mostra solo libri disponibili")
        self.filtro_disponibili.stateChanged.connect(lambda: self.aggiorna())

        self.scheda = SchedaInfo("Nessun libro selezionato")

        riga_ricerca = QHBoxLayout()
        riga_ricerca.addWidget(self.campo_ricerca)
        riga_ricerca.addWidget(bottone_cerca)

        riga_reset = QHBoxLayout()
        riga_reset.addStretch()
        riga_reset.addWidget(bottone_reset)

        colonna_ricerca = QVBoxLayout()
        colonna_ricerca.addLayout(riga_ricerca)
        colonna_ricerca.addSpacing(8)
        colonna_ricerca.addLayout(riga_reset)
        colonna_ricerca.addSpacing(10)
        colonna_ricerca.addWidget(self.filtro_disponibili)

        colonna_sinistra = QVBoxLayout()
        colonna_sinistra.addWidget(
            Pannello("Ricerca libri", da_layout(colonna_ricerca), espandi=False, compatto=True)
        )
        colonna_sinistra.addSpacing(14)
        colonna_sinistra.addWidget(self.scheda)
        colonna_sinistra.addStretch()

        contenitore_sinistra = da_layout(colonna_sinistra)
        contenitore_sinistra.setFixedWidth(LARGHEZZA_COLONNA)
        contenitore_sinistra.setFocusPolicy(Qt.ClickFocus)

        self.tabella = TabellaDati(
            ["ID", "Titolo", "Autore", "ISBN", "Categoria", "Prezzo", "Copie", "Disponibilità"]
        )
        for colonna in (0, 5, 6, 7):
            self.tabella.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )
        self.tabella.itemSelectionChanged.connect(self.riga_selezionata)

        layout = QHBoxLayout()
        layout.addWidget(contenitore_sinistra)
        layout.addWidget(Pannello("Risultati", self.tabella), 1)
        self.setLayout(layout)

        self.aggiorna()

    def aggiorna(self):
        db.commit()

        query = (
            "SELECT l.id_libro, l.titolo, l.autore, l.isbn, c.nome, l.prezzo, m.copie "
            "FROM libri l "
            "JOIN magazzino m ON l.id_libro = m.id_libro "
            "LEFT JOIN categorie c ON l.id_categoria = c.id_categoria "
        )
        condizioni = []
        parametri = []

        if self.testo_cercato:
            condizioni.append("(l.titolo LIKE %s OR l.autore LIKE %s OR l.isbn LIKE %s)")
            parametri.extend([f"%{self.testo_cercato}%"] * 3)
        if self.filtro_disponibili.isChecked():
            condizioni.append("m.copie > 0")

        if condizioni:
            query += "WHERE " + " AND ".join(condizioni) + " "
        query += "ORDER BY l.titolo"

        cursor.execute(query, parametri)
        righe = cursor.fetchall()

        self.tabella.setRowCount(len(righe))
        trovato = False
        for numero, riga in enumerate(righe):
            for colonna, valore in enumerate(riga):
                if colonna == 5:
                    testo = f"{valore:.2f} €"
                else:
                    testo = "" if valore is None else str(valore)
                self.tabella.setItem(numero, colonna, QTableWidgetItem(testo))

            disponibile = riga[6] > 0
            voce = QTableWidgetItem("Disponibile" if disponibile else "Esaurito")
            voce.setForeground(QColor(COLORE_OK if disponibile else COLORE_KO))
            carattere = self.tabella.font()
            carattere.setBold(True)
            voce.setFont(carattere)
            self.tabella.setItem(numero, 7, voce)

            if riga[0] == self.id_selezionato:
                self.tabella.selectRow(numero)
                trovato = True

        if not trovato:
            self.id_selezionato = None
            self.scheda.svuota("Nessun libro selezionato" if righe else "Nessun libro trovato")

    def cerca(self):
        self.testo_cercato = self.campo_ricerca.text().strip()
        self.aggiorna()

    def reset_ricerca(self):
        self.setFocus()
        self.campo_ricerca.azzera()
        self.testo_cercato = ""
        self.id_selezionato = None
        self.tabella.clearSelection()
        self.aggiorna()

    def riga_selezionata(self):
        selezione = self.tabella.selectedItems()
        if not selezione:
            return

        riga = selezione[0].row()
        self.id_selezionato = int(self.tabella.item(riga, 0).text())

        titolo = self.tabella.item(riga, 1).text()
        autore = self.tabella.item(riga, 2).text()
        isbn = self.tabella.item(riga, 3).text() or "-"
        categoria = self.tabella.item(riga, 4).text() or "-"
        prezzo = self.tabella.item(riga, 5).text()
        copie = self.tabella.item(riga, 6).text()
        stato = self.tabella.item(riga, 7).text()
        colore_stato = COLORE_OK if stato == "Disponibile" else COLORE_KO

        self.scheda.mostra(titolo, [
            ("Autore", autore),
            ("ISBN", isbn),
            ("Categoria", categoria),
            ("Prezzo", prezzo),
            ("Copie in magazzino", copie),
            ("Stato", stato, colore_stato),
        ])


# ==================================================
# CERCA PERSONE
# ==================================================

class TabCercaPersone(QWidget):
    def __init__(self):
        super().__init__()
        self.id_selezionato = None
        self.testo_cercato = ""
        self.setFocusPolicy(Qt.ClickFocus)

        self.campo_ricerca = CampoConSuggerimento("Cerca persona")
        self.campo_ricerca.returnPressed.connect(self.cerca)
        bottone_cerca = QPushButton("Cerca")
        bottone_cerca.setFixedWidth(120)
        bottone_cerca.clicked.connect(self.cerca)

        bottone_reset = QPushButton("Reset")
        bottone_reset.setFixedWidth(120)
        bottone_reset.clicked.connect(self.reset_ricerca)

        self.filtro_acquisti = QCheckBox("Mostra solo clienti con acquisti")
        self.filtro_acquisti.stateChanged.connect(lambda: self.aggiorna())

        self.scheda = SchedaInfo("Nessun cliente selezionato")

        riga_ricerca = QHBoxLayout()
        riga_ricerca.addWidget(self.campo_ricerca)
        riga_ricerca.addWidget(bottone_cerca)

        riga_reset = QHBoxLayout()
        riga_reset.addStretch()
        riga_reset.addWidget(bottone_reset)

        colonna_ricerca = QVBoxLayout()
        colonna_ricerca.addLayout(riga_ricerca)
        colonna_ricerca.addSpacing(8)
        colonna_ricerca.addLayout(riga_reset)
        colonna_ricerca.addSpacing(10)
        colonna_ricerca.addWidget(self.filtro_acquisti)

        colonna_sinistra = QVBoxLayout()
        colonna_sinistra.addWidget(
            Pannello("Ricerca clienti", da_layout(colonna_ricerca), espandi=False, compatto=True)
        )
        colonna_sinistra.addSpacing(14)
        colonna_sinistra.addWidget(self.scheda)
        colonna_sinistra.addStretch()

        contenitore_sinistra = da_layout(colonna_sinistra)
        contenitore_sinistra.setFixedWidth(LARGHEZZA_COLONNA)
        contenitore_sinistra.setFocusPolicy(Qt.ClickFocus)

        self.tabella = TabellaDati(
            ["ID", "Nome", "Cognome", "Telefono", "Email", "Acquisti", "Totale speso"]
        )
        for colonna in (0, 3, 5, 6):
            self.tabella.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )
        self.tabella.itemSelectionChanged.connect(self.riga_selezionata)

        self.tabella_storico = TabellaDati(
            ["Data", "Vendita", "Libro", "Autore", "Quantità", "Prezzo", "Totale"]
        )
        self.tabella_storico.setSelectionMode(QAbstractItemView.NoSelection)
        for colonna in (0, 1, 4, 5, 6):
            self.tabella_storico.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )

        pannello_storico = Pannello("Storico acquisti", self.tabella_storico)
        self.etichetta_storico = pannello_storico.etichetta_titolo

        colonna_destra = QVBoxLayout()
        colonna_destra.addWidget(Pannello("Clienti", self.tabella), 1)
        colonna_destra.addWidget(pannello_storico, 1)

        layout = QHBoxLayout()
        layout.addWidget(contenitore_sinistra)
        layout.addLayout(colonna_destra)
        self.setLayout(layout)

        self.aggiorna()

    def aggiorna(self):
        db.commit()

        query = (
            "SELECT u.id_utente, u.nome, u.cognome, u.telefono, u.email, "
            "COUNT(DISTINCT v.id_vendita), "
            "COALESCE(SUM(d.quantita * d.prezzo_unitario), 0) "
            "FROM utenti u "
            "LEFT JOIN vendite v ON u.id_utente = v.id_utente "
            "LEFT JOIN vendite_dettagli d ON v.id_vendita = d.id_vendita "
        )
        parametri = []

        if self.testo_cercato:
            query += (
                "WHERE (CONCAT(u.nome, ' ', u.cognome) LIKE %s "
                "OR CONCAT(u.cognome, ' ', u.nome) LIKE %s "
                "OR u.telefono LIKE %s OR u.email LIKE %s) "
            )
            parametri.extend([f"%{self.testo_cercato}%"] * 4)

        query += "GROUP BY u.id_utente, u.nome, u.cognome, u.telefono, u.email "
        if self.filtro_acquisti.isChecked():
            query += "HAVING COUNT(DISTINCT v.id_vendita) > 0 "
        query += "ORDER BY u.cognome, u.nome"

        cursor.execute(query, parametri)
        righe = cursor.fetchall()

        self.tabella.setRowCount(len(righe))
        trovato = False
        for numero, riga in enumerate(righe):
            for colonna, valore in enumerate(riga):
                if colonna == 6:
                    testo = f"{valore:.2f} €"
                else:
                    testo = str(valore)
                self.tabella.setItem(numero, colonna, QTableWidgetItem(testo))
            if riga[0] == self.id_selezionato:
                self.tabella.selectRow(numero)
                trovato = True

        if trovato:
            self.mostra_dettaglio()
        else:
            self.id_selezionato = None
            self.svuota_dettaglio()

    def cerca(self):
        self.testo_cercato = self.campo_ricerca.text().strip()
        self.aggiorna()

    def reset_ricerca(self):
        self.setFocus()
        self.campo_ricerca.azzera()
        self.testo_cercato = ""
        self.id_selezionato = None
        self.tabella.clearSelection()
        self.aggiorna()

    def riga_selezionata(self):
        selezione = self.tabella.selectedItems()
        if not selezione:
            return

        self.id_selezionato = int(self.tabella.item(selezione[0].row(), 0).text())
        self.mostra_dettaglio()

    def svuota_dettaglio(self):
        self.scheda.svuota()
        self.etichetta_storico.setText("Storico acquisti")
        self.tabella_storico.setRowCount(0)

    def mostra_dettaglio(self):
        cursor.execute(
            "SELECT nome, cognome, indirizzo, citta, cap, telefono, email "
            "FROM utenti WHERE id_utente = %s",
            (self.id_selezionato,)
        )
        nome, cognome, indirizzo, citta, cap, telefono, email = cursor.fetchone()

        cursor.execute(
            "SELECT v.data_vendita, v.id_vendita, l.titolo, l.autore, "
            "d.quantita, d.prezzo_unitario "
            "FROM vendite v "
            "JOIN vendite_dettagli d ON v.id_vendita = d.id_vendita "
            "JOIN libri l ON d.id_libro = l.id_libro "
            "WHERE v.id_utente = %s "
            "ORDER BY v.data_vendita DESC, v.id_vendita DESC, l.titolo",
            (self.id_selezionato,)
        )
        acquisti = cursor.fetchall()

        vendite = []
        for riga in acquisti:
            if riga[1] not in vendite:
                vendite.append(riga[1])
        numero_vendite = len(vendite)
        totale = sum(riga[4] * riga[5] for riga in acquisti)
        ultimo = acquisti[0][0].strftime("%d/%m/%Y") if acquisti else "-"

        self.scheda.mostra(f"{nome} {cognome}", [
            ("Telefono", telefono),
            ("Email", email),
            ("Indirizzo", indirizzo or "-"),
            ("Città", citta or "-"),
            ("CAP", cap or "-"),
            ("Acquisti effettuati", str(numero_vendite)),
            ("Totale speso", f"{totale:.2f} €"),
            ("Ultimo acquisto", ultimo),
        ])

        if acquisti:
            self.etichetta_storico.setText(f"Storico acquisti di {nome} {cognome}")
        else:
            self.etichetta_storico.setText(
                f"Storico acquisti di {nome} {cognome}: nessun acquisto registrato"
            )

        self.tabella_storico.setRowCount(len(acquisti))
        for numero, (data, vendita, titolo, autore, quantita, prezzo) in enumerate(acquisti):
            valori = (
                data.strftime("%d/%m/%Y %H:%M"), str(vendita), titolo, autore,
                str(quantita), f"{prezzo:.2f} €", f"{quantita * prezzo:.2f} €"
            )
            for colonna, testo in enumerate(valori):
                self.tabella_storico.setItem(numero, colonna, QTableWidgetItem(testo))


# ==================================================
# ACQUISTI
# ==================================================

CARRELLO = {}
CLIENTE_ACQUISTO = {"id": None}


class ErroreAcquisto(Exception):
    pass


class NuovoClienteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuovo cliente")
        self.setFixedWidth(340)
        self.id_creato = None

        self.campo_nome = QLineEdit()
        self.campo_cognome = QLineEdit()
        self.campo_telefono = QLineEdit()
        self.campo_email = QLineEdit()
        self.campo_indirizzo = QLineEdit()
        self.campo_citta = QLineEdit()
        self.campo_cap = QLineEdit()
        self.campo_cap.setMaxLength(10)

        form = QFormLayout()
        form.addRow("Nome *", self.campo_nome)
        form.addRow("Cognome *", self.campo_cognome)
        form.addRow("Telefono *", self.campo_telefono)
        form.addRow("Email *", self.campo_email)
        form.addRow("Indirizzo", self.campo_indirizzo)
        form.addRow("Città", self.campo_citta)
        form.addRow("CAP", self.campo_cap)

        bottone_salva = QPushButton("Salva e seleziona")
        bottone_salva.clicked.connect(self.salva)
        bottone_annulla = QPushButton("Annulla")
        bottone_annulla.clicked.connect(self.reject)

        riga_pulsanti = QHBoxLayout()
        riga_pulsanti.addStretch()
        riga_pulsanti.addWidget(bottone_annulla)
        riga_pulsanti.addWidget(bottone_salva)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("I campi contrassegnati con * sono obbligatori."))
        layout.addSpacing(8)
        layout.addLayout(form)
        layout.addSpacing(12)
        layout.addLayout(riga_pulsanti)
        self.setLayout(layout)

    def salva(self):
        nome = self.campo_nome.text().strip()
        cognome = self.campo_cognome.text().strip()
        telefono = self.campo_telefono.text().strip()
        email = self.campo_email.text().strip()
        indirizzo = self.campo_indirizzo.text().strip() or None
        citta = self.campo_citta.text().strip() or None
        cap = self.campo_cap.text().strip() or None

        if not nome or not cognome or not telefono or not email:
            QMessageBox.warning(
                self, "Attenzione",
                "Nome, cognome, telefono ed email sono obbligatori."
            )
            return
        if not all(c.isdigit() or c in "+- " for c in telefono):
            QMessageBox.warning(self, "Attenzione", "Il telefono può contenere solo cifre, spazi, + e -.")
            return
        if "@" not in email or "." not in email:
            QMessageBox.warning(self, "Attenzione", "L'indirizzo email non è valido.")
            return

        try:
            cursor.execute(
                "INSERT INTO utenti (nome, cognome, indirizzo, citta, cap, telefono, email) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (nome, cognome, indirizzo, citta, cap, telefono, email)
            )
            self.id_creato = cursor.lastrowid
            db.commit()
        except mysql.connector.Error as errore:
            db.rollback()
            QMessageBox.critical(self, "Errore", f"Impossibile salvare il cliente.\n{errore}")
            return

        self.accept()


class TabAcquisti(QWidget):
    def __init__(self):
        super().__init__()
        self.carrello = CARRELLO
        self.totale_carrello = 0
        self.libro_corrente = None
        self.testo_cliente = ""
        self.testo_libro = ""
        self.setFocusPolicy(Qt.ClickFocus)

        self.campo_ricerca_cliente = CampoConSuggerimento("Cerca cliente")
        self.campo_ricerca_cliente.returnPressed.connect(self.cerca_cliente)
        self.bottone_cerca_cliente = QPushButton("Cerca")
        self.bottone_cerca_cliente.setFixedWidth(120)
        self.bottone_cerca_cliente.clicked.connect(self.cerca_cliente)

        self.bottone_nuovo = QPushButton("Nuovo cliente")
        self.bottone_nuovo.clicked.connect(self.nuovo_cliente)
        self.bottone_reset_cliente = QPushButton("Reset")
        self.bottone_reset_cliente.setFixedWidth(120)
        self.bottone_reset_cliente.clicked.connect(self.reset_cliente)

        self.etichetta_blocco = QLabel(
            "Acquisto in corso con questo cliente. "
            "Per sceglierne un altro, conferma o annulla l'acquisto."
        )
        self.etichetta_blocco.setWordWrap(True)
        self.etichetta_blocco.setVisible(False)

        self.filtro_acquirenti = QCheckBox("Solo acquirenti del libro selezionato")
        self.filtro_acquirenti.setEnabled(False)
        self.filtro_acquirenti.stateChanged.connect(lambda: self.carica_clienti())

        self.lista_clienti = QListWidget()
        self.lista_clienti.setMinimumHeight(200)
        self.lista_clienti.setWordWrap(True)
        self.lista_clienti.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.lista_clienti.itemSelectionChanged.connect(self.cliente_selezionato)

        self.bottone_annulla_cliente = QPushButton("Annulla selezione")
        self.bottone_annulla_cliente.clicked.connect(self.annulla_cliente)

        self.scheda_cliente = SchedaInfo("Nessun cliente selezionato")
        self.scheda_libro = SchedaInfo("Nessun libro selezionato")

        riga_ricerca_cliente = QHBoxLayout()
        riga_ricerca_cliente.addWidget(self.campo_ricerca_cliente)
        riga_ricerca_cliente.addWidget(self.bottone_cerca_cliente)

        riga_nuovo_reset = QHBoxLayout()
        riga_nuovo_reset.addWidget(self.bottone_nuovo)
        riga_nuovo_reset.addWidget(self.bottone_reset_cliente)

        colonna_cliente = QVBoxLayout()
        colonna_cliente.addLayout(riga_ricerca_cliente)
        colonna_cliente.addSpacing(8)
        colonna_cliente.addLayout(riga_nuovo_reset)
        colonna_cliente.addSpacing(8)
        colonna_cliente.addWidget(self.etichetta_blocco)
        colonna_cliente.addWidget(self.filtro_acquirenti)
        colonna_cliente.addSpacing(6)
        colonna_cliente.addWidget(self.lista_clienti)
        colonna_cliente.addSpacing(8)
        colonna_cliente.addWidget(self.bottone_annulla_cliente)

        colonna_sinistra = QVBoxLayout()
        colonna_sinistra.addWidget(
            Pannello("Cliente", da_layout(colonna_cliente), espandi=False, compatto=True)
        )
        colonna_sinistra.addSpacing(12)
        colonna_sinistra.addWidget(self.scheda_cliente)
        colonna_sinistra.addSpacing(12)
        colonna_sinistra.addWidget(self.scheda_libro)
        colonna_sinistra.addStretch()

        contenitore_sinistra = da_layout(colonna_sinistra)

        area_sinistra = QScrollArea()
        area_sinistra.setWidget(contenitore_sinistra)
        area_sinistra.setWidgetResizable(True)
        area_sinistra.setFrameShape(QFrame.NoFrame)
        area_sinistra.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        area_sinistra.setFixedWidth(LARGHEZZA_COLONNA_SCORRIMENTO)

        self.campo_ricerca_libro = CampoConSuggerimento("Cerca libro per titolo, autore o ISBN")
        self.campo_ricerca_libro.returnPressed.connect(self.cerca_libro)
        bottone_cerca_libro = QPushButton("Cerca")
        bottone_cerca_libro.setFixedWidth(120)
        bottone_cerca_libro.clicked.connect(self.cerca_libro)
        bottone_reset_libro = QPushButton("Reset")
        bottone_reset_libro.setFixedWidth(120)
        bottone_reset_libro.clicked.connect(self.reset_libro)

        self.tabella_libri = TabellaDati(["ID", "Titolo", "Autore", "Prezzo", "Copie"])
        self.tabella_libri.setSelectionMode(QAbstractItemView.MultiSelection)
        for colonna in (0, 3, 4):
            self.tabella_libri.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )
        self.tabella_libri.itemSelectionChanged.connect(self.libri_selezionati_cambiati)

        self.campo_quantita = QSpinBox()
        self.campo_quantita.setRange(1, 999)
        self.campo_quantita.setValue(1)
        bottone_aggiungi = QPushButton("Aggiungi al carrello")
        bottone_aggiungi.clicked.connect(self.aggiungi_al_carrello)
        bottone_aggiungi.setStyleSheet(
            f"QPushButton {{ background-color: {COLORI['azione_blu']}; color: #ffffff; "
            f"border: 1px solid {COLORI['azione_blu']}; border-radius: 4px; "
            f"padding: 5px 14px; font-weight: bold; }}"
            f"QPushButton:hover {{ background-color: {COLORI['azione_blu_hover']}; "
            f"border: 1px solid {COLORI['azione_blu_hover']}; }}"
        )
        self.bottone_annulla_libri = QPushButton("Annulla selezione")
        self.bottone_annulla_libri.clicked.connect(self.annulla_libri)
        self.etichetta_selezionati = QLabel("Libri selezionati: 0")

        self.tabella_carrello = TabellaDati(["ID", "Titolo", "Quantità", "Prezzo", "Totale"])
        self.tabella_carrello.chiave_base = "carrello_riga"
        self.tabella_carrello.chiave_selezione = "carrello_selezionata"
        self.tabella_carrello.setSelectionMode(QAbstractItemView.MultiSelection)
        for colonna in (0, 2, 3, 4):
            self.tabella_carrello.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )

        bottone_rimuovi = QPushButton("Rimuovi selezionati")
        bottone_rimuovi.clicked.connect(self.rimuovi_dal_carrello)
        bottone_svuota = QPushButton("Svuota carrello")
        bottone_svuota.clicked.connect(self.svuota_carrello)

        self.etichetta_totale = QLabel("Totale: 0.00 €")
        self.etichetta_totale.setStyleSheet("font-size: 19px; font-weight: bold;")

        bottone_conferma = QPushButton("Conferma acquisto")
        bottone_conferma.clicked.connect(self.conferma_acquisto)
        bottone_conferma.setStyleSheet(
            f"QPushButton {{ background-color: {COLORI['spunta_attiva']}; color: #ffffff; "
            f"border: 1px solid {COLORI['spunta_attiva']}; border-radius: 4px; "
            f"padding: 5px 16px; font-weight: bold; }}"
            f"QPushButton:hover {{ background-color: {COLORI['tab_hover_bg']}; "
            f"color: {COLORI['tab_hover_testo']}; }}"
        )

        riga_libri = QHBoxLayout()
        riga_libri.addWidget(self.campo_ricerca_libro)
        riga_libri.addWidget(bottone_cerca_libro)
        riga_libri.addWidget(bottone_reset_libro)

        riga_aggiunta = QHBoxLayout()
        riga_aggiunta.addWidget(QLabel("Quantità"))
        riga_aggiunta.addWidget(self.campo_quantita)
        riga_aggiunta.addWidget(bottone_aggiungi)
        riga_aggiunta.addWidget(self.bottone_annulla_libri)
        riga_aggiunta.addSpacing(8)
        riga_aggiunta.addWidget(self.etichetta_selezionati)
        riga_aggiunta.addStretch()

        riga_conferma = QHBoxLayout()
        riga_conferma.addWidget(bottone_rimuovi)
        riga_conferma.addWidget(bottone_svuota)
        riga_conferma.addStretch()
        riga_conferma.addWidget(self.etichetta_totale)
        riga_conferma.addSpacing(12)
        riga_conferma.addWidget(bottone_conferma)

        contenuto_catalogo = QVBoxLayout()
        contenuto_catalogo.addLayout(riga_libri)
        contenuto_catalogo.addWidget(self.tabella_libri, 1)
        contenuto_catalogo.addLayout(riga_aggiunta)

        contenuto_carrello = QVBoxLayout()
        contenuto_carrello.addWidget(self.tabella_carrello, 1)
        contenuto_carrello.addLayout(riga_conferma)

        colonna_destra = QVBoxLayout()
        colonna_destra.addWidget(Pannello("Catalogo libri", da_layout(contenuto_catalogo)), 3)
        colonna_destra.addWidget(Pannello("Carrello", da_layout(contenuto_carrello)), 2)

        layout = QHBoxLayout()
        layout.addWidget(area_sinistra)
        layout.addLayout(colonna_destra)
        self.setLayout(layout)

        self.aggiorna()

    @property
    def id_cliente(self):
        return CLIENTE_ACQUISTO["id"]

    @id_cliente.setter
    def id_cliente(self, valore):
        CLIENTE_ACQUISTO["id"] = valore

    def aggiorna_pulsanti(self):
        cliente = self.id_cliente is not None
        self.bottone_annulla_cliente.setEnabled(cliente)
        self.bottone_annulla_cliente.setStyleSheet(STILE_ANNULLA if cliente else "")

        libri = len(self.ids_libri_selezionati())
        self.bottone_annulla_libri.setEnabled(libri > 0)
        self.bottone_annulla_libri.setStyleSheet(STILE_ANNULLA if libri > 0 else "")
        self.etichetta_selezionati.setText(f"Libri selezionati: {libri}")

    def aggiorna_blocco(self):
        libero = self.id_cliente is None
        self.campo_ricerca_cliente.setEnabled(libero)
        self.bottone_cerca_cliente.setEnabled(libero)
        self.bottone_nuovo.setEnabled(libero)
        self.bottone_reset_cliente.setEnabled(libero)
        self.filtro_acquirenti.setEnabled(libero and self.libro_corrente is not None)
        self.etichetta_blocco.setVisible(not libero)

    def aggiorna(self):
        db.commit()
        self.carica_clienti()
        self.carica_catalogo()
        self.ridisegna_carrello()
        if self.id_cliente is not None:
            self.mostra_scheda_cliente()
        self.aggiorna_blocco()
        self.aggiorna_pulsanti()

    def carica_clienti(self):
        query = (
            "SELECT u.id_utente, u.cognome, u.nome, u.telefono, u.email, "
            "u.indirizzo, u.citta, u.cap FROM utenti u "
        )
        condizioni = []
        parametri = []

        if self.id_cliente is not None:
            condizioni.append("u.id_utente = %s")
            parametri.append(self.id_cliente)
        else:
            if self.testo_cliente:
                condizioni.append(
                    "(CONCAT(u.nome, ' ', u.cognome) LIKE %s "
                    "OR CONCAT(u.cognome, ' ', u.nome) LIKE %s "
                    "OR u.telefono LIKE %s OR u.email LIKE %s)"
                )
                parametri.extend([f"%{self.testo_cliente}%"] * 4)

            if self.filtro_acquirenti.isChecked() and self.libro_corrente is not None:
                condizioni.append(
                    "u.id_utente IN (SELECT v.id_utente FROM vendite v "
                    "JOIN vendite_dettagli d ON v.id_vendita = d.id_vendita "
                    "WHERE d.id_libro = %s)"
                )
                parametri.append(self.libro_corrente)

        if condizioni:
            query += "WHERE " + " AND ".join(condizioni) + " "
        query += "ORDER BY u.cognome, u.nome"

        cursor.execute(query, parametri)
        clienti = cursor.fetchall()

        self.lista_clienti.blockSignals(True)
        self.lista_clienti.clear()
        for id_utente, cognome, nome, telefono, email, indirizzo, citta, cap in clienti:
            righe = [f"{cognome} {nome}", f"Tel. {telefono}  ·  {email}"]
            zona = " ".join(parte for parte in (cap, citta) if parte)
            indirizzo_completo = ", ".join(parte for parte in (indirizzo, zona) if parte)
            if indirizzo_completo:
                righe.append(indirizzo_completo)

            voce = QListWidgetItem("\n".join(righe))
            voce.setData(Qt.UserRole, id_utente)
            self.lista_clienti.addItem(voce)
            if id_utente == self.id_cliente:
                self.lista_clienti.setCurrentItem(voce)
        self.lista_clienti.blockSignals(False)

    def cerca_cliente(self):
        self.testo_cliente = self.campo_ricerca_cliente.text().strip()
        self.carica_clienti()

    def reset_cliente(self):
        self.setFocus()
        self.campo_ricerca_cliente.azzera()
        self.testo_cliente = ""

        self.filtro_acquirenti.blockSignals(True)
        self.filtro_acquirenti.setChecked(False)
        self.filtro_acquirenti.blockSignals(False)

        self.scheda_cliente.svuota()
        self.carica_clienti()
        self.aggiorna_pulsanti()

    def nascondi_altri_clienti(self):
        for indice in range(self.lista_clienti.count()):
            voce = self.lista_clienti.item(indice)
            voce.setHidden(voce.data(Qt.UserRole) != self.id_cliente)

    def cliente_selezionato(self):
        selezione = self.lista_clienti.selectedItems()
        if not selezione:
            return

        id_scelto = selezione[0].data(Qt.UserRole)
        if self.id_cliente is not None and id_scelto != self.id_cliente:
            return

        self.id_cliente = id_scelto
        self.filtro_acquirenti.blockSignals(True)
        self.filtro_acquirenti.setChecked(False)
        self.filtro_acquirenti.blockSignals(False)

        self.nascondi_altri_clienti()
        self.mostra_scheda_cliente()
        self.aggiorna_blocco()
        self.aggiorna_pulsanti()

    def sblocca_cliente(self):
        self.setFocus()
        self.id_cliente = None
        self.lista_clienti.clearSelection()
        self.scheda_cliente.svuota()
        self.carica_clienti()
        self.aggiorna_blocco()
        self.aggiorna_pulsanti()

    def annulla_cliente(self):
        if self.carrello:
            if not conferma(
                    self, "Annulla selezione",
                    "Annullando la selezione del cliente verrà annullato anche "
                    "l'acquisto in corso e il carrello sarà svuotato.\n\n"
                    "Vuoi continuare?"
            ):
                return
            self.carrello.clear()
            self.ridisegna_carrello()

        self.sblocca_cliente()

    def mostra_scheda_cliente(self):
        cursor.execute(
            "SELECT nome, cognome, telefono, email FROM utenti WHERE id_utente = %s",
            (self.id_cliente,)
        )
        riga = cursor.fetchone()
        if riga is None:
            self.sblocca_cliente()
            return
        nome, cognome, telefono, email = riga

        cursor.execute(
            "SELECT COUNT(DISTINCT v.id_vendita), "
            "COALESCE(SUM(d.quantita * d.prezzo_unitario), 0) "
            "FROM vendite v LEFT JOIN vendite_dettagli d ON v.id_vendita = d.id_vendita "
            "WHERE v.id_utente = %s",
            (self.id_cliente,)
        )
        acquisti, totale = cursor.fetchone()

        self.scheda_cliente.mostra(f"{nome} {cognome}", [
            ("Telefono", telefono),
            ("Email", email),
            ("Acquisti effettuati", str(acquisti)),
            ("Totale speso", f"{totale:.2f} €"),
        ])

    def nome_cliente(self):
        cursor.execute(
            "SELECT nome, cognome FROM utenti WHERE id_utente = %s", (self.id_cliente,)
        )
        riga = cursor.fetchone()
        return f"{riga[0]} {riga[1]}" if riga else ""

    def nuovo_cliente(self):
        dialogo = NuovoClienteDialog(self)
        if dialogo.exec() != QDialog.Accepted:
            return

        self.campo_ricerca_cliente.azzera()
        self.testo_cliente = ""
        self.filtro_acquirenti.blockSignals(True)
        self.filtro_acquirenti.setChecked(False)
        self.filtro_acquirenti.blockSignals(False)

        self.id_cliente = dialogo.id_creato
        self.carica_clienti()
        self.mostra_scheda_cliente()
        self.aggiorna_blocco()
        self.aggiorna_pulsanti()

    def carica_catalogo(self):
        query = (
            "SELECT l.id_libro, l.titolo, l.autore, l.prezzo, m.copie "
            "FROM libri l JOIN magazzino m ON l.id_libro = m.id_libro "
            "WHERE m.copie > 0 "
        )
        parametri = []
        if self.testo_libro:
            query += "AND (l.titolo LIKE %s OR l.autore LIKE %s OR l.isbn LIKE %s) "
            parametri.extend([f"%{self.testo_libro}%"] * 3)
        query += "ORDER BY l.titolo"

        cursor.execute(query, parametri)
        righe = cursor.fetchall()

        self.tabella_libri.clearSelection()
        self.tabella_libri.setRowCount(len(righe))
        for numero, riga in enumerate(righe):
            for colonna, valore in enumerate(riga):
                if colonna == 3:
                    testo = f"{valore:.2f} €"
                else:
                    testo = str(valore)
                self.tabella_libri.setItem(numero, colonna, QTableWidgetItem(testo))

    def cerca_libro(self):
        self.testo_libro = self.campo_ricerca_libro.text().strip()
        self.carica_catalogo()

    def reset_libro(self):
        self.setFocus()
        self.campo_ricerca_libro.azzera()
        self.testo_libro = ""
        self.campo_quantita.setValue(1)
        self.carica_catalogo()

    def ids_libri_selezionati(self):
        righe = []
        for voce in self.tabella_libri.selectedItems():
            if voce.row() not in righe:
                righe.append(voce.row())
        righe.sort()
        return [int(self.tabella_libri.item(riga, 0).text()) for riga in righe]

    def libri_selezionati_cambiati(self):
        ids = self.ids_libri_selezionati()

        if not ids:
            self.libro_corrente = None
        else:
            self.libro_corrente = ids[-1]
            riga = self.tabella_libri.currentRow()
            if riga >= 0:
                id_riga = int(self.tabella_libri.item(riga, 0).text())
                if id_riga in ids:
                    self.libro_corrente = id_riga

        self.aggiorna_pulsanti()
        self.aggiorna_blocco()

        if self.libro_corrente is None:
            self.scheda_libro.svuota()
            if self.filtro_acquirenti.isChecked():
                self.filtro_acquirenti.setChecked(False)
        else:
            self.mostra_scheda_libro()
            if self.filtro_acquirenti.isChecked():
                self.carica_clienti()

    def mostra_scheda_libro(self):
        cursor.execute(
            "SELECT l.titolo, l.autore, c.nome, l.prezzo, m.copie, "
            "COALESCE(SUM(d.quantita), 0), COUNT(DISTINCT v.id_utente), "
            "COALESCE(SUM(d.quantita * d.prezzo_unitario), 0) "
            "FROM libri l "
            "JOIN magazzino m ON l.id_libro = m.id_libro "
            "LEFT JOIN categorie c ON l.id_categoria = c.id_categoria "
            "LEFT JOIN vendite_dettagli d ON l.id_libro = d.id_libro "
            "LEFT JOIN vendite v ON d.id_vendita = v.id_vendita "
            "WHERE l.id_libro = %s "
            "GROUP BY l.id_libro, l.titolo, l.autore, c.nome, l.prezzo, m.copie",
            (self.libro_corrente,)
        )
        riga = cursor.fetchone()
        if riga is None:
            self.scheda_libro.svuota()
            return

        titolo, autore, categoria, prezzo, copie, vendute, clienti, incasso = riga
        self.scheda_libro.mostra(titolo, [
            ("Autore", autore),
            ("Categoria", categoria or "-"),
            ("Prezzo", f"{prezzo:.2f} €"),
            ("Copie disponibili", str(copie)),
            ("Copie vendute", str(vendute)),
            ("Clienti acquirenti", str(clienti)),
            ("Incasso generato", f"{incasso:.2f} €"),
        ])

    def annulla_libri(self):
        self.setFocus()
        self.tabella_libri.clearSelection()

    def aggiungi_al_carrello(self):
        ids = self.ids_libri_selezionati()
        if not ids:
            QMessageBox.warning(self, "Attenzione", "Seleziona almeno un libro dal catalogo.")
            return

        quantita = self.campo_quantita.value()
        problemi = []
        for id_libro in ids:
            cursor.execute(
                "SELECT l.titolo, m.copie FROM libri l "
                "JOIN magazzino m ON l.id_libro = m.id_libro WHERE l.id_libro = %s",
                (id_libro,)
            )
            riga = cursor.fetchone()
            if riga is None:
                problemi.append("un libro selezionato non è più disponibile")
                continue

            titolo, disponibili = riga
            nel_carrello = self.carrello.get(id_libro, 0)
            if nel_carrello + quantita > disponibili:
                problemi.append(
                    f'"{titolo}": disponibili {disponibili}, già nel carrello {nel_carrello}'
                )

        if problemi:
            QMessageBox.warning(
                self, "Copie insufficienti",
                "Non è stato aggiunto nulla al carrello:\n\n" + "\n".join(problemi)
            )
            return

        for id_libro in ids:
            self.carrello[id_libro] = self.carrello.get(id_libro, 0) + quantita

        self.campo_quantita.setValue(1)
        self.tabella_libri.clearSelection()
        self.ridisegna_carrello()

    def ridisegna_carrello(self):
        righe = []
        if self.carrello:
            segnaposti = ", ".join(["%s"] * len(self.carrello))
            cursor.execute(
                f"SELECT id_libro, titolo, prezzo FROM libri "
                f"WHERE id_libro IN ({segnaposti}) ORDER BY titolo",
                list(self.carrello.keys())
            )
            righe = cursor.fetchall()

        trovati = [riga[0] for riga in righe]
        for id_libro in list(self.carrello.keys()):
            if id_libro not in trovati:
                del self.carrello[id_libro]

        totale = 0
        self.tabella_carrello.clearSelection()
        self.tabella_carrello.setRowCount(len(righe))
        for numero, (id_libro, titolo, prezzo) in enumerate(righe):
            quantita = self.carrello[id_libro]
            totale_riga = prezzo * quantita
            totale += totale_riga

            valori = (
                str(id_libro), titolo, str(quantita),
                f"{prezzo:.2f} €", f"{totale_riga:.2f} €"
            )
            for colonna, testo in enumerate(valori):
                self.tabella_carrello.setItem(numero, colonna, QTableWidgetItem(testo))

        self.totale_carrello = totale
        self.etichetta_totale.setText(f"Totale: {totale:.2f} €")

    def rimuovi_dal_carrello(self):
        righe = []
        for voce in self.tabella_carrello.selectedItems():
            if voce.row() not in righe:
                righe.append(voce.row())

        if not righe:
            QMessageBox.warning(
                self, "Attenzione", "Seleziona almeno una riga del carrello."
            )
            return

        if len(righe) == 1:
            destinatari = "il libro selezionato"
        else:
            destinatari = f"i {len(righe)} libri selezionati"

        if not conferma(
                self, "Rimuovi dal carrello", f"Vuoi rimuovere {destinatari} dal carrello?"
        ):
            return

        for riga in righe:
            id_libro = int(self.tabella_carrello.item(riga, 0).text())
            if id_libro in self.carrello:
                del self.carrello[id_libro]

        self.ridisegna_carrello()

    def svuota_carrello(self):
        if not self.carrello:
            QMessageBox.warning(self, "Attenzione", "Il carrello è già vuoto.")
            return

        if conferma(self, "Svuota carrello", "Vuoi rimuovere tutti i libri dal carrello?"):
            self.carrello.clear()
            self.ridisegna_carrello()

    def conferma_acquisto(self):
        if self.id_cliente is None:
            QMessageBox.warning(self, "Attenzione", "Seleziona il cliente che effettua l'acquisto.")
            return
        if not self.carrello:
            QMessageBox.warning(self, "Attenzione", "Il carrello è vuoto.")
            return

        nome_cliente = self.nome_cliente()
        copie = sum(self.carrello.values())
        titoli = len(self.carrello)
        messaggio = (
            f"Vuoi registrare l'acquisto di {copie} "
            f"{'copia' if copie == 1 else 'copie'} "
            f"({titoli} {'titolo' if titoli == 1 else 'titoli'}) "
            f"per un totale di {self.totale_carrello:.2f} € "
            f"a nome di {nome_cliente}?"
        )
        if not conferma(self, "Conferma acquisto", messaggio):
            return

        try:
            cursor.execute(
                "INSERT INTO vendite (id_utente, id_operatore) VALUES (%s, %s)",
                (self.id_cliente, operatore_corrente[0])
            )
            id_vendita = cursor.lastrowid

            totale = 0
            for id_libro, quantita in self.carrello.items():
                cursor.execute(
                    "SELECT l.titolo, l.prezzo, m.copie "
                    "FROM libri l JOIN magazzino m ON l.id_libro = m.id_libro "
                    "WHERE l.id_libro = %s FOR UPDATE",
                    (id_libro,)
                )
                riga = cursor.fetchone()
                if riga is None:
                    raise ErroreAcquisto("Un libro nel carrello non è più disponibile.")

                titolo, prezzo, disponibili = riga
                if quantita > disponibili:
                    raise ErroreAcquisto(
                        f'Copie insufficienti per "{titolo}": disponibili {disponibili}.'
                    )

                cursor.execute(
                    "INSERT INTO vendite_dettagli "
                    "(id_vendita, id_libro, quantita, prezzo_unitario) "
                    "VALUES (%s, %s, %s, %s)",
                    (id_vendita, id_libro, quantita, prezzo)
                )
                cursor.execute(
                    "UPDATE magazzino SET copie = copie - %s WHERE id_libro = %s",
                    (quantita, id_libro)
                )
                totale += prezzo * quantita

            db.commit()
        except ErroreAcquisto as errore:
            db.rollback()
            QMessageBox.warning(self, "Acquisto non registrato", str(errore))
            self.aggiorna()
            return
        except mysql.connector.Error as errore:
            db.rollback()
            QMessageBox.critical(
                self, "Errore", f"Impossibile registrare l'acquisto.\n{errore}"
            )
            return

        self.carrello.clear()
        self.campo_quantita.setValue(1)
        QMessageBox.information(
            self, "Acquisto registrato",
            f"Vendita n. {id_vendita} registrata a nome di {nome_cliente}.\n"
            f"Totale: {totale:.2f} €"
        )
        self.sblocca_cliente()
        self.aggiorna()


# ==================================================
# STORICO VENDITE
# ==================================================

class TabStoricoVendite(QWidget):
    def __init__(self):
        super().__init__()
        self.id_selezionato = None
        self.testo_cercato = ""
        self.setFocusPolicy(Qt.ClickFocus)

        self.campo_ricerca = CampoConSuggerimento("Cerca vendita")
        self.campo_ricerca.setToolTip("Cerca per cliente, operatore o numero vendita")
        self.campo_ricerca.returnPressed.connect(self.cerca)
        bottone_cerca = QPushButton("Cerca")
        bottone_cerca.setFixedWidth(120)
        bottone_cerca.clicked.connect(self.cerca)

        bottone_reset = QPushButton("Reset")
        bottone_reset.setFixedWidth(120)
        bottone_reset.clicked.connect(self.reset_ricerca)

        self.filtro_periodo = QCheckBox("Filtra per periodo")
        self.filtro_periodo.stateChanged.connect(self.periodo_cambiato)

        oggi = QDate.currentDate()
        self.data_dal = QDateEdit(QDate(oggi.year(), oggi.month(), 1))
        self.data_al = QDateEdit(oggi)
        for campo in (self.data_dal, self.data_al):
            campo.setCalendarPopup(True)
            campo.setDisplayFormat("dd/MM/yyyy")
            campo.setEnabled(False)
            campo.dateChanged.connect(lambda: self.aggiorna())

        form_periodo = QFormLayout()
        form_periodo.addRow("Dal", self.data_dal)
        form_periodo.addRow("Al", self.data_al)

        self.etichetta_riepilogo = QLabel("Vendite: 0  |  Incasso: 0.00 €")
        carattere = self.etichetta_riepilogo.font()
        carattere.setBold(True)
        self.etichetta_riepilogo.setFont(carattere)

        self.scheda = SchedaInfo("Nessuna vendita selezionata")

        riga_ricerca = QHBoxLayout()
        riga_ricerca.addWidget(self.campo_ricerca)
        riga_ricerca.addWidget(bottone_cerca)

        riga_periodo = QHBoxLayout()
        riga_periodo.addWidget(self.filtro_periodo)
        riga_periodo.addStretch()
        riga_periodo.addWidget(bottone_reset)

        colonna_ricerca = QVBoxLayout()
        colonna_ricerca.addLayout(riga_ricerca)
        colonna_ricerca.addSpacing(8)
        colonna_ricerca.addLayout(riga_periodo)
        colonna_ricerca.addSpacing(6)
        colonna_ricerca.addLayout(form_periodo)
        colonna_ricerca.addSpacing(10)
        colonna_ricerca.addWidget(self.etichetta_riepilogo)

        colonna_sinistra = QVBoxLayout()
        colonna_sinistra.addWidget(
            Pannello("Ricerca vendite", da_layout(colonna_ricerca), espandi=False, compatto=True)
        )
        colonna_sinistra.addSpacing(14)
        colonna_sinistra.addWidget(self.scheda)
        colonna_sinistra.addStretch()

        contenitore_sinistra = da_layout(colonna_sinistra)
        contenitore_sinistra.setFixedWidth(LARGHEZZA_COLONNA)
        contenitore_sinistra.setFocusPolicy(Qt.ClickFocus)

        self.tabella = TabellaDati(
            ["N°", "Data", "Cliente", "Operatore", "Copie", "Totale"]
        )
        for colonna in (0, 1, 4, 5):
            self.tabella.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )
        self.tabella.itemSelectionChanged.connect(self.riga_selezionata)

        self.tabella_dettaglio = TabellaDati(
            ["Libro", "Autore", "Quantità", "Prezzo", "Totale"]
        )
        self.tabella_dettaglio.setSelectionMode(QAbstractItemView.NoSelection)
        for colonna in (2, 3, 4):
            self.tabella_dettaglio.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )

        pannello_dettaglio = Pannello("Dettaglio vendita", self.tabella_dettaglio)
        self.etichetta_dettaglio = pannello_dettaglio.etichetta_titolo

        colonna_destra = QVBoxLayout()
        colonna_destra.addWidget(Pannello("Vendite registrate", self.tabella), 1)
        colonna_destra.addWidget(pannello_dettaglio, 1)

        layout = QHBoxLayout()
        layout.addWidget(contenitore_sinistra)
        layout.addLayout(colonna_destra)
        self.setLayout(layout)

        self.aggiorna()

    def periodo_cambiato(self):
        attivo = self.filtro_periodo.isChecked()
        self.data_dal.setEnabled(attivo)
        self.data_al.setEnabled(attivo)
        self.aggiorna()

    def aggiorna(self):
        db.commit()

        query = (
            "SELECT v.id_vendita, v.data_vendita, CONCAT(u.cognome, ' ', u.nome), "
            "o.nome, COALESCE(SUM(d.quantita), 0), "
            "COALESCE(SUM(d.quantita * d.prezzo_unitario), 0) "
            "FROM vendite v "
            "JOIN utenti u ON v.id_utente = u.id_utente "
            "LEFT JOIN operatori o ON v.id_operatore = o.id_operatore "
            "LEFT JOIN vendite_dettagli d ON v.id_vendita = d.id_vendita "
        )
        condizioni = []
        parametri = []

        if self.testo_cercato:
            condizioni.append(
                "(CONCAT(u.nome, ' ', u.cognome) LIKE %s "
                "OR CONCAT(u.cognome, ' ', u.nome) LIKE %s "
                "OR o.nome LIKE %s OR CAST(v.id_vendita AS CHAR) LIKE %s)"
            )
            parametri.extend([f"%{self.testo_cercato}%"] * 4)

        if self.filtro_periodo.isChecked():
            dal = self.data_dal.date().toPython()
            al = self.data_al.date().toPython()
            if dal > al:
                dal, al = al, dal
            condizioni.append(
                "(v.data_vendita >= %s AND v.data_vendita < DATE_ADD(%s, INTERVAL 1 DAY))"
            )
            parametri.extend([dal, al])

        if condizioni:
            query += "WHERE " + " AND ".join(condizioni) + " "
        query += (
            "GROUP BY v.id_vendita, v.data_vendita, u.cognome, u.nome, o.nome "
            "ORDER BY v.data_vendita DESC, v.id_vendita DESC"
        )

        cursor.execute(query, parametri)
        righe = cursor.fetchall()

        incasso = 0
        self.tabella.setRowCount(len(righe))
        trovato = False
        for numero, (id_vendita, data, cliente, operatore, copie, totale) in enumerate(righe):
            valori = (
                str(id_vendita), data.strftime("%d/%m/%Y %H:%M"), cliente,
                operatore or "-", str(copie), f"{totale:.2f} €"
            )
            for colonna, testo in enumerate(valori):
                self.tabella.setItem(numero, colonna, QTableWidgetItem(testo))

            incasso += totale
            if id_vendita == self.id_selezionato:
                self.tabella.selectRow(numero)
                trovato = True

        self.etichetta_riepilogo.setText(
            f"Vendite: {len(righe)}  |  Incasso: {incasso:.2f} €"
        )

        if trovato:
            self.mostra_dettaglio()
        else:
            self.id_selezionato = None
            self.svuota_dettaglio()

    def cerca(self):
        self.testo_cercato = self.campo_ricerca.text().strip()
        self.aggiorna()

    def reset_ricerca(self):
        self.setFocus()
        self.campo_ricerca.azzera()
        self.testo_cercato = ""
        self.id_selezionato = None
        self.tabella.clearSelection()

        oggi = QDate.currentDate()
        for campo, data in (
            (self.data_dal, QDate(oggi.year(), oggi.month(), 1)),
            (self.data_al, oggi),
        ):
            campo.blockSignals(True)
            campo.setDate(data)
            campo.blockSignals(False)

        self.filtro_periodo.blockSignals(True)
        self.filtro_periodo.setChecked(False)
        self.filtro_periodo.blockSignals(False)
        self.data_dal.setEnabled(False)
        self.data_al.setEnabled(False)

        self.aggiorna()

    def riga_selezionata(self):
        selezione = self.tabella.selectedItems()
        if not selezione:
            return

        self.id_selezionato = int(self.tabella.item(selezione[0].row(), 0).text())
        self.mostra_dettaglio()

    def svuota_dettaglio(self):
        self.scheda.svuota()
        self.etichetta_dettaglio.setText("Dettaglio vendita")
        self.tabella_dettaglio.setRowCount(0)

    def mostra_dettaglio(self):
        cursor.execute(
            "SELECT v.data_vendita, u.nome, u.cognome, u.telefono, u.email, o.nome "
            "FROM vendite v "
            "JOIN utenti u ON v.id_utente = u.id_utente "
            "LEFT JOIN operatori o ON v.id_operatore = o.id_operatore "
            "WHERE v.id_vendita = %s",
            (self.id_selezionato,)
        )
        data, nome, cognome, telefono, email, operatore = cursor.fetchone()

        cursor.execute(
            "SELECT l.titolo, l.autore, d.quantita, d.prezzo_unitario "
            "FROM vendite_dettagli d JOIN libri l ON d.id_libro = l.id_libro "
            "WHERE d.id_vendita = %s ORDER BY l.titolo",
            (self.id_selezionato,)
        )
        righe = cursor.fetchall()

        copie = sum(riga[2] for riga in righe)
        totale = sum(riga[2] * riga[3] for riga in righe)

        self.scheda.mostra(f"Vendita n. {self.id_selezionato}", [
            ("Data", data.strftime("%d/%m/%Y %H:%M")),
            ("Cliente", f"{nome} {cognome}"),
            ("Telefono", telefono),
            ("Email", email),
            ("Operatore", operatore or "-"),
            ("Libri acquistati", str(copie)),
            ("Totale", f"{totale:.2f} €"),
        ])

        self.etichetta_dettaglio.setText(f"Dettaglio della vendita n. {self.id_selezionato}")
        self.tabella_dettaglio.setRowCount(len(righe))
        for numero, (titolo, autore, quantita, prezzo) in enumerate(righe):
            valori = (
                titolo, autore, str(quantita),
                f"{prezzo:.2f} €", f"{quantita * prezzo:.2f} €"
            )
            for colonna, testo in enumerate(valori):
                self.tabella_dettaglio.setItem(numero, colonna, QTableWidgetItem(testo))


# ==================================================
# STATISTICHE
# ==================================================

MESI = [
    "Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
    "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"
]

COLORI_PODIO = ["#c9a227", "#9a9a9a", "#b06a2c"]


class GraficoBarre(QWidget):
    def __init__(self):
        super().__init__()
        self.dati = []
        self.evidenziata = None
        self.setMinimumHeight(150)

    def imposta_dati(self, dati, evidenziata=None):
        self.dati = dati
        self.evidenziata = evidenziata
        self.update()

    def paintEvent(self, evento):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        larghezza, altezza = self.width(), self.height()
        testo = QColor(COLORI["pannello_testo"])
        valori = [valore for _, valore in self.dati]
        if not valori or max(valori) <= 0:
            painter.setPen(testo)
            painter.drawText(
                QRectF(0, 0, larghezza, altezza), Qt.AlignCenter,
                "Nessuna vendita nel periodo"
            )
            return

        margine_x, margine_alto, margine_basso = 6, 24, 24
        area_larghezza = larghezza - 2 * margine_x
        area_altezza = altezza - margine_alto - margine_basso
        base = altezza - margine_basso
        massimo = max(valori)
        passo = area_larghezza / len(self.dati)
        larghezza_barra = min(passo * 0.6, 56)

        carattere = painter.font()
        carattere.setPointSize(9)
        painter.setFont(carattere)

        painter.setPen(QPen(QColor(COLORI["pannello_linea"]), 1))
        painter.drawLine(QPointF(margine_x, base), QPointF(larghezza - margine_x, base))

        for indice, (etichetta, valore) in enumerate(self.dati):
            centro = margine_x + passo * indice + passo / 2
            altezza_barra = valore / massimo * (area_altezza - 6)
            if indice == self.evidenziata:
                colore = COLORI["spunta_attiva"]
            else:
                colore = COLORI["azione_blu"]

            if altezza_barra > 0:
                painter.setPen(Qt.NoPen)
                painter.setBrush(QColor(colore))
                painter.drawRoundedRect(
                    QRectF(
                        centro - larghezza_barra / 2, base - altezza_barra,
                        larghezza_barra, altezza_barra
                    ),
                    3, 3
                )

            painter.setPen(testo)
            painter.drawText(
                QRectF(centro - passo / 2, base - altezza_barra - 20, passo, 16),
                Qt.AlignCenter, f"{valore:.0f}"
            )
            painter.drawText(
                QRectF(centro - passo / 2, base + 5, passo, 16),
                Qt.AlignCenter, etichetta
            )


class TabStatistiche(QWidget):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.ClickFocus)

        self.campo_anno = QComboBox()
        self.campo_mese = QComboBox()
        self.campo_mese.addItem("Tutti i mesi", None)
        for numero, nome in enumerate(MESI, start=1):
            self.campo_mese.addItem(nome, numero)
        self.campo_anno.currentIndexChanged.connect(lambda: self.aggiorna())
        self.campo_mese.currentIndexChanged.connect(lambda: self.aggiorna())

        bottone_reset = QPushButton("Reset")
        bottone_reset.setFixedWidth(120)
        bottone_reset.clicked.connect(self.reset_filtri)

        form = QFormLayout()
        form.addRow("Anno", self.campo_anno)
        form.addRow("Mese", self.campo_mese)

        riga_reset = QHBoxLayout()
        riga_reset.addStretch()
        riga_reset.addWidget(bottone_reset)

        contenuto_periodo = QWidget()
        layout_periodo = QVBoxLayout(contenuto_periodo)
        layout_periodo.setContentsMargins(0, 0, 0, 0)
        layout_periodo.addLayout(form)
        layout_periodo.addSpacing(6)
        layout_periodo.addLayout(riga_reset)
        pannello_periodo = Pannello("Periodo", contenuto_periodo, espandi=False)

        self.scheda = SchedaInfo("Nessuna vendita nel periodo")
        self.scheda.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        colonna_sinistra = QVBoxLayout()
        colonna_sinistra.addWidget(pannello_periodo)
        colonna_sinistra.addSpacing(14)
        colonna_sinistra.addWidget(self.scheda)
        colonna_sinistra.addStretch()

        contenitore_sinistra = QWidget()
        contenitore_sinistra.setLayout(colonna_sinistra)
        contenitore_sinistra.setFixedWidth(LARGHEZZA_COLONNA)
        contenitore_sinistra.setFocusPolicy(Qt.ClickFocus)

        self.grafico = GraficoBarre()
        self.pannello_grafico = Pannello("Incasso", self.grafico)

        self.tabella_libri = TabellaDati(["#", "Libro", "Autore", "Copie", "Incasso"])
        self.tabella_clienti = TabellaDati(["#", "Cliente", "Acquisti", "Copie", "Speso"])
        for colonna in (0, 3, 4):
            self.tabella_libri.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )
        for colonna in (0, 2, 3, 4):
            self.tabella_clienti.horizontalHeader().setSectionResizeMode(
                colonna, QHeaderView.ResizeToContents
            )
        for tabella in (self.tabella_libri, self.tabella_clienti):
            tabella.setSelectionMode(QAbstractItemView.NoSelection)

        pannello_libri = Pannello("Libri più venduti", self.tabella_libri)
        pannello_clienti = Pannello("Classifica clienti", self.tabella_clienti)

        riga_tabelle = QHBoxLayout()
        riga_tabelle.addWidget(pannello_libri)
        riga_tabelle.addWidget(pannello_clienti)

        colonna_destra = QVBoxLayout()
        colonna_destra.addWidget(self.pannello_grafico, 2)
        colonna_destra.addLayout(riga_tabelle, 3)

        layout = QHBoxLayout()
        layout.addWidget(contenitore_sinistra)
        layout.addLayout(colonna_destra)
        self.setLayout(layout)

        self.aggiorna()

    def carica_anni(self):
        corrente = self.campo_anno.currentData()

        cursor.execute("SELECT DISTINCT YEAR(data_vendita) FROM vendite ORDER BY 1 DESC")
        anni = [riga[0] for riga in cursor.fetchall()]

        self.campo_anno.blockSignals(True)
        self.campo_anno.clear()
        self.campo_anno.addItem("Tutti gli anni", None)
        for anno in anni:
            self.campo_anno.addItem(str(anno), anno)
        self.campo_anno.setCurrentIndex(max(self.campo_anno.findData(corrente), 0))
        self.campo_anno.blockSignals(False)

    def condizioni_periodo(self):
        condizioni = []
        parametri = []

        anno = self.campo_anno.currentData()
        mese = self.campo_mese.currentData()
        if anno is not None:
            condizioni.append("YEAR(v.data_vendita) = %s")
            parametri.append(anno)
        if mese is not None:
            condizioni.append("MONTH(v.data_vendita) = %s")
            parametri.append(mese)

        clausola = ""
        if condizioni:
            clausola = "WHERE " + " AND ".join(condizioni) + " "
        return clausola, parametri

    def descrizione_periodo(self):
        anno = self.campo_anno.currentData()
        mese = self.campo_mese.currentData()
        if anno is not None and mese is not None:
            return f"{MESI[mese - 1]} {anno}"
        if anno is not None:
            return str(anno)
        if mese is not None:
            return f"{MESI[mese - 1]} (tutti gli anni)"
        return "tutto il periodo"

    def riempi(self, tabella, righe):
        tabella.setRowCount(len(righe))
        for numero, riga in enumerate(righe):
            for colonna, testo in enumerate(riga):
                voce = QTableWidgetItem(testo)
                voce.setTextAlignment(Qt.AlignCenter)
                if colonna == 0:
                    carattere = tabella.font()
                    carattere.setBold(True)
                    voce.setFont(carattere)
                    if numero < len(COLORI_PODIO):
                        voce.setForeground(QColor(COLORI_PODIO[numero]))
                tabella.setItem(numero, colonna, voce)

    def aggiorna(self):
        db.commit()
        self.carica_anni()
        clausola, parametri = self.condizioni_periodo()

        cursor.execute(
            "SELECT COUNT(DISTINCT v.id_vendita), COALESCE(SUM(d.quantita), 0), "
            "COALESCE(SUM(d.quantita * d.prezzo_unitario), 0), "
            "COUNT(DISTINCT v.id_utente) "
            "FROM vendite v "
            "LEFT JOIN vendite_dettagli d ON v.id_vendita = d.id_vendita "
            + clausola,
            parametri
        )
        vendite, copie, incasso, clienti = cursor.fetchone()

        query_libri = (
            "SELECT l.titolo, l.autore, SUM(d.quantita), "
            "SUM(d.quantita * d.prezzo_unitario) "
            "FROM vendite_dettagli d "
            "JOIN vendite v ON d.id_vendita = v.id_vendita "
            "JOIN libri l ON d.id_libro = l.id_libro "
            + clausola +
            "GROUP BY l.id_libro, l.titolo, l.autore "
            "ORDER BY SUM(d.quantita) DESC, SUM(d.quantita * d.prezzo_unitario) DESC "
            "LIMIT 10"
        )
        cursor.execute(query_libri, parametri)
        libri = cursor.fetchall()

        query_clienti = (
            "SELECT CONCAT(u.cognome, ' ', u.nome), COUNT(DISTINCT v.id_vendita), "
            "SUM(d.quantita), SUM(d.quantita * d.prezzo_unitario) "
            "FROM vendite v "
            "JOIN utenti u ON v.id_utente = u.id_utente "
            "JOIN vendite_dettagli d ON v.id_vendita = d.id_vendita "
            + clausola +
            "GROUP BY u.id_utente, u.cognome, u.nome "
            "ORDER BY SUM(d.quantita * d.prezzo_unitario) DESC "
            "LIMIT 10"
        )
        cursor.execute(query_clienti, parametri)
        classifica = cursor.fetchall()

        self.riempi(self.tabella_libri, [
            (str(posizione), titolo, autore, str(int(venduti)), f"{ricavo:.2f} €")
            for posizione, (titolo, autore, venduti, ricavo) in enumerate(libri, start=1)
        ])
        self.riempi(self.tabella_clienti, [
            (str(posizione), cliente, str(acquisti), str(int(copie_cliente)), f"{speso:.2f} €")
            for posizione, (cliente, acquisti, copie_cliente, speso)
            in enumerate(classifica, start=1)
        ])

        if vendite == 0:
            self.scheda.svuota("Nessuna vendita nel periodo")
        else:
            self.scheda.mostra(f"Riepilogo: {self.descrizione_periodo()}", [
                ("Vendite registrate", str(vendite)),
                ("Copie vendute", str(int(copie))),
                ("Incasso totale", f"{incasso:.2f} €"),
                ("Scontrino medio", f"{incasso / vendite:.2f} €"),
                ("Clienti attivi", str(clienti)),
                ("Libro più venduto", libri[0][0] if libri else "-"),
                ("Cliente migliore", classifica[0][0] if classifica else "-"),
            ])

        titolo, dati, evidenziata = self.dati_grafico()
        self.pannello_grafico.imposta_titolo(titolo)
        self.grafico.imposta_dati(dati, evidenziata)

    def dati_grafico(self):
        anno = self.campo_anno.currentData()
        mese = self.campo_mese.currentData()

        if anno is not None:
            cursor.execute(
                "SELECT MONTH(v.data_vendita), SUM(d.quantita * d.prezzo_unitario) "
                "FROM vendite v JOIN vendite_dettagli d ON v.id_vendita = d.id_vendita "
                "WHERE YEAR(v.data_vendita) = %s GROUP BY MONTH(v.data_vendita)",
                (anno,)
            )
            per_mese = {}
            for numero_mese, totale in cursor.fetchall():
                per_mese[numero_mese] = float(totale)

            dati = [
                (MESI[indice][:3], per_mese.get(indice + 1, 0.0)) for indice in range(12)
            ]
            evidenziata = mese - 1 if mese is not None else None
            return f"Incasso per mese - {anno}", dati, evidenziata

        query = (
            "SELECT YEAR(v.data_vendita), SUM(d.quantita * d.prezzo_unitario) "
            "FROM vendite v JOIN vendite_dettagli d ON v.id_vendita = d.id_vendita "
        )
        parametri = []
        titolo = "Incasso per anno"
        if mese is not None:
            query += "WHERE MONTH(v.data_vendita) = %s "
            parametri.append(mese)
            titolo = f"Incasso per anno - {MESI[mese - 1]}"
        query += "GROUP BY YEAR(v.data_vendita) ORDER BY YEAR(v.data_vendita)"

        cursor.execute(query, parametri)
        dati = [(str(riga[0]), float(riga[1])) for riga in cursor.fetchall()]
        return titolo, dati, None

    def reset_filtri(self):
        self.setFocus()
        for campo in (self.campo_anno, self.campo_mese):
            campo.blockSignals(True)
            campo.setCurrentIndex(0)
            campo.blockSignals(False)
        self.aggiorna()


# ==================================================
# FINESTRA PRINCIPALE
# ==================================================

class FinestraPrincipale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionale Libreria")
        self.resize(1280, 820)
        self.setMinimumSize(1180, 720)
        self.logout_richiesto = False
        CARRELLO.clear()
        CLIENTE_ACQUISTO["id"] = None

        self.crea_pagine(0)
        self.crea_barra()
        self.statusBar().showMessage(f"Operatore: {operatore_corrente[1]}")

    def crea_pagine(self, indice):
        self.tab = QTabWidget()
        self.tab.addTab(TabLibri(), "Libri")
        self.tab.addTab(TabSenzaCategoria(), "Senza categoria")
        self.tab.addTab(TabMagazzino(), "Magazzino")
        self.tab.addTab(TabContatti(), "Contatti")
        self.tab.addTab(TabCercaLibri(), "Cerca libri")
        self.tab.addTab(TabCercaPersone(), "Cerca persone")
        self.tab.addTab(TabAcquisti(), "Acquisti")
        self.tab.addTab(TabStoricoVendite(), "Storico vendite")
        self.tab.addTab(TabStatistiche(), "Statistiche")
        self.tab.setCurrentIndex(indice)
        self.tab.currentChanged.connect(self.aggiorna_tab)
        self.setCentralWidget(self.tab)

    def aggiorna_tab(self, indice):
        pagina = self.tab.widget(indice)
        if hasattr(pagina, "aggiorna"):
            pagina.aggiorna()

    def crea_barra(self):
        self.azione_logout = QAction("Logout", self)
        self.azione_logout.setShortcut("Ctrl+L")
        self.azione_logout.setToolTip("Logout (Ctrl+L)")
        self.azione_logout.triggered.connect(self.logout)

        self.interruttore_tema = InterruttoreTema(TEMA_CORRENTE == "scuro")
        self.interruttore_tema.cambiato.connect(self.scegli_tema)

        azione_tema = QAction("Tema", self)
        azione_tema.setShortcut("Ctrl+T")
        azione_tema.triggered.connect(self.interruttore_tema.alterna)
        self.addAction(azione_tema)

        barra = self.addToolBar("Principale")
        barra.setMovable(False)
        barra.setFloatable(False)
        barra.setContextMenuPolicy(Qt.PreventContextMenu)
        barra.setIconSize(QSize(22, 22))
        barra.addAction(self.azione_logout)
        barra.addSeparator()
        barra.addWidget(self.interruttore_tema)

        pulsante_logout = barra.widgetForAction(self.azione_logout)
        pulsante_logout.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.aggiorna_icone()

    def aggiorna_icone(self):
        colore = COLORI["icone"]
        self.azione_logout.setIcon(crea_icona(disegna_logout, colore))

    def scegli_tema(self, nome):
        if nome == TEMA_CORRENTE:
            return

        indice = self.tab.currentIndex()
        imposta_tema(nome)
        salva_tema(nome)
        self.crea_pagine(indice)
        self.aggiorna_icone()

    def logout(self):
        if conferma(
            self, "Logout",
            "Vuoi uscire dall'account e tornare alla schermata di accesso?"
        ):
            self.logout_richiesto = True
            self.close()


# ==================================================
# AVVIO
# ==================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    carica_font_tabelle()
    app.setFont(crea_font_base())
    imposta_tema(leggi_tema_salvato())

    while True:
        login = LoginDialog()
        if login.exec() != QDialog.Accepted:
            break

        finestra = FinestraPrincipale()
        finestra.show()
        app.exec()

        if not finestra.logout_richiesto:
            break

    sys.exit(0)