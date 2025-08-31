from reference99names import table_data as references_data

def get_references_for(id_):
    for entry in references_data:
        if "id" in entry and entry["id"] == id_:
            return entry.get("references", [])
    return []

def load_esma_with_references():
    """
    Return the 99 names, each augmented with its 'references' list.
    If `id` is missing, use auto-increment index as fallback.
    """
    result = []
    for index, item in enumerate(references_data, start=1):
        item_id = item.get("id", index)  # use existing ID or fallback to index
        merged = item.copy()
        merged["id"] = item_id
        merged["references"] = get_references_for(item_id)
        result.append(merged)
    return result
