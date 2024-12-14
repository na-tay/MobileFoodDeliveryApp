import re
import hashlib
import unittest

# 模拟数据库类
class Database:
    def __init__(self):
        self.users = {}

    def get_user(self, email):
        return self.users.get(email)

    def save_user(self, email, password):
        self.users[email] = {'email': email, 'password': password}
        return True


# 用户注册类
class UserRegistration:
    def __init__(self, database):
        self.database = database

    def validate_email(self, email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        else:
            raise ValueError("Invalid email format")

    def validate_password(self, password):
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return True

    def encrypt_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register(self, email, password, confirm_password):
        self.validate_email(email)
        self.validate_password(password)
        if password != confirm_password:
            raise ValueError("Passwords do not match")
        if self.database.get_user(email):
            raise ValueError("User already registered")
        encrypted_password = self.encrypt_password(password)
        self.database.save_user(email, encrypted_password)
        return "Registration successful"


# 用户登录类
class UserLogin:
    def __init__(self, database):
        self.database = database

    def authenticate(self, email, password):
        encrypted_password = hashlib.sha256(password.encode()).hexdigest()
        user = self.database.get_user(email)
        if user and user['password'] == encrypted_password:
            return True
        return False


# 用户注册测试类
class TestUserRegistration(unittest.TestCase):
    def setUp(self):
        self.database = Database()
        self.user_registration = UserRegistration(self.database)

    def test_successful_registration(self):
        result = self.user_registration.register("user@example.com", "Password123", "Password123")
        self.assertEqual(result, "Registration successful")

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            self.user_registration.register("userexample.com", "Password123", "Password123")

    def test_password_mismatch(self):
        with self.assertRaises(ValueError):
            self.user_registration.register("user@example.com", "Password123", "Password321")

    def test_weak_password(self):
        with self.assertRaises(ValueError):
            self.user_registration.register("user@example.com", "pass", "pass")

    def test_email_already_registered(self):
        self.user_registration.register("user@example.com", "Password123", "Password123")
        with self.assertRaises(ValueError):
            self.user_registration.register("user@example.com", "Password123", "Password123")


# 用户登录测试类
class TestUserLogin(unittest.TestCase):
    def setUp(self):
        self.database = Database()
        self.user_registration = UserRegistration(self.database)
        self.user_login = UserLogin(self.database)

    def test_successful_login(self):
        self.user_registration.register("test@example.com", "password123", "password123")
        result = self.user_login.authenticate("test@example.com", "password123")
        self.assertTrue(result)

    def test_failed_login_wrong_password(self):
        self.user_registration.register("test@example.com", "password123", "password123")
        result = self.user_login.authenticate("test@example.com", "wrongpassword")
        self.assertFalse(result)

    def test_failed_login_nonexistent_user(self):
        result = self.user_login.authenticate("nonexistent@example.com", "password123")
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()