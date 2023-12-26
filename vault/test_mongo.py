from pymongo import MongoClient

def enable_sharding_and_shard_collection(client):
    # Kết nối đến MongoDB
    # db = client.BIGDATA

    # Kích hoạt sharding cho database
    client.admin.command('enableSharding', 'BIGDATA')

    # Đặt shard key cho collection "test"
    client.admin.command("shardCollection", "BIGDATA.test", key={"genre": "hashed"})

def upload_example(client):
    db = client.BIGDATA
    collection = db.test

    # Dữ liệu mẫu
    sample_data = {
        "title": "Sample Movie",
        "genre": "Comedy",
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
connection_string = f"mongodb://localhost:60000/"
# Kết nối đến MongoDB Atlas
client = MongoClient(connection_string)

# Kiểm tra kết nối
try:
    client.server_info()
    enable_sharding_and_shard_collection(client)
    upload_example(client)
    print("Kết nối và tạo sharding thành công!")
except Exception as e:
    print(f"Kết nối thất bại hoặc tạo sharding không thành công: {e}")
finally:
    # Đóng kết nối
    client.close()
