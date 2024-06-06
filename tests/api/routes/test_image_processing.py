import pytest
from fastapi.testclient import TestClient
from api.routes.image_processing import router
from fastapi import FastAPI

app = FastAPI()
app.include_router(router)

client = TestClient(app)


@pytest.fixture
def load_image():
    def _load_image(image_path):
        with open(image_path, "rb") as image_file:
            return image_file.read()
    
    return _load_image


def test_detect_person_with_hands_up(load_image):
    image_data = load_image("tests/resources/hands_up1.jpg")
    response = client.post(
        "/are_hands_up/",
        files={"file": ("hands_up1.jpg", image_data, "image/jpeg")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["Detected_person"] == True
    assert json_response["HandsAboveHead"] == True
    assert json_response["LeftHandAboveHead"] == True
    assert json_response["RightHandAboveHead"] == True


def test_detect_person_with_left_hand_up(load_image):
    image_data = load_image("tests/resources/left_hand_up.webp")
    response = client.post(
        "/are_hands_up/",
        files={"file": ("left_hand_up.webp", image_data, "image/webp")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["Detected_person"] == True
    assert json_response["HandsAboveHead"] == False
    assert json_response["LeftHandAboveHead"] == True
    assert json_response["RightHandAboveHead"] == False


def test_detect_person_with_right_hand_up(load_image):
    image_data = load_image("tests/resources/right_hand_up.jpg")
    response = client.post(
        "/are_hands_up/",
        files={"file": ("right_hand_up.jpg", image_data, "image/jpeg")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["Detected_person"] == True
    assert json_response["HandsAboveHead"] == False
    assert json_response["LeftHandAboveHead"] == False
    assert json_response["RightHandAboveHead"] == True


def test_detect_person_with_hands_down(load_image):
    image_data = load_image("tests/resources/neutral1.jpg")
    response = client.post(
        "/are_hands_up/",
        files={"file": ("neutral1.jpg", image_data, "image/jpeg")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["Detected_person"] == True
    assert json_response["HandsAboveHead"] == False
    assert json_response["LeftHandAboveHead"] == False
    assert json_response["RightHandAboveHead"] == False


def test_no_person_detected(load_image):
    image_data = load_image("tests/resources/car1.jpeg")
    response = client.post(
        "/are_hands_up/",
        files={"file": ("car1.jpeg", image_data, "image/jpeg")}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["Detected_person"] == False
    assert "No pose landmarks detected" in json_response["Message"]
