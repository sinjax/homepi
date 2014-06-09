import sys, os
sys.path.append(os.getcwd())
from homepi import app

app.run(host='0.0.0.0', port=7171, debug=True)
