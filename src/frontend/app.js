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
                <div style="display:flex; gap: 8px;">
                    <input type="text" id="cab-pickup" placeholder="Enter street, colony, or city" list="cab-pickup-suggestions" autocomplete="off" oninput="fetchAddressSuggestions(this.value, 'cab-pickup-suggestions')" style="flex:1;">
                    <datalist id="cab-pickup-suggestions"></datalist>
                    <button type="button" class="btn-outline" onclick="openMapModal('cab-pickup')" title="Select on Map" style="padding: 0 14px; border-radius: 6px; font-size: 1.2rem;"><i class="fa-solid fa-map-location-dot"></i></button>
                    <button type="button" class="btn-outline" onclick="useLiveLocation(this)" title="Use Live Location" style="padding: 0 14px; border-radius: 6px; font-size: 1.2rem;"><i class="fa-solid fa-location-crosshairs"></i></button>
                </div>
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">DROP LOCATION</span>
                <div style="display:flex; gap: 8px;">
                    <input type="text" id="cab-drop" placeholder="Enter street, colony, or city" list="cab-drop-suggestions" autocomplete="off" oninput="fetchAddressSuggestions(this.value, 'cab-drop-suggestions')" style="flex:1;">
                    <datalist id="cab-drop-suggestions"></datalist>
                    <button type="button" class="btn-outline" onclick="openMapModal('cab-drop')" title="Select on Map" style="padding: 0 14px; border-radius: 6px; font-size: 1.2rem;"><i class="fa-solid fa-map-location-dot"></i></button>
                </div>
            </div>
            <div class="mmt-input-block" style="min-width: 220px; position: relative;">
                <span class="mmt-label">WHEN</span>
                <div style="display:flex; gap: 15px; height: 50px; align-items: center; border-bottom: 2px solid transparent;">
                    <label style="cursor:pointer; display:flex; align-items:center; gap:5px; font-weight:500; font-size:1.1rem; color:#0f172a;">
                        <input type="radio" name="cab_time_type" value="now" checked onchange="document.getElementById('cab-schedule-time').style.display='none'"> Book Now
                    </label>
                    <label style="cursor:pointer; display:flex; align-items:center; gap:5px; font-weight:500; font-size:1.1rem; color:#0f172a;">
                        <input type="radio" name="cab_time_type" value="schedule" onchange="document.getElementById('cab-schedule-time').style.display='block'"> Schedule
                    </label>
                </div>
                <input type="datetime-local" id="cab-schedule-time" style="display:none; position:absolute; top: 100%; left:0; width: 100%; z-index:10; background:white; border: 1px solid #ccc; box-shadow: 0 4px 6px rgba(0,0,0,0.1); padding: 10px; border-radius: 6px;">
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
                <input type="text" id="train-origin" placeholder="Delhi, Mumbai..." list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">TO STATION</span>
                <input type="text" id="train-dest" placeholder="Goa, Chennai..." list="locations-list" autocomplete="off">
            </div>
            <div class="mmt-input-block">
                <span class="mmt-label">TRAVEL DATE</span>
                <input type="date" id="train-date">
            </div>
            <button type="button" class="btn-search" onclick="showTrainComingSoon()">
                <i class="fa-solid fa-magnifying-glass"></i> SEARCH
            </button>
        </div>
        <div id="train-coming-soon" style="display:none; margin-top:20px; text-align:center; padding:40px 20px; background:linear-gradient(135deg, rgba(220,38,38,0.05), rgba(248,113,113,0.08)); border-radius:16px; border:1.5px dashed rgba(220,38,38,0.3);">
            <i class="fa-solid fa-train" style="font-size:3rem; color:#dc2626; margin-bottom:16px; display:block; animation: float 3s ease-in-out infinite;"></i>
            <h3 style="font-size:1.3rem; color:#1e293b; margin-bottom:8px;">Train Booking Powered by IRCTC</h3>
            <p style="color:#64748b; font-size:0.95rem; margin-bottom:16px;">We're integrating with IRCTC to bring you seamless train bookings.<br>This feature will be available very soon!</p>
            <div style="display:inline-flex; align-items:center; gap:8px; background:rgba(220,38,38,0.1); color:#dc2626; padding:8px 20px; border-radius:20px; font-weight:600; font-size:0.85rem;"><i class="fa-solid fa-clock"></i> Coming Soon</div>
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

// Service-specific theme colors and text
const serviceThemes = {
    flights:  { 
        gradient: 'linear-gradient(135deg, #0f1c6b 0%, #1a56db 50%, #1171ef 100%)', 
        primary: '#1a56db', primaryDark: '#1040a8', primaryLight: '#eef2ff', 
        accent: '#ff6b35', btnGrad: 'linear-gradient(135deg, #ff6b35, #f43f5e)', icon: 'fa-plane',
        tagline: "✈️ India's Most Trusted Travel Platform",
        title: "Where Do You Want<br><span class=\"gradient-text\">To Fly?</span>"
    },
    hotels:   { 
        gradient: 'linear-gradient(135deg, #4c1d95 0%, #7c3aed 50%, #a78bfa 100%)', 
        primary: '#7c3aed', primaryDark: '#5b21b6', primaryLight: '#f5f3ff', 
        accent: '#f59e0b', btnGrad: 'linear-gradient(135deg, #f59e0b, #fbbf24)', icon: 'fa-hotel',
        tagline: "🏨 Premium Handpicked Stays",
        title: "Find Your Perfect<br><span class=\"gradient-text\">Hotel</span>"
    },
    buses:    { 
        gradient: 'linear-gradient(135deg, #064e3b 0%, #059669 50%, #34d399 100%)', 
        primary: '#059669', primaryDark: '#047857', primaryLight: '#ecfdf5', 
        accent: '#f59e0b', btnGrad: 'linear-gradient(135deg, #f59e0b, #fbbf24)', icon: 'fa-bus',
        tagline: "🚌 Comfortable Journeys",
        title: "Book Your Next<br><span class=\"gradient-text\">Bus Ticket</span>"
    },
    cabs:     { 
        gradient: 'linear-gradient(135deg, #78350f 0%, #d97706 50%, #fbbf24 100%)', 
        primary: '#d97706', primaryDark: '#b45309', primaryLight: '#fffbeb', 
        accent: '#1e293b', btnGrad: 'linear-gradient(135deg, #1e293b, #334155)', icon: 'fa-taxi',
        tagline: "🚕 Safe & Reliable Rides",
        title: "Book Your City<br><span class=\"gradient-text\">Cab</span>"
    },
    packages: { 
        gradient: 'linear-gradient(135deg, #9a3412 0%, #ea580c 50%, #fb923c 100%)', 
        primary: '#ea580c', primaryDark: '#c2410c', primaryLight: '#fff7ed', 
        accent: '#4ade80', btnGrad: 'linear-gradient(135deg, #10b981, #34d399)', icon: 'fa-suitcase-rolling',
        tagline: "🌴 Unforgettable Experiences",
        title: "Explore Holiday<br><span class=\"gradient-text\">Packages</span>"
    },
    trains:   { 
        gradient: 'linear-gradient(135deg, #7f1d1d 0%, #dc2626 50%, #f87171 100%)', 
        primary: '#dc2626', primaryDark: '#b91c1c', primaryLight: '#fef2f2', 
        accent: '#fbbf24', btnGrad: 'linear-gradient(135deg, #f59e0b, #fbbf24)', icon: 'fa-train',
        tagline: "🚆 Partnered with IRCTC",
        title: "Book Your Express<br><span class=\"gradient-text\">Train Ticket</span>"
    }
};

function switchTab(target, btnEl) {
    activeTab = target;
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    if (btnEl) btnEl.classList.add('active');
    
    const container = document.getElementById('form-container');
    container.innerHTML = formTemplates[target] || '<p style="padding:20px;text-align:center;color:#64748b">Coming soon!</p>';
    
    // Apply service-specific theme
    const theme = serviceThemes[target] || serviceThemes.flights;
    
    // Update Hero background, tagline, and title
    const hero = document.querySelector('.hero');
    if (hero) hero.style.background = theme.gradient;
    
    const heroTagline = document.querySelector('.hero-tagline');
    if (heroTagline) heroTagline.innerHTML = theme.tagline;
    
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) heroTitle.innerHTML = theme.title;
    
    // Update watermark dynamically with animation
    const watermark = document.getElementById('hero-watermark');
    if (watermark) {
        watermark.classList.add('animating');
        setTimeout(() => {
            watermark.innerHTML = `<i class="fa-solid ${theme.icon}"></i>`;
            watermark.classList.remove('animating');
        }, 300);
    }
    
    // Update global CSS variables for a complete theme change across the application
    document.documentElement.style.setProperty('--primary', theme.primary);
    document.documentElement.style.setProperty('--primary-dark', theme.primaryDark);
    document.documentElement.style.setProperty('--primary-light', theme.primaryLight);
    document.documentElement.style.setProperty('--accent', theme.accent);
    
    // Update active tab color fallback
    document.querySelectorAll('.tab-btn.active').forEach(btn => {
        btn.style.color = theme.primary;
        btn.style.borderBottomColor = theme.primary;
    });
    
    // Update search button gradient specifically
    setTimeout(() => {
        const searchBtn = container.querySelector('.btn-search');
        if (searchBtn) searchBtn.style.background = theme.btnGrad;
    }, 10);
    
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
// CABS AUTOCOMPLETE & GPS
// ========================
function useLiveLocation(btn) {
    if (!navigator.geolocation) {
        alert("Geolocation is not supported by your browser.");
        return;
    }
    
    const originalContent = btn.innerHTML;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
    btn.disabled = true;

    navigator.geolocation.getCurrentPosition((position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        
        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}`)
            .then(res => res.json())
            .then(data => {
                const address = data.address;
                let locStr = address.city || address.town || address.state_district || address.state || 'Unknown Location';
                if (address.suburb) locStr = address.suburb + ', ' + locStr;
                
                const pickupInput = document.getElementById('cab-pickup');
                if (pickupInput) pickupInput.value = locStr;
                
                btn.innerHTML = originalContent;
                btn.disabled = false;
            })
            .catch(err => {
                console.error(err);
                alert("Failed to reverse-geocode your location.");
                btn.innerHTML = originalContent;
                btn.disabled = false;
            });
    }, (error) => {
        console.error(error);
        alert("Unable to retrieve your location.");
        btn.innerHTML = originalContent;
        btn.disabled = false;
    });
}

let addressFetchTimer;
function fetchAddressSuggestions(query, listId) {
    if (!query || query.length < 3) return;
    if (!listId) listId = 'cab-drop-suggestions'; // fallback
    
    clearTimeout(addressFetchTimer);
    addressFetchTimer = setTimeout(() => {
        const url = `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(query)}&format=json&addressdetails=1&countrycodes=in&limit=5`;
        fetch(url)
            .then(res => res.json())
            .then(data => {
                const datalist = document.getElementById(listId);
                if (!datalist) return;
                
                datalist.innerHTML = '';
                data.forEach(item => {
                    const opt = document.createElement('option');
                    opt.value = item.display_name;
                    datalist.appendChild(opt);
                });
            })
            .catch(err => console.error("Could not fetch address suggestions", err));
    }, 400);
}

// ========================
// MAP MODAL LOGIC
// ========================
let mapInstance = null;
let mapMarker = null;
let mapTargetInputId = null;

function openMapModal(targetInputId) {
    mapTargetInputId = targetInputId;
    document.getElementById('map-modal').style.display = 'flex';
    
    if (!mapInstance) {
        // Initialize map on first open
        mapInstance = L.map('map').setView([19.0760, 72.8777], 12); // Default Mumbai
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(mapInstance);
        
        mapMarker = L.marker([19.0760, 72.8777], { draggable: true }).addTo(mapInstance);
        
        // Try to get user's location to center map
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition((pos) => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                mapInstance.setView([lat, lon], 14);
                mapMarker.setLatLng([lat, lon]);
            }, () => {});
        }

        // On map click, move marker
        mapInstance.on('click', function(e) {
            mapMarker.setLatLng(e.latlng);
        });
    }
    
    // Invalidate size to fix rendering issues inside hidden modals
    setTimeout(() => {
        mapInstance.invalidateSize();
    }, 100);
}

function closeMapModal() {
    document.getElementById('map-modal').style.display = 'none';
}

function closeMapModalOutside(e) {
    if (e.target.id === 'map-modal') closeMapModal();
}

function confirmMapLocation() {
    if (!mapMarker || !mapTargetInputId) {
        closeMapModal();
        return;
    }
    
    const latlng = mapMarker.getLatLng();
    const btn = document.querySelector('#map-modal .btn-primary');
    const originalText = btn.innerText;
    btn.innerText = 'Confirming...';
    btn.disabled = true;

    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${latlng.lat}&lon=${latlng.lng}`)
        .then(res => res.json())
        .then(data => {
            const address = data.address;
            let locStr = data.display_name; // Use full display name for map selection for more accuracy
            
            const targetInput = document.getElementById(mapTargetInputId);
            if (targetInput) {
                targetInput.value = locStr;
            }
            
            btn.innerText = originalText;
            btn.disabled = false;
            closeMapModal();
        })
        .catch(err => {
            console.error(err);
            alert("Failed to fetch address for selected location.");
            btn.innerText = originalText;
            btn.disabled = false;
            closeMapModal();
        });
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
    
    const errorDiv = document.getElementById('payment-error');
    if (errorDiv) {
        errorDiv.style.display = 'none';
        errorDiv.innerText = '';
    }

    const payMethodNode = document.querySelector('input[name="pay_method"]:checked');
    const payMethod = payMethodNode ? payMethodNode.value : 'card';
    
    if (payMethod === 'card') {
        const cNum = (document.getElementById('card-number').value || '').replace(/\s/g, '');
        const cExp = (document.getElementById('card-expiry').value || '').trim();
        const cCvv = (document.getElementById('card-cvv').value || '').trim();
        
        if (cNum.length !== 16 || isNaN(cNum)) {
            if (errorDiv) { errorDiv.innerText = 'Invalid Card Number. Must be exactly 16 digits.'; errorDiv.style.display = 'block'; }
            return;
        }
        if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(cExp)) {
            if (errorDiv) { errorDiv.innerText = 'Invalid Expiry Date format (MM/YY).'; errorDiv.style.display = 'block'; }
            return;
        }
        
        const [expM, expY] = cExp.split('/');
        const now = new Date();
        const expDate = new Date(2000 + parseInt(expY), parseInt(expM), 0);
        if (expDate < now) {
            if (errorDiv) { errorDiv.innerText = 'Card has expired. Please use a valid card.'; errorDiv.style.display = 'block'; }
            return;
        }

        if (cCvv.length !== 3 || isNaN(cCvv)) {
            if (errorDiv) { errorDiv.innerText = 'Invalid CVV. Must be exactly 3 digits.'; errorDiv.style.display = 'block'; }
            return;
        }
    }
    
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

function sendSupportMsg() {
    const input = document.getElementById('support-input');
    const text = input.value.trim();
    if (!text) return;
    input.value = '';

    addSupportMsg(text, true);
    showTyping();

    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {
        removeTyping();
        addSupportMsg(data.reply || "Thanks for reaching out!", false);
    })
    .catch(() => {
        removeTyping();
        addSupportMsg("Sorry, I'm having trouble connecting right now. For urgent queries, call 1800-XXX-XXXX.", false);
    });
}

function quickReply(text) {
    const qr = document.querySelector('.support-quick-replies');
    if (qr) qr.remove();
    addSupportMsg(text, true);
    showTyping();
    
    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text })
    })
    .then(res => res.json())
    .then(data => {
        removeTyping();
        addSupportMsg(data.reply || "Thanks for reaching out!", false);
    })
    .catch(() => {
        removeTyping();
        addSupportMsg("Sorry, I'm having trouble connecting right now. For urgent queries, call 1800-XXX-XXXX.", false);
    });
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

    fetch(`/api/user/bookings/${currentUser.id}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                content.innerHTML = `<div style="text-align:center; padding:40px; color:#ef4444;">Error: ${data.error}</div>`;
                return;
            }
            if (!data || data.length === 0) {
                content.innerHTML = '<div style="text-align:center;padding:32px;"><i class="fa-solid fa-plane-circle-check" style="font-size:2.5rem;color:#94a3b8;margin-bottom:16px;display:block;"></i><h3 style="margin-bottom:8px;">No trips yet</h3><p style="color:#64748b;margin-bottom:20px;">Start searching for flights, hotels, or buses to plan your next trip!</p><button class="btn-primary" style="width:auto;padding:12px 28px;" onclick="closeModal2(\'trips\');">Search Now</button></div>';
            } else {
                let html = '<p style="color:#64748b;font-size:0.9rem;margin-bottom:16px;">Showing your recent trips.</p><div style="display:flex;flex-direction:column;gap:12px; max-height:400px; overflow-y:auto; padding-right:8px;">';
                data.forEach(b => {
                    let date = new Date(b.booking_date).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });
                    let icon = 'fa-plane';
                    let desc = '';
                    let typeLower = (b.service_type || '').toLowerCase();
                    if (typeLower.includes('flight')) {
                        icon = 'fa-plane';
                        desc = `${b.airline || 'Flight'}: ${b.flight_origin || ''} to ${b.flight_dest || ''}`;
                    } else if (typeLower.includes('hotel')) {
                        icon = 'fa-hotel';
                        desc = `${b.hotel_name || 'Hotel'} in ${b.hotel_loc || ''}`;
                    } else if (typeLower.includes('bus')) {
                        icon = 'fa-bus';
                        desc = `${b.operator_name || 'Bus'}: ${b.bus_origin || ''} to ${b.bus_dest || ''}`;
                    } else if (typeLower.includes('cab')) {
                        icon = 'fa-car';
                        desc = `Cab Type: ${b.cab_type || ''}`;
                    } else if (typeLower.includes('package')) {
                        icon = 'fa-suitcase-rolling';
                        desc = `Package to ${b.package_dest || ''}`;
                    } else {
                        desc = b.service_type;
                    }
                    html += `
                    <div style="border:1px solid #e2e8f0;border-radius:12px;padding:16px;display:flex;justify-content:space-between;align-items:center;">
                        <div style="display:flex;align-items:center;gap:16px;">
                            <div style="width:40px;height:40px;background:#f8fafc;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#64748b;font-size:1.1rem;flex-shrink:0;">
                                <i class="fa-solid ${icon}"></i>
                            </div>
                            <div>
                                <h4 style="margin:0;font-size:0.95rem;color:#1e293b;line-height:1.2;">${desc}</h4>
                                <p style="margin:4px 0 0;font-size:0.8rem;color:#64748b;">Booked on ${date} &bull; <span style="color:#059669;font-weight:600;">${b.status}</span></p>
                            </div>
                        </div>
                        <div style="text-align:right;flex-shrink:0;margin-left:10px;">
                            <div style="font-weight:700;color:#1e293b;">&#8377;${parseFloat(b.total_price).toFixed(2)}</div>
                            <div style="font-size:0.75rem;color:#94a3b8;margin-top:2px;">#TB-000${b.id}</div>
                        </div>
                    </div>`;
                });
                html += '</div>';
                content.innerHTML = html;
            }
        })
        .catch(err => {
            content.innerHTML = `<div style="text-align:center; padding:40px; color:#ef4444;">Failed to fetch trips.</div>`;
        });
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

function copyCode(code, element) {
    navigator.clipboard.writeText(code).then(() => {
        const origHtml = element.innerHTML;
        element.innerHTML = 'Copied! <i class="fa-solid fa-check"></i>';
        setTimeout(() => element.innerHTML = origHtml, 2000);
    });
}

// ========================
// LIVE LOCATION (CABS)
// ========================
function useLiveLocation(btn) {
    const input = document.getElementById('cab-pickup');
    
    const fallbackIPLocation = () => {
        fetch('https://ipapi.co/json/')
            .then(res => res.json())
            .then(data => {
                btn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i>';
                if (data && data.city) {
                    if (input) input.value = data.city;
                } else {
                    alert("Could not determine city from your IP address.");
                }
            })
            .catch(() => {
                btn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i>';
                alert("Failed to fetch location data.");
            });
    };

    if (!navigator.geolocation || window.location.protocol === 'http:' && window.location.hostname !== 'localhost') {
        // Fallback to IP geolocation if HTML5 Geolocation is not supported or we're on insecure HTTP
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
        fallbackIPLocation();
        return;
    }
    
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lon}&zoom=10`)
                .then(res => res.json())
                .then(data => {
                    btn.innerHTML = '<i class="fa-solid fa-location-crosshairs"></i>';
                    if (data && data.address) {
                        let city = data.address.city || data.address.town || data.address.state_district || "Unknown Location";
                        if (input) input.value = city;
                    } else {
                        fallbackIPLocation();
                    }
                })
                .catch(() => {
                    fallbackIPLocation();
                });
        },
        (error) => {
            // User denied permission or error occurred, fallback to IP
            fallbackIPLocation();
        }
    );
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
        
        // Fetch Admin Data and Users
        Promise.all([
            fetch('/api/admin/stats').then(r => r.json()),
            fetch('/api/admin/users').then(r => r.json())
        ])
        .then(([data, users]) => {
            if (data.error) {
                alert('Error loading dashboard: ' + data.error);
                return;
            }
            if (users.error) {
                console.error("Failed to load users:", users.error);
                users = [];
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

            let usersHtml = '';
            if (users && users.length > 0) {
                users.forEach(u => {
                    usersHtml += `
                        <tr style="border-bottom: 1px solid rgba(255,255,255,0.1); cursor: pointer; transition: background 0.2s;" onmouseover="this.style.background='rgba(255,255,255,0.05)'" onmouseout="this.style.background='transparent'" onclick="viewAdminUserBookings(${u.id}, '${u.name}')">
                            <td style="padding: 15px; font-weight: 600; color: #60a5fa;">#${u.id}</td>
                            <td style="padding: 15px;">${u.name}</td>
                            <td style="padding: 15px;">${u.email}</td>
                            <td style="padding: 15px; color: #94a3b8;">${u.joined}</td>
                            <td style="padding: 15px; text-align: right;"><button onclick="showAdminUserBookings(${u.id}, \'${u.name}\')" style="background: rgba(37, 99, 235, 0.2); color: #60a5fa; border: none; padding: 6px 12px; border-radius: 6px; cursor: pointer;">View History <i class="fa-solid fa-arrow-right"></i></button></td>
                        </tr>
                    `;
                });
            } else {
                usersHtml = '<tr><td colspan="5" style="padding: 15px; text-align: center; color: #94a3b8;">No users found.</td></tr>';
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

                            <!-- Users Table -->
                            <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 30px; backdrop-filter: blur(10px); margin-top: 40px;">
                                <h3 style="margin: 0 0 20px 0; font-size: 1.4rem; font-weight: 600;">Registered Users</h3>
                                <p style="color: #94a3b8; font-size: 0.9rem; margin-top: -15px; margin-bottom: 20px;">Click on a user to view their booking history.</p>
                                <div style="overflow-x: auto;">
                                    <table style="width: 100%; border-collapse: collapse; text-align: left;">
                                        <thead>
                                            <tr style="border-bottom: 2px solid rgba(255,255,255,0.1); color: #94a3b8;">
                                                <th style="padding: 15px; font-weight: 600;">ID</th>
                                                <th style="padding: 15px; font-weight: 600;">Name</th>
                                                <th style="padding: 15px; font-weight: 600;">Email</th>
                                                <th style="padding: 15px; font-weight: 600;">Joined</th>
                                                <th style="padding: 15px; font-weight: 600;"></th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${usersHtml}
                                        </tbody>
                                    </table>
                                </div>
                            </div>

                        </div>
                    </div>

                    <!-- Admin User Bookings Modal -->
                    <div id="admin-user-modal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 9999; align-items: center; justify-content: center; backdrop-filter: blur(4px);">
                        <div style="background: #1e293b; color: white; border-radius: 16px; width: 90%; max-width: 800px; max-height: 85vh; display: flex; flex-direction: column; border: 1px solid rgba(255,255,255,0.1); overflow: hidden;">
                            <div style="padding: 20px 25px; border-bottom: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02);">
                                <h2 style="margin: 0; font-size: 1.4rem;" id="admin-user-modal-title">User Bookings</h2>
                                <button onclick="document.getElementById('admin-user-modal').style.display='none'" style="background: transparent; border: none; color: #94a3b8; font-size: 1.5rem; cursor: pointer;">&times;</button>
                            </div>
                            <div id="admin-user-modal-content" style="padding: 25px; overflow-y: auto; flex: 1;">
                                Loading...
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


function showAdminUserBookings(userId, userName) {
    const modal = document.getElementById('admin-user-modal');
    const title = document.getElementById('admin-user-modal-title');
    const content = document.getElementById('admin-user-modal-content');
    
    title.innerText = `Bookings for ${userName}`;
    content.innerHTML = '<div style="text-align:center;padding:20px;"><div class="loader-spinner" style="margin:0 auto;"></div></div>';
    modal.style.display = 'flex';

    fetch(`/api/user/bookings/${userId}`)
        .then(res => res.json())
        .then(data => {
            if (data.error) {
                content.innerHTML = `<div style="text-align:center; padding:40px; color:#ef4444;">Error: ${data.error}</div>`;
                return;
            }
            if (!data || data.length === 0) {
                content.innerHTML = '<div style="text-align:center;padding:32px;color:#94a3b8;">No bookings found for this user.</div>';
            } else {
                let html = '<div style="display:flex;flex-direction:column;gap:12px; max-height:60vh; overflow-y:auto; padding-right:8px;">';
                data.forEach(b => {
                    let date = new Date(b.booking_date).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });
                    let icon = 'fa-plane';
                    let desc = '';
                    let typeLower = (b.service_type || '').toLowerCase();
                    if (typeLower.includes('flight')) {
                        icon = 'fa-plane';
                        desc = `${b.airline || 'Flight'}: ${b.flight_origin || ''} to ${b.flight_dest || ''}`;
                    } else if (typeLower.includes('hotel')) {
                        icon = 'fa-hotel';
                        desc = `${b.hotel_name || 'Hotel'} in ${b.hotel_loc || ''}`;
                    } else if (typeLower.includes('bus')) {
                        icon = 'fa-bus';
                        desc = `${b.operator_name || 'Bus'}: ${b.bus_origin || ''} to ${b.bus_dest || ''}`;
                    } else if (typeLower.includes('cab')) {
                        icon = 'fa-car';
                        desc = `Cab Type: ${b.cab_type || ''}`;
                    } else if (typeLower.includes('package')) {
                        icon = 'fa-suitcase-rolling';
                        desc = `Package to ${b.package_dest || ''}`;
                    } else {
                        desc = b.service_type;
                    }
                    html += `
                    <div style="border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:16px;display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,0.02);">
                        <div style="display:flex;align-items:center;gap:16px;">
                            <div style="width:40px;height:40px;background:rgba(59,130,246,0.1);border-radius:8px;display:flex;align-items:center;justify-content:center;color:#60a5fa;font-size:1.1rem;flex-shrink:0;">
                                <i class="fa-solid ${icon}"></i>
                            </div>
                            <div>
                                <h4 style="margin:0;font-size:0.95rem;color:#f8fafc;line-height:1.2;">${desc}</h4>
                                <p style="margin:4px 0 0;font-size:0.8rem;color:#94a3b8;">Booked on ${date} &bull; <span style="color:#10b981;font-weight:600;">${b.status}</span></p>
                            </div>
                        </div>
                        <div style="text-align:right;flex-shrink:0;margin-left:10px;">
                            <div style="font-weight:700;color:#f8fafc;">&#8377;${parseFloat(b.total_price).toFixed(2)}</div>
                            <div style="font-size:0.75rem;color:#64748b;margin-top:2px;">#TB-000${b.id}</div>
                        </div>
                    </div>`;
                });
                html += '</div>';
                content.innerHTML = html;
            }
        })
        .catch(err => {
            console.error(err);
            content.innerHTML = `<div style="text-align:center; padding:40px; color:#ef4444;">Failed to fetch trips.</div>`;
        });
}

// Alias for row-click handler in admin users table
function viewAdminUserBookings(userId, userName) {
    showAdminUserBookings(userId, userName);
}

// ========================
// TRAIN COMING SOON
// ========================
function showTrainComingSoon() {
    const panel = document.getElementById('train-coming-soon');
    if (panel) {
        panel.style.display = 'block';
        panel.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

// ========================
// SERVICE-THEMED CHECKOUT
// ========================
const checkoutThemeMap = {
    flights:  { icon: 'fa-plane',             color: '#1a56db', label: 'Flight' },
    hotels:   { icon: 'fa-hotel',             color: '#7c3aed', label: 'Hotel' },
    buses:    { icon: 'fa-bus',               color: '#059669', label: 'Bus' },
    cabs:     { icon: 'fa-taxi',              color: '#d97706', label: 'Cab' },
    packages: { icon: 'fa-suitcase-rolling',  color: '#ea580c', label: 'Package' }
};

// Override startCheckout to apply service theme
const _originalStartCheckout = startCheckout;
startCheckout = function(service_type, service_id, price, title) {
    _originalStartCheckout(service_type, service_id, price, title);
    
    const theme = checkoutThemeMap[service_type] || checkoutThemeMap.flights;
    const header = document.querySelector('.checkout-header');
    if (header) {
        const iconEl = header.querySelector('.checkout-icon');
        if (iconEl) {
            iconEl.className = 'fa-solid ' + theme.icon + ' checkout-icon';
            iconEl.style.color = theme.color;
        }
    }
    
    const summary = document.getElementById('booking-summary');
    if (summary) {
        summary.style.borderLeft = `4px solid ${theme.color}`;
        summary.style.background = `linear-gradient(135deg, ${theme.color}08, ${theme.color}15)`;
    }
    
    const payBtn = document.getElementById('pay-btn');
    if (payBtn) {
        payBtn.style.background = `linear-gradient(135deg, ${theme.color}, ${theme.color}dd)`;
    }
};
