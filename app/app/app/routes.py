from flask import Blueprint, render_template, request, jsonify
from .mpesa import lipa_na_mpesa_online

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/stk-push', methods=['POST'])
def stk_push():
    data = request.get_json()
    phone = data.get('phone')
    amount = data.get('amount')
    
    if not phone or not amount:
        return jsonify({'message': 'Phone and amount are required'}), 400

    response = lipa_na_mpesa_online(phone, amount)
    return jsonify(response)

@bp.route('/api/payment-callback', methods=['POST'])
def payment_callback():
    data = request.get_json()
    print("M-Pesa callback:", data)
    return jsonify({'ResultCode': 0, 'ResultDesc': 'Success'})
