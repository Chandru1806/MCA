from flask import Blueprint, request, jsonify, send_from_directory, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.controllers.pdf_controller import PDFController

pdf_bp = Blueprint('pdf', __name__, url_prefix='/api/pdf')

@pdf_bp.post('/upload')
@jwt_required()
def upload_pdf():
    profile_id = get_jwt_identity()
    
    if 'pdf' not in request.files:
        return jsonify({'error': 'No PDF file'}), 400
    
    pdf_file = request.files['pdf']
    if pdf_file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400
    
    # Get manual bank selection (required for now)
    bank = request.form.get('bank', '').strip().upper()
    if not bank or bank not in ['HDFC', 'KOTAK', 'SBI', 'ICICI', 'AXIS', 'CUB', 'IDFC']:
        return jsonify({'error': 'Bank required. Valid: HDFC, KOTAK, SBI, ICICI, AXIS, CUB, IDFC'}), 400
    
    try:
        result = PDFController.process_pdf(
            pdf_file, 
            profile_id, 
            current_app.config['UPLOAD_FOLDER'],
            current_app.config['OUTPUT_FOLDER'],
            bank
        )
        return jsonify({'success': True, 'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@pdf_bp.get('/download/<filename>')
@jwt_required()
def download_csv(filename):
    return send_from_directory(
        current_app.config['OUTPUT_FOLDER'], 
        filename, 
        as_attachment=True
    )
