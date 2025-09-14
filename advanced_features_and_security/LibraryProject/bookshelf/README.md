"""
Permissions & Groups Setup:
- Custom permissions added to Book model: can_view, can_create, can_edit, can_delete.
- Groups:
    Viewers  -> can_view
    Editors  -> can_view, can_create, can_edit
    Admins   -> can_view, can_create, can_edit, can_delete
- Views are protected using @permission_required with raise_exception=True.
"""
