# Free Proxy Hunter
This app can get the list of the max 10 free proxies and tests response times of the proxies, then returns top 3 proxies as list with their response times.

## Installation:

### Automatic:
- Execute `curl -sSL https://raw.githubusercontent.com/RecNes/free-proxy-hunter/main/install.sh | bash` command in a linux console.
- Execute `curl -sSL https://raw.githubusercontent.com/RecNes/free-proxy-hunter/main/install.bat -o install.bat && install.bat` in cmd.
- Execute `curl.exe -sSL "https://raw.githubusercontent.com/RecNes/free-proxy-hunter/main/install.bat" -OutFile "install.bat"; .\install.bat` in Power Shell

### Manual:
- Fetch with `git clone https://github.com/RecNes/free-proxy-hunter.git`
- Create environment in free-proxy-hunter directory with `python -m venv venv`
- Activate the environment with `source venv/bin/activate`
- Install required libraries `pip install -r requirements.txt`

## Usage:
- Go into `free-proxy-hunter` directory
- Activate the environment with `source venv/bin/activate`
- Run the app wiith `python fpc.py`

