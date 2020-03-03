class Pin:
    """A basic Pin class for use with FT232H."""

    IN = 0
    OUT = 1
    LOW = 0
    HIGH = 1

    ft232h_gpio = None
    controller_one = None
    controller_two = None
    def __init__(self, control="one", pin_id=None):
        # setup GPIO controller if not done yet
        # use one provided by I2C as default
        if not Pin.ft232h_gpio:
            from pyftdi.i2c import I2cController
            i2c = I2cController()
            i2c.configure("ftdi://ftdi:ft232h:white/1")
            Pin.ft232h_gpio = i2c.get_gpio()
            Pin.controller_one = i2c.get_gpio()
            i2c_second = I2cController()
            i2c_second.configure("ftdi://ftdi:ft232h:black/1")
            Pin.controller_two=i2c_second.get_gpio()
        # check if pin is valid
        if pin_id:
            if Pin.ft232h_gpio.all_pins & 1 << pin_id == 0:
                raise ValueError("Can not use pin {} as GPIO.".format(pin_id))
        # ID is just bit position
        if control=="one":
            self.controller=Pin.controller_one
        else:
            self.controller=Pin.controller_two
        self.id = pin_id

    def init(self, mode=IN, pull=None):
        if not self.id:
            raise RuntimeError("Can not init a None type pin.")
        # FT232H does't have configurable internal pulls?
        if pull:
            raise ValueError("Internal pull up/down not currently supported.")
        pin_mask = self.controller.pins | 1 << self.id
        current = self.controller.direction
        if mode == self.OUT:
            current |= 1 << self.id
        else:
            current &= ~(1 << self.id)
        self.controller.set_direction(pin_mask, current)

    def value(self, controller, val=None):
        if not self.id:
            raise RuntimeError("Can not access a None type pin.")
        current = self.controller.read(with_output=True)
        # read
        if val is None:
            return 1 if current & 1 << self.id != 0 else 0
        # write
        elif val in (self.LOW, self.HIGH):
            if val == self.HIGH:
                current |= 1 << self.id
            else:
                current &= ~(1 << self.id)
            # must mask out any input pins
            self.controller.write(current & Pin.controller.direction)
        # release the kraken
        else:
            raise RuntimeError("Invalid value for pin")

# create pin instances for each pin
# D0 to D3 are used by I2C/SPI
D4_1 = Pin(4, "one")
D5_1 = Pin(5, "one")
D6_1 = Pin(6, "one")
D7_1 = Pin(7, "one")
C0_1 = Pin(8, "one")
C1_1 = Pin(9, "one")
C2_1 = Pin(10, "one")
C3_1 = Pin(11, "one")
C4_1 = Pin(12, "one")
C5_1 = Pin(13, "one")
C6_1 = Pin(14, "one")
C7_1 = Pin(15, "one")

D4_2 = Pin(4, "two")
D5_2 = Pin(5, "two")
D6_2 = Pin(6, "two")
D7_2 = Pin(7, "two")
C0_2 = Pin(8, "two")
C1_2 = Pin(9, "two")
C2_2 = Pin(10, "two")
C3_2 = Pin(11, "two")
C4_2 = Pin(12, "two")
C5_2 = Pin(13, "two")
C6_2 = Pin(14, "two")
C7_2 = Pin(15, "two")
# C8 and C9 are not GPIO

# create None type pins for I2C and SPI since they are expected to be defined
SCL = Pin()
SDA = Pin()
SCK = SCLK = Pin()
MOSI = Pin()
MISO = Pin()
