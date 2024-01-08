option trader

# package development
cd option_trader/src
pip install e .
py -m build
py -m twine upload --repository pypi dist/*
docker run --restart always -p 8000:8000 docker.io/jihuang/optiontrader
docker run --restart always -p 8000:8000 --mount type=bind,source="$(pwd)"/,target=/option_trader/sites docker.io/jihuang/optiontrader

#tests
https://docs.pytest.org/en/latest/explanation/goodpractices.html

#SSH setup
https://woshub.com/connect-to-windows-via-ssh/
https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_keymanagement
gateway installation
apt-get download curl
apt-get install curl
IBDOWNLOAD=https://download.interactivebrokers.com/installers/ibgateway

https://ibkrcampus.com/ibkr-quant-news/interactive-brokers-gateway-install-setup/
chmod u+x ibgateway-standalone-linux-x64.sh
./ibgateway-standalone-linux-x64.sh
# Stable version
curl -o ibgateway-standalone-linux-x64.sh $IBDOWNLOAD/stable-standalone/ibgateway-stable-standalone-linux-x64.sh
# Latest version
curl -o ibgateway-standalone-linux-x64.sh $IBDOWNLOAD/latest-standalone/ibgateway-latest-standalone-linux-x64.sh
apt-get install libx11-6
apt-get install libxext6
apt-get install libxrender1
apt-get install libxtst6
apt-get install libxi6