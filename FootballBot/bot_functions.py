"""This module for helpers functions for bot"""


def build_leagues_menu_btn(mark_up_cls, btn_cls, objects, row_width):
    btn_group = mark_up_cls(row_width=row_width)
    for key in range(len(objects)-1):
        a = None
        row = []
        try:
            for _ in range(btn_group.row_width):
                a = objects.popitem()
                leag1 = btn_cls(text=a[1]['name'], callback_data=a[0])
                row.append(leag1)
            btn_group.row(*row)
        except KeyError:
            if a is not None:
                btn_group.row(*row)
    return btn_group
