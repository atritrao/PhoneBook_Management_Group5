import json
import os
import datetime
from models import Member, Admin, Contact, Group, ContactGroupMembership

DATA_FILE = "phonebook_data.json"

class DataManager:
    """
    Lớp chịu trách nhiệm đọc và ghi dữ liệu xuống file JSON.
    """

    @staticmethod
    def save_data(admins, members, logs):
        """
        Lưu toàn bộ danh sách Admins, Members và Logs xuống file JSON.
        
        Args:
            admins (list[Admin]): Danh sách admin.
            members (list[Member]): Danh sách member.
            logs (list[str]): Danh sách log hệ thống.
        """
        data = {
            "admins": [],
            "members": [],
            "logs": logs 
        }

        # 1. Lưu Admin
        for admin in admins:
            data["admins"].append({
                "admin_id": admin.admin_id, 
                "username": admin.username, 
                "password": admin.password # Đã hash
            })

        # 2. Lưu Member
        for mem in members:
            member_dict = {
                "member_id": mem.member_id, "username": mem.username, 
                "password": mem.password, "email": mem.email,
                "is_active": mem.is_active,
                "contacts": [], "groups": [], "memberships": []
            }

            # Lưu Contacts
            for c in mem.contacts:
                c_dict = {
                    "contact_id": c.contact_id, "name": c.name, "phone": c.phone,
                    "email": c.email, "address": c.address, "notes": c.notes
                }
                if c.last_viewed_at:
                    c_dict["last_viewed_at"] = c.last_viewed_at.strftime("%Y-%m-%d %H:%M:%S")
                member_dict["contacts"].append(c_dict)

            # Lưu Groups
            for g in mem.groups:
                member_dict["groups"].append({"group_id": g.group_id, "group_name": g.group_name})

            # Lưu Memberships
            for m in mem.memberships:
                member_dict["memberships"].append({
                    "contact_id": m.contact_id, "group_id": m.group_id,
                    "added_at": m.added_at.strftime("%Y-%m-%d %H:%M:%S")
                })

            data["members"].append(member_dict)

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"⚠️ Lỗi lưu file: {e}")

    @staticmethod
    def load_data():
        """
        Đọc dữ liệu từ file JSON và khôi phục lại các object.
        
        Returns:
            tuple: (admins, members, logs)
        """
        admins, members, logs = [], [], []
        if not os.path.exists(DATA_FILE): return [], [], []

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Load Logs
            logs = data.get("logs", [])

            # Load Admin
            for ad in data.get("admins", []):
                # Password từ file json đã là hash, Member.__init__ sẽ tự nhận diện qua độ dài
                admins.append(Admin(ad["admin_id"], ad["username"], ad["password"]))

            # Load Member
            for m_data in data.get("members", []):
                new_mem = Member(m_data["member_id"], m_data["username"], m_data["password"], m_data["email"])
                new_mem.is_active = m_data.get("is_active", True)

                for c_data in m_data.get("contacts", []):
                    contact = Contact(
                        c_data["contact_id"], c_data["name"], c_data["phone"],
                        c_data.get("email", ""), c_data.get("address", ""), c_data.get("notes", "")
                    )
                    if "last_viewed_at" in c_data and c_data["last_viewed_at"]:
                        try: contact.last_viewed_at = datetime.datetime.strptime(c_data["last_viewed_at"], "%Y-%m-%d %H:%M:%S")
                        except: pass
                    new_mem.contacts.append(contact)

                for g_data in m_data.get("groups", []):
                    new_mem.groups.append(Group(g_data["group_id"], g_data["group_name"]))

                for lnk in m_data.get("memberships", []):
                    ms = ContactGroupMembership(lnk["contact_id"], lnk["group_id"])
                    try: ms.added_at = datetime.datetime.strptime(lnk["added_at"], "%Y-%m-%d %H:%M:%S")
                    except: pass
                    new_mem.memberships.append(ms)

                members.append(new_mem)
            
            return admins, members, logs
        except Exception: return [], [], []