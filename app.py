from flask import Flask, request, jsonify
import datetime
import uuid

app = Flask(__name__)

# Mock database to store invoice details
invoices = []

# Endpoint to create a new invoice
@app.route('/api/invoices', methods=['POST'])
def create_invoice():
    try:
        data = request.get_json()
        
        # Generate unique invoice ID
        invoice_id = str(uuid.uuid4())
        
        # Extract and validate input details
        client_name = data.get('client_name')
        items = data.get('items')
        due_date = data.get('due_date')
        
        if not client_name or not items or not due_date:
            return jsonify({'error': 'client_name, items, and due_date are required fields.'}), 400
        
        # Calculate total amount for the invoice
        total_amount = sum(item['quantity'] * item['price'] for item in items)
        
        invoice = {
            'invoice_id': invoice_id,
            'client_name': client_name,
            'items': items,
            'total_amount': total_amount,
            'due_date': due_date,
            'created_at': datetime.datetime.now().isoformat()
        }
        
        invoices.append(invoice)
        return jsonify(invoice), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to get all invoices
@app.route('/api/invoices', methods=['GET'])
def get_invoices():
    return jsonify(invoices), 200

# Endpoint to get a single invoice by ID
@app.route('/api/invoices/<invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    invoice = next((inv for inv in invoices if inv['invoice_id'] == invoice_id), None)
    if invoice:
        return jsonify(invoice), 200
    else:
        return jsonify({'error': 'Invoice not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
