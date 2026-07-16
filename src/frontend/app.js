// ========================
// APPLICATION STATE
// ========================
let currentUser = null;
let currentBooking = null;
let activeTab = 'flights';

// ========================
// SEARCH FORM TEMPLATES
// ========================
const formTemplates = {
    flights: `
        <div class="search-form">
            <div class="mmt-input-block">
                <span class="mmt-label">FROM</span>
                <input type="text" id="flight-origin" placeholder="Delhi, Mumbai..." list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">TO</span>
                <input type="text" id="flight-dest" placeholder="Goa, Bangalore..." list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">DEPARTURE DATE</span>
                <input type="date" id="flight-date">
            </div>
            <div class="mmt-input-block" style="max-width: 160px;">
                <span class="mmt-label">SORT BY</span>
                <select id="flight-sort">
                    <option value="">Recommended</option>
                    <option value="price_asc">Price: Low to High</option>
                    <option value="price_desc">Price: High to Low</option>
                </select>
            </div>
            <button type="button" class="btn-search" onclick="searchData('flights')">
                <i class="fa-solid fa-magnifying-glass"></i> SEARCH
            </button>
        </div>
    `,
    hotels: `
        <div class="search-form">
            <div class="mmt-input-block">
                <span class="mmt-label">CITY OR PROPERTY</span>
                <input type="text" id="hotel-loc" placeholder="Goa, Mumbai, Delhi..." list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">CHECK-IN</span>
                <input type="date" id="hotel-checkin">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">CHECK-OUT</span>
                <input type="date" id="hotel-checkout">
            </div>
            <div class="mmt-input-block" style="max-width: 160px;">
                <span class="mmt-label">SORT BY</span>
                <select id="hotel-sort">
                    <option value="">Recommended</option>
                    <option value="price_asc">Price: Low to High</option>
                    <option value="price_desc">Price: High to Low</option>
                </select>
            </div>
            <button type="button" class="btn-search" onclick="searchData('hotels')">
                <i class="fa-solid fa-magnifying-glass"></i> SEARCH
            </button>
        </div>
    `,
    buses: `
        <div class="search-form">
            <div class="mmt-input-block">
                <span class="mmt-label">FROM</span>
                <input type="text" id="bus-origin" placeholder="Delhi, Pune..." list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">TO</span>
                <input type="text" id="bus-dest" placeholder="Manali, Goa..." list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">DATE OF JOURNEY</span>
                <input type="date" id="bus-date">
            </div>
            <button type="button" class="btn-search" onclick="searchData('buses')">
                <i class="fa-solid fa-magnifying-glass"></i> SEARCH
            </button>
        </div>
    `,
    cabs: `
        <div class="search-form">
            <div class="mmt-input-block">
                <span class="mmt-label">PICKUP LOCATION</span>
                <input type="text" placeholder="Enter pickup city" list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">DROP LOCATION</span>
                <input type="text" placeholder="Enter drop city" list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">PICKUP DATE & TIME</span>
                <input type="datetime-local">
            </div>
            <button type="button" class="btn-search" onclick="searchData('cabs')">
                <i class="fa-solid fa-magnifying-glass"></i> SEARCH
            </button>
        </div>
    `,
    packages: `
        <div class="search-form">
            <div class="mmt-input-block">
                <span class="mmt-label">WHERE TO?</span>
                <input type="text" id="package-dest" placeholder="Goa, Manali, Dubai..." list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">TRAVEL MONTH</span>
                <input type="month">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">TRAVELERS</span>
                <select>
                    <option>1 Traveler</option>
                    <option>2 Travelers</option>
                    <option>3 Travelers</option>
                    <option>4+ Travelers</option>
                </select>
            </div>
            <button type="button" class="btn-search" onclick="searchData('packages')">
                <i class="fa-solid fa-magnifying-glass"></i> SEARCH
            </button>
        </div>
    `,
    trains: `
        <div class="search-form">
            <div class="mmt-input-block">
                <span class="mmt-label">FROM STATION</span>
                <input type="text" placeholder="Delhi, Mumbai..." list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">TO STATION</span>
                <input type="text" placeholder="Goa, Chennai..." list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">TRAVEL DATE</span>
                <input type="date">
            </div>
            <button type="button" class="btn-search" onclick="alert('Train booking powered by IRCTC — integration coming soon!')">
                <i class="fa-solid fa-magnifying-glass"></i> SEARCH
            </button>
        </div>
    `
};

// ========================
// INIT
// ========================
document.addEventListener('DOMContentLoaded', () => {
    switchTab('flights', document.querySelector('.tab-btn'));
    fetchLocations();
    
    // Set today's date as default on date fields
    const today = new Date().toISOString().split('T')[0];
    setTimeout(() => {
        ['flight-date', 'hotel-checkin', 'hotel-checkout', 'bus-date'].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = today;
        });
    }, 50);
});

function switchTab(target, btnEl) {
    activeTab = target;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');
    
    const container = document.getElementById('form-container');
    container.innerHTML = formTemplates[target] || '<p style="padding:20px;text-align:center;color:#64748b">Coming soon!</p>';
    
    // Set today's date as default
    const today = new Date().toISOString().split('T')[0];
    setTimeout(() => {
        ['flight-date', 'hotel-checkin', 'hotel-checkout', 'bus-date'].forEach(id => {
            const el = document.getElementById(id);
            if (el && !el.value) el.value = today;
        });
    }, 50);
}

// ========================
// LOCATIONS AUTOCOMPLETE
// ========================
function fetchLocations() {
    fetch('/api/locations')
        .then(r => r.json())
        .then(data => {
            const datalist = document.getElementById('locations-list');
            if (!datalist) return;
            datalist.innerHTML = '';
            (data.locations || []).forEach(loc => {
                const opt = document.createElement('option');
                opt.value = loc;
                datalist.appendChild(opt);
            });
        })
        .catch(err => console.warn('Could not fetch locations', err));
}

// ========================
// SEARCH
// ========================
function searchData(type) {
    let url = '/api/' + type + '?';
    
    if (type === 'flights') {
        const orig = (document.getElementById('flight-origin') || {}).value || '';
        const dest = (document.getElementById('flight-dest') || {}).value || '';
        const sort = (document.getElementById('flight-sort') || {}).value || '';
        if (orig) url += 'origin=' + encodeURIComponent(orig) + '&';
        if (dest) url += 'destination=' + encodeURIComponent(dest) + '&';
        if (sort) url += 'sort=' + sort + '&';
    } else if (type === 'hotels') {
        const loc = (document.getElementById('hotel-loc') || {}).value || '';
        const sort = (document.getElementById('hotel-sort') || {}).value || '';
        if (loc) url += 'location=' + encodeURIComponent(loc) + '&';
        if (sort) url += 'sort=' + sort + '&';
    } else if (type === 'buses') {
        const orig = (document.getElementById('bus-origin') || {}).value || '';
        const dest = (document.getElementById('bus-dest') || {}).value || '';
        if (orig) url += 'origin=' + encodeURIComponent(orig) + '&';
        if (dest) url += 'destination=' + encodeURIComponent(dest) + '&';
    } else if (type === 'cabs') {
        // Just get all cabs
    } else if (type === 'packages') {
        const dest = (document.getElementById('package-dest') || {}).value || '';
        if (dest) url += 'destination=' + encodeURIComponent(dest) + '&';
    }

    // Show results section
    document.getElementById('results-section').style.display = 'block';
    document.getElementById('results-grid').innerHTML = '';
    document.getElementById('loader').style.display = 'flex';
    document.getElementById('results-title').innerText = 'Searching...';
    document.getElementById('results-subtitle').innerText = '';
    
    // Smooth scroll to results
    document.getElementById('results-section').scrollIntoView({ behavior: 'smooth', block: 'start' });

    fetch(url)
        .then(res => {
            if (!res.ok) return res.json().then(e => Promise.reject(e));
            return res.json();
        })
        .then(data => {
            document.getElementById('loader').style.display = 'none';
            if (data && data.error) {
                showError(data.error);
                return;
            }
            const results = Array.isArray(data) ? data : [];
            displayResults(type, results);
        })
        .catch(err => {
            document.getElementById('loader').style.display = 'none';
            showError(err.error || 'Search failed. Please try again.');
        });
}

function showError(msg) {
    document.getElementById('results-title').innerText = 'Something went wrong';
    document.getElementById('results-grid').innerHTML = `
        <div class="no-results" style="grid-column:1/-1">
            <i class="fa-solid fa-triangle-exclamation" style="color:#ef4444"></i>
            <h3>Oops!</h3>
            <p>${msg}</p>
        </div>`;
}

function hideResults() {
    document.getElementById('results-section').style.display = 'none';
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ========================
// DISPLAY RESULTS
// ========================
function displayResults(type, data) {
    const grid = document.getElementById('results-grid');
    const title = document.getElementById('results-title');
    const subtitle = document.getElementById('results-subtitle');
    grid.innerHTML = '';

    const typeLabel = { flights: 'Flights', hotels: 'Hotels', buses: 'Buses', cabs: 'Cabs', packages: 'Packages' }[type] || type;

    if (!data || data.length === 0) {
        title.innerText = 'No results found';
        subtitle.innerText = 'Try searching with different criteria or browse all options below';
        grid.innerHTML = `
            <div class="no-results" style="grid-column:1/-1">
                <i class="fa-solid fa-magnifying-glass"></i>
                <h3>No ${typeLabel} Found</h3>
                <p>Try with different cities or remove filters to see all available options.</p>
                <button class="btn-search" style="margin-top:20px" onclick="searchData('${type}')">Show All ${typeLabel}</button>
            </div>`;
        return;
    }

    title.innerText = `${data.length} ${typeLabel} Found`;
    subtitle.innerText = 'Sorted by best match · Prices include taxes & fees';

    data.forEach(item => {
        const card = createCard(type, item);
        grid.appendChild(card);
    });
}

function createCard(type, item) {
    const div = document.createElement('div');
    div.className = 'result-card';

    let price = 0, title = '', html = '';

    if (type === 'flights') {
        price = parseFloat(item.price) || 0;
        title = item.airline;
        const dep = item.departure_time ? new Date(item.departure_time) : null;
        const arr = item.arrival_time ? new Date(item.arrival_time) : null;
        const depTime = dep ? dep.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) : '--';
        const arrTime = arr ? arr.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit' }) : '--';
        html = `
            <div class="card-top">
                <div class="card-airline-row">
                    <div class="card-airline-name">
                        <div class="card-icon"><i class="fa-solid fa-plane"></i></div>
                        ${item.airline}
                    </div>
                    <div class="card-price">&#8377;${price.toLocaleString('en-IN')}</div>
                </div>
                <div class="card-route">
                    <div><div class="city">${item.origin}</div><div class="time">${depTime}</div></div>
                    <div class="route-arrow"><i class="fa-solid fa-arrow-right-long"></i><span>${item.duration || '~2h'}</span></div>
                    <div style="text-align:right"><div class="city">${item.destination}</div><div class="time">${arrTime}</div></div>
                </div>
                <div class="card-meta">
                    <span class="card-badge">${item.class_type || 'Economy'}</span>
                    <span class="card-badge green">Non-stop</span>
                </div>
            </div>
            <div class="card-bottom">
                <span style="font-size:0.8rem;color:#64748b">Incl. taxes</span>
                <button class="btn-book" onclick="startCheckout('flights', ${item.id}, ${price}, '${item.airline} — ${item.origin} to ${item.destination}')">Book Now</button>
            </div>`;

    } else if (type === 'hotels') {
        price = parseFloat(item.price_per_night) || 0;
        title = item.name;
        const stars = Math.round(parseFloat(item.rating) || 4);
        const starStr = '★'.repeat(stars) + '☆'.repeat(5 - stars);
        html = `
            <div class="card-top">
                <div class="card-airline-row">
                    <div class="card-airline-name">
                        <div class="card-icon"><i class="fa-solid fa-hotel"></i></div>
                        ${item.name}
                    </div>
                    <div class="card-price">&#8377;${price.toLocaleString('en-IN')}<span class="price-label">/night</span></div>
                </div>
                <div class="card-route" style="justify-content:flex-start;gap:16px">
                    <div><div class="city">${item.location}</div><div class="time">Location</div></div>
                </div>
                <div class="card-meta">
                    <span class="card-badge gold" style="font-size:1rem">${starStr}</span>
                    ${item.amenities ? '<span class="card-badge">' + item.amenities.split(',')[0].trim() + '</span>' : ''}
                </div>
                <p style="font-size:0.8rem;color:#64748b;margin-top:10px;">${item.amenities || ''}</p>
            </div>
            <div class="card-bottom">
                <div class="card-rating"><i class="fa-solid fa-star"></i> ${item.rating}</div>
                <button class="btn-book" onclick="startCheckout('hotels', ${item.id}, ${price}, '${item.name}, ${item.location}')">Book Now</button>
            </div>`;

    } else if (type === 'buses') {
        price = parseFloat(item.price) || 0;
        title = item.operator_name;
        html = `
            <div class="card-top">
                <div class="card-airline-row">
                    <div class="card-airline-name">
                        <div class="card-icon"><i class="fa-solid fa-bus"></i></div>
                        ${item.operator_name}
                    </div>
                    <div class="card-price">&#8377;${price.toLocaleString('en-IN')}</div>
                </div>
                <div class="card-route">
                    <div><div class="city">${item.origin}</div><div class="time">${item.pickup_point || ''}</div></div>
                    <div class="route-arrow"><i class="fa-solid fa-arrow-right-long"></i><span>${item.duration}</span></div>
                    <div style="text-align:right"><div class="city">${item.destination}</div><div class="time">${item.drop_point || ''}</div></div>
                </div>
                <div class="card-meta">
                    <span class="card-badge">${item.bus_type}</span>
                    <span class="card-badge green">AC Available</span>
                </div>
            </div>
            <div class="card-bottom">
                <span style="font-size:0.8rem;color:#64748b">Per Seat</span>
                <button class="btn-book" onclick="startCheckout('buses', ${item.id}, ${price}, '${item.operator_name} — ${item.origin} to ${item.destination}')">Book Now</button>
            </div>`;

    } else if (type === 'cabs') {
        price = parseFloat(item.price_per_km) || 0;
        title = item.type + ' Cab';
        html = `
            <div class="card-top">
                <div class="card-airline-row">
                    <div class="card-airline-name">
                        <div class="card-icon"><i class="fa-solid fa-taxi"></i></div>
                        ${item.type}
                    </div>
                    <div class="card-price">&#8377;${price}<span class="price-label">/km</span></div>
                </div>
                <div class="card-route" style="justify-content:flex-start;gap:24px">
                    <div><div class="city">${item.driver_name || 'Assigned Driver'}</div><div class="time">Driver</div></div>
                    <div><div class="city">${item.availability ? '✅ Available' : '⚠️ Busy'}</div><div class="time">Status</div></div>
                </div>
                <div class="card-meta">
                    <span class="card-badge">Sedan</span>
                    <span class="card-badge green">GPS Tracked</span>
                </div>
            </div>
            <div class="card-bottom">
                <span style="font-size:0.8rem;color:#64748b">Per KM</span>
                <button class="btn-book" onclick="startCheckout('cabs', ${item.id}, ${price * 25}, '${item.type} Cab')">Book Now</button>
            </div>`;

    } else if (type === 'packages') {
        price = parseFloat(item.price) || 0;
        title = item.destination + ' Package';
        html = `
            <div class="card-top">
                <div class="card-airline-row">
                    <div class="card-airline-name">
                        <div class="card-icon"><i class="fa-solid fa-suitcase-rolling"></i></div>
                        ${item.destination}
                    </div>
                    <div class="card-price">&#8377;${price.toLocaleString('en-IN')}</div>
                </div>
                <div class="card-route" style="justify-content:flex-start;gap:24px">
                    <div><div class="city">${item.days} Days</div><div class="time">Duration</div></div>
                </div>
                <div class="card-meta">
                    <span class="card-badge">All Inclusive</span>
                </div>
                <p style="font-size:0.8rem;color:#64748b;margin-top:10px;">${item.includes || ''}</p>
            </div>
            <div class="card-bottom">
                <span style="font-size:0.8rem;color:#64748b">Per Person</span>
                <button class="btn-book" onclick="startCheckout('packages', ${item.id}, ${price}, '${item.destination} Package — ${item.days} Days')">Book Now</button>
            </div>`;
    }

    div.innerHTML = html;
    return div;
}

// ========================
// CHECKOUT
// ========================
function startCheckout(service_type, service_id, price, title) {
    if (!currentUser) {
        showModal('login');
        return;
    }
    
    currentBooking = { service_type, service_id, price };
    
    document.getElementById('main-view').style.display = 'none';
    document.getElementById('results-section').style.display = 'none';
    document.getElementById('success-view').style.display = 'none';
    document.getElementById('checkout-view').style.display = 'block';
    
    document.getElementById('booking-summary').innerHTML = `
        <div style="font-size:0.9rem;opacity:0.9">${title}</div>
        <span class="price-highlight">&#8377;${parseFloat(price).toLocaleString('en-IN')}</span>
    `;
    
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function goBackToSearch() {
    document.getElementById('checkout-view').style.display = 'none';
    document.getElementById('success-view').style.display = 'none';
    document.getElementById('main-view').style.display = 'block';
    document.getElementById('results-section').style.display = 'block';
    currentBooking = null;
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Payment method toggle
function showPaymentForm(type) {
    ['card', 'upi', 'netbanking'].forEach(t => {
        const el = document.getElementById('payment-fields-' + t);
        if (el) el.style.display = t === type ? 'block' : 'none';
        const lbl = document.getElementById('pm-' + t);
        if (lbl) lbl.classList.toggle('active', t === type);
    });
}

function selectUpi(el, app) {
    document.querySelectorAll('.upi-app-btn').forEach(b => b.classList.remove('selected'));
    el.classList.add('selected');
}

function formatCard(input) {
    let val = input.value.replace(/\D/g, '').substring(0, 16);
    input.value = val.replace(/(.{4})/g, '$1 ').trim();
}

// Payment form submission
function submitPayment(e) {
    e.preventDefault();
    if (!currentBooking || !currentUser) return;
    
    const btn = document.getElementById('pay-btn');
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Processing...';
    btn.disabled = true;
    
    const payload = {
        user_id: currentUser.id,
        service_type: currentBooking.service_type,
        service_id: currentBooking.service_id,
        total_price: currentBooking.price
    };
    
    fetch('/api/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        btn.innerHTML = '<i class="fa-solid fa-shield-halved"></i> Pay Securely';
        btn.disabled = false;
        if (data.success) {
            document.getElementById('checkout-view').style.display = 'none';
            document.getElementById('success-view').style.display = 'block';
            document.getElementById('booking-id-display').innerText = '#TB-' + String(data.booking_id).padStart(6, '0');
        } else {
            alert('Booking failed: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(() => {
        btn.innerHTML = '<i class="fa-solid fa-shield-halved"></i> Pay Securely';
        btn.disabled = false;
        alert('Network error. Please try again.');
    });
}

// ========================
// MODAL & AUTH
// ========================
function showModal(type) {
    document.getElementById(type + '-modal').classList.add('active');
}

function closeModal(type) {
    document.getElementById(type + '-modal').classList.remove('active');
}

function closeModalOutside(e) {
    if (e.target === e.currentTarget) closeModal('login');
}

function switchAuthTab(tab) {
    document.getElementById('auth-error').style.display = 'none';
    if (tab === 'login') {
        document.getElementById('login-form').style.display = 'block';
        document.getElementById('signup-form').style.display = 'none';
        document.getElementById('tab-login').classList.add('active');
        document.getElementById('tab-signup').classList.remove('active');
    } else {
        document.getElementById('login-form').style.display = 'none';
        document.getElementById('signup-form').style.display = 'block';
        document.getElementById('tab-login').classList.remove('active');
        document.getElementById('tab-signup').classList.add('active');
    }
}

function handleAuth(e, type) {
    e.preventDefault();
    const errorDiv = document.getElementById('auth-error');
    errorDiv.style.display = 'none';
    
    const url = type === 'login' ? '/api/login' : '/api/register';
    let payload = {};
    
    if (type === 'login') {
        payload.email = document.getElementById('login-email').value;
        payload.password = document.getElementById('login-password').value;
    } else {
        payload.name = document.getElementById('signup-name').value;
        payload.email = document.getElementById('signup-email').value;
        payload.password = document.getElementById('signup-password').value;
    }
    
    const btn = e.target.querySelector('button[type="submit"]');
    btn.innerText = 'Please wait...';
    btn.disabled = true;
    
    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        btn.disabled = false;
        btn.innerText = type === 'login' ? 'Login' : 'Create Account';
        
        if (data.error) {
            errorDiv.innerText = data.error;
            errorDiv.style.display = 'block';
        } else {
            currentUser = data;
            closeModal('login');
            const initials = (data.name || 'U').split(' ').map(n => n[0]).join('').toUpperCase().substring(0, 2);
            document.getElementById('user-section').innerHTML = `
                <div class="user-logged-in">
                    <div class="user-avatar">${initials}</div>
                    <span style="font-weight:600;font-size:0.9rem">Hi, ${data.name.split(' ')[0]}!</span>
                    <button class="btn-logout" onclick="logout()">Logout</button>
                </div>`;
        }
    })
    .catch(() => {
        btn.disabled = false;
        btn.innerText = type === 'login' ? 'Login' : 'Create Account';
        errorDiv.innerText = 'Network error. Please try again.';
        errorDiv.style.display = 'block';
    });
}

function logout() {
    currentUser = null;
    document.getElementById('user-section').innerHTML = `
        <button class="btn-login" onclick="showModal('login')">
            <i class="fa-regular fa-user"></i> Login / Signup
        </button>`;
    goBackToSearch();
}

// ========================
// SUPPORT CHAT
// ========================
let supportOpen = false;

function openSupport() {
    const panel = document.getElementById('support-panel');
    panel.classList.add('open');
    supportOpen = true;
    document.getElementById('support-fab-icon').className = 'fa-solid fa-xmark';
    document.getElementById('support-fab').onclick = closeSupport;
    setTimeout(() => document.getElementById('support-input').focus(), 300);
}

function closeSupport() {
    document.getElementById('support-panel').classList.remove('open');
    supportOpen = false;
    document.getElementById('support-fab-icon').className = 'fa-solid fa-headset';
    document.getElementById('support-fab').onclick = openSupport;
}

function addSupportMsg(text, isUser) {
    const body = document.getElementById('support-chat-body');
    const div = document.createElement('div');
    div.className = 'support-msg' + (isUser ? ' support-msg-user' : '');
    div.innerHTML = isUser
        ? '<div class="support-bubble">' + text + '</div>'
        : '<div class="support-avatar"><i class="fa-solid fa-robot"></i></div><div class="support-bubble">' + text + '</div>';
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
}

function showTyping() {
    const body = document.getElementById('support-chat-body');
    const div = document.createElement('div');
    div.className = 'support-msg support-typing';
    div.id = 'typing-indicator';
    div.innerHTML = '<div class="support-avatar"><i class="fa-solid fa-robot"></i></div><div class="support-bubble"><div class="dot-typing"></div><div class="dot-typing"></div><div class="dot-typing"></div></div>';
    body.appendChild(div);
    body.scrollTop = body.scrollHeight;
}

function removeTyping() {
    const el = document.getElementById('typing-indicator');
    if (el) el.remove();
}

const botReplies = {
    'track': 'To track your booking, please go to <strong>My Trips</strong> in the top nav. You can view all your confirmed bookings there with the Booking ID.',
    'booking': 'Your booking ID is shown on the confirmation screen. You can also find it in <strong>My Trips</strong>. Need help with a specific booking ID?',
    'cancel': 'Cancellations are allowed up to 24 hours before travel. You will receive a full refund to your original payment method within 5-7 business days. To cancel, go to <strong>My Trips</strong> and click Cancel.',
    'refund': 'Refunds are processed within 5-7 business days to your original payment method. Card refunds may take up to 10 days depending on your bank.',
    'payment': 'We accept Credit/Debit Cards, UPI (Google Pay, PhonePe, Paytm), and Net Banking. If your payment failed, please try again or use a different method.',
    'change': 'Flight changes depend on the airline policy. Most Economy tickets allow one free date change. To change your flight, go to <strong>My Trips</strong> and click Modify.',
    'hotel': 'Hotel check-in is usually at 2 PM and check-out by 12 PM. Early check-in and late check-out may be available for an additional charge.',
    'bus': 'Buses typically depart from the listed pickup point. Arrive 15 minutes early. Most buses have charging points and WiFi on board.',
    'support': 'You can reach our 24/7 support team at <strong>support@travelease.in</strong> or call <strong>1800-XXX-XXXX</strong> (toll free).',
    'hello': 'Hello! \uD83D\uDC4B How can I assist you with your travel today?',
    'hi': 'Hi there! \uD83D\uDE0A What can I help you with today?'
};

function getBotReply(msg) {
    const lower = msg.toLowerCase();
    for (const [key, reply] of Object.entries(botReplies)) {
        if (lower.includes(key)) return reply;
    }
    return 'Thanks for reaching out! \uD83D\uDE4F Our support team will get back to you shortly. For urgent queries, call <strong>1800-XXX-XXXX</strong> (toll free, 24/7).';
}

function sendSupportMsg() {
    const input = document.getElementById('support-input');
    const text = input.value.trim();
    if (!text) return;
    input.value = '';

    addSupportMsg(text, true);
    showTyping();

    setTimeout(() => {
        removeTyping();
        addSupportMsg(getBotReply(text), false);
    }, 900 + Math.random() * 600);
}

function quickReply(text) {
    const qr = document.querySelector('.support-quick-replies');
    if (qr) qr.remove();
    addSupportMsg(text, true);
    showTyping();
    setTimeout(() => {
        removeTyping();
        addSupportMsg(getBotReply(text), false);
    }, 900 + Math.random() * 600);
}

// ========================
// MY TRIPS
// ========================
function showMyTrips() {
    const modal = document.getElementById('trips-modal');
    const content = document.getElementById('trips-content');
    modal.classList.add('active');

    if (!currentUser) {
        content.innerHTML = '<div style="text-align:center;padding:32px;"><i class="fa-solid fa-user-lock" style="font-size:2.5rem;color:#94a3b8;margin-bottom:16px;display:block;"></i><p style="color:#64748b;margin-bottom:20px;">Please log in to view your trips.</p><button class="btn-primary" style="width:auto;padding:12px 28px;" onclick="closeModal2(\'trips\'); showModal(\'login\');">Login Now</button></div>';
        return;
    }

    content.innerHTML = '<div style="text-align:center;padding:20px;"><div class="loader-spinner" style="margin:0 auto;"></div></div>';

    // Show last booking if exists
    setTimeout(() => {
        if (currentBooking) {
            content.innerHTML = '<p style="color:#64748b;font-size:0.9rem;">Showing your recent trips.</p>';
        } else {
            content.innerHTML = '<div style="text-align:center;padding:32px;"><i class="fa-solid fa-plane-circle-check" style="font-size:2.5rem;color:#94a3b8;margin-bottom:16px;display:block;"></i><h3 style="margin-bottom:8px;">No trips yet</h3><p style="color:#64748b;margin-bottom:20px;">Start searching for flights, hotels, or buses to plan your next trip!</p><button class="btn-primary" style="width:auto;padding:12px 28px;" onclick="closeModal2(\'trips\');">Search Now</button></div>';
        }
    }, 600);
}

function closeModal2(type) {
    document.getElementById(type + '-modal').classList.remove('active');
}

function closeModalOutside2(e) {
    if (e.target === e.currentTarget) {
        e.currentTarget.classList.remove('active');
    }
}

// ========================
// OFFERS
// ========================
function showOffers() {
    const offers = [
        { title: 'FLAT 20% OFF on Flights', code: 'FLY20', desc: 'Valid on all domestic flights. Min booking &#8377;3000.', icon: 'fa-plane', color: '#1a56db' },
        { title: '&#8377;500 OFF on Hotels', code: 'HOTEL500', desc: 'Use on any hotel booking above &#8377;2500.', icon: 'fa-hotel', color: '#7c3aed' },
        { title: '15% OFF on Buses', code: 'BUS15', desc: 'Get 15% off on all bus bookings. Max discount &#8377;200.', icon: 'fa-bus', color: '#059669' },
        { title: 'FREE Cab on Packages', code: 'PKGCAB', desc: 'Book any holiday package and get a free airport cab.', icon: 'fa-suitcase-rolling', color: '#d97706' },
    ];

    const offerHtml = offers.map(o => `
        <div style="border:1.5px solid #e2e8f0;border-radius:14px;padding:18px 20px;display:flex;align-items:center;gap:16px;">
            <div style="width:48px;height:48px;background:${o.color}15;border-radius:12px;display:flex;align-items:center;justify-content:center;color:${o.color};font-size:1.3rem;flex-shrink:0;">
                <i class="fa-solid ${o.icon}"></i>
            </div>
            <div style="flex:1;">
                <div style="font-weight:700;font-size:0.95rem;margin-bottom:4px;">${o.title}</div>
                <div style="font-size:0.8rem;color:#64748b;margin-bottom:8px;">${o.desc}</div>
                <div style="font-family:monospace;font-weight:700;color:${o.color};background:${o.color}15;padding:4px 12px;border-radius:6px;display:inline-block;font-size:0.85rem;cursor:pointer;" onclick="copyCode('${o.code}', this)">${o.code} <i class="fa-regular fa-copy"></i></div>
            </div>
        </div>`).join('');

    // Build a temporary modal inline
    const existing = document.getElementById('offers-modal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'offers-modal';
    modal.className = 'modal-overlay active';
    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };
    modal.innerHTML = `
        <div class="modal-box" style="max-width:520px;">
            <button class="modal-close" onclick="document.getElementById('offers-modal').remove()"><i class="fa-solid fa-xmark"></i></button>
            <h2 style="margin-bottom:6px;font-size:1.3rem;"><i class="fa-solid fa-tag" style="color:#1a56db"></i> Exclusive Offers</h2>
            <p style="color:#64748b;font-size:0.85rem;margin-bottom:20px;">Use these codes at checkout to save big!</p>
            <div style="display:flex;flex-direction:column;gap:12px;">${offerHtml}</div>
        </div>`;
    document.body.appendChild(modal);
}

function copyCode(code, el) {
    navigator.clipboard.writeText(code).then(() => {
        el.innerHTML = 'Copied! <i class="fa-solid fa-check"></i>';
        setTimeout(() => { el.innerHTML = code + ' <i class="fa-regular fa-copy"></i>'; }, 1500);
    });
}


// ========================
// ADMIN LOGIN
// ========================
function handleAdminLogin(e) {
    e.preventDefault();
    const user = document.getElementById('admin-user').value;
    const pwd = document.getElementById('admin-pwd').value;
    
    if (user === 'admin' && pwd === 'admin123') {
        
        document.getElementById('admin-error').style.display = 'none';
        
        // Fetch Admin Data
        fetch('/api/admin/stats')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert('Error loading dashboard: ' + data.error);
                    return;
                }
                
                closeModal('admin-login');
                
                let recentBookingsHtml = '';
                if (data.recent_bookings && data.recent_bookings.length > 0) {
                    data.recent_bookings.forEach(b => {
                        const dateObj = new Date(b.booking_date);
                        const dateStr = dateObj.toLocaleDateString('en-IN') + ' ' + dateObj.toLocaleTimeString('en-IN', {hour: '2-digit', minute:'2-digit'});
                        recentBookingsHtml += `
                            <tr style="border-bottom: 1px solid rgba(255,255,255,0.1);">
                                <td style="padding: 15px;">#${b.booking_id}</td>
                                <td style="padding: 15px;">${b.user_name}</td>
                                <td style="padding: 15px;">
                                    <span style="background: rgba(37, 99, 235, 0.2); color: #60a5fa; padding: 4px 10px; border-radius: 20px; font-size: 0.85rem;">${b.booking_type}</span>
                                </td>
                                <td style="padding: 15px;">&#8377;${parseFloat(b.amount).toLocaleString('en-IN')}</td>
                                <td style="padding: 15px; color: #94a3b8;">${dateStr}</td>
                            </tr>
                        `;
                    });
                } else {
                    recentBookingsHtml = '<tr><td colspan="5" style="padding: 15px; text-align: center; color: #94a3b8;">No recent bookings found.</td></tr>';
                }

                document.body.innerHTML = `
                    <div style="min-height: 100vh; background: linear-gradient(135deg, #0f172a, #1e293b); color: white; font-family: 'Inter', sans-serif; padding: 40px;">
                        
                        <div style="max-width: 1200px; margin: 0 auto;">
                            <!-- Header -->
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px;">
                                <div>
                                    <h1 style="font-size: 2.5rem; font-weight: 700; margin: 0; background: linear-gradient(90deg, #3b82f6, #8b5cf6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Admin Dashboard</h1>
                                    <p style="color: #94a3b8; margin-top: 5px;">Welcome back, Admin.</p>
                                </div>
                                <button onclick="location.reload()" style="padding: 12px 24px; background: rgba(255, 255, 255, 0.1); color: white; border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 8px; cursor: pointer; font-weight: 600; backdrop-filter: blur(10px); transition: all 0.3s ease;" onmouseover="this.style.background='rgba(255,255,255,0.2)'" onmouseout="this.style.background='rgba(255,255,255,0.1)'">
                                    <i class="fa-solid fa-right-from-bracket"></i> Logout
                                </button>
                            </div>

                            <!-- Stat Cards -->
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-bottom: 40px;">
                                <!-- Total Users -->
                                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px; backdrop-filter: blur(10px);">
                                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                        <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(59, 130, 246, 0.2); color: #3b82f6; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-right: 15px;">
                                            <i class="fa-solid fa-users"></i>
                                        </div>
                                        <h3 style="margin: 0; color: #94a3b8; font-weight: 500; font-size: 1.1rem;">Total Users</h3>
                                    </div>
                                    <div style="font-size: 2.5rem; font-weight: 700;">${data.total_users}</div>
                                </div>
                                
                                <!-- Total Bookings -->
                                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px; backdrop-filter: blur(10px);">
                                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                        <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(16, 185, 129, 0.2); color: #10b981; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-right: 15px;">
                                            <i class="fa-solid fa-ticket"></i>
                                        </div>
                                        <h3 style="margin: 0; color: #94a3b8; font-weight: 500; font-size: 1.1rem;">Total Bookings</h3>
                                    </div>
                                    <div style="font-size: 2.5rem; font-weight: 700;">${data.total_bookings}</div>
                                </div>

                                <!-- Total Revenue -->
                                <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px; backdrop-filter: blur(10px);">
                                    <div style="display: flex; align-items: center; margin-bottom: 15px;">
                                        <div style="width: 48px; height: 48px; border-radius: 12px; background: rgba(139, 92, 246, 0.2); color: #8b5cf6; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; margin-right: 15px;">
                                            <i class="fa-solid fa-wallet"></i>
                                        </div>
                                        <h3 style="margin: 0; color: #94a3b8; font-weight: 500; font-size: 1.1rem;">Total Revenue</h3>
                                    </div>
                                    <div style="font-size: 2.5rem; font-weight: 700;">&#8377;${data.total_revenue.toLocaleString('en-IN')}</div>
                                </div>
                            </div>

                            <!-- Recent Bookings Table -->
                            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px; backdrop-filter: blur(10px);">
                                <h3 style="margin: 0 0 20px 0; font-size: 1.4rem; font-weight: 600;">Recent Transactions</h3>
                                <div style="overflow-x: auto;">
                                    <table style="width: 100%; border-collapse: collapse; text-align: left;">
                                        <thead>
                                            <tr style="border-bottom: 2px solid rgba(255,255,255,0.1); color: #94a3b8;">
                                                <th style="padding: 15px; font-weight: 600;">Booking ID</th>
                                                <th style="padding: 15px; font-weight: 600;">User Name</th>
                                                <th style="padding: 15px; font-weight: 600;">Service Type</th>
                                                <th style="padding: 15px; font-weight: 600;">Amount</th>
                                                <th style="padding: 15px; font-weight: 600;">Date</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${recentBookingsHtml}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            })
            .catch(err => {
                console.error(err);
                alert('Failed to load dashboard data.');
            });

    } else {
        document.getElementById('admin-error').style.display = 'block';
    }
}
