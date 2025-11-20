import sys
import datetime
from models import Member, Admin
from data import DataManager

class PhoneBookSystem:
    """
    Lớp chính điều khiển luồng hoạt động của ứng dụng (Controller).
    """
    def __init__(self):
        """Khởi tạo hệ thống, tải dữ liệu từ file."""
        self.members = []
        self.admins = []
        self.logs = [] 
        self.current_user = None
        
        loaded_admins, loaded_members, loaded_logs = DataManager.load_data()
        self.logs = loaded_logs if loaded_logs else []

        if loaded_admins or loaded_members:
            self.admins = loaded_admins
            self.members = loaded_members
        else:
            print(">> Khởi tạo dữ liệu mẫu...")
            self.load_dummy_data()
            self.save_changes()

    def write_log(self, message):
        """Ghi log hệ thống."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"[{now}] {message}")
        if len(self.logs) > 100: self.logs.pop(0)

    def save_changes(self):
        """Lưu thay đổi xuống file."""
        DataManager.save_data(self.admins, self.members, self.logs)

    def load_dummy_data(self):
        """Tạo dữ liệu mẫu nếu chạy lần đầu."""
        self.admins.append(Admin(1, "admin", "123456"))
        mem = Member(101, "sinhvien", "123", "sv@email.com")
        mem.add_contact("Bố", "090111", "dad@email.com", "Home", "Gia đình")
        mem.create_group("Gia Đình")
        self.members.append(mem)
        self.write_log("System init with dummy data.")

    # --- MAIN MENU ---
    def main_menu(self):
        """Hiển thị menu chính (Login)."""
        while True:
            print("\n=== PHONE BOOK SYSTEM ===")
            print("1. Member Login")
            print("2. Admin Login")
            print("3. Exit")
            c = input("👉 Chọn: ")
            
            if c == '1': self.login_member_flow()
            elif c == '2': self.login_admin_flow()
            elif c == '3': 
                self.write_log("System shutdown.")
                self.save_changes()
                sys.exit()

    # --- CẬP NHẬT: XỬ LÝ LOGIN MEMBER CÓ THÔNG BÁO ---
    def login_member_flow(self):
        print("\n--- ĐĂNG NHẬP MEMBER ---")
        u = input("User: ")
        p = input("Pass: ")
        
        user = next((m for m in self.members if m.username == u), None)
        
        # Kiểm tra login
        if user and user.login(p):
            self.current_user = user
            print(f"\n✅ Đăng nhập thành công! Xin chào {u}.")
            self.write_log(f"Member '{u}' login.")
            self.member_dashboard()
        else:
            # Hiển thị thông báo lỗi và dừng màn hình
            print("\n❌ ĐĂNG NHẬP THẤT BẠI!")
            print("⚠️  Tên đăng nhập hoặc mật khẩu không đúng.")
            print("💡 Gợi ý: User mẫu là 'sinhvien', Pass '123'")
            input("\n👉 Nhấn Enter để quay lại menu chính...")

    # --- CẬP NHẬT: XỬ LÝ LOGIN ADMIN CÓ THÔNG BÁO ---
    def login_admin_flow(self):
        print("\n--- ĐĂNG NHẬP ADMIN ---")
        u = input("User: ")
        p = input("Pass: ")
        
        admin = next((a for a in self.admins if a.username == u), None)
        
        if admin and admin.login(p):
            self.current_user = admin
            print(f"\n✅ Đăng nhập thành công! Xin chào Admin {u}.")
            self.write_log(f"Admin '{u}' login.")
            self.admin_dashboard()
        else:
            print("\n❌ ĐĂNG NHẬP THẤT BẠI!")
            print("⚠️  Tên đăng nhập hoặc mật khẩu Admin không đúng.")
            print("💡 Gợi ý: User mẫu là 'admin', Pass '123456'")
            input("\n👉 Nhấn Enter để quay lại menu chính...")

    # --- ADMIN DASHBOARD ---
    def admin_dashboard(self):
        """Menu chức năng cho Admin."""
        while True:
            print(f"\n=== ADMIN DASHBOARD ===")
            print("1. Xem danh sách User")
            print("2. Tạo tài khoản Member")
            print("3. Xóa tài khoản Member")
            print("4. 📜 Xem System Log") 
            print("0. Đăng xuất")
            
            c = input("👉 Admin: ")
            
            if c == '1':
                print("\n--- USER LIST ---")
                for m in self.members:
                    print(f"ID: {m.member_id} | User: {m.username} | Contacts: {len(m.contacts)}")
            
            elif c == '2':
                u = input("User mới: ")
                if any(m.username == u for m in self.members):
                    print("⚠️ Trùng tên."); continue
                p = input("Pass: "); e = input("Email: ")
                new_id = 101 if not self.members else max(m.member_id for m in self.members) + 1
                self.members.append(Member(new_id, u, p, e))
                self.write_log(f"Admin created user {u}.")
                self.save_changes()
                print(f"✅ Đã tạo user {u} thành công.")
                
            elif c == '3':
                try:
                    mid = int(input("ID User xóa: "))
                    t = next((m for m in self.members if m.member_id == mid), None)
                    if t:
                        if input(f"Sure to delete {t.username}? (y/n): ")=='y':
                            self.members.remove(t)
                            self.write_log(f"Admin deleted user {t.username}.")
                            self.save_changes()
                            print("✅ Đã xóa thành công.")
                    else:
                        print("❌ Không tìm thấy User ID này.")
                except: pass

            elif c == '4':
                print("\n--- SYSTEM LOGS ---")
                if not self.logs: print("(Trống)")
                for line in self.logs: print(line)
                input("Enter để quay lại...")
            
            elif c == '0':
                self.current_user = None; break

    # --- MEMBER DASHBOARD ---
    def member_dashboard(self):
        """Menu chức năng cho Member."""
        while True:
            print(f"\n--- MENU: {self.current_user.username} ---")
            print("--- CONTACT ---")
            print("1. Xem danh bạ")
            print("2. Thêm liên hệ")
            print("3. Sửa liên hệ")
            print("4. Xóa liên hệ")
            print("5. Xem Recent (Vừa truy cập)")
            print("9. 🔍 Tìm kiếm tên (Smart Search)")
            print("--- GROUP ---")
            print("6. Tạo Nhóm (Create)")
            print("7. Xóa Nhóm (Delete)")
            print("8. 📂 Vào Chi Tiết Nhóm (Add/Remove Member)")
            print("0. Đăng xuất")
            
            c = input("👉 Chọn: ")

            if c == '1': # VIEW ALL
                print(f"--- Danh bạ ({len(self.current_user.contacts)}) ---")
                print(f"{'ID':<5} {'Tên':<20} {'SĐT':<15}")
                for ct in self.current_user.contacts: 
                    print(f"{ct.contact_id:<5} {ct.name:<20} {ct.phone:<15}")
                input("Nhấn Enter để tiếp tục...")

            elif c == '2': # ADD
                n = input("Tên: ")
                while True:
                    p = input("SĐT: ")
                    if p.isdigit(): break
                    print("⚠️ Lỗi: SĐT chỉ được chứa số. Vui lòng nhập lại.")
                
                e = input("Email: ") 
                nt = input("Ghi chú: ") 
                self.current_user.add_contact(n, p, e, "", nt)
                self.write_log(f"{self.current_user.username} added contact.")
                self.save_changes()

            elif c == '3': # EDIT
                try:
                    cid = int(input("ID cần sửa: "))
                    n = input("Tên mới (Enter bỏ qua): ").strip() or None
                    
                    p = input("SĐT mới (Enter bỏ qua): ").strip() or None
                    if p and not p.isdigit():
                        print("⚠️ SĐT không hợp lệ, bỏ qua cập nhật SĐT.")
                        p = None
                    
                    e = input("Email mới (Enter bỏ qua): ").strip() or None 
                    nt = input("Note mới (Enter bỏ qua): ").strip() or None 
                    
                    self.current_user.edit_contact_details(cid, n, p, e, nt)
                    self.save_changes()
                except: pass

            elif c == '4': # DELETE
                try:
                    self.current_user.delete_contact(int(input("ID xóa: ")))
                    self.write_log(f"{self.current_user.username} deleted contact.")
                    self.save_changes()
                except: pass

            elif c == '5': # RECENT
                print("\n--- 🕒 RECENT ---")
                recent = self.current_user.get_recent_contacts()
                if not recent: print(">> (Bạn chưa xem chi tiết ai cả)")
                for ct in recent: print(f"[{ct.last_viewed_at.strftime('%H:%M')}] {ct.name}")
                input("Nhấn Enter để tiếp tục...")

            elif c == '9': # SMART SEARCH
                kw = input("Nhập tên tìm: ")
                res = self.current_user.search_contact_by_name(kw)
                
                if not res:
                    print("❌ Không thấy.")
                elif len(res) == 1:
                    target = res[0]
                    print(f"✅ Tìm thấy: {target.name} - {target.phone}")
                    if self.current_user.view_contact_detail(target.contact_id):
                        self.save_changes()
                        input("Nhấn Enter để tiếp tục...")
                else:
                    print(f"--- Tìm thấy {len(res)} kết quả ---")
                    for ct in res: print(f"ID: {ct.contact_id} | {ct.name} | {ct.phone}")
                    vid = input("Nhập ID muốn xem chi tiết: ")
                    if vid.isdigit():
                        if self.current_user.view_contact_detail(int(vid)): 
                            self.save_changes()
                            input("Nhấn Enter để tiếp tục...")

            elif c == '6': # CREATE GROUP
                self.current_user.create_group(input("Tên nhóm: "))
                self.save_changes()

            elif c == '7': # DELETE GROUP
                try:
                    print("DS Nhóm:", end=" ")
                    for g in self.current_user.groups: print(f"[{g.group_id}:{g.group_name}]", end=" ")
                    self.current_user.remove_group(int(input("\nID Nhóm xóa: ")))
                    self.save_changes()
                except: pass

            elif c == '8': # GROUP DETAILS
                self.group_management_menu()

            elif c == '0':
                self.current_user = None; break

    def group_management_menu(self):
        """Menu quản lý chi tiết thành viên trong nhóm."""
        while True:
            print("\n--- 📂 QUẢN LÝ CHI TIẾT NHÓM ---")
            print("DS Nhóm:", end=" ")
            for g in self.current_user.groups: print(f"[{g.group_id}:{g.group_name}]", end=" ")
            print("\n1. Thêm người vào nhóm")
            print("2. Mời người ra khỏi nhóm")
            print("3. Đổi tên nhóm")
            print("4. Xem thành viên nhóm")
            print("0. Back")
            
            c = input("👉 Chọn: ")
            changed = False

            if c == '1':
                try: 
                    self.current_user.add_contact_to_group(int(input("ID Contact: ")), int(input("ID Group: ")))
                    changed = True
                except: pass
            elif c == '2':
                try:
                    gid = int(input("ID Group: "))
                    self.current_user.view_contacts_in_group(gid)
                    cid = int(input("ID Contact cần mời ra: "))
                    if self.current_user.remove_contact_from_group(cid, gid): changed = True
                except: pass
            elif c == '3':
                try: 
                    self.current_user.rename_group(int(input("ID Group: ")), input("Tên mới: "))
                    changed = True
                except: pass
            elif c == '4':
                try: self.current_user.view_contacts_in_group(int(input("ID Group: ")))
                except: pass
            elif c == '0': break
            
            if changed: self.save_changes()

if __name__ == "__main__":
    app = PhoneBookSystem()
    app.main_menu()