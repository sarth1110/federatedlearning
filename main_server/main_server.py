from flask import Flask, request,render_template
import requests, json
import ast
from fl_agg import model_aggregation

app = Flask(__name__)

@app.route('/')
def hello():
	return "Server running !"

@app.route('/clientstatus', methods=['GET','POST'])
def client_status():
	url = "http://localhost:8001/serverack"

	if request.method == 'POST':
		client_port = request.json['client_id']
		
		with open('/main_server/clients.txt', 'a+') as f:
			f.write('http://localhost:' + client_port + '/\n')

		print(client_port)

		if client_port:
			serverack = {'server_ack': '1'}
			return str(serverack)
		else:
			return "Client status not OK!"
	else:
		return "Client GET request received!"
		
@app.route('/cfile', methods=['POST'])
def filename():
	if request.method == 'POST':
		file = request.files['model'].read()
		fname = request.files['json'].read()
		# cli = request.files['id'].read()

		fname = ast.literal_eval(fname.decode("utf-8"))
		cli = fname['id']+'\n'
		fname = fname['fname']
		
		return "<h1>str(fname)</h1>"
		
@app.route('/cmodel', methods=['POST'])
def getmodel():
	if request.method == 'POST':
		file = request.files['model'].read()
		fname = request.files['json'].read()
		# cli = request.files['id'].read()

		fname = ast.literal_eval(fname.decode("utf-8"))
		cli = fname['id']+'\n'
		fname = fname['fname']

		# with open('clients.txt', 'a+') as f:
		# 	f.write(cli)
		
		print(fname)
		wfile = open("/main_server/client_models/"+fname, 'wb')
		wfile.write(file)
			
		return "Model received!"
	else:
		return "No file received!"
		
@app.route('/aggregate_models')
def perform_model_aggregation():
	model_aggregation()
	return 'Model aggregation done!\nGlobal model written to persistent storage.'

"""@app.route('/send_model_secagg')
def send_agg_to_mainserver():
	file = open("/main_server/agg_model/agg_model.h5", 'rb')
	data = {'fname':'agg_model.h5', 'id':'sec_agg'}
	files = {
		'json': ('json_data', json.dumps(data), 'application/json'),
		'model': ('agg_model.h5', file, 'application/octet-stream')
	}
	
	print('aggmodel')
	req = requests.post(url='http://localhost:8000/secagg_model', files=files)
	print(req.status_code)
	
	return render_template("recive.html")
	
@app.route('/secagg_model', methods=['POST'])
def get_secagg_model():
	if request.method == 'POST':
		file = request.files['model'].read()
		fname = request.files['json'].read()

		fname = ast.literal_eval(fname.decode("utf-8"))
		cli = fname['id']+'\n'
		fname = fname['fname']

		wfile = open("/main_server/agg_model/"+fname, 'wb')
		wfile.write(file)
			
		return render_template("recive.html")
	else:
		return "No file received!"
"""

@app.route('/send_model_clients')
def send_agg_to_clients():
	clients = ''
	with open('/main_server/clients.txt', 'r') as f:
		clients = f.read()
	clients = clients.split('\n')
	
	for c in clients:
		if c != '':
			file = open("/main_server/agg_model/agg_model.h5", 'rb')
			data = {'fname':'agg_model.h5'}
			files = {
				'json': ('json_data', json.dumps(data), 'application/json'),
				'model': ('agg_model.h5', file, 'application/octet-stream')
			}
			
			print(c+'aggmodel')
			req = requests.post(url=c+'aggmodel', files=files)
			print(req.status_code)
	
	return "Aggregated model sent !"




if __name__ == '__main__':
	app.run(host='localhost', port=8000, debug=False, use_reloader=True)















