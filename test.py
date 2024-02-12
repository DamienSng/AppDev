from werkzeug.security import generate_password_hash, check_password_hash

hashed_test_password = generate_password_hash('test_password', method='pbkdf2:sha256')

