from checker import Checker
import configs

app = Checker()
app.check_range(configs.area_code, configs.start_range, configs.end_range)
