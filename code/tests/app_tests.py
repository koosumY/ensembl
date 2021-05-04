import requests


def test_check_status_code_equals_200():
    response = requests.get("http://0.0.0.0:5000/gene_suggest?query=w&species=rhinopithecus_roxellana")
    assert response.status_code == 200


def test__check_content_type_equals_json():
    response = requests.get("http://0.0.0.0:5000/gene_suggest?query=wnt&species=rhinopithecus_roxellana")
    assert response.headers["Content-Type"] == "application/json"


def test_check_species_equals_amazona_collaria():
    response = requests.get("http://0.0.0.0:5000/gene_suggest?query=w&species=amazona_collaria")
    response_body = response.json()
    assert response_body[0]["resultList"][0]["species"] == "amazona_collaria"


def test_check_limit_equals_15():
    response = requests.get("http://0.0.0.0:5000/gene_suggest?query=wnt5&limit=15")
    response_body = response.json()
    assert response_body[0]["request"][0]["pageSize"] == 15
