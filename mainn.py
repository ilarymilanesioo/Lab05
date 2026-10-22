import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    #AGGIUNTO DA ME
    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label="Tipo")
    input_marca = ft.TextField(label="Marca")
    input_anno = ft.TextField(label="Anno acquisto")
    valore_strumento = ft.TextField(value="0")

    #funzionamento del valore
    def decrementa_valore(e):
        valore=float(valore_strumento.value)
        if valore>=0:
           valore_strumento.value =valore - 10
           page.update()
    def incrementa_valore(e):
        valore = float(valore_strumento.value)
        valore_strumento.value = valore + 10
        page.update()

    btn_meno = ft.IconButton(icon=ft.Icons.REMOVE,on_click=decrementa_valore)
    btn_piu = ft.IconButton(icon=ft.Icons.ADD,on_click=incrementa_valore)
    # TODO

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    #AGGIUNTO DA ME
    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aggiungi_nuovo_strumento(e):
        try:
            tipo = input_tipo.value.strip()
            marca = input_marca.value.strip()
            if not tipo or not marca:
                alert.show_alert("Inserire un Tipo e una Marca validi.")
                return
            anno = int(input_anno.value)
            valore = float(valore_strumento.value)

            # Aggiunge lo strumento nel sistema
            deposito.aggiungi_strumento(tipo, marca, anno, valore)

            # Svuota i campi di testo e azzera il valore
            input_tipo.value = ""
            input_marca.value = ""
            input_anno.value = ""
            valore_strumento.value = "0"

            # Aggiorna la lista visibile a schermo
            aggiorna_lista_strumenti()

        except ValueError:
            alert.show_alert("L'anno di acquisto e il valore devono essere numeri validi.")
    # TODO

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    pulsante_aggiungi_strumento = ft.Button(
        "Aggiungi strumento",
        on_click=aggiungi_nuovo_strumento
    )
    # TODO

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(
            controls=[
                input_tipo,
                input_marca,
                input_anno,
                btn_piu,
                valore_strumento,
                btn_meno,
            ]
        ),
        pulsante_aggiungi_strumento,
        # TODO

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)