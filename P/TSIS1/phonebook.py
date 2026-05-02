import csv
import json
from connect import connect

def filter_by_group(group_name):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        SELECT contacts.name, contacts.email 
        FROM contacts 
        JOIN groups ON contacts.group_id = groups.id 
        WHERE groups.name = %s
    """, (group_name,))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def search_by_email(email_part):
    conn = connect()
    cur = conn.cursor()
    search_text = "%" + email_part + "%"
    cur.execute("SELECT name, email FROM contacts WHERE email ILIKE %s", (search_text,))
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def sort_contacts(order_by):
    conn = connect()
    cur = conn.cursor()
    if order_by == 'name':
        cur.execute("SELECT name, email, birthday, date_added FROM contacts ORDER BY name")
    elif order_by == 'birthday':
        cur.execute("SELECT name, email, birthday, date_added FROM contacts ORDER BY birthday")
    elif order_by == 'date':
        cur.execute("SELECT name, email, birthday, date_added FROM contacts ORDER BY date_added")
    else:
        print("Неверное поле")
        return
    for row in cur.fetchall():
        print(row)
    cur.close()
    conn.close()

def navigate_pages():
    limit = 5
    offset = 0
    while True:
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT name, email FROM contacts ORDER BY name LIMIT %s OFFSET %s", (limit, offset))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        
        if len(rows) == 0:
            print("Контактов больше нет.")
            break
            
        for r in rows:
            print(r)
            
        cmd = input("След(n) / Пред(p) / Выход(q): ")
        if cmd == 'n':
            offset = offset + limit
        elif cmd == 'p':
            offset = offset - limit
            if offset < 0:
                offset = 0
        elif cmd == 'q':
            break

def export_json():
    conn = connect()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT contacts.id, contacts.name, contacts.email, contacts.birthday, groups.name 
        FROM contacts 
        LEFT JOIN groups ON contacts.group_id = groups.id
    """)
    contacts_rows = cur.fetchall()
    
    data = []
    for c in contacts_rows:
        contact_id = c[0]
        

        cur.execute("SELECT phone, type FROM phones WHERE contact_id = %s", (contact_id,))
        phone_rows = cur.fetchall()
        
        phones_list = []
        for p in phone_rows:
            phones_list.append({"phone": p[0], "type": p[1]})
            
        birthday_str = str(c[3]) if c[3] else None
        
        contact_dict = {
            "name": c[1],
            "email": c[2],
            "birthday": birthday_str,
            "group": c[4],
            "phones": phones_list
        }
        data.append(contact_dict)
        
    cur.close()
    conn.close()
    
    with open('contacts.json', 'w') as f:
        json.dump(data, f, indent=4)
    print("Экспорт завершен.")

def import_json():
    with open('contacts.json', 'r') as f:
        data = json.load(f)
        
    conn = connect()
    cur = conn.cursor()
    
    for item in data:
        name = item["name"]
        
        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        exists = cur.fetchone()
        
        if exists is not None:
            ans = input(f"Контакт {name} уже есть. Заменить(o) или Пропустить(s)? ")
            if ans == 'o':
                cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
            else:
                continue
                
        group_id = None
        group_name = item.get("group")
        if group_name is not None:
            cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
            grp = cur.fetchone()
            if grp is None:
                cur.execute("INSERT INTO groups (name) VALUES (%s) RETURNING id", (group_name,))
                group_id = cur.fetchone()[0]
            else:
                group_id = grp[0]
                
        cur.execute("INSERT INTO contacts (name, email, birthday, group_id) VALUES (%s, %s, %s, %s) RETURNING id",
                    (name, item.get("email"), item.get("birthday"), group_id))
        new_contact_id = cur.fetchone()[0]
        
        for p in item.get("phones", []):
            cur.execute("INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                        (new_contact_id, p["phone"], p["type"]))
                        
    conn.commit()
    cur.close()
    conn.close()
    print("Импорт завершен.")

if __name__ == '__main__':
    while True:
        print("\n--- МЕНЮ ---")
        print("1. Поиск по email")
        print("2. Экспорт JSON")
        print("3. Листать страницы")
        print("0. Выход")
        
        choice = input("Выбор: ")
        
        if choice == '1':
            email = input("Email: ")
            search_by_email(email)
        elif choice == '2':
            export_json()
        elif choice == '3':
            navigate_pages()
        elif choice == '0':
            break