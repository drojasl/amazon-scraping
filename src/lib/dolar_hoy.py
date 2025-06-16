import requests

def get_trm_banrep():
    try:
        url = "https://www.datos.gov.co/resource/32sa-8pi3.json"
        params = {
            '$limit': 1,
            '$order': 'vigenciahasta DESC'
        }
        response = requests.get(url, params=params)
        data = response.json()[0]
        trm = float(data['valor'])
        fecha = data['vigenciahasta'][:10]
        
        print(f"🏦 TRM Colombia ({fecha}): 1 USD = ${trm:,.2f} COP")
        return trm
        
    except Exception as e:
        print(f"Error BanRep: {e}")
        return None