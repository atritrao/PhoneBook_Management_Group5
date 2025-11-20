import pytest
import hashlib
from models import Member, Admin

# ============================================================
# MODULE: AUTHENTICATION & ADMIN (Mã: AUTH)
# Tổng số Test Case: 16
# ============================================================

# --- GROUP 1: PASSWORD SECURITY (4 Cases) ---
def test_01_password_hashing_creation():
    """[AUTH_TC01] Kiểm tra mật khẩu được hash ngay khi tạo."""
    raw = "123456"
    mem = Member(1, "user", raw, "mail")
    assert mem.password != raw
    assert len(mem.password) == 64

def test_02_password_hashing_consistency():
    """[AUTH_TC02] Cùng input mật khẩu phải ra cùng mã hash."""
    mem1 = Member(1, "u1", "abc", "m1")
    mem2 = Member(2, "u2", "abc", "m2")
    assert mem1.password == mem2.password

def test_03_password_hashing_diff():
    """[AUTH_TC03] Khác input mật khẩu phải ra khác mã hash."""
    mem1 = Member(1, "u1", "abc", "m1")
    mem2 = Member(2, "u2", "abd", "m2")
    assert mem1.password != mem2.password

def test_04_admin_hashing():
    """[AUTH_TC04] Admin password cũng phải được hash."""
    adm = Admin(1, "ad", "pass")
    assert len(adm.password) == 64

# --- GROUP 2: MEMBER LOGIN (7 Cases) ---
def test_05_mem_login_success():
    """[AUTH_TC05] Member đăng nhập thành công."""
    mem = Member(1, "sv", "123", "mail")
    assert mem.login("123") is True

def test_06_mem_login_fail_wrong_pass():
    """[AUTH_TC06] Member đăng nhập sai mật khẩu."""
    mem = Member(1, "sv", "123", "mail")
    assert mem.login("wrong") is False

def test_07_mem_login_fail_empty_pass():
    """[AUTH_TC07] Member đăng nhập với mật khẩu rỗng."""
    mem = Member(1, "sv", "123", "mail")
    assert mem.login("") is False

def test_08_mem_login_fail_case_sensitive():
    """[AUTH_TC08] Mật khẩu phân biệt hoa thường."""
    mem = Member(1, "sv", "abc", "mail")
    assert mem.login("ABC") is False

def test_09_mem_login_inactive_user():
    """[AUTH_TC09] User bị khóa (is_active=False) không thể login."""
    mem = Member(1, "sv", "123", "mail")
    mem.is_active = False
    assert mem.login("123") is False

def test_10_mem_login_spaces():
    """[AUTH_TC10] Mật khẩu có chứa khoảng trắng."""
    mem = Member(1, "sv", "a b c", "mail")
    assert mem.login("a b c") is True
    assert mem.login("abc") is False

def test_11_mem_login_special_chars():
    """[AUTH_TC11] Mật khẩu chứa ký tự đặc biệt."""
    mem = Member(1, "sv", "@#$%", "mail")
    assert mem.login("@#$%") is True

# --- GROUP 3: ADMIN LOGIN (5 Cases) ---
def test_12_admin_login_success():
    """[AUTH_TC12] Admin đăng nhập thành công."""
    adm = Admin(1, "admin", "123")
    assert adm.login("123") is True

def test_13_admin_login_fail():
    """[AUTH_TC13] Admin đăng nhập sai mật khẩu."""
    adm = Admin(1, "admin", "123")
    assert adm.login("456") is False

def test_14_admin_login_empty():
    """[AUTH_TC14] Admin đăng nhập mật khẩu rỗng."""
    adm = Admin(1, "admin", "123")
    assert adm.login("") is False

def test_15_admin_init_id():
    """[AUTH_TC15] Kiểm tra khởi tạo ID Admin."""
    adm = Admin(99, "root", "root")
    assert adm.admin_id == 99

def test_16_admin_username_check():
    """[AUTH_TC16] Kiểm tra username Admin lưu đúng."""
    adm = Admin(1, "superadmin", "123")
    assert adm.username == "superadmin"