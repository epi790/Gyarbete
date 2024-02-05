from flask import Flask, render_template, request, make_response, send_file, jsonify
import keys
import ast
import base64
from io import BytesIO
from apscheduler.schedulers.background import BackgroundScheduler
import json


app = Flask(__name__)

@app.route('/')
def index():
    private_key = request.cookies.get('privatekey')
    sessionId = request.cookies.get('sessionId')

    if not private_key:
        
        # 'privatekey' cookie not set, generate and set the cookie
        private_key = keys.generate_private_key_pem().decode()
        
        # Create a response object
        resp = make_response(render_template('index.html'))
        
        # Set the 'privatekey' cookie with the generated key
        resp.set_cookie('privatekey', private_key, max_age=3600, httponly=False, samesite='None')

        return resp

    derived_key_image_data, public_key_image_data = create_image_datas()
    
        
    return render_template('index.html', derived_key_image_data=derived_key_image_data, public_key_image_data=public_key_image_data)

def get_cookie():
    # Try to get the 'my_cookie' from the request's cookies
    session = request.cookies.get('sessionId')
    if session:
        return f'The value of my_cookie is: {session}'
    else:
        return 'Cookie not found.'

@app.route('/create_image_datas_jsonified')
def create_image_datas_jsonified():

    #(request.cookies.get('sessionId'))
    #print(request.cookies.get('privatekey'))

    private_key = request.cookies.get('privatekey')
    sessionId = request.cookies.get('sessionId')

    private_key = private_key.encode()
    private_key = keys.private_pem_to_key(private_key)
    shared_key = keys.generate_shared_key(private_key, keys.public_pem_to_key(keys.publicmasterkey))
    key_now = keys.derive_new_key_from_time(shared_key)

    derived_key_image_url = keys.generate_qr_from_key(f"{base64.b64encode(key_now)},{sessionId}")
    image_io = BytesIO()
    derived_key_image_url.save(image_io, 'PNG')
    derived_key_image_data = 'data:image/png;base64,' + base64.b64encode(image_io.getvalue()).decode('ascii')
   

    public_key = private_key.public_key()
    public_key = keys.public_key_to_pem(public_key)
    
    public_key_qr = keys.generate_qr_from_key(f"{public_key.decode()},{sessionId}")
    image_io = BytesIO()
    public_key_qr.save(image_io, 'PNG')
    
    
    public_key_image_data = 'data:image/png;base64,' + base64.b64encode(image_io.getvalue()).decode('ascii')

    return jsonify({'derived': derived_key_image_data, 'public':public_key_image_data})



# @app.route('/update_images')
# def update_images():
    
#     derived_key_image_data = "data:image/png;base64,derived_key_image_base64_data"
#     public_key_image_data = "data:image/png;base64,public_key_image_base64_data"

#     return jsonify({'derived': derived_key_image_data, 'public': public_key_image_data})



def create_image_datas():
    private_key = request.cookies.get('privatekey')
    sessionId = request.cookies.get('sessionId')
    private_key = private_key.encode()
    private_key = keys.private_pem_to_key(private_key)
    shared_key = keys.generate_shared_key(private_key, keys.public_pem_to_key(keys.publicmasterkey))
    key_now = keys.derive_new_key_from_time(shared_key)

    derived_key_image_url = keys.generate_qr_from_key(f"{base64.b64encode(key_now)},{sessionId}")
    image_io = BytesIO()
    derived_key_image_url.save(image_io, 'PNG')
    derived_key_image_data = 'data:image/png;base64,' + base64.b64encode(image_io.getvalue()).decode('ascii')
   

    public_key = private_key.public_key()
    public_key = keys.public_key_to_pem(public_key)
    
    public_key_qr = keys.generate_qr_from_key(f"{public_key.decode()},{sessionId}")
    image_io = BytesIO()
    public_key_qr.save(image_io, 'PNG')
    
    
    public_key_image_data = 'data:image/png;base64,' + base64.b64encode(image_io.getvalue()).decode('ascii')

    return derived_key_image_data, public_key_image_data


# scheduler = BackgroundScheduler()
# scheduler.add_job(index, 'interval', seconds=1)  # Run my_job every 10 seconds
# scheduler.start()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)