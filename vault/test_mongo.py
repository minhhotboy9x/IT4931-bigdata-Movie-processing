from pymongo import MongoClient


def upload_example(client):
    db = client.BIGDATA
    collection = db.movie
    # Dữ liệu mẫu
    sample_data = {
        "title": "Sample Movie",
        "genre": "Action",
        "release_year": 2023,
        "director": "John Doe"
    }

    # Thêm một bản ghi (document)
    result = collection.insert_one(sample_data)

    # In thông báo về việc thêm dữ liệu
    print(f"Inserted document ID: {result.inserted_id}")
# Thay thế các giá trị dưới đây bằng thông tin tài khoản MongoDB Atlas của bạn
username = "minhhotboy9x"
password = "MUvodich"

# Tạo chuỗi kết nối
# connection_string = f"mongodb+srv://{username}:{password}@atlascluster.zdoemtz.mongodb.net/BIGDATA.movie"
connection_string = 'mongodb://localhost:60000/'

# Kết nối đến MongoDB Atlas
client = MongoClient(connection_string)

# Kiểm tra kết nối
try:
    client.server_info()
    upload_example(client)
    print("Kết nối thành công!")
except Exception as e:
    print(f"Kết nối thất bại: {e}")
finally:
    # Đóng kết nối
    client.close()
