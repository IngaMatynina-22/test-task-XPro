from src.category.models import Category


def get_status_label(status: int) -> str:
    return "Включена" if status == 1 else "Выключена"


def build_category_path(
    category: Category,
    categories_by_id: dict[int, Category],
) -> str:
    names = [category.name]
    parent_id = category.parent_category_id
    visited_ids = {category.category_id}

    while parent_id is not None and parent_id in categories_by_id:
        if parent_id in visited_ids:
            break

        visited_ids.add(parent_id)

        parent = categories_by_id[parent_id]
        names.append(parent.name)
        parent_id = parent.parent_category_id

    return " > ".join(reversed(names))