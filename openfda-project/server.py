from flask import Flask,request,abort,redirect
import json
import http.client

app = Flask(__name__)








@app.route("/")
def encuesta():
    html_encuesta = """<!DOCTYPE html>
<html>
<body>

<h2><center>Medicamentos</center></h2>

<center><form action="searchDrug">
  Principio activo:<br>
  <input type="text" name="active_ingredient" value="">
  <br>
  Límite:<br>
  <input type="text" name="limit" value="">
  <br><br>
  <input type="submit" value="Enviar">
</form></center> 



<h2><center>Empresas</center></h2>

<center><form action="searchCompany">
  Empresa:<br>
  <input type="text" name="company" value="">
  <br>
  Límite:<br>
  <input type="text" name="limit" value="">
  <br><br>
  <input type="submit" value="Enviar">
</form> </center>



<h2><center>Listado de medicamentos</center></h2>

<center><form action="listDrugs">

  Límite:<br>
  <input type="text" name="limit" value="">
  <br><br>
  <input type="submit" value="Enviar">
</form> </center>




<h2><center>Listado de empresas</center></h2>

<center><form action="listCompanies">

  Límite:<br>
  <input type="text" name="limit" value="">
  <br><br>
  <input type="submit" value="Enviar">
</form> </center>



<h2><center>Listado de advertencias</center></h2>

<center><form action="listWarnings">

  Límite:<br>
  <input type="text" name="limit" value="">
  <br><br>
  <input type="submit" value="Enviar">
</form> </center>


</body>
</html>"""
    return html_encuesta




# searchDrug
@app.route('/searchDrug')
def get_drug():
    principio_activo = request.args.get('active_ingredient')
    limit = request.args.get('limit')
    if limit:
        limit = limit

    else:
        limit = str(10)

    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET",
                 "https://api.fda.gov/drug/label.json?search=active_ingredient:" + principio_activo + "&limit=" + limit,
                 None, headers)

    info = conn.getresponse()

    print(info.status, info.reason)
    archivo_raw = info.read().decode("utf-8")
    conn.close()

    archivo = json.loads(archivo_raw)

    info = ""

    if "results" in archivo:

        for drug in archivo['results']:

            if 'generic_name' in drug['openfda']:
                info += "<li>" + str(drug['openfda']['generic_name']) + "</li>"

            else:
                info += "<li> Medicamento sin nombre genérico</li>"

        contenido = """
              <!doctype html>
              <html>
              <body>
                <h1>Resultado búsqueda medicamentos</h2> """

        contenido += "<ul>" + info + """</ul></body></html>"""

    else:
        contenido = """
                      <!doctype html>
                      <html>
                      <body>
                        <h1>No hay resultados</h2> """

    return contenido


# searchCompany
@app.route('/searchCompany')

def get_company():
    company = request.args.get('company')
    limit = request.args.get('limit')

    if limit:
        limit = limit

    else:
        limit= str(10)

    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET",
             "https://api.fda.gov/drug/label.json?search=openfda.manufacturer_name:" + company + "&limit=" + limit,
             None, headers)

    info = conn.getresponse()

    print(info.status, info.reason)
    archivo_raw = info.read().decode("utf-8")
    conn.close()

    archivo = json.loads(archivo_raw)

    info = ""
    if "results" in archivo:
        for drug in archivo['results']:

            if 'manufacturer_name' in drug['openfda']:
                info += "<li>" + str(drug['openfda']['manufacturer_name']) + "</li>"

            else:
                info += "<li> Desconocida </li>"

        contenido = """
              <!doctype html>
              <html>
              <body>
                <h1>Resultado búsqueda empresas</h2> """

        contenido += "<ul>" + info + """</ul></body></html>"""


    else:

        contenido = """
              <!doctype html>
              <html>
              <body>
                <h1>No hay resultados</h2> """

    return contenido












# listDrugs
@app.route('/listDrugs')

def list_drugs():
    limit = request.args.get('limit')
    if limit:
        limit = limit

    else:
        limit = str(10)

    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET",
                 "https://api.fda.gov/drug/label.json?&limit=" + limit,
                 None, headers)

    info = conn.getresponse()

    print(info.status, info.reason)
    archivo_raw = info.read().decode("utf-8")
    conn.close()

    archivo = json.loads(archivo_raw)

    info = ""



    for drug in archivo['results']:

        if 'generic_name' in drug['openfda']:
            info += "<li>" + str(drug['openfda']['generic_name']) + "</li>"

        else:
            info += "<li> Medicamento sin nombre genérico</li>"

    contenido = """
                  <!doctype html>
                  <html>
                  <body>
                    <h1>Resultado búsqueda medicamentos</h2> """

    contenido += "<ul>" + info + """</ul></body></html>"""


    return contenido


# listCompanies
@app.route('/listCompanies')
def list_companies():
    limit = request.args.get('limit')
    if limit:
        limit = limit

    else:
        limit = str(10)

    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET",
                 "https://api.fda.gov/drug/label.json?&limit=" + limit,
                 None, headers)

    info = conn.getresponse()

    print(info.status, info.reason)
    archivo_raw = info.read().decode("utf-8")
    conn.close()

    archivo = json.loads(archivo_raw)

    info = ""

    for drug in archivo['results']:

        if 'manufacturer_name' in drug['openfda']:
            info += "<li>" + str(drug['openfda']['manufacturer_name']) + "</li>"

        else:
            info += "<li> Medicamento sin nombre genérico</li>"

    contenido = """
                      <!doctype html>
                      <html>
                      <body>
                        <h1>Resultado búsqueda medicamentos</h2> """

    contenido += "<ul>" + info + """</ul></body></html>"""

    return contenido


# listado de advertencias
@app.route('/listWarnings')

def list_warnings():
    limit = request.args.get('limit')
    if limit:
        limit = limit

    else:
        limit = str(10)

    headers = {'User-Agent': 'http-client'}
    conn = http.client.HTTPSConnection("api.fda.gov")
    conn.request("GET",
                 "https://api.fda.gov/drug/label.json?&limit=" + limit,
                 None, headers)

    info = conn.getresponse()

    print(info.status, info.reason)
    archivo_raw = info.read().decode("utf-8")
    conn.close()

    archivo = json.loads(archivo_raw)

    info = ""

    for drug in archivo['results']:

        if 'warnings' in drug:
            info += "<li>" + str(drug['warnings']) + "</li>"

        else:
            info += "<li> Medicamento sin nombre genérico</li>"

    contenido = """
                      <!doctype html>
                      <html>
                      <body>
                        <h1>Resultado búsqueda medicamentos</h2> """

    contenido += "<ul>" + info + """</ul></body></html>"""

    return contenido







@app.route('/secret')

def login():
    return abort(401)




@app.route('/redirect')

def redireccion():
    return redirect('http://localhost:8000/', code=302)






if __name__ == "__main__":
    app.run(host="127.0.0.1",port=8000)