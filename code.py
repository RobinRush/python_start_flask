from flask import Flask, render_template
import datetime
import RPi.GPIO as gpio

app = Flask(__name__)

gpio.setmode(gpio.BCM)
pins = {
	18:{'name':'18','state':gpio.LOW},
	23:{'name':'23','state':gpio.LOW},
	24:{'name':'24','state':gpio.LOW},
	25:{'name':'25','state':gpio.LOW}
}
for pin in pins:
	gpio.setup(pin,gpio.OUT)
	gpio.output(pin,gpio.LOW)

@app.route("/")
def fun_default():
	for pin in pins:
		pins[pin]['state'] = gpio.input(pin)
	retData = {
		'pins' : pins
	}
	return render_template('main.html', **retData)

@app.route("/light/<pin>/<action>")
def changeLight(pin,action):

	print(pin + ',' + action)
	pin = int(pin)
	try:
		if action == 'on':
			gpio.output(pin,gpio.HIGH)
		else:
			gpio.output(pin,gpio.LOW)
			pins[pin]['state'] = gpio.input(pin)
	except:
		gpio.cleanup()
	retData = {
		'pins':pins
	}

	return render_template("main.html",**retData)

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8081,debug=True)