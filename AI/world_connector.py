import requests

class WorldConnector:

    def world_status(self):

        try:

            r=requests.get(
            "https://api.coindesk.com/v1/bpi/currentprice.json",
            timeout=3)

            data=r.json()

            return {

            "btc":data["bpi"]["USD"]["rate"]

            }

        except:

            return {"btc":"offline"}
