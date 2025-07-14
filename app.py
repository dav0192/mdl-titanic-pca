from flask import Flask, request, render_template, jsonify;
import joblib;
import pandas as pd;
import logging;
import numpy as np;

# Creando la instancia de flask
app = Flask(__name__);

# Configurando el registro
logging.basicConfig(level = logging.DEBUG);

# Cargando los codificadores
sex_enc = joblib.load("./pkl/sex_encoder.pkl");
ticket_enc = joblib.load("./pkl/ticket_encoder.pkl");
app.logger.debug("Codificadores cargados");

# Cargando los escaladores
age_scl = joblib.load("./pkl/age_scaler.pkl");
fare_scl = joblib.load("./pkl/fare_scaler.pkl");
ticket_scl = joblib.load("./pkl/ticket_scaler.pkl");
app.logger.debug("Escaladores cargados");

# Cargando el PCA
pca_comp = joblib.load("./pkl/pca_components.pkl");
app.logger.debug("PCA cargado");

# Cargando el modelo entrenado
model = joblib.load("./pkl/rnfc_titanic.pkl");
app.logger.debug("Modelo cargado");

# Raíz de la API
@app.route('/')
def home():
    # Devuelve el formulario HTML
    return render_template("index.html");

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Recibiendo información de la petición JSON
        data_js = request.get_json();
        # Separando los datos del request
        sex = str(data_js.get("sex"));
        age = float(data_js.get("age"));
        fare = float(data_js.get("fare"));
        ticket = str(data_js.get("ticket"));
        # Codificando valores
        sex_encoded = sex_enc.transform(pd.DataFrame({"Sex": [sex]}));
        ticket_encoded = ticket_enc.transform(pd.DataFrame({"Ticket": [ticket]}));
        # Escalando valores
        age_scaled = age_scl.transform(pd.DataFrame({"Age": [age]}));
        fare_scaled = fare_scl.transform(pd.DataFrame({"Fare": [fare]}));
        ticket_scaled = ticket_scl.transform(pd.DataFrame({"Ticket_encoded": [ticket_encoded]}));
        # app.logger.debug(sex, age, fare, ticket);
        # Creando df para crear los PCA
        final_df = pd.DataFrame({"Sex_encoded": [sex_encoded], "Age_scaled": [age_scaled], "Fare_scaled": [fare_scaled], "Ticket_scaled": [ticket_scaled]});
        pca_orig = pca_comp.transform(final_df);
        # Usando el modelo
        prediction = model.predict([[pca_orig[0][0], pca_orig[0][1]]]);
        # Devolviendo la respuesta en JSON
        return jsonify({"Survived": int(prediction[0])}), 200;
    except Exception as e:
        app.logger.error(f'Error en la clasificación: {str(e)}');
        return jsonify({'error': str(e)}), 400;

# Iniciar la ejecución de la API
if __name__ == '__main__':
    app.run(debug = True);