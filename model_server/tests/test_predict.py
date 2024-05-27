import requests

def test_predict_endpoint():

    input_json_format = '{"Age":{"0":40},"Sex":{"0":"M"},"ChestPainType":{"0":"ATA"},"RestingBP":{"0":140},"Cholesterol":{"0":289},"FastingBS":{"0":0},"RestingECG":{"0":"Normal"},"MaxHR":{"0":172},"ExerciseAngina":{"0":"N"},"Oldpeak":{"0":0.0},"ST_Slope":{"0":"Up"}}'
    response = requests.post('http://localhost:8080/predict', json=input_json_format)
    assert response.status_code == 200, "El servicio no respondió correctamente a /predict"
    