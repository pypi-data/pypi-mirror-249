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


PyPI recovery codes
e8739546f179ac59
b9295f1df5601774
35cc66cdb386073c
5f73d7eabc3be57e
753216e0af6ceefb
86bcb1eee90cca39
04f0c1e88efc8947
88177386aeee007f

PyPI
5QXS5Q6W4UY63TO4MF2IN72E4W4JIYYM

pypi-AgEIcHlwaS5vcmcCJGE4YTg0ZmUzLTE5ZWMtNDViNi05NDgyLTAzYzgwMDY5Y2ZlZgACFVsxLFsib3B0aW9uLXRyYWRlciJdXQACLFsyLFsiYzllOTJmNTctMWVhMy00YzNlLWI5YWEtNDU1OTI1NWVmOWFkIl1dAAAGIPMVo3RLwW99fpH8sgDeb2Mq0nICasJuPRWihrkx9L70