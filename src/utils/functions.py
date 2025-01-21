def get_model_info(json_list, model_name):
    """
    모델 이름을 사용하여 모델 정보를 반환합니다.
    """

    for model in json_list:
        if model["name"] == model_name:
            return model

    return None