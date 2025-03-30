# Pinewood Lane Indicator

This is the specs and code for a Pinewood Derby lane indicator, basically a pair of "electric eye" devices to call a winner by lane. The device uses an [Adafruit Trinket M0](https://www.adafruit.com/product/3500) microcontroller running [CircuitPython](https://circuitpython.org/) to constantly monitor a pair of infrared recievers opposite 940nm infrared LEDs. The first lane to have a majority of the light blocked by a passing race car is flagged as the winner.


## Track Specs

Some info about the track used with this project.

* Total Width: 11-7/8”
* Lane Track Centers: 1.5” Wide
* 3.75” between lane edges
* 5/8” on each side of lane for vehicles
* 2.5” between max lane widths


## Parts

- [1x Adafruit Trinket M0](https://www.adafruit.com/product/3500)
	- Digital #3/A3 as input
	- Digital #4/A4 as input
	- 3.3V out from Trinket M0 to IR LEDs

- [5mm 940nm LEDs Infrared Emitters and IR Receivers](https://a.co/d/4zAPhaF)

		Clear: Emitter
		Black: Receiver
		Receiving Angle: 40 degrees
		Forward Voltage: 1.2-1.3V, Power: 0.15 W
		Maximum power: 70 mw;
		Maximum forward current: 30 ma;
		Maximum reverse voltage: 5 v;
		Maximum pulse current peak: 75 ma;

- 2x 5K pull-down resistors
	- Used with IR receivers

- 2x 5mm Green LEDs
	- Use a 100ohm resistor for each

- AA Battery Box (3xAA) for 4.5V supply via USB


## References

* [Trinket M0 Pinout Reference](https://cdn-learn.adafruit.com/assets/assets/000/049/778/original/
adafruit_products_Adafruit_Trinket_M0.png)
* [https://www.electronicwings.com/arduino/ir-communication-using-arduino-uno](https://www.electronicwings.com/arduino/ir-communication-using-arduino-uno)
* [https://startrobotics.blogspot.com/2013/05/how-to-use-ir-led-and-photodiode-with-arduino.html](https://www.electronicwings.com/arduino/ir-communication-using-arduino-uno)
* [Photo Album](Photos/)