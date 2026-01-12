def mock_lead_capture(name: str, email: str, platform: str):
    """
    Mock API function to capture lead information.
    Only called after all three values are collected.
"""
    print(" Lead captured successfully!")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Platform: {platform}")
    return {
        "status": "success",
        "data": {
            "name": name,
            "email": email,
            "platform": platform
        }
    }