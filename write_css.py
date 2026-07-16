content = '''
:root {
    --primary: #008cff;
    --primary-gradient: linear-gradient(93deg,#53b2fe,#065af3);
    --secondary: #0a223d;
    --dark: #000000;
    --light: #ffffff;
    --grey-light: #f2f2f2;
    --grey-text: #4a4a4a;
    --border: #e7e7e7;
    --bg: #e5eef4;
    --font-main: 'Outfit', sans-serif;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: var(--font-main);
    background-color: var(--bg);
    color: var(--dark);
    line-height: 1.6;
}

.header-bg {
    background: linear-gradient(to right, #041422, #104170);
    height: 350px;
    width: 100%;
    position: absolute;
    top: 0;
    z-index: -1;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 5%;
    color: var(--light);
}

.logo {
    font-size: 1.8rem;
    font-weight: 800;
    letter-spacing: 1px;
}

.user-actions .btn {
    margin-left: 1rem;
    font-weight: 600;
    border-radius: 4px;
    padding: 0.5rem 1.2rem;
}

.btn-primary {
    background: var(--primary-gradient);
    color: var(--light);
    border: none;
    cursor: pointer;
    transition: 0.3s ease;
}
.btn-primary:hover {
    box-shadow: 0 2px 8px rgba(0,140,255,0.5);
}

.btn-outline {
    background: transparent;
    color: var(--light);
    border: 1px solid var(--light);
    cursor: pointer;
    transition: 0.3s ease;
}
.btn-outline:hover {
    background: rgba(255,255,255,0.1);
}

#main-view {
    padding-top: 2rem;
}

.search-section {
    max-width: 1200px;
    margin: 0 auto;
    position: relative;
    padding: 0 20px;
}

.search-container {
    background: var(--light);
    border-radius: 8px;
    box-shadow: 0 1px 6px 0 rgba(0,0,0,0.2);
    padding: 0;
    margin-top: 30px;
    position: relative;
    display: flex;
    flex-direction: column;
}

.search-tabs {
    display: flex;
    justify-content: center;
    background: #ffffff;
    padding: 15px 0;
    border-bottom: 1px solid var(--border);
    border-radius: 8px 8px 0 0;
    box-shadow: 0 1px 4px 0 rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

.tab-btn {
    background: none;
    border: none;
    padding: 10px 20px;
    margin: 0 10px;
    color: var(--grey-text);
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    transition: 0.3s ease;
}
.tab-btn i {
    font-size: 1.5rem;
    color: #9b9b9b;
}

.tab-btn.active {
    color: var(--primary);
    border-bottom: 3px solid var(--primary);
}
.tab-btn.active i {
    color: var(--primary);
}

.tab-btn:hover {
    color: var(--primary);
}

.search-form-container {
    padding: 20px 40px 60px 40px; 
}

.search-form {
    display: flex;
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 8px;
}

.mmt-input-block {
    padding: 15px 20px;
    border-right: 1px solid var(--border);
    position: relative;
    display: flex;
    flex-direction: column;
    cursor: pointer;
    flex: 1;
}
.mmt-input-block:last-child {
    border-right: none;
}
.mmt-input-block:hover {
    background: #f4f8ff;
}

.mmt-label {
    font-size: 0.85rem;
    color: var(--grey-text);
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 5px;
    display: flex;
    align-items: center;
    gap: 5px;
}

.mmt-input-block input, .mmt-input-block select {
    border: none;
    background: transparent;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--dark);
    outline: none;
    width: 100%;
    cursor: pointer;
}

.mmt-input-block input::placeholder {
    color: #000000;
}

.btn-search {
    position: absolute;
    bottom: -25px;
    left: 50%;
    transform: translateX(-50%);
    background: var(--primary-gradient);
    color: var(--light);
    font-size: 1.2rem;
    font-weight: 700;
    padding: 12px 60px;
    border-radius: 30px;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    cursor: pointer;
    text-transform: uppercase;
}
.btn-search:hover {
    box-shadow: 0 6px 15px rgba(0,140,255,0.4);
}

.results-section {
    max-width: 1200px;
    margin: 40px auto;
    padding: 0 20px;
}

.results-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}
.results-header h2 {
    font-size: 1.5rem;
    font-weight: 700;
}
.filters select {
    padding: 0.5rem 1rem;
    border: 1px solid var(--border);
    border-radius: 4px;
    font-family: inherit;
    font-weight: 600;
}

.results-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.result-card {
    background: #ffffff;
    border-radius: 4px;
    box-shadow: 0 1px 4px 0 rgba(0,0,0,0.1);
    overflow: hidden;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    border: 1px solid var(--border);
    display: flex;
    flex-direction: column;
}
.result-card:hover {
    box-shadow: 0 4px 12px 0 rgba(0,0,0,0.15);
}

.card-header {
    padding: 15px 20px;
    background: #f9f9f9;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.card-header h3 {
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0;
}
.price {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--dark);
}

.card-body {
    padding: 20px;
    flex-grow: 1;
}
.card-body p {
    margin-bottom: 8px;
    font-size: 0.95rem;
    color: var(--grey-text);
}
.card-body p strong {
    color: var(--dark);
}

.card-footer {
    padding: 15px 20px;
    border-top: 1px solid var(--border);
    background: #ffffff;
}

.btn-book {
    width: 100%;
    background: var(--primary-gradient);
    color: var(--light);
    border: none;
    padding: 10px;
    border-radius: 4px;
    font-weight: 700;
    cursor: pointer;
    font-size: 1rem;
}

.checkout-section, .success-section {
    max-width: 600px;
    margin: 60px auto;
    padding: 0 20px;
}

.checkout-container, .success-container {
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 1px 6px 0 rgba(0,0,0,0.2);
    padding: 40px;
}

.checkout-container h2 {
    margin-bottom: 20px;
    font-size: 1.5rem;
}

.input-group {
    margin-bottom: 1.2rem;
}
.input-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: 600;
    font-size: 0.9rem;
}
.input-group input, .input-group select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-family: inherit;
    font-size: 1rem;
}

.row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 15px;
}

.btn-block {
    width: 100%;
    padding: 12px;
    font-size: 1rem;
}

.success-icon {
    font-size: 4rem;
    color: #2e7d32;
    margin-bottom: 20px;
}

.text-center {
    text-align: center;
}

.mt-2 { margin-top: 10px; }
.mt-4 { margin-top: 20px; }

.loader {
    display: flex;
    justify-content: center;
    margin: 40px 0;
}
.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid var(--border);
    border-top: 4px solid var(--primary);
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.6);
    align-items: center;
    justify-content: center;
}
.modal.active { display: flex; }

.modal-content {
    background: #ffffff;
    padding: 30px;
    border-radius: 8px;
    width: 90%;
    max-width: 400px;
    position: relative;
}

.close {
    position: absolute;
    right: 20px;
    top: 15px;
    font-size: 1.5rem;
    cursor: pointer;
    color: var(--grey-text);
}
.close:hover { color: var(--dark); }

footer {
    text-align: center;
    padding: 3rem;
    color: var(--grey-text);
    font-size: 0.9rem;
}
'''
with open('src/frontend/style.css', 'w', encoding='utf-8') as f:
    f.write(content)
