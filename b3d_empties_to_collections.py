bl_info = {
    "name" : "Empties To Collections",
    "version" : (1,0),
    "author" : "bi1ash" 
    "blender" : (4,3,1),
    "location" : "Outliner > Right-Click Menu",
    "doc_url" : "https://github.com/bi1ash/b3d_tools"
    "description" : "Convert selected Empties to Collections",
    "category" : "USD Tools",
}


import bpy

class OBJECT_OT_create_collections_from_empties(bpy.types.Operator):
    """Converts selected empties to Collections"""
    bl_idname = "object.create_collections_from_empties"
    bl_label = "Convert Selected Empties"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_empties = [obj for obj in context.selected_objects if obj.type == 'EMPTY']

        if not selected_empties:
            self.report({'WARNING'}, "No Empties selected.")
            return {'CANCELLED'}
        
        for empty in selected_empties:
            
            objects_to_process = []
            objects_to_process.append(empty)
            
            def get_children_recursive(obj, objects_list):
                 for child in obj.children:
                     objects_list.append(child)
                     get_children_recursive(child, objects_list)
            
            get_children_recursive(empty, objects_to_process)

            for obj in objects_to_process:
                context.view_layer.objects.active = obj
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

            collection_name = empty.name
            new_collection = bpy.data.collections.new(name=collection_name)
            context.scene.collection.children.link(new_collection)

            for obj in objects_to_process:
                 if obj.users_collection:
                      for col in list(obj.users_collection):
                          col.objects.unlink(obj)
                 new_collection.objects.link(obj)

            bpy.data.objects.remove(empty, do_unlink=True)

        return {'FINISHED'}


def menu_func_outliner_object(self, context):
    if context.object: # Only show if an object is selected
       layout = self.layout
       layout.separator()  # optional separator
       layout.operator(OBJECT_OT_create_collections_from_empties.bl_idname)


def register():
    bpy.utils.register_class(OBJECT_OT_create_collections_from_empties)
    bpy.types.OUTLINER_MT_object.append(menu_func_outliner_object)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_create_collections_from_empties)
    bpy.types.OUTLINER_MT_object.remove(menu_func_outliner_object)


if __name__ == "__main__":
    register()
