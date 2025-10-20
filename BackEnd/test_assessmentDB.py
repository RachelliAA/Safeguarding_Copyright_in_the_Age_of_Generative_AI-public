# Assumes your AssessmentDB and Assessment classes are already defined in the project
from database.assessment_DB import AssessmentDB
from core.init_DB import init_db_client

def test_insert_get_delete():
    init_db_client()
    db = AssessmentDB()

    # Create a test document
    assessment = {
        "image_url": "http://example.com/test.png",
        "policy_id": "policy-test-1",
        "results": {
            "image_to_text": "This is a test image.",
            "image_to_json": {"key": "value"},
            "compare_images": {"similarity_score": 0.95}
        },
        "policy_breach": False,
        "used_tools": ["image_to_text", "image_to_json", "compare_images"],
        "action_id": "action-test-1",
        "time_stamp": "2023-10-01T12:00:00Z"
    }

    # Insert
    inserted_id = db.insert_assessment(assessment)
    print("Inserted ID:", inserted_id)

    # Get
    result = db.get_assessment(inserted_id)
    print("Retrieved:", result)

    if result and result["policy_id"] == "policy-test-1":
        print("✅ Get test passed")
    else:
        print("❌ Get test failed")

    # Delete
    deleted = db.delete_assessment(inserted_id)
    print("Deleted:", deleted)

    if deleted:
        print("✅ Delete test passed")
    else:
        print("❌ Delete test failed")
    #trying to get it again
    if result and result["policy_id"] == "policy-test-1":
        print("✅ Get test passed")
    else:
        print("❌ Get test failed")



# Run the test
test_insert_get_delete()
