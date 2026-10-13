from src.app import activities


def test_get_activities_returns_expected_activity_data(client):
    # Arrange
    expected_activity_names = {"Chess Club", "Programming Class", "Soccer Team"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity_names.issubset(payload)
    assert payload["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_for_activity_adds_student_to_participants(client):
    # Arrange
    activity_name = "Soccer Team"
    student_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {student_email} for {activity_name}"}
    assert student_email in activities[activity_name]["participants"]


def test_signup_for_activity_rejects_duplicate_registration(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_for_missing_activity_returns_not_found(client):
    # Arrange
    activity_name = "Not Real Club"
    student_email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": student_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_participant_removes_student(client):
    # Arrange
    activity_name = "Chess Club"
    student_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": student_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {student_email} from {activity_name}"}
    assert student_email not in activities[activity_name]["participants"]


def test_unregister_participant_returns_not_found_for_missing_student(client):
    # Arrange
    activity_name = "Soccer Team"
    student_email = "missing@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": student_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_redirect = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_redirect
