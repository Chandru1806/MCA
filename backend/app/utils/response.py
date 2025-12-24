from flask import jsonify

def success_response(data=None, message="Success", status=200):
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response), status

def error_response(message="Error", code=None, details=None, status=400):
    error_obj = {'message': message}
    if code:
        error_obj['code'] = code
    if details:
        error_obj['details'] = details
    return jsonify({'success': False, 'error': error_obj}), status
