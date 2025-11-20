import pytest
from models import Member
import time

# MODULE: SEARCH & HISTORY (Mã: SEARCH)
# Tổng số Test Case: 15

# --- GROUP 1: SEARCH (9 Cases) ---
def test_01_search_exact():
    """[SEARCH_TC01] Tìm kiếm chính xác tên."""
    m = Member(1, "u", "p", "e")
    m.add_contact("Alpha", "1")
    res = m.search_contact_by_name("Alpha")
    assert len(res) == 1

def test_02_search_lowercase():
    """[SEARCH_TC02] Tìm kiếm bằng chữ thường."""
    m = Member(1, "u", "p", "e")
    m.add_contact("Alpha", "1")
    res = m.search_contact_by_name("alpha")
    assert len(res) == 1

def test_03_search_uppercase():
    """[SEARCH_TC03] Tìm kiếm bằng chữ hoa."""
    m = Member(1, "u", "p", "e")
    m.add_contact("alpha", "1")
    res = m.search_contact_by_name("ALPHA")
    assert len(res) == 1

def test_04_search_partial_prefix():
    """[SEARCH_TC04] Tìm kiếm theo tiền tố."""
    m = Member(1, "u", "p", "e")
    m.add_contact("Halloween", "1")
    res = m.search_contact_by_name("Hallo")
    assert len(res) == 1

def test_05_search_partial_suffix():
    """[SEARCH_TC05] Tìm kiếm theo hậu tố."""
    m = Member(1, "u", "p", "e")
    m.add_contact("Halloween", "1")
    res = m.search_contact_by_name("ween")
    assert len(res) == 1

def test_06_search_partial_middle():
    """[SEARCH_TC06] Tìm kiếm ký tự ở giữa."""
    m = Member(1, "u", "p", "e")
    m.add_contact("Halloween", "1")
    res = m.search_contact_by_name("low")
    assert len(res) == 1

def test_07_search_not_found():
    """[SEARCH_TC07] Tìm kiếm không có kết quả."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1")
    res = m.search_contact_by_name("Z")
    assert len(res) == 0

def test_08_search_multiple_results():
    """[SEARCH_TC08] Tìm kiếm trả về nhiều kết quả."""
    m = Member(1, "u", "p", "e")
    m.add_contact("Nguyen A", "1"); m.add_contact("Nguyen B", "2")
    res = m.search_contact_by_name("Nguyen")
    assert len(res) == 2

def test_09_search_special_char():
    """[SEARCH_TC09] Tìm kiếm ký tự đặc biệt."""
    m = Member(1, "u", "p", "e")
    m.add_contact("User #1", "1")
    res = m.search_contact_by_name("#")
    assert len(res) == 1

# --- GROUP 2: HISTORY (6 Cases) ---
def test_10_view_updates_timestamp():
    """[SEARCH_TC10] Xem chi tiết cập nhật thời gian xem."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1")
    m.view_contact_detail(1)
    assert m.contacts[0].last_viewed_at is not None

def test_11_recent_list_order():
    """[SEARCH_TC11] Danh sách xem gần đây: Mới xem lên đầu."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1"); m.add_contact("B", "2")
    m.view_contact_detail(1); time.sleep(0.01)
    m.view_contact_detail(2)
    recent = m.get_recent_contacts()
    assert recent[0].name == "B"

def test_12_recent_list_reorder():
    """[SEARCH_TC12] Xem lại người cũ -> Nhảy lên đầu."""
    m = Member(1, "u", "p", "e")
    m.add_contact("A", "1"); m.add_contact("B", "2")
    m.view_contact_detail(1); time.sleep(0.01)
    m.view_contact_detail(2); time.sleep(0.01)
    m.view_contact_detail(1) # Xem lại A
    recent = m.get_recent_contacts()
    assert recent[0].name == "A"

def test_13_recent_empty():
    """[SEARCH_TC13] List Recent rỗng khi chưa xem ai."""
    m = Member(1, "u", "p", "e")
    assert len(m.get_recent_contacts()) == 0

def test_14_recent_only_viewed_ones():
    """[SEARCH_TC14] Chỉ hiện những người đã xem."""
    m = Member(1, "u", "p", "e")
    m.add_contact("Viewed", "1")
    m.add_contact("Not", "2")
    m.view_contact_detail(1)
    rec = m.get_recent_contacts()
    assert len(rec) == 1 and rec[0].name == "Viewed"

def test_15_view_invalid_id():
    """[SEARCH_TC15] Xem ID không tồn tại (Không lỗi)."""
    m = Member(1, "u", "p", "e")
    res = m.view_contact_detail(999)
    assert res is False