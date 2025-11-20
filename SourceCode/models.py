import datetime
import hashlib

# ==========================================
# 1. CLASS CONTACT
# ==========================================
class Contact:
    """
    Lớp đại diện cho một liên hệ (Contact).
    Lưu trữ các thông tin cá nhân như tên, sđt, email, v.v.
    """
    def __init__(self, contact_id, name, phone, email="", address="", notes=""):
        """
        Khởi tạo một Contact mới.
        
        Args:
            contact_id (int): ID định danh duy nhất.
            name (str): Tên liên hệ.
            phone (str): Số điện thoại.
            email (str, optional): Địa chỉ email.
            address (str, optional): Địa chỉ nhà.
            notes (str, optional): Ghi chú thêm.
        """
        self.contact_id = contact_id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address
        self.notes = notes
        self.created_at = datetime.datetime.now()
        self.last_viewed_at = None

    def update_details(self, name=None, phone=None, email=None, notes=None):
        """
        Cập nhật thông tin của liên hệ. Chỉ cập nhật các trường có giá trị (không None).
        
        Args:
            name (str): Tên mới.
            phone (str): SĐT mới.
            email (str): Email mới.
            notes (str): Ghi chú mới.
        """
        if name: self.name = name
        if phone: self.phone = phone
        if email: self.email = email
        if notes: self.notes = notes
        self.updated_at = datetime.datetime.now()

    def view(self):
        """Ghi nhận thời gian vừa xem liên hệ này."""
        self.last_viewed_at = datetime.datetime.now()

    def __str__(self):
        return f"ID: {self.contact_id} | {self.name} | {self.phone}"

# ==========================================
# 2. CLASS GROUP
# ==========================================
class Group:
    """
    Lớp đại diện cho nhóm liên hệ (ví dụ: Gia đình, Công ty).
    """
    def __init__(self, group_id, group_name):
        """
        Khởi tạo Group.
        
        Args:
            group_id (int): ID nhóm.
            group_name (str): Tên nhóm.
        """
        self.group_id = group_id
        self.group_name = group_name
    
    def rename_group(self, new_name):
        """Đổi tên nhóm."""
        self.group_name = new_name

    def __str__(self):
        return f"[{self.group_id}] {self.group_name}"

# ==========================================
# 3. CLASS TRUNG GIAN
# ==========================================
class ContactGroupMembership:
    """
    Lớp liên kết giữa Contact và Group (quan hệ nhiều-nhiều).
    """
    def __init__(self, contact_id, group_id):
        """
        Khởi tạo mối quan hệ thành viên.
        
        Args:
            contact_id (int): ID của liên hệ.
            group_id (int): ID của nhóm.
        """
        self.contact_id = contact_id
        self.group_id = group_id
        self.added_at = datetime.datetime.now()

    def check_membership(self, c_id, g_id):
        """Kiểm tra xem cặp (contact_id, group_id) này có khớp không."""
        return self.contact_id == c_id and self.group_id == g_id

# ==========================================
# 4. CLASS MEMBER
# ==========================================
class Member:
    """
    Lớp đại diện cho người dùng thông thường (Member).
    Có khả năng quản lý danh bạ cá nhân.
    """
    def __init__(self, member_id, username, password, email):
        """
        Khởi tạo Member.
        
        Args:
            member_id (int): ID người dùng.
            username (str): Tên đăng nhập.
            password (str): Mật khẩu (sẽ được tự động mã hóa nếu chưa mã hóa).
            email (str): Email người dùng.
        """
        self.member_id = member_id
        self.username = username
        self.email = email
        self.is_active = True
        
        # Xử lý mã hóa mật khẩu (Requirement 2.2.1)
        # Nếu độ dài khác 64 (độ dài SHA256 hex), coi như là plain text và thực hiện băm.
        if len(password) != 64:
            self.password = hashlib.sha256(password.encode()).hexdigest()
        else:
            self.password = password

        self.contacts = []      # List[Contact]
        self.groups = []        # List[Group]
        self.memberships = []   # List[ContactGroupMembership]

    def login(self, password_input):
        """
        Kiểm tra đăng nhập bằng cách so sánh hash của mật khẩu nhập vào.
        
        Args:
            password_input (str): Mật khẩu người dùng nhập (plain text).
            
        Returns:
            bool: True nếu mật khẩu đúng và tài khoản active, ngược lại False.
        """
        input_hashed = hashlib.sha256(password_input.encode()).hexdigest()
        return self.password == input_hashed and self.is_active

    # --- CONTACT MANAGEMENT ---
    
    def add_contact(self, name, phone, email="", addr="", note=""):
        """Thêm một liên hệ mới vào danh bạ."""
        new_id = 1
        if self.contacts: new_id = max(c.contact_id for c in self.contacts) + 1
        self.contacts.append(Contact(new_id, name, phone, email, addr, note))
        print(f"✅ Đã thêm: {name}")

    def edit_contact_details(self, contact_id, name=None, phone=None, email=None, notes=None):
        """Sửa thông tin liên hệ theo ID."""
        target = next((c for c in self.contacts if c.contact_id == contact_id), None)
        if target:
            target.update_details(name, phone, email, notes)
            print(f"✅ Đã cập nhật thông tin ID {contact_id}")
            return True
        return False

    def delete_contact(self, contact_id):
        """Xóa liên hệ và xóa cả các liên kết nhóm liên quan."""
        self.memberships = [m for m in self.memberships if m.contact_id != contact_id]
        target = next((c for c in self.contacts if c.contact_id == contact_id), None)
        if target:
            self.contacts.remove(target)
            print(f"✅ Đã xóa liên hệ ID {contact_id}")
        else:
            print("❌ Không tìm thấy ID.")

    def view_contact_detail(self, contact_id):
        """Xem chi tiết và ghi nhận lịch sử xem."""
        target = next((c for c in self.contacts if c.contact_id == contact_id), None)
        if target:
            target.view()
            print(f"\n--- CHI TIẾT: {target.name} ---")
            print(f"SĐT  : {target.phone}")
            print(f"Email: {target.email}")
            print(f"Note : {target.notes}")
            if target.last_viewed_at:
                print(f"Xem lần cuối: {target.last_viewed_at.strftime('%H:%M %d/%m')}")
            return True
        return False

    def get_recent_contacts(self):
        """Lấy danh sách các liên hệ vừa xem gần đây."""
        viewed = [c for c in self.contacts if c.last_viewed_at is not None]
        viewed.sort(key=lambda x: x.last_viewed_at, reverse=True)
        return viewed

    def search_contact_by_name(self, keyword):
        """Tìm kiếm liên hệ theo tên (gần đúng)."""
        keyword = keyword.lower().strip()
        found = [c for c in self.contacts if keyword in c.name.lower()]
        return found

    # --- GROUP MANAGEMENT ---
    def create_group(self, group_name):
        """Tạo nhóm mới."""
        new_id = 1
        if self.groups: new_id = max(g.group_id for g in self.groups) + 1
        self.groups.append(Group(new_id, group_name))
        print(f"✅ Đã tạo nhóm: {group_name}")

    def remove_group(self, group_id):
        """Xóa nhóm và các liên kết thành viên trong nhóm đó."""
        target = next((g for g in self.groups if g.group_id == group_id), None)
        if target:
            self.memberships = [m for m in self.memberships if m.group_id != group_id]
            self.groups.remove(target)
            print(f"✅ Đã xóa nhóm ID {group_id}")
        else: print("❌ Không tìm thấy nhóm.")

    def rename_group(self, group_id, new_name):
        """Đổi tên nhóm."""
        target = next((g for g in self.groups if g.group_id == group_id), None)
        if target: target.rename_group(new_name)

    def add_contact_to_group(self, contact_id, group_id):
        """Thêm một contact vào một group."""
        if not any(c.contact_id == contact_id for c in self.contacts): return
        if not any(g.group_id == group_id for g in self.groups): return
        for m in self.memberships:
            if m.check_membership(contact_id, group_id): return
        self.memberships.append(ContactGroupMembership(contact_id, group_id))
        print(f"✅ Đã thêm vào nhóm.")

    def remove_contact_from_group(self, contact_id, group_id):
        """Xóa contact khỏi group."""
        initial = len(self.memberships)
        self.memberships = [m for m in self.memberships if not (m.contact_id == contact_id and m.group_id == group_id)]
        if len(self.memberships) < initial:
            print(f"✅ Đã mời Contact {contact_id} ra khỏi nhóm.")
            return True
        return False

    def view_contacts_in_group(self, group_id):
        """Hiển thị tất cả thành viên trong một nhóm."""
        print(f"\n--- Thành viên Nhóm {group_id} ---")
        linked_ids = [m.contact_id for m in self.memberships if m.group_id == group_id]
        if not linked_ids: print("(Trống)")
        for cid in linked_ids:
            c = next((x for x in self.contacts if x.contact_id == cid), None)
            if c: print(f"{c.contact_id}. {c.name} - {c.phone}")

# ==========================================
# 5. CLASS ADMIN
# ==========================================
class Admin:
    """
    Lớp đại diện cho Quản trị viên (Admin).
    """
    def __init__(self, admin_id, username, password):
        """
        Khởi tạo Admin.
        Mật khẩu sẽ được băm SHA-256 nếu chưa băm.
        """
        self.admin_id = admin_id
        self.username = username
        if len(password) != 64:
            self.password = hashlib.sha256(password.encode()).hexdigest()
        else:
            self.password = password

    def login(self, password_input):
        """
        Đăng nhập Admin với mật khẩu đã băm.
        """
        input_hashed = hashlib.sha256(password_input.encode()).hexdigest()
        return self.password == input_hashed