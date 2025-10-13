from pathlib import Path
import dearpygui.dearpygui as dpg

import DearPyGui_DragAndDrop as dpg_dnd

from flpslicer import get_flp_slices


def select_file(file_path: str):
    file = Path(file_path)
    if not file.exists() or not file.is_file() or file.suffix != ".flp":
        print("Invalid file path: ", file_path)
        return

    parse_file(file_path)


def parse_file(file_path: str):
    slice_result = get_flp_slices(file_path)

    dpg.configure_item("arrangement", items=[arrangement.name for arrangement in slice_result.arrangements])
    dpg.configure_item("arrangement", enabled=True)
    dpg.set_value("arrangement", slice_result.arrangements[slice_result.selected_arrangement].name)

    children = dpg.get_item_children("tracks")
    for child in children[1]:
        if dpg.get_item_alias(child) != "select_all_tracks":
            dpg.delete_item(child)
    for track in slice_result.arrangement_tracks:
        dpg.add_checkbox(label=track.name, parent="tracks", tag=track.iid, default_value=track.iid in slice_result.selected_tracks)
    
    dpg.set_value("num_samples", f"{len(slice_result.samples)} samples")


def on_change_arrangement(sender, app_data):
    slice_result = get_flp_slices(file_path)


def on_file_selected(sender, app_data):    
    select_file(app_data["file_path_name"])


def on_file_dropped(data, keys):
    dpg.bind_item_theme("primary_window", None)
    if len(data) == 1:
        select_file(data[0])


def on_drag_enter(data, keys):
    dpg.bind_item_theme("primary_window", "hover_drag_theme")


def on_drag_leave():
    dpg.bind_item_theme("primary_window", None)


def create_window():
    with dpg.window(tag="primary_window"):
        with dpg.file_dialog(show=False, modal=True, callback=on_file_selected, width=700, height=400, tag="file_dialog"):
            dpg.add_file_extension(".flp")

        with dpg.menu_bar():
            dpg.add_menu_item(label="Open .flp", callback=lambda: dpg.show_item("file_dialog"))
        
        dpg.add_combo([], label="Arrangement", tag="arrangement", enabled=False, callback=on_change_arrangement)
        dpg.add_collapsing_header(label="Tracks", tag="tracks", default_open=True)

        dpg.add_text("0 samples", tag="num_samples")


def main():
    dpg.create_context()
    dpg_dnd.initialize()

    with dpg.theme(tag="hover_drag_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Border, (0, 180, 255), category=dpg.mvThemeCat_Core)

    dpg_dnd.set_drop(on_file_dropped)
    dpg_dnd.set_drag_enter(on_drag_enter)
    dpg_dnd.set_drag_leave(on_drag_leave)

    create_window()

    dpg.create_viewport(title='flpslicer', width=1000, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("primary_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
