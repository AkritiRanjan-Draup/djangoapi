get_note_of_id = ("SELECT title, content, created_at, updated_at, user_id, folder_id FROM notes_note WHERE id = {"
                  "note_id} AND user_id = {user_id} ORDER BY created_at DESC")

get_folders = "SELECT name, created_at, updated_at FROM notes_folder WHERE user_id = {user_id} ORDER BY created_at DESC"

get_folder_of_id = ("SELECT name, created_at, updated_at FROM notes_folder WHERE user_id = {user_id} AND id = {"
                    "folder_id} ORDER BY created_at DESC")

get_notes_of_folder = ("SELECT title, content, created_at, updated_at, user_id, folder_id FROM notes_note WHERE "
                       "folder_id = {folder_id} ORDER BY created_at DESC")
