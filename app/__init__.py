import os
import json
from flask import Flask, request, abort, jsonify, render_template


app = Flask(__name__)

path = os.path.abspath(os.path.join(os.getcwd(), ".."))

normalGamesJsonFile = open(path+'/crawler/json/normalGames.json' ,"r")
normalGamesJson = json.loads(normalGamesJsonFile.read())

contrastJsonFile = open(path+'/crawler/json/contrast.json' ,"r")
contrastJson = json.loads(contrastJsonFile.read())


@app.route('/', methods=['GET'])
def index():

	url = request.url+'?'

	s = request.args.get('s', False)
	c = request.args.get('c', False)
	t = request.args.get('t', False)
	n = request.args.get('n', False)

	sportData = normalGamesJson
	contrast = contrastJson['s']
	if s :
		url = request.url+'&'
		sportData = normalGamesJson[s]
		contrast = contrastJson['c']
	if c :
		sportData = normalGamesJson[s][c]
		contrast = contrastJson['t']
	if t :
		sportData = normalGamesJson[s][c][t]
		contrast = contrastJson['n']
	if n :
		sportData = normalGamesJson[s][c][t][n]
		contrast = None

	return render_template('index.html', sport=sportData, contrast=contrast, url=url)


if __name__ == '__main__':
	app.run(debug=True)