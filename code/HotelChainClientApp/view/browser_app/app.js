const API_BASE = "/api";

const state = {
  currentUser: null,
  hotels: [],
  rooms: [],
  adminRooms: [],
  reviews: [],
  reservations: [],
  users: [],
  language: "en",
};

const translations = {
  en: {
    guest: "Guest", signIn: "Sign in", register: "Register", signOut: "Sign out",
    stays: "Stays", reservations: "Reservations", rooms: "Rooms", myReviews: "My reviews",
    stats: "Stats", users: "Users", notifications: "Notifications",
    heroTitle: "Find your next stay",
    heroText: "Hotels, rooms, reviews, reservations and role-based workflows in one place.",
    hotel: "Hotel", allHotels: "All hotels", location: "Location", checkIn: "Check-in",
    checkOut: "Check-out", maxPrice: "Max price", search: "Search",
    availableStays: "Available stays", liveAvailability: "Live availability from the room and reservation services.",
    showReviews: "Show reviews", guestReviews: "Guest reviews", noReviews: "No reviews yet.",
    noReservedHotels: "No reserved hotels", noReservedRooms: "No reserved rooms",
    reservedOnly: "Only rooms reserved by the logged client appear here.",
    shareStay: "Share your stay", addReview: "Add review",
    loadNotifications: "Load notifications",
    notificationsHelp: "Authentication-change notifications sent through email, SMS and WhatsApp.",
  },
  fr: {
    guest: "Invite", signIn: "Connexion", register: "Creer un compte", signOut: "Deconnexion",
    stays: "Sejours", reservations: "Reservations", rooms: "Chambres", myReviews: "Mes avis",
    stats: "Statistiques", users: "Utilisateurs", notifications: "Notifications",
    heroTitle: "Trouvez votre prochain sejour",
    heroText: "Hotels, chambres, avis, reservations et flux par role au meme endroit.",
    hotel: "Hotel", allHotels: "Tous les hotels", location: "Lieu", checkIn: "Arrivee",
    checkOut: "Depart", maxPrice: "Prix max.", search: "Rechercher",
    availableStays: "Sejours disponibles", liveAvailability: "Disponibilite en direct depuis les services chambres et reservations.",
    showReviews: "Voir les avis", guestReviews: "Avis clients", noReviews: "Aucun avis.",
    noReservedHotels: "Aucun hotel reserve", noReservedRooms: "Aucune chambre reservee",
    reservedOnly: "Seules les chambres reservees par le client connecte apparaissent ici.",
    shareStay: "Partagez votre sejour", addReview: "Ajouter un avis",
    loadNotifications: "Charger les notifications",
    notificationsHelp: "Notifications de changement d'identifiants envoyees par email, SMS et WhatsApp.",
  },
  es: {
    guest: "Invitado", signIn: "Iniciar sesion", register: "Registrarse", signOut: "Cerrar sesion",
    stays: "Estancias", reservations: "Reservas", rooms: "Habitaciones", myReviews: "Mis opiniones",
    stats: "Estadisticas", users: "Usuarios", notifications: "Notificaciones",
    heroTitle: "Encuentra tu proxima estancia",
    heroText: "Hoteles, habitaciones, opiniones, reservas y flujos por rol en un solo lugar.",
    hotel: "Hotel", allHotels: "Todos los hoteles", location: "Ubicacion", checkIn: "Entrada",
    checkOut: "Salida", maxPrice: "Precio max.", search: "Buscar",
    availableStays: "Estancias disponibles", liveAvailability: "Disponibilidad en vivo desde los servicios de habitaciones y reservas.",
    showReviews: "Ver opiniones", guestReviews: "Opiniones", noReviews: "Sin opiniones.",
    noReservedHotels: "Sin hoteles reservados", noReservedRooms: "Sin habitaciones reservadas",
    reservedOnly: "Aqui solo aparecen habitaciones reservadas por el cliente conectado.",
    shareStay: "Comparte tu estancia", addReview: "Agregar opinion",
    loadNotifications: "Cargar notificaciones",
    notificationsHelp: "Notificaciones de cambios de autenticacion enviadas por email, SMS y WhatsApp.",
  },
};

function t(key) {
  return translations[state.language]?.[key] || translations.en[key] || key;
}

const hotelImages = {
  1: "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80",
  2: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=1200&q=80",
  3: "https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=1200&q=80",
};

const roomImages = {
  "street view": "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=1200&q=80",
  "garden view": "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=1200&q=80",
  "city view": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=1200&q=80",
  "mountain view": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=1200&q=80",
  "sea view": "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?auto=format&fit=crop&w=1200&q=80",
};

const fallbackRoomImage = "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?auto=format&fit=crop&w=1200&q=80";

function today(offset = 0) {
  const date = new Date();
  date.setDate(date.getDate() + offset);
  return date.toISOString().slice(0, 10);
}

function qs(selector) {
  return document.querySelector(selector);
}

function qsa(selector) {
  return [...document.querySelectorAll(selector)];
}

function toast(message) {
  const box = qs("#toast");
  box.textContent = message;
  box.classList.remove("hidden");
  window.clearTimeout(toast.timer);
  toast.timer = window.setTimeout(() => box.classList.add("hidden"), 3600);
}

async function api(service, path = "", options = {}) {
  const url = new URL(`${API_BASE}/${service}${path ? `/${path}` : ""}`, window.location.origin);
  if (options.params) {
    Object.entries(options.params).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== "") url.searchParams.set(key, value);
    });
  }
  const response = await fetch(url, {
    method: options.method || "GET",
    headers: { "Content-Type": "application/json" },
    body: options.body ? JSON.stringify(options.body) : undefined,
  });
  const text = await response.text();
  const data = text ? JSON.parse(text) : {};
  if (!response.ok) {
    throw new Error(data.detail || data.message || response.statusText);
  }
  return data;
}

function formData(form) {
  return Object.fromEntries(new FormData(form).entries());
}

function normalize(value) {
  return String(value || "").trim().toLowerCase();
}

function sanitizeUsername(value) {
  const normalized = String(value || "")
    .toLowerCase()
    .replace(/@.*$/, "")
    .replace(/[^a-z0-9._-]/g, "");
  return normalized || `client${Date.now()}`;
}

function money(value) {
  return `${Number(value || 0).toLocaleString("en-US")} lei`;
}

function hotelById(id) {
  return state.hotels.find((hotel) => String(hotel.id) === String(id));
}

function sortRooms(rooms) {
  return [...rooms].sort((a, b) => {
    const locationCompare = String(a.location || "").localeCompare(String(b.location || ""));
    if (locationCompare !== 0) return locationCompare;
    return String(a.room_number || "").localeCompare(String(b.room_number || ""), undefined, { numeric: true });
  });
}

function roomImage(room) {
  return roomImages[String(room.position || "").toLowerCase()] || fallbackRoomImage;
}

function updateRoleUI() {
  const role = state.currentUser?.role || "";
  qs("#sessionLabel").textContent = state.currentUser
    ? `${state.currentUser.full_name || state.currentUser.username} (${role})`
    : t("guest");
  qs("#openLoginBtn").classList.toggle("hidden", Boolean(state.currentUser));
  qs("#openSignupBtn").classList.toggle("hidden", Boolean(state.currentUser));
  qs("#logoutBtn").classList.toggle("hidden", !state.currentUser);

  qsa("[data-role]").forEach((element) => {
    const roles = element.dataset.role.split(" ");
    element.classList.toggle("hidden", !roles.includes(role));
  });

  if (qs(".nav-tab.active.hidden")) {
    switchView("browse");
  }
}

function applyTranslations() {
  const setText = (selector, text) => {
    const element = qs(selector);
    if (element) element.textContent = text;
  };
  const setLabelText = (selector, text) => {
    const label = qs(selector);
    if (!label) return;
    const textNode = [...label.childNodes].find((node) => node.nodeType === Node.TEXT_NODE);
    if (textNode) textNode.nodeValue = `\n          ${text}\n          `;
  };
  setText('[data-view="browse"]', t("stays"));
  setText('[data-view="reservations"]', t("reservations"));
  setText('[data-view="rooms"]', t("rooms"));
  setText('[data-view="reviews"]', t("myReviews"));
  setText('[data-view="stats"]', t("stats"));
  setText('[data-view="users"]', t("users"));
  setText('[data-view="notifications"]', t("notifications"));
  setText("#openLoginBtn", t("signIn"));
  setText("#openSignupBtn", t("register"));
  setText("#logoutBtn", t("signOut"));
  setText(".search-copy h1", t("heroTitle"));
  setText(".search-copy p", t("heroText"));
  setLabelText('#searchForm label:nth-of-type(1)', t("hotel"));
  setLabelText('#searchForm label:nth-of-type(2)', t("location"));
  setLabelText('#searchForm label:nth-of-type(3)', t("checkIn"));
  setLabelText('#searchForm label:nth-of-type(4)', t("checkOut"));
  setLabelText('#searchForm label:nth-of-type(5)', t("maxPrice"));
  setText('#searchForm button[type="submit"]', t("search"));
  setText("#browse .section-head h2", t("availableStays"));
  setText("#resultsMeta", t("liveAvailability"));
  setText("#loadReviewsBtn", t("showReviews"));
  setText("#reviewPanel h3", t("guestReviews"));
  setText("#reviews .section-head h2", t("myReviews"));
  setText("#reviews .section-head p", t("reservedOnly"));
  setText("#reviewForm button", t("addReview"));
  setText("#notifications .section-head h2", t("notifications"));
  setText("#notifications .section-head p", t("notificationsHelp"));
  setText("#loadNotificationsBtn", t("loadNotifications"));
  const comment = qs('#reviewForm input[name="comment"]');
  if (comment) comment.placeholder = t("shareStay");
  renderHotels();
  if (state.rooms.length) renderRooms(state.rooms);
  updateRoleUI();
}

function switchView(viewName) {
  qsa(".view").forEach((view) => view.classList.toggle("active-view", view.id === viewName));
  qsa(".nav-tab").forEach((tab) => tab.classList.toggle("active", tab.dataset.view === viewName));
  if (viewName === "reviews") refreshClientReviewSelectors();
  if (viewName === "stats") loadStat("room", "availability");
  if (viewName === "users") loadUsers();
  if (viewName === "notifications") loadNotifications();
  if (viewName === "reservations") loadReservations();
  if (viewName === "rooms") loadRoomsForEmployee();
}

function renderHotels() {
  const select = qs("#hotelFilter");
  select.innerHTML = `<option value="">${t("allHotels")}</option>`;
  const roomSelect = qs("#roomHotelFilter");
  if (roomSelect) roomSelect.innerHTML = `<option value="">${t("allHotels")}</option>`;
  state.hotels.forEach((hotel) => {
    select.insertAdjacentHTML("beforeend", `<option value="${hotel.id}">${hotel.name} - ${hotel.location}</option>`);
    if (roomSelect) roomSelect.insertAdjacentHTML("beforeend", `<option value="${hotel.id}">${hotel.name} - ${hotel.location}</option>`);
  });

  qs("#hotelHighlights").innerHTML = state.hotels.map((hotel) => `
    <article class="hotel-card">
      <img src="${hotelImages[hotel.id] || hotelImages[1]}" alt="${hotel.name}">
      <div class="card-body">
        <h3>${hotel.name}</h3>
        <div class="muted">${hotel.location}</div>
      </div>
    </article>
  `).join("");
}

function renderRooms(rooms) {
  rooms = sortRooms(rooms);
  qs("#resultsMeta").textContent = `${rooms.length} rooms found`;
  qs("#roomGrid").innerHTML = rooms.map((room) => {
    const hotel = hotelById(room.hotel_id);
    const available = Boolean(room.is_available);
    return `
      <article class="room-card">
        <img src="${roomImage(room)}" alt="Room ${room.room_number}">
        <div class="card-body">
          <h3>${hotel?.name || `Hotel ${room.hotel_id}`} - Room ${room.room_number}</h3>
          <div class="muted">${room.location} · ${room.position || "view"}</div>
          <div class="meta-row">
            <span class="pill ${available ? "" : "no"}">${available ? "Available" : "Available: No"}</span>
            <span class="pill">${room.facilities || "standard"}</span>
          </div>
          <div class="price-line">
            <span class="price">${money(room.price_per_night)}</span>
            <button class="light-btn" data-room-reviews="${room.id}">Reviews</button>
          </div>
        </div>
      </article>
    `;
  }).join("");
}

function renderRoomTable() {
  renderTable("#roomTable", state.adminRooms, [
    "id", "hotel_id", "room_number", "location", "floor", "room_type", "price_per_night", "position", "facilities", "image_urls", "is_available", "max_guests",
  ]);
}

function renderReviews(container, reviews) {
  qs(container).innerHTML = reviews.length
    ? reviews.map((review) => `
      <article class="review-item">
        <strong>${review.client_name || "Guest"} · ${review.rating}/5</strong>
        <p>${review.comment || ""}</p>
        <span class="muted">Room ${review.room_id}</span>
      </article>
    `).join("")
    : `<article class="review-item">${t("noReviews")}</article>`;
}

function renderTable(container, rows, columns) {
  qs(container).innerHTML = `
    <table>
      <thead><tr>${columns.map((column) => `<th>${column}</th>`).join("")}</tr></thead>
      <tbody>
        ${rows.map((row, index) => `<tr data-row-index="${index}">${columns.map((column) => `<td>${row[column] ?? ""}</td>`).join("")}</tr>`).join("")}
      </tbody>
    </table>
  `;
}

function fillForm(formSelector, values) {
  const form = qs(formSelector);
  Object.entries(values).forEach(([key, value]) => {
    const field = form.elements[key];
    if (field) field.value = value ?? "";
  });
}

async function loadInitialData() {
  qs("#checkInFilter").value = today();
  qs("#checkOutFilter").value = today(1);
  state.hotels = await api("hotel");
  renderHotels();
  await searchRooms();
}

async function searchRooms() {
  const params = {
    hotel_id: qs("#hotelFilter").value,
    location: qs("#locationFilter").value,
    price_max: qs("#priceFilter").value,
    check_in: qs("#checkInFilter").value,
    check_out: qs("#checkOutFilter").value,
  };
  state.rooms = sortRooms(await api("room", "", { params }));
  renderRooms(state.rooms);
}

async function loadRoomsForEmployee() {
  const params = { hotel_id: qs("#roomHotelFilter").value };
  state.adminRooms = sortRooms(await api("room", "", { params }));
  renderRoomTable();
}

async function loadReviews(roomId = "") {
  state.reviews = await api("review", "", { params: { room_id: roomId } });
  renderReviews("#reviewList", state.reviews);
  qs("#reviewPanel").classList.remove("hidden");
}

async function login(username, password) {
  const result = await api("user", "login", { method: "POST", body: { username, password } });
  state.currentUser = result.user;
  updateRoleUI();
  toast("Signed in successfully.");
}

async function signup(data) {
  const existing = await api("user", "", { params: { username: data.username } });
  if (existing.length) throw new Error("Username already exists.");
  const user = await api("user", "", {
    method: "POST",
    body: { ...data, role: "client", is_active: true },
  });
  state.currentUser = user;
  updateRoleUI();
  toast("Account created.");
}

function reservationBelongsToCurrentClient(reservation) {
  if (!state.currentUser) return false;
  const currentId = String(state.currentUser.id);
  const currentEmail = normalize(state.currentUser.email);
  const currentName = normalize(state.currentUser.full_name || state.currentUser.username);
  return String(reservation.client_id) === currentId
    || (currentEmail && normalize(reservation.client_email) === currentEmail)
    || (currentName && normalize(reservation.client_name) === currentName);
}

async function getOrCreateReservationClient(data) {
  const clients = await api("user", "", { params: { role: "client" } });
  const byEmail = clients.find((user) => data.client_email && String(user.email).toLowerCase() === String(data.client_email).toLowerCase());
  if (byEmail) return byEmail;

  let username = sanitizeUsername(data.client_email || data.client_name);
  const sameUsername = await api("user", "", { params: { username } });
  if (sameUsername.length) username = `${username}${Date.now().toString().slice(-4)}`;

  const password = data.client_phone || "client123";
  const created = await api("user", "", {
    method: "POST",
    body: {
      username,
      password,
      role: "client",
      full_name: data.client_name || username,
      email: data.client_email || "",
      phone: data.client_phone || "",
      is_active: true,
    },
  });
  console.info(`[HotelChain] Client nou creat pentru rezervare: username=${username}, password=${password}`);
  toast(`Client account created: ${username} / ${password}`);
  return created;
}

async function loadReservations() {
  state.reservations = await api("reservation");
  renderTable("#reservationTable", state.reservations, [
    "id", "hotel_id", "room_id", "client_name", "client_email", "client_phone", "start_date", "end_date", "status",
  ]);
}

async function refreshClientReviewSelectors() {
  const hotelSelect = qs("#reviewHotelSelect");
  const roomSelect = qs("#reviewRoomSelect");
  if (!state.currentUser || state.currentUser.role !== "client") {
    hotelSelect.innerHTML = `<option>${t("signIn")}</option>`;
    roomSelect.innerHTML = `<option>${t("noReservedRooms")}</option>`;
    return;
  }
  const allReservations = await api("reservation");
  const reservations = allReservations.filter(reservationBelongsToCurrentClient);
  const rooms = await api("room");
  const hotelIds = [...new Set(reservations.map((reservation) => String(reservation.hotel_id)))];
  hotelSelect.innerHTML = hotelIds.map((id) => {
    const hotel = hotelById(id);
    return `<option value="${id}">${hotel?.name || `Hotel ${id}`}</option>`;
  }).join("") || `<option value="">${t("noReservedHotels")}</option>`;

  function refreshRoomsForHotel() {
    const hotelId = hotelSelect.value;
    const roomIds = new Set(reservations.filter((reservation) => String(reservation.hotel_id) === String(hotelId)).map((reservation) => String(reservation.room_id)));
    roomSelect.innerHTML = rooms
      .filter((room) => roomIds.has(String(room.id)))
      .map((room) => `<option value="${room.id}">Room ${room.room_number} - ${room.position}</option>`)
      .join("") || `<option value="">${t("noReservedRooms")}</option>`;
  }

  hotelSelect.onchange = refreshRoomsForHotel;
  refreshRoomsForHotel();
  const myReviews = await api("review");
  renderReviews("#myReviewList", myReviews.filter((review) => String(review.client_id) === String(state.currentUser.id)));
}

async function loadStat(service, criterion) {
  const data = await api(service, `statistics/${criterion}`);
  qs("#statsGrid").innerHTML = Object.entries(data).map(([key, value]) => `
    <article class="stat-card">
      <span>${key}</span>
      <strong>${value}</strong>
    </article>
  `).join("");
}

async function loadUsers() {
  const role = qs("#userRoleFilter").value;
  state.users = await api("user", "", { params: { role } });
  renderTable("#userTable", state.users, ["id", "username", "role", "full_name", "email", "phone", "is_active"]);
}

async function loadNotifications() {
  const params = state.currentUser?.role === "client" ? { user_id: state.currentUser.id } : {};
  const rows = await api("notification", "", { params });
  renderTable("#notificationTable", rows, ["id", "user_id", "channel", "recipient", "message", "status", "created_at"]);
}

function bindEvents() {
  qs("#languageSelect").addEventListener("change", (event) => {
    state.language = event.target.value;
    applyTranslations();
    if (qs("#reviews").classList.contains("active-view")) {
      refreshClientReviewSelectors().catch((error) => toast(error.message));
    }
  });
  qsa(".nav-tab").forEach((tab) => tab.addEventListener("click", () => switchView(tab.dataset.view)));
  qs("#searchForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try { await searchRooms(); } catch (error) { toast(error.message); }
  });
  qs("#hotelFilter").addEventListener("change", async () => {
    qs("#locationFilter").value = "";
    qs("#priceFilter").value = "";
    try { await searchRooms(); } catch (error) { toast(error.message); }
  });
  qs("#roomGrid").addEventListener("click", async (event) => {
    const button = event.target.closest("[data-room-reviews]");
    if (!button) return;
    try { await loadReviews(button.dataset.roomReviews); } catch (error) { toast(error.message); }
  });
  qs("#loadReviewsBtn").addEventListener("click", () => loadReviews().catch((error) => toast(error.message)));
  qs("#openLoginBtn").addEventListener("click", () => qs("#loginDialog").showModal());
  qs("#openSignupBtn").addEventListener("click", () => qs("#signupDialog").showModal());
  qs("#logoutBtn").addEventListener("click", () => {
    state.currentUser = null;
    updateRoleUI();
    switchView("browse");
    toast("Signed out.");
  });
  qs("#loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = formData(event.currentTarget);
    try {
      await login(data.username, data.password);
      qs("#loginDialog").close();
    } catch (error) { toast(error.message); }
  });
  qs("#signupForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await signup(formData(event.currentTarget));
      qs("#signupDialog").close();
    } catch (error) { toast(error.message); }
  });
  qs("#reservationForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = formData(event.currentTarget);
    try {
      const client = await getOrCreateReservationClient(data);
      await api("reservation", "", { method: "POST", body: { ...data, client_id: client.id, status: "reserved", total_price: 0 } });
      toast("Reservation created.");
      await loadReservations();
      await searchRooms();
    } catch (error) { toast(error.message); }
  });
  qs("#exportReservationsBtn").addEventListener("click", async () => {
    try {
      const fmt = qs("#reservationExportFormat").value;
      const result = await api("reservation", `export/${fmt}`);
      toast(`Export saved: ${result.path}`);
    } catch (error) { toast(error.message); }
  });
  qsa("[data-room-action]").forEach((button) => button.addEventListener("click", async () => {
    const form = qs("#roomForm");
    const data = formData(form);
    const payload = {
      hotel_id: Number(data.hotel_id || 1),
      room_number: data.room_number || "",
      location: data.location || "",
      floor: Number(data.floor || 1),
      room_type: data.room_type || "Single",
      price_per_night: Number(data.price_per_night || 0),
      position: data.position || "",
      facilities: data.facilities || "",
      image_urls: data.image_urls || "",
      is_available: data.is_available === "true",
      max_guests: Number(data.max_guests || 1),
    };
    try {
      if (button.dataset.roomAction === "create") await api("room", "", { method: "POST", body: payload });
      if (button.dataset.roomAction === "update") await api("room", data.id, { method: "PUT", body: payload });
      if (button.dataset.roomAction === "delete") await api("room", data.id, { method: "DELETE" });
      toast("Room operation completed.");
      await searchRooms();
      await loadRoomsForEmployee();
    } catch (error) { toast(error.message); }
  }));
  qs("#loadRoomsBtn").addEventListener("click", () => loadRoomsForEmployee().catch((error) => toast(error.message)));
  qs("#roomHotelFilter").addEventListener("change", () => loadRoomsForEmployee().catch((error) => toast(error.message)));
  qs("#roomTable").addEventListener("click", (event) => {
    const row = event.target.closest("tr[data-row-index]");
    if (!row) return;
    const room = state.adminRooms[Number(row.dataset.rowIndex)];
    if (!room) return;
    fillForm("#roomForm", room);
    toast(`Selected room ${room.room_number}.`);
  });
  qs("#reviewForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    const data = formData(event.currentTarget);
    try {
      await api("review", "", {
        method: "POST",
        body: {
          room_id: Number(qs("#reviewRoomSelect").value),
          client_id: Number(state.currentUser.id),
          client_name: state.currentUser.full_name || state.currentUser.username,
          client_email: state.currentUser.email || "",
          rating: Number(data.rating || 5),
          comment: data.comment || "Great stay.",
          created_at: today(),
        },
      });
      toast("Review added.");
      await refreshClientReviewSelectors();
    } catch (error) { toast(error.message); }
  });
  qsa("[data-stat]").forEach((button) => button.addEventListener("click", () => {
    loadStat(button.dataset.statService, button.dataset.stat).catch((error) => toast(error.message));
  }));
  qs("#loadUsersBtn").addEventListener("click", () => loadUsers().catch((error) => toast(error.message)));
  qs("#exportUsersBtn").addEventListener("click", async () => {
    try {
      const fmt = qs("#userExportFormat").value;
      const result = await api("user", `export/${fmt}`, { params: { role: qs("#userRoleFilter").value } });
      toast(`Export saved: ${result.path}`);
    } catch (error) { toast(error.message); }
  });
  qs("#userTable").addEventListener("click", (event) => {
    const row = event.target.closest("tr[data-row-index]");
    if (!row) return;
    const user = state.users[Number(row.dataset.rowIndex)];
    if (!user) return;
    fillForm("#userForm", user);
    console.info("[HotelChain] User selected for edit:", user);
    toast(`Selected user ${user.username}.`);
  });
  qsa("[data-user-action]").forEach((button) => button.addEventListener("click", async () => {
    const data = formData(qs("#userForm"));
    let password = data.password;
    if (button.dataset.userAction === "update" && !password) {
      const existing = state.users.find((user) => String(user.id) === String(data.id));
      password = existing?.password || "1234";
    }
    const payload = {
      username: data.username,
      password: password || "1234",
      role: data.role || "client",
      full_name: data.full_name || "",
      email: data.email || "",
      phone: data.phone || "",
      is_active: true,
    };
    try {
      if (button.dataset.userAction === "create") await api("user", "", { method: "POST", body: payload });
      if (button.dataset.userAction === "update") await api("user", data.id, { method: "PUT", body: payload });
      if (button.dataset.userAction === "delete") await api("user", data.id, { method: "DELETE" });
      toast("User operation completed.");
      await loadUsers();
      await loadNotifications();
    } catch (error) { toast(error.message); }
  }));
  qs("#loadNotificationsBtn").addEventListener("click", () => loadNotifications().catch((error) => toast(error.message)));
}

async function boot() {
  bindEvents();
  applyTranslations();
  updateRoleUI();
  try {
    await loadInitialData();
  } catch (error) {
    toast(`Start backend first: ${error.message}`);
  }
}

boot();
