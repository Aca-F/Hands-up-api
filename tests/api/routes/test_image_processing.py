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


@pytest.mark.parametrize("image_path, mime_type, expected_detected_person, expected_hands_up", [
    ("tests/resources/car1.jpeg", "image/jpeg", False, False),  # No person detected
    ("tests/resources/hands_up1.jpg", "image/jpeg", True, True),  # Person detected with hands up
    ("tests/resources/left_hand_up.webp", "image/webp", True, False),  # Person detected, left hand up
    ("tests/resources/neutral1.jpg", "image/jpeg", True, False),  # Person detected, no hands up
    ("tests/resources/right_hand_up.jpg", "image/jpeg", True, False),  # Person detected, right hand up
    ("tests/resources/three_people_1_up.jpg", "image/jpeg", True, True),  # Three people, one with hands up
    ("tests/resources/three_people_neutral.webp", "image/webp", True, False),  # Three people, no hands up
    ("tests/resources/two_people_1_up.webp", "image/webp", True, True),  # Two people, one with hands up
], ids=[
    "no_person_detected_car",
    "person_with_hands_up",
    "person_with_left_hand_up",
    "person_with_no_hands_up",
    "person_with_right_hand_up",
    "three_people_one_with_hands_up",
    "three_people_no_hands_up",
    "two_people_one_with_hands_up",
])
def test_are_hands_up(load_image, image_path, mime_type, expected_detected_person, expected_hands_up):
    image_data = load_image(image_path)
    response = client.post(
        "/are_hands_up/",
        files={"file": ("file", image_data, mime_type)}
    )
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["Detected_person"] == expected_detected_person
    assert json_response["Hands_up"] == expected_hands_up
