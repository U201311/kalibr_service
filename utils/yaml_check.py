import yaml 

def check_yaml_data(data):
    # 检查data 数据是否包含target_type，targetCols，targetRows 字段
    if data["target_type"] == "aprilgrid":
        required_fields = {
            "tagCols": int,
            "tagRows": int,
            "tagSize": float,
            "tagSpacing": float
        }
    elif data["target_type"] == "checkerboard":
        
        required_fields = {
            "targetCols": int,
            "targetRows": int,
            "rowSpacingMeters": float,
            "colSpacingMeters": float
        }
        
    elif data["target_type"] == "circlegrid":
        required_fields = {
            "targetCols": int,
            "targetRows": int,
            "spacingMeters": float,
            "asymmetricGrid": bool
        }
    for field, field_type in required_fields.items():
        if field not in data:
            return False, f"Missing required field: {field}"
        if not isinstance(data[field], field_type):
            return False, f"Invalid type for field {field}. Expected {field_type.__name__}"
    return True, None