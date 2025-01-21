def memorize_system_context():
    system_context = """
특정 정보를 기억해야 합니다. 기억하기 위해 아래의 규칙을 따라야 합니다.
1. 선호 언어: 한국어를 기본으로 하되, 필요에 따라 다른 언어를 사용할 수 있습니다.
2. 기억해야 할 정보를 아래의 양식에 맞춰 변환해야 합니다:
{
    "id": "id는 별도로 생성될 값입니다. 비어있는 string으로 두어야 합니다.",
    "subject": "기억할 정보의 주제를 입력합니다.",
    "tags": ["기억할 정보의 태그를 입력합니다. 필요에 따라 여러 개의 태그를 입력할 수 있으나, 다섯개를 넘기지 마세요"],
    "contents": "기억할 정보의 내용을 입력합니다."
}
"""
    return system_context

def memorize_done_system_context():
    system_context = """
특정 정보를 기억하라는 작업을 완료하였으니 사용자에게 알립니다.
"""
    return system_context