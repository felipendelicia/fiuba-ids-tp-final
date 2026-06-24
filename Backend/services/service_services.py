from db import execute


def listar_servicios():
    return execute("SELECT * FROM Service ORDER BY sort_order ASC")


def obtener_servicio(service_id):
    rows = execute("SELECT * FROM Service WHERE id = %s", (service_id,))
    return rows[0] if rows else None


def crear_servicio(data):
    execute(
        "INSERT INTO Service (name, tab_icon, summary_title, summary_text, bullet_1, bullet_2, tab_image, "
        "detail_title, detail_subtitle, section_1_title, section_1_text, section_2_title, section_2_text, "
        "detail_image_1, detail_image_2, breadcrumb_label, sort_order) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (
            data.get("name"), data.get("tab_icon") or "bi bi-gear", data.get("summary_title"),
            data.get("summary_text"), data.get("bullet_1"), data.get("bullet_2"),
            data.get("tab_image"), data.get("detail_title"), data.get("detail_subtitle"),
            data.get("section_1_title"), data.get("section_1_text"),
            data.get("section_2_title"), data.get("section_2_text"),
            data.get("detail_image_1"), data.get("detail_image_2"),
            data.get("breadcrumb_label"), data.get("sort_order", 0),
        ),
    )
    return True


def actualizar_servicio(service_id, data):
    execute(
        "UPDATE Service SET name=%s, tab_icon=%s, summary_title=%s, summary_text=%s, "
        "bullet_1=%s, bullet_2=%s, tab_image=%s, detail_title=%s, detail_subtitle=%s, "
        "section_1_title=%s, section_1_text=%s, section_2_title=%s, section_2_text=%s, "
        "detail_image_1=%s, detail_image_2=%s, breadcrumb_label=%s, sort_order=%s WHERE id=%s",
        (
            data.get("name"), data.get("tab_icon") or "bi bi-gear", data.get("summary_title"),
            data.get("summary_text"), data.get("bullet_1"), data.get("bullet_2"),
            data.get("tab_image"), data.get("detail_title"), data.get("detail_subtitle"),
            data.get("section_1_title"), data.get("section_1_text"),
            data.get("section_2_title"), data.get("section_2_text"),
            data.get("detail_image_1"), data.get("detail_image_2"),
            data.get("breadcrumb_label"), data.get("sort_order", 0),
            service_id,
        ),
    )
    return True


def eliminar_servicio(service_id):
    execute("DELETE FROM Service WHERE id = %s", (service_id,))
    return True