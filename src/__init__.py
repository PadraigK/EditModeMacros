import bpy
from bpy.types import Operator


class EDITMODE_OT_switch_to_vertex(Operator):
    """Switch to Edit Mode - Vertex Select"""
    bl_idname = "editmode.switch_to_vertex"
    bl_label = "Switch to Edit Mode - Vertex"
    bl_description = "Switch to Edit Mode with Vertex selection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Check if we're in object mode and have an active mesh object
        if (context.mode == 'OBJECT' and
                context.active_object and
                context.active_object.type == 'MESH'):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='VERT')

        return {"FINISHED"}


class EDITMODE_OT_switch_to_edge(Operator):
    """Switch to Edit Mode - Edge Select"""
    bl_idname = "editmode.switch_to_edge"
    bl_label = "Switch to Edit Mode - Edge"
    bl_description = "Switch to Edit Mode with Edge selection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Check if we're in object mode and have an active mesh object
        if (context.mode == 'OBJECT' and
                context.active_object and
                context.active_object.type == 'MESH'):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='EDGE')

        return {"FINISHED"}


class EDITMODE_OT_switch_to_face(Operator):
    """Switch to Edit Mode - Face Select"""
    bl_idname = "editmode.switch_to_face"
    bl_label = "Switch to Edit Mode - Face"
    bl_description = "Switch to Edit Mode with Face selection"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Check if we're in object mode and have an active mesh object
        if (context.mode == 'OBJECT' and
                context.active_object and
                context.active_object.type == 'MESH'):
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_mode(type='FACE')

        return {"FINISHED"}


class EDITMODE_OT_switch_to_object(Operator):
    """Switch to Object Mode"""
    bl_idname = "editmode.switch_to_object"
    bl_label = "Switch to Object Mode"
    bl_description = "Switch back to Object Mode"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Check if we're in edit mode
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.mode_set(mode='OBJECT')

        return {"FINISHED"}


# Keymap handling
addon_keymaps = []
disabled_keymaps = []


def disable_default_number_keys():
    """Disable default 1-4 key assignments"""
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.default

    # Look for existing 1-4 key assignments in 3D View
    if kc:
        for km in kc.keymaps:
            if km.name == '3D View':
                for kmi in km.keymap_items:
                    if kmi.type in ['ONE', 'TWO', 'THREE', 'FOUR'] and kmi.active:
                        disabled_keymaps.append((km, kmi))
                        kmi.active = False


def restore_default_number_keys():
    """Restore default 1-4 key assignments"""
    for km, kmi in disabled_keymaps:
        kmi.active = True
    disabled_keymaps.clear()


def register():
    # Register operators
    bpy.utils.register_class(EDITMODE_OT_switch_to_vertex)
    bpy.utils.register_class(EDITMODE_OT_switch_to_edge)
    bpy.utils.register_class(EDITMODE_OT_switch_to_face)
    bpy.utils.register_class(EDITMODE_OT_switch_to_object)

    # Disable default number key assignments
    disable_default_number_keys()

    # Add our custom keymaps
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')

        # Key 1: Object mode → Edit mode (Vertex)
        kmi = km.keymap_items.new(EDITMODE_OT_switch_to_vertex.bl_idname, 'ONE', 'PRESS')
        addon_keymaps.append((km, kmi))

        # Key 2: Object mode → Edit mode (Edge)
        kmi = km.keymap_items.new(EDITMODE_OT_switch_to_edge.bl_idname, 'TWO', 'PRESS')
        addon_keymaps.append((km, kmi))

        # Key 3: Object mode → Edit mode (Face)
        kmi = km.keymap_items.new(EDITMODE_OT_switch_to_face.bl_idname, 'THREE', 'PRESS')
        addon_keymaps.append((km, kmi))

        # Key 4: Edit mode → Object mode
        kmi = km.keymap_items.new(EDITMODE_OT_switch_to_object.bl_idname, 'FOUR', 'PRESS')
        addon_keymaps.append((km, kmi))


def unregister():
    # Remove our keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

    # Restore default number key assignments
    restore_default_number_keys()

    # Unregister operators
    bpy.utils.unregister_class(EDITMODE_OT_switch_to_vertex)
    bpy.utils.unregister_class(EDITMODE_OT_switch_to_edge)
    bpy.utils.unregister_class(EDITMODE_OT_switch_to_face)
    bpy.utils.unregister_class(EDITMODE_OT_switch_to_object)