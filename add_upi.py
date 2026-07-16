with open('src/frontend/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the payment form with a UPI compatible one
new_form = '''                <form id="payment-form" class="payment-form">
                    <div class="input-group" style="margin-bottom: 1rem;">
                        <label>Payment Method</label>
                        <select id="payment-method" onchange="togglePaymentFields()">
                            <option value="card">Credit/Debit Card</option>
                            <option value="upi">UPI</option>
                        </select>
                    </div>

                    <!-- Card Fields -->
                    <div id="card-fields">
                        <div class="input-group">
                            <label>Cardholder Name</label>
                            <input type="text" id="card-name" placeholder="John Doe">
                        </div>
                        <div class="input-group">
                            <label>Card Number</label>
                            <input type="text" id="card-num" placeholder="XXXX XXXX XXXX XXXX">
                        </div>
                        <div class="row">
                            <div class="input-group">
                                <label>Expiry</label>
                                <input type="text" id="card-exp" placeholder="MM/YY">
                            </div>
                            <div class="input-group">
                                <label>CVV</label>
                                <input type="password" id="card-cvv" placeholder="***">
                            </div>
                        </div>
                    </div>

                    <!-- UPI Fields -->
                    <div id="upi-fields" style="display: none;">
                        <div class="input-group">
                            <label>UPI ID</label>
                            <input type="text" id="upi-id" placeholder="yourname@okbank">
                        </div>
                    </div>

                    <button type="submit" class="btn btn-primary btn-block mt-4">Pay Securely</button>
                    <button type="button" class="btn btn-outline btn-block mt-2" onclick="goBackToSearch()">Cancel</button>
                </form>

                <script>
                    function togglePaymentFields() {
                        const method = document.getElementById('payment-method').value;
                        if (method === 'card') {
                            document.getElementById('card-fields').style.display = 'block';
                            document.getElementById('upi-fields').style.display = 'none';
                        } else {
                            document.getElementById('card-fields').style.display = 'none';
                            document.getElementById('upi-fields').style.display = 'block';
                        }
                    }
                </script>'''

# Replace the existing form block
import re
content = re.sub(r'<form id="payment-form" class="payment-form">.*?</form>', new_form, content, flags=re.DOTALL)

with open('src/frontend/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
