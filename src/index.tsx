/**
 * @file entry of this example.
 */
import * as React from 'react';
import ReactDOM from 'react-dom';
import App from './App';
import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/css/v4-shims.css';
import 'amis/lib/themes/cxd.css';
import 'amis/lib/helper.css';
import 'amis/sdk/iconfont.css';
import 'amis-editor-core/lib/style.css';
import './scss/style.scss';
import {setDefaultTheme} from 'amis';
import {setThemeConfig} from 'amis-editor-core';
import themeConfig from 'amis-theme-editor-helper/lib/systemTheme/cxd';

// import * as dotenv from 'dotenv';
// dotenv.config();
// import "/Users/peng/PROGRAM/GitHub/amis-admin/public/my.js";
// import * as my from "./custom/my"
//     my.custom()
// try {
//     let my = require('./custom/my');
// } catch (e) {
//     console.log(e);
// }
// let my = require('./my');
self.MonacoEnvironment = {
  getWorker: async function (workerId, label) {
    switch (label) {
      case 'json': {
        // @ts-ignore
        const jsonWorker = (await import('monaco-editor/esm/vs/language/json/json.worker?worker')).default;
        return jsonWorker();
      }
      case 'css':
      case 'scss':
      case 'less': {
        // @ts-ignore
        const cssWorker = (await import("monaco-editor/esm/vs/language/css/css.worker?worker")).default;
        return cssWorker();
      }
      case 'html':
      {
        // @ts-ignore
        const htmlWorker = (await import('monaco-editor/esm/vs/language/html/html.worker?worker')).default;
        return htmlWorker();
      }
      case 'typescript':
      case 'javascript': {
        // @ts-ignore
        const tsWorker = (await import('monaco-editor/esm/vs/language/typescript/ts.worker?worker')).default;
        return tsWorker();
      }
      default: {
        // @ts-ignore
        const EditorWorker = (await import('monaco-editor/esm/vs/editor/editor.worker?worker')).default;
        return EditorWorker();
      }
    }
  }
};

setDefaultTheme('cxd');
setThemeConfig(themeConfig);

// react < 18
ReactDOM.render(<App/>, document.getElementById('root'));
