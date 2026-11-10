import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = "Nessun filtro"
        self.genere_selezionato = "Nessun filtro"

    # POPOLA DROPDOWN
    # TODO
    def popola_dropdowns(self):
        """ Popola i menu a tendina di biblioteca e genere recuperando i dati dal modello. """
        # Popola Dropdown Biblioteche
        self._view.dd_biblioteca.options.append(ft.dropdown.Option("Nessun filtro"))
        biblioteche = self._model.get_biblioteche()
        for b in biblioteche:
            self._view.dd_biblioteca.options.append(ft.dropdown.Option(b.nome))
        self._view.dd_biblioteca.value = "Nessun filtro"

        # Popola Dropdown Generi
        self._view.dd_genere.options.append(ft.dropdown.Option("Nessun filtro"))
        generi = self._model.get_generi()
        for g in generi:
            self._view.dd_genere.options.append(ft.dropdown.Option(g))
        self._view.dd_genere.value = "Nessun filtro"

        self._view.update()

    # CALLBACKS DROPDOWN
    # TODO
    def leggi_biblioteca(self, e):
        """ Cattura la selezione della biblioteca. """
        if e.control.value is not None:
            self.biblioteca_selezionata = e.control.value

    def leggi_genere(self, e):
        """ Cattura la selezione del genere. """
        if e.control.value is not None:
            self.genere_selezionato = e.control.value

    # AZIONE: MOSTRA LIBRI
    # TODO
    def mostra_libri(self, e):
        """ Gestisce l'evento di click sul bottone 'Mostra Libri', filtrando e mostrando i risultati nella ListView. """
        biblioteca = self.biblioteca_selezionata
        genere = self.genere_selezionato

        # Recupera i libri filtrati dal model
        libri = self._model.get_libri_filtrati(biblioteca, genere)

        # Pulisce la lista visiva precedente
        self._view.lv_libri.controls.clear()

        # Se non ci sono risultati, mostra un alert a schermo[cite: 7]
        if not libri:
            self._view.show_alert("Nessun libro trovato con i criteri di filtraggio selezionati.")
        else:
            for libro in libri:
                self._view.lv_libri.controls.append(ft.Text(str(libro)))

        self._view.update()
