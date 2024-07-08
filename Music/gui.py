import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from music import Sammlung, Album, Track
from frame import Window
import re


collection = Sammlung()
collection.load_from_file('./albums.json')
print("Albums loaded from file:")
for album in collection.alben:
    print(f"- {album.title}")

def create_album_interface():
    frame_name = 'Add Album'
    window = Window(root, frame_name)
    create_album_dialogue = window.dialogue

    def clear_placeholder(event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")
            event.widget.config(foreground='black')

    def set_placeholder(widget, placeholder):
        if widget.get() == "":
            widget.insert(0, placeholder)
            widget.config(foreground='#A9A9A9')

    def add_track():
        track_info = create_track_entry.get()
        if track_info != 'Title, MP3, Duration...' and track_info != '':
            track_box.insert(tk.END, track_info)
        create_track_entry.delete(0, "end")
        set_placeholder(create_track_entry, 'Title, MP3, Duration...')
        set_placeholder(create_interpret_entry, 'Interpret...')
        set_placeholder(create_title_entry, 'Album Title...')

    def del_track():
        selected_items = track_box.curselection()
        for item in selected_items[::-1]:
            track_box.delete(item)

    def create_album():
        title = create_title_entry.get()
        interpret = create_interpret_entry.get()
        if title == 'Album Title...' or interpret == 'Interpret...':
            messagebox.showwarning("Input Error", "Please provide both album title and interpret.")
            return

        tracks = []
        for i in range(track_box.size()):
            track_info = track_box.get(i).split(',')
            if len(track_info) != 3:
                messagebox.showwarning("Input Error", f"Track {i+1} is not in the correct format (Title, MP3, Duration...).")
                return
            track_title, track_mp3, track_duration = track_info[0].strip(), track_info[1].strip(), track_info[2].strip()
            if not re.match(r'^\d{2}:\d{2}:\d{2}$', track_duration):
                messagebox.showwarning("Input Error", f"Track {i+1} duration is not in the correct format (HH:MM:SS).")
                return
            track = Track(track_title, track_mp3, track_duration)
            tracks.append(track)

        album = Album(title, interpret, tracks)
        collection.add_album(album)
        collection.save_to_file('./albums.json')
        messagebox.showinfo("Success", f"Added {album.title} by {album.interpret} with total playtime of {album.get_total_time_to_play()}")
        create_album_dialogue.destroy()
        root.deiconify()

    create_album_dialogue.grid_columnconfigure(0, weight=1)
    create_album_dialogue.grid_columnconfigure(1, weight=1)
    create_album_dialogue.grid_columnconfigure(2, weight=1)
    create_album_dialogue.grid_rowconfigure(0, weight=1)
    create_album_dialogue.grid_rowconfigure(9, weight=1)

    style = ttk.Style()
    style.configure('TLabel', background='black', font=('Arial', 12))
    style.configure('TButton', font=('Helvetica', 12), background="black", foreground="black", width=12, height=5)
    style.configure('TEntry', font=('Helvetica', 12))

    create_title_entry = ttk.Entry(create_album_dialogue, foreground='#A9A9A9')
    create_title_entry.grid(row=1, column=1, padx=10, pady=5)
    create_title_entry.insert(0, 'Album Title...')
    create_title_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, 'Album Title...'))
    create_title_entry.bind("<FocusOut>", lambda event: set_placeholder(event.widget, 'Album Title...'))

    create_interpret_entry = ttk.Entry(create_album_dialogue, foreground='#A9A9A9')
    create_interpret_entry.grid(row=2, column=1, padx=10, pady=5)
    create_interpret_entry.insert(0, 'Interpret...')
    create_interpret_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, 'Interpret...'))
    create_interpret_entry.bind("<FocusOut>", lambda event: set_placeholder(event.widget, 'Interpret...'))

    create_track_entry = ttk.Entry(create_album_dialogue, foreground='#A9A9A9')
    create_track_entry.grid(row=3, column=1, padx=10, pady=5)
    create_track_entry.insert(0, 'Title, MP3, Duration...')
    create_track_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, 'Title, MP3, Duration...'))
    create_track_entry.bind("<FocusOut>", lambda event: set_placeholder(event.widget, 'Title, MP3, Duration...'))

    track_box = tk.Listbox(create_album_dialogue)
    track_box.grid(row=4, column=1, padx=10, pady=5)
    track_box.configure(background='aliceblue')

    ttk.Button(create_album_dialogue, text="Add Track", command=add_track).grid(row=5, column=1, pady=3)
    ttk.Button(create_album_dialogue, text="Del Track", command=del_track).grid(row=6, column=1, pady=3)
    ttk.Button(create_album_dialogue, text="OK", command=create_album).grid(row=7, column=1, pady=3)

    def close_create_album():
        create_album_dialogue.destroy()
        root.deiconify()

    ttk.Button(create_album_dialogue, text="Close", command=close_create_album).grid(row=8, column=1, pady=3)

    create_album_dialogue.after(0, window.center_window)

def view_album_interface():
    frame_name = 'View Album'
    window = Window(root, frame_name)
    view_album_dialogue = window.dialogue

    def clear_placeholder(event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")
            event.widget.config(foreground='black')

    def set_placeholder(widget, placeholder):
        if widget.get() == "":
            widget.insert(0, placeholder)
            widget.config(foreground='#A9A9A9')

    def choice():
        action = action_var.get()
        album_title = album_entry.get().strip().lower()  
        print(f"Album title to search: '{album_title}'")
        print("Albums in collection:")
        for album in collection.alben:
            print(f"- '{album.title.lower().strip()}'")  
        
        album = None
        for a in collection.alben:
            if a.title.lower().strip() == album_title:
                album = a
                break

        if action == "view Album":
            if album:
                info = album.printInformation()
                messagebox.showinfo("Album Information", info)
            else:
                messagebox.showwarning("Error", "Album not found.")
        elif action == "Delete Album":
            if album:
                collection.remove_album(album)
                collection.save_to_file('./albums.json')
                messagebox.showinfo("Success", "Album deleted.")
            else:
                messagebox.showwarning("Error", "Album not found.")
        elif action == "view all Albums":
            info = collection.printInformation()
            messagebox.showinfo("All Albums Information", info)

    view_album_dialogue.grid_columnconfigure(0, weight=1)
    view_album_dialogue.grid_columnconfigure(1, weight=1)
    view_album_dialogue.grid_columnconfigure(2, weight=1)
    view_album_dialogue.grid_rowconfigure(0, weight=1)
    view_album_dialogue.grid_rowconfigure(6, weight=1)

    style = ttk.Style()
    style.configure('TLabel', background='black', font=('Arial', 12))
    style.configure('TButton', font=('Helvetica', 12), background="black", foreground="black", width=12, height=5)
    style.configure('TEntry', font=('Helvetica', 12))

    actions = ["view Album", "Delete Album", "view all Albums"]
    action_var = tk.StringVar(view_album_dialogue)
    action_var.set(actions[0])
    action_menu = ttk.Combobox(view_album_dialogue, textvariable=action_var, values=actions, state='readonly', width=20)
    action_menu.grid(row=1, column=1, pady=10)

    album_entry = ttk.Entry(view_album_dialogue, foreground='#A9A9A9', width=23)
    album_entry.grid(row=2, column=1, padx=10, pady=10)
    album_entry.insert(0, 'Album Title...')
    album_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, 'Album Title...'))
    album_entry.bind("<FocusOut>", lambda event: set_placeholder(event.widget, 'Album Title...'))

    ttk.Button(view_album_dialogue, text="OK", command=choice).grid(row=3, column=1, pady=10)

    def close_view_album():
        view_album_dialogue.destroy()
        root.deiconify()

    ttk.Button(view_album_dialogue, text="Close", command=close_view_album).grid(row=4, column=1, pady=10)

    view_album_dialogue.after(0, window.center_window)

def manage_tracks_interface():
    frame_name = 'Manage Tracks'
    window = Window(root, frame_name)
    manage_tracks_dialogue = window.dialogue

    def clear_placeholder(event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, "end")
            event.widget.config(foreground='black')

    def set_placeholder(widget, placeholder):
        if widget.get() == "":
            widget.insert(0, placeholder)
            widget.config(foreground='#A9A9A9')

    def load_tracks():
        album_title = album_entry.get().strip().lower()
        album = None
        for a in collection.alben:
            if a.title.lower().strip() == album_title:
                album = a
                break

        track_box.delete(0, tk.END)  
        if album:
            for track in album.tracks:
                track_box.insert(tk.END, f"{track.title}, {track.MP3}, {track.duration}")
        else:
            messagebox.showwarning("Error", "Album not found.")

    def add_track():
        album_title = album_entry.get().strip().lower()
        track_info = track_entry.get().strip()

        album = None
        for a in collection.alben:
            if a.title.lower().strip() == album_title:
                album = a
                break

        if album:
            track_details = track_info.split(',')
            if len(track_details) != 3:
                messagebox.showwarning("Input Error", "Track details should be in the format: Title, MP3, Duration.")
                return
            title, mp3, duration = track_details[0].strip(), track_details[1].strip(), track_details[2].strip()
            if not re.match(r'^\d{2}:\d{2}:\d{2}$', duration):
                messagebox.showwarning("Input Error", "Track duration is not in the correct format (HH:MM:SS).")
                return
            track = Track(title, mp3, duration)
            album.add_track(track)
            collection.save_to_file('./albums.json')
            load_tracks()  # Refresh the listbox
            messagebox.showinfo("Success", f"Track {title} added to album {album_title}.")
        else:
            messagebox.showwarning("Error", "Album not found.")

    def delete_track():
        album_title = album_entry.get().strip().lower()
        selected_items = track_box.curselection()

        album = None
        for a in collection.alben:
            if a.title.lower().strip() == album_title:
                album = a
                break

        if album:
            for item in selected_items[::-1]:
                track_info = track_box.get(item).split(',')
                title, mp3, duration = track_info[0].strip(), track_info[1].strip(), track_info[2].strip()
                track = next((t for t in album.tracks if t.title == title and t.MP3 == mp3 and t.duration == duration), None)
                if track:
                    album.remove_track(track)
                    track_box.delete(item)
            collection.save_to_file('./albums.json')
            messagebox.showinfo("Success", "Selected tracks removed.")
        else:
            messagebox.showwarning("Error", "Album not found.")

    manage_tracks_dialogue.grid_columnconfigure(0, weight=1)
    manage_tracks_dialogue.grid_columnconfigure(1, weight=1)
    manage_tracks_dialogue.grid_columnconfigure(2, weight=1)
    manage_tracks_dialogue.grid_rowconfigure(0, weight=1)
    manage_tracks_dialogue.grid_rowconfigure(9, weight=1)

    style = ttk.Style()
    style.configure('TLabel', background='black', font=('Arial', 12))
    style.configure('TButton', font=('Helvetica', 12), background="black", foreground="black", width=12, height=5)
    style.configure('TEntry', font=('Helvetica', 12))

    album_entry = ttk.Entry(manage_tracks_dialogue, foreground='#A9A9A9')
    album_entry.grid(row=1, column=1, padx=10, pady=5)
    album_entry.insert(0, 'Album Title...')
    album_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, 'Album Title...'))
    album_entry.bind("<FocusOut>", lambda event: set_placeholder(event.widget, 'Album Title...'))

    track_entry = ttk.Entry(manage_tracks_dialogue, foreground='#A9A9A9')
    track_entry.grid(row=2, column=1, padx=10, pady=5)
    track_entry.insert(0, 'Title, MP3, Duration...')
    track_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, 'Title, MP3, Duration...'))
    track_entry.bind("<FocusOut>", lambda event: set_placeholder(event.widget, 'Title, MP3, Duration...'))

    ttk.Button(manage_tracks_dialogue, text="Load Tracks", command=load_tracks).grid(row=3, column=1, pady=3)
    track_box = tk.Listbox(manage_tracks_dialogue)
    track_box.grid(row=4, column=1, padx=10, pady=5)
    track_box.configure(background='aliceblue')

    ttk.Button(manage_tracks_dialogue, text="Add Track", command=add_track).grid(row=5, column=1, pady=3)
    ttk.Button(manage_tracks_dialogue, text="Delete Track", command=delete_track).grid(row=6, column=1, pady=3)

    def close_manage_tracks():
        manage_tracks_dialogue.destroy()
        root.deiconify()

    ttk.Button(manage_tracks_dialogue, text="Close", command=close_manage_tracks).grid(row=7, column=1, pady=3)

    manage_tracks_dialogue.after(0, window.center_window)

def import_export_interface():
    frame_name = 'Import/Export Albums'
    window = Window(root, frame_name)
    import_export_dialogue = window.dialogue

    def export_albums():
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            collection.save_to_file(file_path)
            messagebox.showinfo("Success", f"Albums exported to {file_path}")

    def import_albums():
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if file_path:
            collection.load_from_file(file_path)
            messagebox.showinfo("Success", f"Albums imported from {file_path}")

    import_export_dialogue.grid_columnconfigure(0, weight=1)
    import_export_dialogue.grid_columnconfigure(1, weight=1)
    import_export_dialogue.grid_columnconfigure(2, weight=1)
    import_export_dialogue.grid_rowconfigure(0, weight=1)
    import_export_dialogue.grid_rowconfigure(4, weight=1)
    
    ttk.Button(import_export_dialogue, text="Export Albums", command=export_albums).grid(row=1, column=1, pady=10, padx=10)
    ttk.Button(import_export_dialogue, text="Import Albums", command=import_albums).grid(row=2, column=1, pady=10, padx=10)

    def close_import_export():
        import_export_dialogue.destroy()
        root.deiconify()

    ttk.Button(import_export_dialogue, text="Close", command=close_import_export).grid(row=3, column=1, pady=10)

    import_export_dialogue.after(0, window.center_window)


root = tk.Tk()
root.title("Music App")
root.geometry("500x309")
root.configure(bg="#c90076")
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f'{width}x{height}+{x}+{y}')

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_rowconfigure(4, weight=1)

frame = tk.Frame(root, bg="#c90076")
frame.grid(row=0, column=0)

style = ttk.Style()
style.configure('TLabel', background='aliceblue', font=('Arial', 12))
style.configure('TButton', font=('Arial', 12), background="black", foreground="black", width=21, height=13)
style.configure('TEntry', font=('Arial', 12))

style.map('TButton', background=[('active', 'purple')], foreground=[('active', 'purple')])

create_album_button = ttk.Button(frame, text="Create Album", command=create_album_interface)
create_album_button.grid(row=0, column=1, padx=20, pady=20)

view_album_button = ttk.Button(frame, text="View Albums", command=view_album_interface)
view_album_button.grid(row=1, column=1, padx=20, pady=20)

manage_tracks_button = ttk.Button(frame, text="Manage Tracks", command=manage_tracks_interface)
manage_tracks_button.grid(row=2, column=1, padx=20, pady=20)

import_export_button = ttk.Button(frame, text="Import/Export Albums", command=import_export_interface)
import_export_button.grid(row=3, column=1, padx=20, pady=20)

root.mainloop()
