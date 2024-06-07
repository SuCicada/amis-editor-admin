import {applySnapshot, flow, types} from "mobx-state-tree";
import {API_HOST} from "@/config";
import * as path from "path";
export const DefaultUtilsStore = {fileType: {}}
export const UtilsStore = types
  .model('utils', {
    fileType: types.frozen(types.model({
      image: types.array(types.string), // You can replace types.frozen() with a more specific type if needed
      video: types.array(types.string)  // Same here
    }))
    // id: types.identifier,
    // icon: '',
    // path: '',
    // label: '',
    // schema: types.frozen({})
  })
  // .views(self => ({}))
  .actions(self => {
    // function updateSchema(schema: any) {
    //   self.schema = schema;
    //   console.log('updateSchema', schema);
    // }
    // function setFileType(fileType: any) {
    //   self.fileType = fileType
    // }
    function getMaterialType(file: string) {
      if(!file) return null
      let file_extension = file.split('.').pop();
      if (!file_extension) return null
      // file_extension = file_extension.slice(1);

      if (self.fileType.video?.includes(file_extension)) return  'video'
      if (self.fileType.image?.includes(file_extension)) return  'image'
      return null
    }

    const loadFileType = flow(function* loadFileType() {
      try {
        console.log(`${API_HOST}/api/settings/file_type`)
        const response:any = yield fetch(`${API_HOST}/api/settings/file_type`);
        const data = yield response.json();
        self.fileType = data.data; // Assign the data directly to fileType
        console.log(data);
      } catch (error) {
        console.error("Failed to load file types", error);
      }
    });
    return {
      getMaterialType,
      async afterCreate() {
        // let response = await fetch(`${API_HOST}/api/settings/file_type`)
        // const data = await response.json();
        // applySnapshot(self.fileType, data)
        // console.log(data)
        await loadFileType();
        // setFileType(data)
      }
      // updateSchema
    };
  });

export type IUtilsStore = typeof UtilsStore.Type;
