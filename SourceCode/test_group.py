import pytest
from models import Member

# ============================================================
# MODULE: GROUP MANAGEMENT (Mã: GROUP)
# Tổng số Test Case: 15
# ============================================================

# --- GROUP 1: CREATE & MANAGE GROUP (5 Cases) ---
def test_01_create_group():
    """[GROUP_TC01] Tạo nhóm thành công."""
    m = Member(1, "u", "p", "e")
    m.create_group("G1")
    assert m.groups[0].group_name == "G1"

def test_02_create_multiple_groups():
    """[GROUP_TC02] Tạo nhiều nhóm, ID tăng dần."""
    m = Member(1, "u", "p", "e")
    m.create_group("G1"); m.create_group("G2")
    assert m.groups[1].group_id == 2

def test_03_create_duplicate_name():
    """[GROUP_TC03] Tạo nhóm trùng tên (Logic cho phép)."""
    m = Member(1, "u", "p", "e")
    m.create_group("G1"); m.create_group("G1")
    assert len(m.groups) == 2

def test_04_rename_group():
    """[GROUP_TC04] Đổi tên nhóm thành công."""
    m = Member(1, "u", "p", "e")
    m.create_group("Old")
    m.rename_group(1, "New")
    assert m.groups[0].group_name == "New"

def test_05_rename_invalid_group():
    """[GROUP_TC05] Đổi tên nhóm không tồn tại."""
    m = Member(1, "u", "p", "e")
    m.rename_group(999, "Ghost")
    assert len(m.groups) == 0

# --- GROUP 2: MEMBERSHIP (6 Cases) ---
def test_06_add_to_group_success():
    """[GROUP_TC06] Thêm liên hệ vào nhóm thành công."""
    m = Member(1, "u", "p", "e")
    m.add_contact("C1", "1"); m.create_group("G1")
    m.add_contact_to_group(1, 1)
    assert len(m.memberships) == 1

def test_07_add_to_group_fail_invalid_contact():
    """[GROUP_TC07] Thêm Contact ID sai vào nhóm."""
    m = Member(1, "u", "p", "e")
    m.create_group("G1")
    m.add_contact_to_group(999, 1)
    assert len(m.memberships) == 0

def test_08_add_to_group_fail_invalid_group():
    """[GROUP_TC08] Thêm vào Group ID sai."""
    m = Member(1, "u", "p", "e")
    m.add_contact("C1", "1")
    m.add_contact_to_group(1, 999)
    assert len(m.memberships) == 0

def test_09_add_duplicate_membership():
    """[GROUP_TC09] Thêm trùng (1 người vào 1 nhóm 2 lần)."""
    m = Member(1, "u", "p", "e")
    m.add_contact("C1", "1"); m.create_group("G1")
    m.add_contact_to_group(1, 1)
    m.add_contact_to_group(1, 1) # Lần 2
    assert len(m.memberships) == 1

def test_10_remove_from_group_success():
    """[GROUP_TC10] Mời người ra khỏi nhóm."""
    m = Member(1, "u", "p", "e")
    m.add_contact("C1", "1"); m.create_group("G1")
    m.add_contact_to_group(1, 1)
    res = m.remove_contact_from_group(1, 1)
    assert res is True and len(m.memberships) == 0

def test_11_remove_not_in_group():
    """[GROUP_TC11] Mời người chưa từng vào nhóm."""
    m = Member(1, "u", "p", "e")
    res = m.remove_contact_from_group(1, 1)
    assert res is False

# --- GROUP 3: DELETE GROUP (4 Cases) ---
def test_12_remove_group_success():
    """[GROUP_TC12] Xóa nhóm thành công."""
    m = Member(1, "u", "p", "e")
    m.create_group("G1")
    m.remove_group(1)
    assert len(m.groups) == 0

def test_13_remove_group_cleanup_membership():
    """[GROUP_TC13] Xóa nhóm phải xóa luôn liên kết thành viên."""
    m = Member(1, "u", "p", "e")
    m.add_contact("C1", "1"); m.create_group("G1")
    m.add_contact_to_group(1, 1)
    m.remove_group(1)
    assert len(m.memberships) == 0

def test_14_remove_group_invalid():
    """[GROUP_TC14] Xóa nhóm sai ID."""
    m = Member(1, "u", "p", "e")
    m.create_group("G1")
    m.remove_group(999)
    assert len(m.groups) == 1

def test_15_group_id_auto_increment():
    """[GROUP_TC15] Kiểm tra ID tự tăng khi tạo/xóa."""
    m = Member(1, "u", "p", "e")
    m.create_group("G1") # ID 1
    m.remove_group(1)    # Xóa
    m.create_group("G2") # Tạo mới
    assert m.groups[0].group_id == 1 # Code logic hiện tại reset nếu list empty