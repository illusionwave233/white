from checker import Checker
import configs
import logging
app = Checker()
print("starting checking numbers from a range...")
app.check_range(configs.area_code, configs.start_range, configs.end_range)
