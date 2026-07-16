document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.tab-btn');
    const navLinks = document.querySelectorAll('.nav-links a');
    const searchForm = document.getElementById('search-form');
    const resultsSection = document.getElementById('results-section');
    const resultsGrid = document.getElementById('results-grid');
    
    let currentTab = 'flights';

    // Tab switching logic
    function switchTab(target) {
        currentTab = target;
        
        // Update active classes for tabs
        tabs.forEach(tab => {
            if(tab.dataset.target === target) {
                tab.classList.add('active');
            } else {
                tab.classList.remove('active');
            }
        });
        
        // Update active classes for nav links
        navLinks.forEach(link => {
            if(link.dataset.target === target) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        // Hide results when switching tabs
        resultsSection.style.display = 'none';
        resultsGrid.innerHTML = '';
    }

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            switchTab(e.target.dataset.target);
        });
    });

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            switchTab(e.target.dataset.target);
        });
    });

    // Form Submission
    searchForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Show loading state
        resultsSection.style.display = 'block';
        resultsGrid.innerHTML = '<p>Loading results...</p>';

        try {
            // Fetch data from our backend API
            const response = await fetch(`/api/${currentTab}`);
            if (!response.ok) throw new Error('Failed to fetch data');
            
            const data = await response.json();
            renderResults(data, currentTab);
        } catch (error) {
            resultsGrid.innerHTML = `<p style="color: #ef4444;">Error loading data. Please try again later.</p>`;
            console.error(error);
        }
    });

    // Render results based on tab
    function renderResults(data, type) {
        resultsGrid.innerHTML = '';
        
        if (data.length === 0) {
            resultsGrid.innerHTML = '<p>No results found.</p>';
            return;
        }

        data.forEach(item => {
            const card = document.createElement('div');
            card.className = 'glass-card result-card';
            
            let html = '';
            
            if (type === 'flights') {
                html = `
                    <h3>${item.flight_name}</h3>
                    <p>${item.source} &rarr; ${item.destination}</p>
                    <p>Departure: ${new Date(item.departure).toLocaleString()}</p>
                    <div class="price">$${item.price}</div>
                    <button class="btn btn-primary">Book Flight</button>
                `;
            } else if (type === 'hotels') {
                html = `
                    <h3>${item.hotel_name}</h3>
                    <p>${item.city} | Rating:  ${item.rating}</p>
                    <p>Available Rooms: ${item.rooms}</p>
                    <div class="price">$${item.price} / night</div>
                    <button class="btn btn-primary">Book Hotel</button>
                `;
            } else if (type === 'cabs') {
                html = `
                    <h3>${item.cab_name}</h3>
                    <p>Location: ${item.location}</p>
                    <p>Driver: ${item.driver}</p>
                    <div class="price">$${item.price}</div>
                    <button class="btn btn-primary">Book Cab</button>
                `;
            } else if (type === 'packages') {
                html = `
                    <h3>${item.package_name}</h3>
                    <p>${item.description}</p>
                    <p>Duration: ${item.days} days</p>
                    <div class="price">$${item.price}</div>
                    <button class="btn btn-primary">Book Package</button>
                `;
            }

            card.innerHTML = html;
            resultsGrid.appendChild(card);
        });
    }
});
