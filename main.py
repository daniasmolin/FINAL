import sqlite3


class DatabaseManager:

  def __init__(self, db_name="dictionary_notes.db"):
    self.db_name = db_name

  def add_entry(self, term, definition):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO entries (term, definition) VALUES (?, ?)",
        (term, definition),
    )
    conn.commit()
    conn.close()

  def get_all_entries(self):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT term, definition FROM entries")
    rows = cursor.fetchall()
    conn.close()
    return rows

  def search_entries(self, keyword):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    pattern = f"%{keyword}%"
    cursor.execute(
        "SELECT term, definition FROM entries WHERE term LIKE ? OR definition"
        " LIKE ?",
        (pattern, pattern),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows

  def clear_entries(self):
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM entries")
    conn.commit()
    conn.close()


class ConsoleUI:

  def __init__(self, db):
    self.db = db

  def show_menu(self):
    print("\n--- Словничок / Нотатник ---")
    print("1. Додати запис")
    print("2. Показати всі записи")
    print("3. Знайти запис за словом")
    print("4. Очистити базу даних")
    print("5. Вийти")

  def print_entries(self, entries):
    for term, definition in entries:
      print(f"{term} — {definition}")

  def start(self):
    while True:
      self.show_menu()
      choice = input("Оберіть дію (1-5): ").strip()

      if choice == "1":
        term = input("Введіть слово або назву: ").strip()
        definition = input("Введіть пояснення або нотатку: ").strip()
        self.db.add_entry(term, definition)
        print("Запис додано.")

      elif choice == "2":
        entries = self.db.get_all_entries()
        if entries:
          self.print_entries(entries)
        else:
          print("Записів немає.")

      elif choice == "3":
        keyword = input("Введіть слово для пошуку: ").strip()
        matches = self.db.search_entries(keyword)
        if matches:
          self.print_entries(matches)
        else:
          print("Збігів не знайдено.")

      elif choice == "4":
        self.db.clear_entries()
        print("Базу даних очищено.")

      elif choice == "5":
        print("Вихід із програми.")
        break

      else:
        print("Невірний вибір.")


def run():
  db = DatabaseManager()
  ui = ConsoleUI(db)
  ui.start()


if __name__ == "__main__":
  run()