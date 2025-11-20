import pytest
from models import Member

# ============================================================
# MODULE: CONTACT MANAGEMENT (Mã: CRUD)
# Tổng số Test Case: 18
# ============================================================

# --- GROUP 1: ADD CONTACT (6 Cases) ---
def test_01_add_contact_full_info():
    """[CRUD_TC01] Thêm liên hệ đầy đủ thông tin."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1", "e", "addr", "note")
    assert m.contacts[0].address == "addr"

def test_02_add_contact_minimal_info():
    """[CRUD_TC02] Thêm liên hệ thiếu thông tin (chỉ tên, sđt)."""
    m = Member(1, "u", "p", "e")
    m.add_contact("B", "2")
    assert m.contacts[0].email == ""

def test_03_add_multiple_contacts():
    """[CRUD_TC03] Thêm nhiều liên hệ, ID tự tăng dần."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1")
    m.add_contact("B", "2")
    assert m.contacts[1].contact_id == 2

def test_04_add_contact_special_chars_name():
    """[CRUD_TC04] Tên liên hệ chứa ký tự đặc biệt."""
    m = Member(1, "u", "p", "e")
    m.add_contact("#$%^&*", "111")
    assert m.contacts[0].name == "#$%^&*"

def test_05_add_contact_long_phone():
    """[CRUD_TC05] Số điện thoại cực dài (Biên)."""
    m = Member(1, "u", "p", "e")
    m.add_contact("Long", "09"*50)
    assert len(m.contacts[0].phone) == 100

def test_06_add_contact_unicode_name():
    """[CRUD_TC06] Tên tiếng Việt có dấu."""
    m = Member(1, "u", "p", "e")
    m.add_contact("Nguyễn Văn A", "123")
    assert m.contacts[0].name == "Nguyễn Văn A"

# --- GROUP 2: EDIT CONTACT (7 Cases) ---
def test_07_edit_name_only():
    """[CRUD_TC07] Chỉ sửa tên liên hệ."""
    m = Member(1, "u", "p", "e")
    m.add_contact("Old", "1")
    m.edit_contact_details(1, name="New")
    assert m.contacts[0].name == "New"

def test_08_edit_phone_only():
    """[CRUD_TC08] Chỉ sửa số điện thoại."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1")
    m.edit_contact_details(1, phone="999")
    assert m.contacts[0].phone == "999"

def test_09_edit_all_fields():
    """[CRUD_TC09] Sửa toàn bộ các trường thông tin."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1", "e1", "a1", "n1")
    m.edit_contact_details(1, "B", "2", "e2", "n2")
    assert m.contacts[0].email == "e2"

def test_10_edit_nothing():
    """[CRUD_TC10] Gọi hàm sửa nhưng không truyền dữ liệu mới."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1")
    m.edit_contact_details(1)
    assert m.contacts[0].name == "A"

def test_11_edit_invalid_id():
    """[CRUD_TC11] Sửa ID không tồn tại."""
    m = Member(1, "u", "p", "e")
    res = m.edit_contact_details(999, name="Ghost")
    assert res is False

def test_12_edit_to_empty_string():
    """[CRUD_TC12] Sửa tên thành rỗng (Kiểm tra logic bỏ qua)."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1")
    m.edit_contact_details(1, name="")
    assert m.contacts[0].name == "A"

def test_13_edit_updated_at_timestamp():
    """[CRUD_TC13] Kiểm tra timestamp thay đổi khi edit."""
    import time
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1")
    old_time = getattr(m.contacts[0], 'updated_at', None)
    time.sleep(0.01)
    m.edit_contact_details(1, name="B")
    assert m.contacts[0].updated_at != old_time

# --- GROUP 3: DELETE CONTACT (5 Cases) ---
def test_14_delete_success():
    """[CRUD_TC14] Xóa liên hệ thành công."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1")
    m.delete_contact(1)
    assert len(m.contacts) == 0

def test_15_delete_fail_invalid_id():
    """[CRUD_TC15] Xóa ID không tồn tại."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1")
    m.delete_contact(999)
    assert len(m.contacts) == 1

def test_16_delete_from_empty_list():
    """[CRUD_TC16] Xóa khi danh bạ rỗng."""
    m = Member(1, "u", "p", "e")
    m.delete_contact(1)
    assert len(m.contacts) == 0

def test_17_delete_middle_element():
    """[CRUD_TC17] Xóa phần tử ở giữa danh sách."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1"); m.add_contact("B", "2"); m.add_contact("C", "3")
    m.delete_contact(2) # Xóa B
    assert len(m.contacts) == 2
    assert m.contacts[1].name == "C"

def test_18_delete_removes_membership():
    """[CRUD_TC18] Xóa liên hệ phải xóa luôn liên kết nhóm."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1")
    m.create_group("G")
    m.add_contact_to_group(1, 1)
    m.delete_contact(1)
    assert len(m.memberships) == 0