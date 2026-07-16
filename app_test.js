let currentServiceType = 'flights';
let currentBookingData = null;
let currentUser = null;
try {
    currentUser = JSON.parse(localStorage.getItem('user'));
} catch (e) {
    console.warn('localStorage error', e);
}

const formTemplates = {
    flights: `
        <div class="search-form">
            <div class="input-group">
                <label><i class="fa-solid fa-plane-departure"></i> From</label>
                <input type="text" id="flight-origin" required placeholder="Select City" list="locations-list" autocomplete="off">
            </div>
            <div class="input-group">
                <label><i class="fa-solid fa-plane-arrival"></i> To</label>
                <input type="text" id="flight-dest" required placeholder="Select City" list="locations-list" autocomplete="off">
            </div>
            <div class="input-group">
                <label><i class="fa-regular fa-calendar"></i> Date</label>
                <input type="date" required id="flight-date">
            </div>
            <button type="button" class="btn btn-primary btn-search" onclick="searchData('flights')"><i class="fa-solid fa-magnifying-glass"></i> Search</button>
        </div>
    `,
    hotels: `
        <div class="search-form" style="grid-template-columns: 2fr 1fr 1fr auto;">
            <div class="input-group">
                <label><i class="fa-solid fa-location-dot"></i> City/Location</label>
                <input type="text" id="hotel-loc" required placeholder="Select City" list="locations-list" autocomplete="off">
            </div>
            <div class="input-group">
                <label>Check-In</label>
                <input type="date" required id="hotel-in">
            </div>
            <div class="input-group">
                <label>Check-Out</label>
                <input type="date" required id="hotel-out">
            </div>
            <button type="button" class="btn btn-primary btn-search" onclick="searchData('hotels')"><i class="fa-solid fa-magnifying-glass"></i> Search</button>
        </div>
    `,
    cabs: `
        <div class="search-form">
            <div class="input-group">
                <label>Pickup Location</label>
                <input type="text" placeholder="Enter Pickup" required list="locations-list" autocomplete="off">
            </div>
            <div class="input-group">
                <label>Drop Location</label>
                <input type="text" placeholder="Enter Drop" required list="locations-list" autocomplete="off">
            </div>
            <button type="button" class="btn btn-primary btn-search" onclick="searchData('cabs')">Search Cabs</button>
        </div>
    `,
    packages: `
        <div class="search-form">
            <div class="input-group">
                <label>Destination</label>
                <input type="text" id="pkg-dest" required placeholder="Any Destination" list="locations-list" autocomplete="off">
            </div>
            <button type="button" class="btn btn-primary btn-search" onclick="searchData('packages')">Explore Packages</button>
        </div>
    `
};

document.addEventListener('DOMContentLoaded', () => {
    updateNavUI();
    fetchLocations();

    const formContainer = document.getElementById('form-container');
    if (formContainer) {
        formContainer.innerHTML = formTemplates['flights'];
    }

    // Tab Switching for main forms
    document.querySelectorAll('.tab-btn').forEach(btn => {
        if(btn.closest('.search-tabs') && !btn.id.startsWith('tab-')) {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.search-container .tab-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                currentServiceType = e.target.getAttribute('data-target');
                if (formContainer) {
                    formContainer.innerHTML = formTemplates[currentServiceType];
                }
                const resultsSection = document.getElementById('results-section');
                if (resultsSection) resultsSection.style.display = 'none';
                
                // Keep top navbar in sync
                document.querySelectorAll('.nav-links a').forEach(l => l.classList.remove('active'));
                const navLink = document.querySelector(`.nav-links a[data-target="${currentServiceType}"]`);
                if(navLink) navLink.classList.add('active');
            });
        }
    });
    
    // Top Navbar switching
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = e.currentTarget.getAttribute('data-target');
            if (target) {
                const lowerTab = document.querySelector(`.search-tabs .tab-btn[data-target="${target}"]`);
                if (lowerTab) {
                    lowerTab.click();
                }
            }
        });
    });
    
    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', () => {
            searchData(currentServiceType);
        });
    }
});

function fetchLocations() {
    fetch('/api/locations')
        .then(res => res.json())
        .then(data => {
            if (data.locations) {
                const list = document.getElementById('locations-list');
                list.innerHTML = '';
                data.locations.forEach(loc => {
                    let option = document.createElement('option');
                    option.value = loc;
                    list.appendChild(option);
                });
            }
        }).catch(err => console.error('Error fetching locations', err));
}

function updateNavUI() {
    const userSection = document.getElementById('user-section');
    if (currentUser) {
        userSection.innerHTML = `
            <span style="margin-right: 15px; font-weight: 600; color: var(--primary-color);">Hi, ${currentUser.name.split(' ')[0]}</span>
            <button class="btn btn-outline" onclick="logout()">Logout</button>
        `;
    } else {
        userSection.innerHTML = `
            <button class="btn btn-outline" onclick="showModal('login')">Log In</button>
            <button class="btn btn-primary" onclick="showModal('login', true)">Sign Up</button>
        `;
    }
}

function showModal(modalId, isSignUp = false) {
    document.getElementById(modalId + '-modal').style.display = 'flex';
    if(modalId === 'login') {
        switchAuthTab(isSignUp ? 'signup' : 'login');
    }
}

function closeModal(modalId) {
    document.getElementById(modalId + '-modal').style.display = 'none';
    document.getElementById('auth-error').style.display = 'none';
}

function switchAuthTab(tab) {
    document.getElementById('tab-login').classList.remove('active');
    document.getElementById('tab-signup').classList.remove('active');
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('signup-form').style.display = 'none';
    
    document.getElementById('tab-' + tab).classList.add('active');
    document.getElementById(tab + '-form').style.display = 'block';
    document.getElementById('auth-error').style.display = 'none';
}

function handleAuth(event, type) {
    event.preventDefault();
    const errorDiv = document.getElementById('auth-error');
    errorDiv.style.display = 'none';
    
    let url = type === 'login' ? '/api/login' : '/api/register';
    let body = {};
    
    if (type === 'login') {
        body.email = document.getElementById('login-email').value;
        body.password = document.getElementById('login-password').value;
    } else {
        body.name = document.getElementById('signup-name').value;
        body.email = document.getElementById('signup-email').value;
        body.password = document.getElementById('signup-password').value;
    }
    
    fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(body)
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            currentUser = data.user;
            localStorage.setItem('user', JSON.stringify(currentUser));
            updateNavUI();
            closeModal('login');
            // If there's a pending booking, maybe we want to proceed to checkout
        } else {
            errorDiv.textContent = data.error || 'Authentication failed';
            errorDiv.style.display = 'block';
        }
    })
    .catch(err => {
        errorDiv.textContent = 'Server error. Please try again.';
        errorDiv.style.display = 'block';
    });
}

function logout() {
    currentUser = null;
    localStorage.removeItem('user');
    updateNavUI();
}

function searchData(type) {
    const grid = document.getElementById('results-grid');
    const resultsSec = document.getElementById('results-section');
    const loader = document.getElementById('loader');
    
    resultsSec.style.display = 'block';
    grid.innerHTML = '';
    loader.style.display = 'flex';
    
    let url = '/api/' + type + '?';
    let sort = document.getElementById('sort-select').value;
    if (sort) url += '&sort=' + sort;
    
    if (type === 'flights') {
        let orig = document.getElementById('flight-origin').value;
        let dest = document.getElementById('flight-dest').value;
        if(orig) url += '&origin=' + encodeURIComponent(orig);
        if(dest) url += '&destination=' + encodeURIComponent(dest);
    } else if (type === 'hotels') {
        let loc = document.getElementById('hotel-loc').value;
        if(loc) url += '&location=' + encodeURIComponent(loc);
    }

    fetch(url)
        .then(res => res.json())
        .then(data => {
            loader.style.display = 'none';
            if (data.error) {
                grid.innerHTML = \`<p style="color:red;">Error: \${data.error}</p>\`;
                return;
            }
            if (data.length === 0) {
                grid.innerHTML = '<p>No results found.</p>';
                return;
            }
            data.forEach(item => {
                grid.appendChild(createCard(type, item));
            });
        }).catch(err => {
            loader.style.display = 'none';
            grid.innerHTML = '<p style="color:red;">Failed to fetch data.</p>';
        });
}

function createCard(type, item) {
    let div = document.createElement('div');
    div.className = 'result-card';
    
    let html = '';
    let price = 0;
    
    if (type === 'flights') {
        price = item.price;
        html = \`
            <div class="card-header">
                <h3>\${item.airline}</h3>
                <div class="price">?\${item.price}</div>
            </div>
            <div class="card-body">
                <p><strong>From:</strong> \${item.origin}</p>
                <p><strong>To:</strong> \${item.destination}</p>
                <p><strong>Duration:</strong> \${item.duration}</p>
            </div>
        \`;
    } else if (type === 'hotels') {
        price = item.price_per_night;
        html = \`
            <div class="card-header">
                <h3>\${item.name}</h3>
                <div class="price">?\${item.price_per_night}</div>
            </div>
            <div class="card-body">
                <p><strong>Location:</strong> \${item.location}</p>
                <p><strong>Rating:</strong> ? \${item.rating}</p>
            </div>
        \`;
    } else if (type === 'cabs') {
        price = item.price_per_km * 20; // Example
        html = \`
            <div class="card-header">
                <h3>\${item.type}</h3>
                <div class="price">?\${item.price_per_km}/km</div>
            </div>
            <div class="card-body">
                <p><strong>Driver:</strong> \${item.driver_name}</p>
            </div>
        \`;
    } else if (type === 'packages') {
        price = item.price;
        html = \`
            <div class="card-header">
                <h3>\${item.destination} (\${item.days} Days)</h3>
                <div class="price">?\${item.price}</div>
            </div>
            <div class="card-body">
                <p><strong>Includes:</strong> \${item.includes}</p>
            </div>
        \`;
    }

    html += \`<button class="btn btn-primary btn-block mt-2" onclick="initiateBooking('\${type}', \${item.id}, \${price})">Book Now</button>\`;
    div.innerHTML = html;
    return div;
}

function initiateBooking(type, id, price) {
    if (!currentUser) {
        showModal('login');
        return; // Wait for login
    }
    
    currentBookingData = { type, id, price };
    document.getElementById('main-view').style.display = 'none';
    document.getElementById('checkout-view').style.display = 'block';
    
    document.getElementById('booking-summary').innerHTML = \`
        <p><strong>Service:</strong> \${type.toUpperCase()}</p>
        <p><strong>Total Amount:</strong> ?\${price}</p>
    \`;
}

function goBackToSearch() {
    document.getElementById('main-view').style.display = 'block';
    document.getElementById('checkout-view').style.display = 'none';
    document.getElementById('success-view').style.display = 'none';
}

document.getElementById('payment-form').addEventListener('submit', (e) => {
    e.preventDefault();
    if (!currentBookingData || !currentUser) return;
    
    // Process Booking Request
    const payload = {
        user_id: currentUser.id,
        service_type: currentBookingData.type,
        service_id: currentBookingData.id,
        total_price: currentBookingData.price
    };
    
    fetch('/api/book', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if(data.status === 'success') {
            document.getElementById('checkout-view').style.display = 'none';
            document.getElementById('success-view').style.display = 'block';
            document.getElementById('booking-id-display').innerText = data.booking_id;
        } else {
            alert("Booking failed: " + data.error);
        }
    })
    .catch(err => {
        alert("Server error occurred");
    });
});
