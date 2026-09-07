from __future__ import annotations

try:
    import customtkinter as ctk
    USE_CTK = True
except Exception:
    import tkinter as ctk
    USE_CTK = False

from tkinter import ttk, messagebox, filedialog
from datetime import date, timedelta
from viewmodel.main_vm import MainVM

BOOKING_BLUE = "#003b95"
BOOKING_DARK = "#00224f"
BOOKING_YELLOW = "#febb02"
BOOKING_LIGHT = "#f5f7fb"
BOOKING_WHITE = "#ffffff"

LANGUAGES = {
    "en": "English",
    "fr": "Français",
    "es": "Español",
}

TEXT = {
    "en": {
        "app_title": "HotelChain Booking",
        "hero_title": "Find the right room for your stay",
        "hero_subtitle": "Hotel chain management app with role-based access",
        "login": "Login",
        "signup": "Sign up",
        "logout": "Logout",
        "username": "Username",
        "password": "Password",
        "language": "Language",
        "guest_status": "Guest mode",
        "logged_as": "Logged in as",
        "role": "role",
        "tab_browse": "Rooms and reviews",
        "tab_client_review": "My reviews",
        "tab_rooms": "Rooms CRUD",
        "tab_reservations": "Reservations",
        "tab_clients": "Clients",
        "tab_statistics": "Statistics",
        "tab_users": "Users",
        "tab_notifications": "Notifications",
        "load_hotels": "Load hotels",
        "load_rooms": "Search rooms",
        "load_reviews": "Load reviews",
        "load_reservations": "Load reservations",
        "load_users": "Load users",
        "load_notifications": "Load notifications",
        "create": "Create",
        "update": "Update",
        "delete": "Delete",
        "clear": "Clear fields",
        "reserve": "Reserve room",
        "add_review": "Add review",
        "export_csv": "Export CSV",
        "export": "Export",
        "export_format": "Export format",
        "export_json": "Export JSON",
        "export_xml": "Export XML",
        "export_doc": "Export DOC",
        "notify": "Change credentials + notify",
        "show_statistics": "Show statistics",
        "show_chart": "Show chart",
        "filter_role": "Filter by role",
        "availability": "Availability",
        "room_type": "Room type",
        "average_price": "Average price / hotel",
        "reservation_status": "Reservation status",
        "select_row": "Select a row first.",
        "success": "Operation completed successfully.",
        "result": "Result",
        "error": "Error",
        "warning": "Warning",
        "login_failed": "Login failed. Check username and password.",
        "signup_success": "Account created. You are now logged in.",
        "username_required": "Username is required.",
        "password_required": "Password is required.",
        "username_exists": "This username already exists.",
        "only_guest": "You are logged out. Only guest operations are available.",
        "booking_design_note": "Public search remains visible only with guest/client/employee/manager permissions.",
        "hotel_id": "Hotel ID",
        "location": "Location",
        "available": "Available",
        "price_max": "Max price",
        "position": "Position",
        "facilities": "Facilities",
        "room_id": "Room ID",
        "client_id": "Client ID",
        "client_name": "Client name",
        "client_email": "Client email",
        "check_in": "Check-in",
        "check_out": "Check-out",
        "start_date": "Check-in",
        "end_date": "Check-out",
        "client_phone": "Client phone",
        "total_price": "Total price",
        "rating": "Rating",
        "comment": "Comment",
        "created_at": "Created at",
        "new_password": "New password",
        "choose_hotel": "Select hotel",
        "choose_room": "Select reserved room",
        "reserved_review_required": "You can add a review only for a room reserved by your account.",
        "no_room_selected": "Select a hotel and a room before adding the review.",
        "all": "All",
    },
    "fr": {
        "app_title": "HotelChain Booking",
        "hero_title": "Trouvez la chambre idéale pour votre séjour",
        "hero_subtitle": "Application de gestion hôtelière avec accès selon le rôle",
        "login": "Connexion",
        "signup": "Inscription",
        "logout": "Déconnexion",
        "username": "Utilisateur",
        "password": "Mot de passe",
        "language": "Langue",
        "guest_status": "Mode visiteur",
        "logged_as": "Connecté comme",
        "role": "rôle",
        "tab_browse": "Chambres et avis",
        "tab_client_review": "Mes avis",
        "tab_rooms": "CRUD chambres",
        "tab_reservations": "Réservations",
        "tab_clients": "Clients",
        "tab_statistics": "Statistiques",
        "tab_users": "Utilisateurs",
        "tab_notifications": "Notifications",
        "load_hotels": "Afficher hôtels",
        "load_rooms": "Rechercher chambres",
        "load_reviews": "Afficher avis",
        "load_reservations": "Afficher réservations",
        "load_users": "Afficher utilisateurs",
        "load_notifications": "Afficher notifications",
        "create": "Ajouter",
        "update": "Modifier",
        "delete": "Supprimer",
        "clear": "Vider champs",
        "reserve": "Réserver chambre",
        "add_review": "Ajouter avis",
        "export_csv": "Exporter CSV",
        "export": "Exporter",
        "export_format": "Format export",
        "export_json": "Exporter JSON",
        "export_xml": "Exporter XML",
        "export_doc": "Exporter DOC",
        "notify": "Modifier identifiants + notifier",
        "show_statistics": "Afficher statistiques",
        "show_chart": "Afficher graphique",
        "filter_role": "Filtrer par rôle",
        "availability": "Disponibilité",
        "room_type": "Type de chambre",
        "average_price": "Prix moyen / hôtel",
        "reservation_status": "Statut réservation",
        "select_row": "Sélectionnez d'abord une ligne.",
        "success": "Opération terminée avec succès.",
        "result": "Résultat",
        "error": "Erreur",
        "warning": "Attention",
        "login_failed": "Connexion échouée. Vérifiez l'utilisateur et le mot de passe.",
        "signup_success": "Compte créé. Vous êtes maintenant connecté.",
        "username_required": "Le nom d'utilisateur est obligatoire.",
        "password_required": "Le mot de passe est obligatoire.",
        "username_exists": "Ce nom d'utilisateur existe déjà.",
        "only_guest": "Vous êtes déconnecté. Seules les opérations visiteur sont disponibles.",
        "booking_design_note": "La recherche publique reste visible seulement avec les droits visiteur/client/employé/manager.",
        "hotel_id": "ID hôtel",
        "location": "Localisation",
        "available": "Disponible",
        "price_max": "Prix max.",
        "position": "Position",
        "facilities": "Équipements",
        "room_id": "ID chambre",
        "client_id": "ID client",
        "client_name": "Nom client",
        "client_email": "Email client",
        "check_in": "Check-in",
        "check_out": "Check-out",
        "start_date": "Check-in",
        "end_date": "Check-out",
        "client_phone": "Téléphone client",
        "total_price": "Prix total",
        "rating": "Note",
        "comment": "Avis",
        "created_at": "Créé le",
        "new_password": "Nouveau mot de passe",
        "choose_hotel": "Choisir l'hôtel",
        "choose_room": "Choisir la chambre réservée",
        "reserved_review_required": "Vous pouvez ajouter un avis uniquement pour une chambre réservée par votre compte.",
        "no_room_selected": "Choisissez un hôtel et une chambre avant d'ajouter l'avis.",
        "all": "Tous",
    },
    "es": {
        "app_title": "HotelChain Booking",
        "hero_title": "Encuentra la habitación adecuada para tu estancia",
        "hero_subtitle": "Aplicación de gestión hotelera con acceso según el rol",
        "login": "Iniciar sesión",
        "signup": "Registro",
        "logout": "Cerrar sesión",
        "username": "Usuario",
        "password": "Contraseña",
        "language": "Idioma",
        "guest_status": "Modo invitado",
        "logged_as": "Conectado como",
        "role": "rol",
        "tab_browse": "Habitaciones y reseñas",
        "tab_client_review": "Mis reseñas",
        "tab_rooms": "CRUD habitaciones",
        "tab_reservations": "Reservas",
        "tab_clients": "Clientes",
        "tab_statistics": "Estadísticas",
        "tab_users": "Usuarios",
        "tab_notifications": "Notificaciones",
        "load_hotels": "Cargar hoteles",
        "load_rooms": "Buscar habitaciones",
        "load_reviews": "Cargar reseñas",
        "load_reservations": "Cargar reservas",
        "load_users": "Cargar usuarios",
        "load_notifications": "Cargar notificaciones",
        "create": "Crear",
        "update": "Actualizar",
        "delete": "Eliminar",
        "clear": "Limpiar campos",
        "reserve": "Reservar habitación",
        "add_review": "Añadir reseña",
        "export_csv": "Exportar CSV",
        "export": "Exportar",
        "export_format": "Formato exportación",
        "export_json": "Exportar JSON",
        "export_xml": "Exportar XML",
        "export_doc": "Exportar DOC",
        "notify": "Cambiar credenciales + notificar",
        "show_statistics": "Mostrar estadísticas",
        "show_chart": "Mostrar gráfico",
        "filter_role": "Filtrar por rol",
        "availability": "Disponibilidad",
        "room_type": "Tipo de habitación",
        "average_price": "Precio medio / hotel",
        "reservation_status": "Estado reserva",
        "select_row": "Selecciona primero una fila.",
        "success": "Operación completada correctamente.",
        "result": "Resultado",
        "error": "Error",
        "warning": "Aviso",
        "login_failed": "Inicio de sesión fallido. Revisa usuario y contraseña.",
        "signup_success": "Cuenta creada. Ya has iniciado sesión.",
        "username_required": "El usuario es obligatorio.",
        "password_required": "La contraseña es obligatoria.",
        "username_exists": "Este usuario ya existe.",
        "only_guest": "Has cerrado sesión. Solo están disponibles las operaciones de invitado.",
        "booking_design_note": "La búsqueda pública solo aparece con permisos de invitado/cliente/empleado/manager.",
        "hotel_id": "ID hotel",
        "location": "Ubicación",
        "available": "Disponible",
        "price_max": "Precio máx.",
        "position": "Posición",
        "facilities": "Instalaciones",
        "room_id": "ID habitación",
        "client_id": "ID cliente",
        "client_name": "Nombre cliente",
        "client_email": "Email cliente",
        "check_in": "Check-in",
        "check_out": "Check-out",
        "start_date": "Check-in",
        "end_date": "Check-out",
        "client_phone": "Teléfono cliente",
        "total_price": "Precio total",
        "rating": "Valoración",
        "comment": "Reseña",
        "created_at": "Creado el",
        "new_password": "Nueva contraseña",
        "choose_hotel": "Seleccionar hotel",
        "choose_room": "Seleccionar habitación reservada",
        "reserved_review_required": "Puedes añadir una reseña solo para una habitación reservada por tu cuenta.",
        "no_room_selected": "Selecciona un hotel y una habitación antes de añadir la reseña.",
        "all": "Todos",
    },
}

COLUMNS = {
    "id": {"en": "ID", "fr": "ID", "es": "ID"},
    "name": {"en": "Name", "fr": "Nom", "es": "Nombre"},
    "location": {"en": "Location", "fr": "Localisation", "es": "Ubicación"},
    "address": {"en": "Address", "fr": "Adresse", "es": "Dirección"},
    "stars": {"en": "Stars", "fr": "Étoiles", "es": "Estrellas"},
    "description": {"en": "Description", "fr": "Description", "es": "Descripción"},
    "hotel_id": {"en": "Hotel ID", "fr": "ID hôtel", "es": "ID hotel"},
    "room_id": {"en": "Room ID", "fr": "ID chambre", "es": "ID habitación"},
    "room_number": {"en": "Room no.", "fr": "N° chambre", "es": "N.º habitación"},
    "floor": {"en": "Floor", "fr": "Étage", "es": "Planta"},
    "room_type": {"en": "Room type", "fr": "Type", "es": "Tipo"},
    "price_per_night": {"en": "Price/night", "fr": "Prix/nuit", "es": "Precio/noche"},
    "position": {"en": "View", "fr": "Vue", "es": "Vista"},
    "facilities": {"en": "Facilities", "fr": "Équipements", "es": "Instalaciones"},
    "image_urls": {"en": "Images", "fr": "Images", "es": "Imágenes"},
    "is_available": {"en": "Available", "fr": "Disponible", "es": "Disponible"},
    "max_guests": {"en": "Guests", "fr": "Voyageurs", "es": "Huéspedes"},
    "client_id": {"en": "Client ID", "fr": "ID client", "es": "ID cliente"},
    "client_name": {"en": "Client", "fr": "Client", "es": "Cliente"},
    "client_email": {"en": "Client email", "fr": "Email client", "es": "Email cliente"},
    "client_phone": {"en": "Client phone", "fr": "Téléphone client", "es": "Teléfono cliente"},
    "check_in": {"en": "Check-in", "fr": "Check-in", "es": "Check-in"},
    "check_out": {"en": "Check-out", "fr": "Check-out", "es": "Check-out"},
    "start_date": {"en": "Check-in", "fr": "Check-in", "es": "Check-in"},
    "end_date": {"en": "Check-out", "fr": "Check-out", "es": "Check-out"},
    "status": {"en": "Status", "fr": "Statut", "es": "Estado"},
    "total_price": {"en": "Total price", "fr": "Prix total", "es": "Precio total"},
    "username": {"en": "Username", "fr": "Utilisateur", "es": "Usuario"},
    "password": {"en": "Password", "fr": "Mot de passe", "es": "Contraseña"},
    "role": {"en": "Role", "fr": "Rôle", "es": "Rol"},
    "full_name": {"en": "Full name", "fr": "Nom complet", "es": "Nombre completo"},
    "email": {"en": "Email", "fr": "Email", "es": "Email"},
    "phone": {"en": "Phone", "fr": "Téléphone", "es": "Teléfono"},
    "is_active": {"en": "Active", "fr": "Actif", "es": "Activo"},
    "rating": {"en": "Rating", "fr": "Note", "es": "Valoración"},
    "comment": {"en": "Comment", "fr": "Avis", "es": "Reseña"},
    "created_at": {"en": "Created at", "fr": "Créé le", "es": "Creado el"},
    "user_id": {"en": "User ID", "fr": "ID utilisateur", "es": "ID usuario"},
    "channel": {"en": "Channel", "fr": "Canal", "es": "Canal"},
    "recipient": {"en": "Recipient", "fr": "Destinataire", "es": "Destinatario"},
    "message": {"en": "Message", "fr": "Message", "es": "Mensaje"},
    "criterion": {"en": "Criterion", "fr": "Critère", "es": "Criterio"},
    "value": {"en": "Value", "fr": "Valeur", "es": "Valor"},
}

VALUE_TRANSLATIONS = {
    "en": {
        True: "Yes", False: "No",
        "client": "Client", "employee": "Employee", "manager": "Manager", "admin": "Administrator",
        "reserved": "Reserved", "sent": "Sent",
        "Single": "Single", "Double": "Double", "Apartment": "Apartment", "Suite": "Suite",
        "street view": "Street view", "garden view": "Garden view", "city view": "City view", "mountain view": "Mountain view", "sea view": "Sea view",
    },
    "fr": {
        True: "Oui", False: "Non",
        "client": "Client", "employee": "Employé", "manager": "Manager", "admin": "Administrateur",
        "reserved": "Réservée", "sent": "Envoyé",
        "Single": "Simple", "Double": "Double", "Apartment": "Appartement", "Suite": "Suite",
        "street view": "Vue rue", "garden view": "Vue jardin", "city view": "Vue ville", "mountain view": "Vue montagne", "sea view": "Vue mer",
        "Hotel central pentru city-break.": "Hôtel central pour un city-break.",
        "Hotel premium aproape de centru.": "Hôtel premium près du centre.",
        "Hotel aproape de plajă.": "Hôtel près de la plage.",
        "Cameră curată și personal amabil.": "Chambre propre et personnel aimable.",
        "Foarte bine, mic dejun bun.": "Très bien, bon petit-déjeuner.",
        "Review adăugat din client.": "Avis ajouté depuis l'application client.",
        "modificare informații autentificare": "modification des informations d'authentification",
    },
    "es": {
        True: "Sí", False: "No",
        "client": "Cliente", "employee": "Empleado", "manager": "Gerente", "admin": "Administrador",
        "reserved": "Reservada", "sent": "Enviado",
        "Single": "Individual", "Double": "Doble", "Apartment": "Apartamento", "Suite": "Suite",
        "street view": "Vista a la calle", "garden view": "Vista al jardín", "city view": "Vista a la ciudad", "mountain view": "Vista a la montaña", "sea view": "Vista al mar",
        "Hotel central pentru city-break.": "Hotel céntrico para escapadas urbanas.",
        "Hotel premium aproape de centru.": "Hotel premium cerca del centro.",
        "Hotel aproape de plajă.": "Hotel cerca de la playa.",
        "Cameră curată și personal amabil.": "Habitación limpia y personal amable.",
        "Foarte bine, mic dejun bun.": "Muy bien, buen desayuno.",
        "Review adăugat din client.": "Reseña añadida desde la aplicación cliente.",
        "modificare informații autentificare": "cambio de datos de autenticación",
    },
}

PERMISSIONS = {
    None: ["browse"],
    "client": ["browse", "client_review"],
    "employee": ["browse", "rooms", "reservations", "clients"],
    "manager": ["browse", "statistics"],
    "admin": ["users", "notifications"],
}

TAB_TEXT_KEY = {
    "browse": "tab_browse",
    "client_review": "tab_client_review",
    "rooms": "tab_rooms",
    "reservations": "tab_reservations",
    "clients": "tab_clients",
    "statistics": "tab_statistics",
    "users": "tab_users",
    "notifications": "tab_notifications",
}


def current_date() -> str:
    return date.today().isoformat()

def tomorrow_date() -> str:
    return (date.today() + timedelta(days=1)).isoformat()


class App:
    def __init__(self):
        self.vm = MainVM()
        self.lang = "en"
        self._last_stats: dict[str, int | float] = {}
        self._tables: list[ttk.Treeview] = []
        self._entry_groups: dict[str, dict[str, object]] = {}
        self._init_root()
        self.rebuild_ui()

    def _init_root(self):
        if USE_CTK:
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("blue")
            self.root = ctk.CTk()
        else:
            self.root = ctk.Tk()
        self.root.geometry("1240x780")
        self.root.minsize(1100, 680)
        self.root.configure(bg=BOOKING_LIGHT)
        self._configure_tree_style()

    def _configure_tree_style(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Booking.Treeview", rowheight=28, font=("Segoe UI", 10), background="white", fieldbackground="white")
        style.configure("Booking.Treeview.Heading", font=("Segoe UI", 10, "bold"), background=BOOKING_BLUE, foreground="white")
        style.map("Booking.Treeview", background=[("selected", BOOKING_BLUE)], foreground=[("selected", "white")])
        style.configure("TNotebook", background=BOOKING_LIGHT, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(14, 8))

    def tr(self, key: str) -> str:
        return TEXT[self.lang].get(key, key)

    def col(self, key: str) -> str:
        return COLUMNS.get(key, {}).get(self.lang, key)

    def value(self, val):
        # Important: în Python, True == 1 și False == 0.
        # De aceea tratăm separat valorile bool, ca ID-ul 1 sau ratingul 1 să nu fie afișate ca Yes/Oui/Sí.
        if isinstance(val, bool):
            return VALUE_TRANSLATIONS.get(self.lang, {}).get(val, val)
        if isinstance(val, (int, float)):
            return val
        translated = VALUE_TRANSLATIONS.get(self.lang, {}).get(val)
        if translated is not None:
            return translated
        if isinstance(val, str) and "," in val and any(x in val.lower() for x in ["wifi", "tv", "ac", "minibar", "parking", "balcony", "jacuzzi"]):
            return val.replace(",", ", ")
        return val

    def role(self):
        user = self.vm.current_user or None
        return user.get("role") if user else None

    def allowed_tabs(self):
        return PERMISSIONS.get(self.role(), ["browse"])

    def frame(self, parent, **kwargs):
        if USE_CTK:
            defaults = {"fg_color": BOOKING_WHITE, "corner_radius": 14}
            defaults.update(kwargs)
            return ctk.CTkFrame(parent, **defaults)
        return ctk.Frame(parent, bg=kwargs.get("fg_color", BOOKING_WHITE))

    def label(self, parent, text="", **kwargs):
        if USE_CTK:
            defaults = {"text": text, "font": ("Segoe UI", 12), "text_color": kwargs.pop("text_color", BOOKING_DARK)}
            defaults.update(kwargs)
            return ctk.CTkLabel(parent, **defaults)
        return ctk.Label(parent, text=text, bg=kwargs.get("fg_color", BOOKING_WHITE), fg=kwargs.get("text_color", BOOKING_DARK), font=kwargs.get("font", ("Segoe UI", 12)))

    def entry(self, parent, placeholder="", show=None, width=150):
        if USE_CTK:
            return ctk.CTkEntry(parent, placeholder_text=placeholder, show=show, width=width, height=34, border_color="#d9e2f3")
        e = ctk.Entry(parent, show=show, width=max(12, width // 10))
        return e

    def combo(self, parent, values, variable, command=None, width=150):
        if USE_CTK:
            return ctk.CTkOptionMenu(parent, values=values, variable=variable, command=command, width=width, fg_color=BOOKING_BLUE, button_color=BOOKING_DARK)
        return ctk.OptionMenu(parent, variable, *values, command=command)

    def set_combo_values(self, combo, values, variable):
        values = values or ["-"]
        if USE_CTK:
            combo.configure(values=values)
        else:
            menu = combo["menu"]
            menu.delete(0, "end")
            for item in values:
                menu.add_command(label=item, command=lambda value=item: variable.set(value))
        if variable.get() not in values:
            variable.set(values[0])

    @staticmethod
    def id_from_label(label: str):
        try:
            return int(str(label).split(" - ", 1)[0].strip())
        except Exception:
            return None

    def button(self, parent, text, command, variant="blue", width=150):
        if USE_CTK:
            colors = {
                "blue": (BOOKING_BLUE, "white"),
                "yellow": (BOOKING_YELLOW, BOOKING_DARK),
                "dark": (BOOKING_DARK, "white"),
                "light": ("#eaf2ff", BOOKING_BLUE),
                "danger": ("#c1121f", "white"),
            }
            fg, txt = colors.get(variant, colors["blue"])
            return ctk.CTkButton(parent, text=text, command=command, width=width, height=36, corner_radius=8, fg_color=fg, hover_color=BOOKING_DARK if variant == "blue" else "#e0a800", text_color=txt, font=("Segoe UI", 11, "bold"))
        return ctk.Button(parent, text=text, command=command)

    def rebuild_ui(self):
        for child in self.root.winfo_children():
            child.destroy()
        self._tables.clear()
        self._entry_groups.clear()
        self.root.title(self.tr("app_title"))
        self._build_header()
        self._build_role_tabs()

    def _build_header(self):
        header = self.frame(self.root, fg_color=BOOKING_BLUE, corner_radius=0)
        header.pack(fill="x")

        left = self.frame(header, fg_color=BOOKING_BLUE, corner_radius=0)
        left.pack(side="left", padx=18, pady=14, fill="x", expand=True)
        self.label(left, self.tr("app_title"), font=("Segoe UI", 24, "bold"), text_color="white", fg_color=BOOKING_BLUE).pack(anchor="w")
        self.label(left, self.tr("hero_subtitle"), font=("Segoe UI", 12), text_color="#dce8ff", fg_color=BOOKING_BLUE).pack(anchor="w")

        right = self.frame(header, fg_color=BOOKING_BLUE, corner_radius=0)
        right.pack(side="right", padx=18, pady=12)

        self.lang_var = ctk.StringVar(value=LANGUAGES[self.lang])
        self.combo(right, list(LANGUAGES.values()), self.lang_var, self.change_language, width=130).pack(side="left", padx=5)

        user = self.vm.current_user
        if user:
            status = f"{self.tr('logged_as')} {user.get('full_name', '')} ({self.value(user.get('role'))})"
            self.label(right, status, font=("Segoe UI", 11, "bold"), text_color="white", fg_color=BOOKING_BLUE).pack(side="left", padx=8)
            self.button(right, self.tr("logout"), self.logout, variant="yellow", width=95).pack(side="left", padx=5)
        else:
            self.username_entry = self.entry(right, self.tr("username"), width=135)
            self.username_entry.pack(side="left", padx=4)
            self.password_entry = self.entry(right, self.tr("password"), show="*", width=135)
            self.password_entry.pack(side="left", padx=4)
            self.button(right, self.tr("login"), self.login, variant="yellow", width=95).pack(side="left", padx=4)
            self.button(right, self.tr("signup"), self.open_signup, variant="light", width=95).pack(side="left", padx=4)

    def _build_role_tabs(self):
        container = self.frame(self.root, fg_color=BOOKING_LIGHT, corner_radius=0)
        container.pack(fill="both", expand=True, padx=16, pady=14)

        card = self.frame(container, fg_color=BOOKING_WHITE, corner_radius=18)
        card.pack(fill="both", expand=True)

        title_bar = self.frame(card, fg_color=BOOKING_WHITE, corner_radius=18)
        title_bar.pack(fill="x", padx=16, pady=(14, 4))
        self.label(title_bar, self.tr("hero_title"), font=("Segoe UI", 20, "bold"), text_color=BOOKING_DARK).pack(anchor="w")
        status_text = self.tr("only_guest") if not self.vm.current_user else self.tr("booking_design_note")
        self.label(title_bar, status_text, font=("Segoe UI", 11), text_color="#52657a").pack(anchor="w")

        self.notebook = ttk.Notebook(card)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        for tab_name in self.allowed_tabs():
            tab_frame = self.frame(self.notebook, fg_color=BOOKING_WHITE, corner_radius=0)
            self.notebook.add(tab_frame, text=self.tr(TAB_TEXT_KEY[tab_name]))
            getattr(self, f"build_{tab_name}")(tab_frame)

    def change_language(self, selected_label):
        for code, label in LANGUAGES.items():
            if label == selected_label:
                self.lang = code
                break
        self.rebuild_ui()

    def login(self):
        try:
            user = self.vm.login(self.username_entry.get().strip(), self.password_entry.get().strip())
        except Exception:
            messagebox.showerror(self.tr("error"), self.tr("login_failed"))
            return
        if user:
            self.rebuild_ui()

    def open_signup(self):
        window = ctk.CTkToplevel(self.root) if USE_CTK else ctk.Toplevel(self.root)
        window.title(self.tr("signup"))
        window.geometry("430x360")
        window.transient(self.root)
        window.grab_set()

        container = self.frame(window, fg_color=BOOKING_WHITE, corner_radius=12)
        container.pack(fill="both", expand=True, padx=16, pady=16)
        self.label(container, self.tr("signup"), font=("Segoe UI", 18, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", padx=8, pady=(4, 12))

        fields = ["username", "password", "full_name", "email", "phone"]
        entries = {}
        for index, field in enumerate(fields, start=1):
            self.label(container, self.col(field), font=("Segoe UI", 10, "bold")).grid(row=index, column=0, sticky="w", padx=8, pady=6)
            entry = self.entry(container, self.col(field), show="*" if field == "password" else None, width=250)
            entry.grid(row=index, column=1, sticky="ew", padx=8, pady=6)
            entries[field] = entry
        container.grid_columnconfigure(1, weight=1)

        def submit():
            data = {key: entry.get().strip() for key, entry in entries.items()}
            if not data["username"]:
                messagebox.showwarning(self.tr("warning"), self.tr("username_required"), parent=window)
                return
            if not data["password"]:
                messagebox.showwarning(self.tr("warning"), self.tr("password_required"), parent=window)
                return
            existing = self.safe(lambda: self.vm.load_users(username=data["username"])) or []
            if existing:
                messagebox.showerror(self.tr("error"), self.tr("username_exists"), parent=window)
                return
            payload = {
                "username": data["username"],
                "password": data["password"],
                "role": "client",
                "full_name": data["full_name"] or data["username"],
                "email": data["email"],
                "phone": data["phone"],
                "is_active": True,
            }
            created = self.safe(lambda: self.vm.create_user(payload))
            if created:
                self.vm.current_user = created
                window.destroy()
                messagebox.showinfo(self.tr("result"), self.tr("signup_success"))
                self.rebuild_ui()

        self.button(container, self.tr("signup"), submit, "yellow", 130).grid(row=len(fields) + 1, column=1, sticky="e", padx=8, pady=(14, 4))

    def logout(self):
        self.vm.current_user = None
        self.rebuild_ui()
        messagebox.showinfo(self.tr("result"), self.tr("only_guest"))

    def input_row(self, parent, fields, group_name):
        box = self.frame(parent, fg_color="#f2f6fc", corner_radius=12)
        box.pack(fill="x", padx=10, pady=8)
        entries = {}
        for index, field in enumerate(fields):
            label = self.label(box, self.col(field) if field in COLUMNS else self.tr(field), font=("Segoe UI", 10, "bold"), fg_color="#f2f6fc")
            label.grid(row=(index // 5) * 2, column=index % 5, sticky="w", padx=8, pady=(8, 0))
            e = self.entry(box, self.col(field) if field in COLUMNS else self.tr(field), width=190)
            e.grid(row=(index // 5) * 2 + 1, column=index % 5, sticky="ew", padx=8, pady=(2, 8))
            entries[field] = e
        for col in range(5):
            box.grid_columnconfigure(col, weight=1)
        self._entry_groups[group_name] = entries
        return entries

    def actions_row(self, parent):
        bar = self.frame(parent, fg_color=BOOKING_WHITE, corner_radius=0)
        bar.pack(fill="x", padx=10, pady=6)
        return bar

    def make_table(self, parent, columns, height=13):
        wrapper = self.frame(parent, fg_color=BOOKING_WHITE, corner_radius=12)
        wrapper.pack(fill="both", expand=True, padx=10, pady=10)
        table = ttk.Treeview(wrapper, columns=columns, show="headings", height=height, style="Booking.Treeview")
        vsb = ttk.Scrollbar(wrapper, orient="vertical", command=table.yview)
        hsb = ttk.Scrollbar(wrapper, orient="horizontal", command=table.xview)
        table.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        table.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        wrapper.grid_rowconfigure(0, weight=1)
        wrapper.grid_columnconfigure(0, weight=1)
        self.configure_table_columns(table, columns)
        table.raw_rows = []
        self._tables.append(table)
        return table

    def configure_table_columns(self, table, columns):
        """Afișează în tabel doar câmpurile cerute pentru cazul de utilizare curent.
        Datele tehnice rămân în obiectele interne doar când sunt necesare pentru update/delete.
        """
        table["columns"] = columns
        for col in columns:
            table.heading(col, text=self.col(col))
            width = 105
            if col in ("comment", "message", "facilities", "image_urls"):
                width = 230
            elif col in ("client_email", "email", "recipient"):
                width = 190
            elif col in ("name", "full_name", "client_name"):
                width = 170
            table.column(col, minwidth=70, width=width, stretch=True)

    def set_rows(self, table, rows):
        table.raw_rows = rows or []
        table.delete(*table.get_children())
        columns = list(table["columns"])
        for row in table.raw_rows:
            table.insert("", "end", values=[self.value(row.get(col, "")) for col in columns])

    def selected_raw(self, table):
        item = table.focus()
        if not item:
            return None
        index = table.index(item)
        if 0 <= index < len(getattr(table, "raw_rows", [])):
            return table.raw_rows[index]
        return None

    def get_entries(self, group_name):
        return {key: entry.get().strip() for key, entry in self._entry_groups.get(group_name, {}).items()}

    def set_entries(self, group_name, row):
        entries = self._entry_groups.get(group_name, {})
        for key, entry in entries.items():
            entry.delete(0, "end")
            if row and row.get(key) is not None:
                entry.insert(0, str(row.get(key)))

    def clear_entries(self, group_name):
        self.set_entries(group_name, {})

    def safe(self, action):
        try:
            return action()
        except Exception as exc:
            messagebox.showerror(self.tr("error"), str(exc))
            return None

    def show_result(self, result=None):
        message = self.tr("success") if result in (None, True) else str(result)
        messagebox.showinfo(self.tr("result"), message)

    def build_browse(self, parent):
        fields = ["hotel_id", "location", "available", "price_max", "position", "facilities", "check_in", "check_out"]
        self.input_row(parent, fields, "filters")
        self._entry_groups["filters"]["check_in"].insert(0, current_date())
        self._entry_groups["filters"]["check_out"].insert(0, tomorrow_date())
        bar = self.actions_row(parent)
        self.button(bar, self.tr("load_hotels"), self.load_hotels, "blue", 135).pack(side="left", padx=4)
        self.button(bar, self.tr("load_rooms"), self.load_rooms, "yellow", 150).pack(side="left", padx=4)
        self.button(bar, self.tr("load_reviews"), self.load_reviews, "light", 130).pack(side="left", padx=4)
        # tabelul public nu mai amestecă hoteluri, camere și review-uri într-o singură listă de coloane
        self.browse_table = self.make_table(parent, ["id", "name", "location"])

    def load_hotels(self):
        rows = self.safe(lambda: self.vm.load_hotels()) or []
        self.configure_table_columns(self.browse_table, ["id", "name", "location"])
        self.set_rows(self.browse_table, rows)

    def load_rooms(self):
        f = self.get_entries("filters")
        params = {
            "hotel_id": f.get("hotel_id"),
            "location": f.get("location"),
            "is_available": self.parse_bool(f.get("available")),
            "price_max": f.get("price_max"),
            "position": f.get("position"),
            "facilities": f.get("facilities"),
            "check_in": f.get("check_in"),
            "check_out": f.get("check_out"),
        }
        rows = self.safe(lambda: self.vm.load_rooms(**params)) or []
        self.configure_table_columns(self.browse_table, ["id", "hotel_id", "room_number", "location", "price_per_night", "position", "facilities", "is_available"])
        self.set_rows(self.browse_table, rows)

    def load_reviews(self):
        f = self.get_entries("filters")
        room_id = f.get("room_id") or None
        rows = self.safe(lambda: self.vm.load_reviews(room_id=room_id)) or []
        self.configure_table_columns(self.browse_table, ["room_id", "client_name", "rating", "comment"])
        self.set_rows(self.browse_table, rows)

    def build_client_review(self, parent):
        user = self.vm.current_user or {}

        selector = self.frame(parent, fg_color="#f2f6fc", corner_radius=12)
        selector.pack(fill="x", padx=10, pady=8)

        self.label(selector, self.tr("choose_hotel"), font=("Segoe UI", 10, "bold"), fg_color="#f2f6fc").grid(row=0, column=0, sticky="w", padx=8, pady=(8, 0))
        self.label(selector, self.tr("choose_room"), font=("Segoe UI", 10, "bold"), fg_color="#f2f6fc").grid(row=0, column=1, sticky="w", padx=8, pady=(8, 0))
        self.label(selector, self.col("rating"), font=("Segoe UI", 10, "bold"), fg_color="#f2f6fc").grid(row=0, column=2, sticky="w", padx=8, pady=(8, 0))
        self.label(selector, self.col("comment"), font=("Segoe UI", 10, "bold"), fg_color="#f2f6fc").grid(row=0, column=3, sticky="w", padx=8, pady=(8, 0))

        self.review_hotel_var = ctk.StringVar(value="-")
        self.review_room_var = ctk.StringVar(value="-")
        self.review_hotel_combo = self.combo(selector, ["-"], self.review_hotel_var, self.on_review_hotel_changed, width=260)
        self.review_hotel_combo.grid(row=1, column=0, sticky="ew", padx=8, pady=(2, 8))
        self.review_room_combo = self.combo(selector, ["-"], self.review_room_var, None, width=280)
        self.review_room_combo.grid(row=1, column=1, sticky="ew", padx=8, pady=(2, 8))

        rating_entry = self.entry(selector, self.col("rating"), width=120)
        rating_entry.grid(row=1, column=2, sticky="ew", padx=8, pady=(2, 8))
        rating_entry.insert(0, "5")
        comment_entry = self.entry(selector, self.col("comment"), width=360)
        comment_entry.grid(row=1, column=3, sticky="ew", padx=8, pady=(2, 8))
        self._entry_groups["review"] = {"rating": rating_entry, "comment": comment_entry}

        for col in range(4):
            selector.grid_columnconfigure(col, weight=1)

        bar = self.actions_row(parent)
        self.button(bar, self.tr("add_review"), self.add_review, "yellow", 160).pack(side="left", padx=4)
        self.button(bar, self.tr("load_reviews"), self.load_my_reviews, "blue", 150).pack(side="left", padx=4)
        self.reviews_table = self.make_table(parent, ["room_id", "rating", "comment"])
        self.refresh_review_hotels()
        if user:
            self.load_my_reviews()

    def refresh_review_hotels(self):
        user = self.vm.current_user or {}
        client_id = int(user.get("id") or 0)
        reservations = self.safe(lambda: self.vm.load_reservations(client_id=client_id)) or []
        rooms = self.safe(lambda: self.vm.load_rooms()) or []
        hotels = self.safe(lambda: self.vm.load_hotels()) or []
        self._review_reservations = reservations
        self._review_rooms_by_id = {int(room.get("id")): room for room in rooms if room.get("id") is not None}
        self._review_hotels_by_id = {int(hotel.get("id")): hotel for hotel in hotels if hotel.get("id") is not None}

        hotel_ids = set()
        for reservation in reservations:
            if reservation.get("hotel_id"):
                hotel_ids.add(int(reservation.get("hotel_id")))
            room = self._review_rooms_by_id.get(int(reservation.get("room_id") or 0))
            if room and room.get("hotel_id"):
                hotel_ids.add(int(room.get("hotel_id")))

        labels = [
            f"{hotel.get('id')} - {hotel.get('name')} ({hotel.get('location')})"
            for hotel_id, hotel in sorted(self._review_hotels_by_id.items())
            if hotel_id in hotel_ids
        ]
        self.set_combo_values(self.review_hotel_combo, labels, self.review_hotel_var)
        if labels:
            self.on_review_hotel_changed(self.review_hotel_var.get())
        else:
            self.set_combo_values(self.review_room_combo, ["-"], self.review_room_var)

    def on_review_hotel_changed(self, selected_label=None):
        hotel_id = self.id_from_label(selected_label or self.review_hotel_var.get())
        if not hotel_id:
            self.set_combo_values(self.review_room_combo, ["-"], self.review_room_var)
            return
        reservations = getattr(self, "_review_reservations", [])
        rooms_by_id = getattr(self, "_review_rooms_by_id", {})
        reserved_room_ids = set()
        for reservation in reservations:
            room_id = int(reservation.get("room_id") or 0)
            room = rooms_by_id.get(room_id)
            reservation_hotel_id = int(reservation.get("hotel_id") or 0)
            room_hotel_id = int(room.get("hotel_id") or 0) if room else 0
            if reservation_hotel_id == hotel_id or room_hotel_id == hotel_id:
                reserved_room_ids.add(room_id)
        rooms = [rooms_by_id[room_id] for room_id in sorted(reserved_room_ids) if room_id in rooms_by_id]
        labels = [
            f"{room.get('id')} - {self.col('room_number')} {room.get('room_number')} ({self.value(room.get('position'))}, {room.get('price_per_night')} lei)"
            for room in rooms
        ]
        self.set_combo_values(self.review_room_combo, labels, self.review_room_var)

    def add_review(self):
        user = self.vm.current_user or {"id": 1, "full_name": "Client Demo"}
        data = self.get_entries("review")
        room_id = self.id_from_label(self.review_room_var.get())
        if not room_id:
            messagebox.showwarning(self.tr("warning"), self.tr("no_room_selected"))
            return
        client_id = int(user.get("id") or 1)
        # Verificare în aplicația client, pentru mesaj prietenos înainte de apelul POST.
        has_reservation = self.safe(lambda: self.vm.client_has_reservation(room_id, client_id))
        if not has_reservation:
            messagebox.showerror(self.tr("error"), self.tr("reserved_review_required"))
            return
        payload = {
            "room_id": int(room_id),
            "client_id": client_id,
            "client_name": user.get("full_name") or "Client Demo",
            "rating": int(data.get("rating") or 5),
            "comment": data.get("comment") or "Review adăugat din client.",
            "created_at": current_date(),
        }
        result = self.safe(lambda: self.vm.add_review(payload))
        if result:
            self.show_result(result)
            self.load_my_reviews()

    def load_my_reviews(self):
        user = self.vm.current_user or {}
        rows = self.safe(lambda: self.vm.load_reviews()) or []
        if user:
            rows = [row for row in rows if str(row.get("client_id")) == str(user.get("id"))]
        self.set_rows(self.reviews_table, rows)

    def build_rooms(self, parent):
        fields = ["id", "hotel_id", "room_number", "location", "price_per_night", "position", "facilities", "is_available"]
        self.input_row(parent, fields, "room_crud")
        bar = self.actions_row(parent)
        self.button(bar, self.tr("load_rooms"), self.load_rooms_crud, "blue", 130).pack(side="left", padx=4)
        self.button(bar, self.tr("create"), self.create_room, "yellow", 100).pack(side="left", padx=4)
        self.button(bar, self.tr("update"), self.update_room, "blue", 100).pack(side="left", padx=4)
        self.button(bar, self.tr("delete"), self.delete_room, "danger", 100).pack(side="left", padx=4)
        self.button(bar, self.tr("clear"), lambda: self.clear_entries("room_crud"), "light", 120).pack(side="left", padx=4)
        self.rooms_table = self.make_table(parent, fields)
        self.rooms_table.bind("<<TreeviewSelect>>", lambda _e: self.set_entries("room_crud", self.selected_raw(self.rooms_table)))
        self.load_rooms_crud()

    def room_payload(self):
        data = self.get_entries("room_crud")
        return {
            "hotel_id": int(data.get("hotel_id") or 1),
            "room_number": data.get("room_number") or "",
            "location": data.get("location") or "",
            "floor": 1,
            "room_type": "",
            "price_per_night": float(data.get("price_per_night") or 0),
            "position": data.get("position") or "",
            "facilities": data.get("facilities") or "",
            "image_urls": "",
            "is_available": self.parse_bool(data.get("is_available"), default=True),
            "max_guests": 1,
        }

    def load_rooms_crud(self):
        rows = self.safe(lambda: self.vm.load_rooms()) or []
        self.set_rows(self.rooms_table, rows)

    def create_room(self):
        result = self.safe(lambda: self.vm.create_room(self.room_payload()))
        if result:
            self.show_result(result); self.load_rooms_crud()

    def update_room(self):
        data = self.get_entries("room_crud")
        room_id = data.get("id")
        if not room_id:
            messagebox.showwarning(self.tr("warning"), self.tr("select_row")); return
        result = self.safe(lambda: self.vm.update_room(room_id, self.room_payload()))
        if result:
            self.show_result(result); self.load_rooms_crud()

    def delete_room(self):
        room_id = self.get_entries("room_crud").get("id")
        if not room_id:
            messagebox.showwarning(self.tr("warning"), self.tr("select_row")); return
        result = self.safe(lambda: self.vm.delete_room(room_id))
        if result:
            self.show_result(result); self.load_rooms_crud()

    def build_reservations(self, parent):
        fields = ["hotel_id", "room_id", "client_name", "client_email", "client_phone", "check_in", "check_out"]
        self.input_row(parent, fields, "reservation")
        self._entry_groups["reservation"]["check_in"].insert(0, current_date())
        self._entry_groups["reservation"]["check_out"].insert(0, tomorrow_date())
        bar = self.actions_row(parent)
        self.button(bar, self.tr("reserve"), self.reserve_room, "yellow", 135).pack(side="left", padx=4)
        self.button(bar, self.tr("load_reservations"), self.load_reservations, "blue", 160).pack(side="left", padx=4)
        self.reservation_export_format = ctk.StringVar(value="csv")
        self.label(bar, self.tr("export_format"), font=("Segoe UI", 10, "bold")).pack(side="left", padx=(12, 4))
        self.combo(bar, ["csv", "json", "xml", "doc"], self.reservation_export_format, width=95).pack(side="left", padx=4)
        self.button(bar, self.tr("export"), self.export_reservations, "light", 120).pack(side="left", padx=4)
        self.reservations_table = self.make_table(parent, ["hotel_id", "room_id", "client_name", "client_email", "client_phone", "start_date", "end_date", "status"])
        self.load_reservations()

    def reserve_room(self):
        data = self.get_entries("reservation")
        payload = {
            "hotel_id": int(data.get("hotel_id") or 1),
            "room_id": int(data.get("room_id") or 1),
            "client_id": 1,
            "client_name": data.get("client_name") or "Client Demo",
            "client_email": data.get("client_email") or "client@example.com",
            "client_phone": data.get("client_phone") or "",
            "start_date": data.get("check_in") or current_date(),
            "end_date": data.get("check_out") or current_date(),
            "status": "reserved",
            "total_price": 0.0,
        }
        result = self.safe(lambda: self.vm.reserve_room(payload))
        if result:
            self.show_result(result); self.load_reservations()

    def load_reservations(self):
        rows = self.safe(lambda: self.vm.api.get("reservation")) or []
        self.set_rows(self.reservations_table, rows)

    def export_reservations(self):
        fmt = self.reservation_export_format.get() or "csv"
        extensions = {
            "csv": [("CSV", "*.csv")],
            "json": [("JSON", "*.json")],
            "xml": [("XML", "*.xml")],
            "doc": [("Word document", "*.doc")],
        }
        path = filedialog.asksaveasfilename(
            title=self.tr("export"),
            defaultextension=f".{fmt}",
            filetypes=extensions.get(fmt, [(fmt.upper(), f"*.{fmt}")]),
        )
        if not path:
            return
        result = self.safe(lambda: self.vm.export("reservation", fmt, output_path=path))
        if result:
            self.show_result(result.get("path", result) if isinstance(result, dict) else result)

    def build_clients(self, parent):
        self.build_users_common(parent, "client_users", only_clients=True)

    def build_users(self, parent):
        self.build_users_common(parent, "admin_users", only_clients=False)

    def build_users_common(self, parent, group, only_clients=False):
        # Parola este câmp de intrare pentru crearea/modificarea contului, dar nu este afișată în tabel.
        fields = ["id", "username", "password", "full_name", "email", "phone"] if only_clients else ["id", "username", "password", "role", "full_name", "email", "phone"]
        table_columns = ["id", "username", "full_name", "email", "phone"] if only_clients else ["id", "username", "role", "full_name", "email", "phone"]
        self.input_row(parent, fields, group)
        filter_bar = self.actions_row(parent)
        self.role_filter = ctk.StringVar(value=self.tr("all"))
        if not only_clients:
            self.label(filter_bar, self.tr("filter_role"), font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 6))
            self.combo(filter_bar, [self.tr("all"), "client", "employee", "manager", "admin"], self.role_filter, lambda _v: self.load_users_table(group, only_clients), width=150).pack(side="left", padx=4)
        self.button(filter_bar, self.tr("load_users"), lambda: self.load_users_table(group, only_clients), "blue", 130).pack(side="left", padx=4)
        self.button(filter_bar, self.tr("create"), lambda: self.create_user(group, only_clients), "yellow", 100).pack(side="left", padx=4)
        self.button(filter_bar, self.tr("update"), lambda: self.update_user(group, only_clients), "blue", 100).pack(side="left", padx=4)
        self.button(filter_bar, self.tr("delete"), lambda: self.delete_user(group, only_clients), "danger", 100).pack(side="left", padx=4)
        self.button(filter_bar, self.tr("notify"), lambda: self.change_password_notify(group), "light", 220).pack(side="left", padx=4)
        if not only_clients:
            self.button(filter_bar, self.tr("export_csv"), lambda: self.show_result(self.vm.export("user", "csv")), "light", 120).pack(side="left", padx=4)
        table = self.make_table(parent, table_columns)
        table.bind("<<TreeviewSelect>>", lambda _e: self.set_entries(group, self.selected_raw(table)))
        setattr(self, f"{group}_table", table)
        self.load_users_table(group, only_clients)

    def user_payload(self, group, only_clients):
        data = self.get_entries(group)
        return {
            "username": data.get("username") or "",
            "password": data.get("password") or "1234",
            "role": "client" if only_clients else (data.get("role") or "client"),
            "full_name": data.get("full_name") or "",
            "email": data.get("email") or "",
            "phone": data.get("phone") or "",
            "is_active": self.parse_bool(data.get("is_active"), default=True),
        }

    def load_users_table(self, group, only_clients=False):
        role = "client" if only_clients else None
        if not only_clients:
            selected = getattr(self, "role_filter", None)
            if selected:
                selected_role = selected.get()
                role = None if selected_role == self.tr("all") else selected_role
        rows = self.safe(lambda: self.vm.load_users(role=role)) or []
        table = getattr(self, f"{group}_table")
        self.set_rows(table, rows)

    def create_user(self, group, only_clients):
        result = self.safe(lambda: self.vm.create_user(self.user_payload(group, only_clients)))
        if result:
            self.show_result(result); self.load_users_table(group, only_clients)

    def update_user(self, group, only_clients):
        user_id = self.get_entries(group).get("id")
        if not user_id:
            messagebox.showwarning(self.tr("warning"), self.tr("select_row")); return
        result = self.safe(lambda: self.vm.update_user(user_id, self.user_payload(group, only_clients)))
        if result:
            self.show_result(result); self.load_users_table(group, only_clients)

    def delete_user(self, group, only_clients):
        user_id = self.get_entries(group).get("id")
        if not user_id:
            messagebox.showwarning(self.tr("warning"), self.tr("select_row")); return
        result = self.safe(lambda: self.vm.delete_user(user_id))
        if result:
            self.show_result(result); self.load_users_table(group, only_clients)

    def change_password_notify(self, group):
        data = self.get_entries(group)
        user_id = data.get("id")
        if not user_id:
            messagebox.showwarning(self.tr("warning"), self.tr("select_row")); return
        new_password = data.get("password") or "parola_noua"
        result = self.safe(lambda: self.vm.update_user_credentials(user_id, {"password": new_password}))
        if result:
            self.show_result(result)
            self.load_users_table(group, only_clients=(group == "client_users"))

    def build_statistics(self, parent):
        bar = self.actions_row(parent)
        self.button(bar, self.tr("availability"), lambda: self.load_stat("room", "availability"), "yellow", 140).pack(side="left", padx=4)
        self.button(bar, self.tr("position"), lambda: self.load_stat("room", "position"), "blue", 140).pack(side="left", padx=4)
        self.button(bar, self.tr("average_price"), lambda: self.load_stat("room", "average-price-hotel"), "blue", 190).pack(side="left", padx=4)
        self.button(bar, self.tr("reservation_status"), lambda: self.load_stat("reservation", "status"), "light", 170).pack(side="left", padx=4)
        self.button(bar, self.tr("show_chart"), self.show_chart, "dark", 130).pack(side="left", padx=4)
        self.stats_table = self.make_table(parent, ["criterion", "value"])

    def load_stat(self, service, criterion):
        result = self.safe(lambda: self.vm.stats(service, criterion)) or {}
        self._last_stats = result
        rows = [{"criterion": self.value(k), "value": v} for k, v in result.items()]
        self.set_rows(self.stats_table, rows)

    def show_chart(self):
        if not self._last_stats:
            messagebox.showwarning(self.tr("warning"), self.tr("show_statistics"))
            return
        try:
            import matplotlib.pyplot as plt
            labels = [str(self.value(k)) for k in self._last_stats.keys()]
            values = [float(v) for v in self._last_stats.values()]
            plt.figure(figsize=(7, 4))
            plt.bar(labels, values)
            plt.title(self.tr("tab_statistics"))
            plt.tight_layout()
            plt.show()
        except Exception as exc:
            messagebox.showerror(self.tr("error"), str(exc))

    def build_notifications(self, parent):
        bar = self.actions_row(parent)
        self.button(bar, self.tr("load_notifications"), self.load_notifications, "blue", 170).pack(side="left", padx=4)
        self.notifications_table = self.make_table(parent, ["user_id", "channel", "recipient", "message"])
        self.load_notifications()

    def load_notifications(self):
        rows = self.safe(lambda: self.vm.api.get("notification")) or []
        self.set_rows(self.notifications_table, rows)

    @staticmethod
    def parse_bool(value, default=None):
        if value in (None, ""):
            return default
        if isinstance(value, bool):
            return value
        text = str(value).strip().lower()
        if text in ["true", "1", "yes", "da", "oui", "sí", "si", "available", "disponible"]:
            return True
        if text in ["false", "0", "no", "nu", "non", "unavailable", "indisponible"]:
            return False
        return default

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    App().run()
