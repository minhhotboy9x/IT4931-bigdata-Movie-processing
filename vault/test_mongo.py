from pymongo import MongoClient

# Thay thế các giá trị dưới đây bằng thông tin tài khoản MongoDB Atlas của bạn
username = "minhhotboy9x"
password = "MUvodich"

# Tạo chuỗi kết nối
connection_string = f"mongodb+srv://{username}:{password}@atlascluster.zdoemtz.mongodb.net/BIGDATA.movie"

# Kết nối đến MongoDB Atlas
client = MongoClient(connection_string)

# Kiểm tra kết nối
try:
    client.server_info()
    print("Kết nối thành công!")
except Exception as e:
    print(f"Kết nối thất bại: {e}")
finally:
    # Đóng kết nối
    client.close()
