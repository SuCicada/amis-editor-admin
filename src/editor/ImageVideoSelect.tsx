import React from 'react';
// import {RendererEditor, BasicEditor} from 'amis-editor';
import {BasePlugin} from 'amis-editor';

// @RendererEditor('my-renderer', {
// })
export default class ImageVideoSelectEditor extends BasePlugin {
  rendererName = 'ImageVideoSelect';
  name= 'ImageVideoSelect';
  description= 'ImageVideoSelect';
  // docLink: '/docs/renderers/Nav',
  // type: 'my-renderer';
  // previewSchema={
  //   // 用来生成预览图的
  //   type: 'video_make_image_select',
  //   // target: 'demo'
  // }
  scaffold={
    // 拖入组件里面时的初始数据
    type: 'video_make_image_select',
    // target: '233'
  };
  panelTitle = 'ImageVideoSelect';
  // tipName = '自定义组件';
  panelBody = [{
    // settingsSchema = {
    title: 'ImageVideoSelect',
    body: [
      {
        type: 'ImageVideoSelect',
      }
    ]
  }];

}
