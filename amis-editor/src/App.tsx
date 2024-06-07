import React from 'react';
import {Provider} from 'mobx-react';
import {toast, alert, confirm, attachmentAdpator} from 'amis';
import axios from 'axios';
import {MainStore} from './store/index';
import RootRoute from './route/index';
import copy from 'copy-to-clipboard';
import {types, getEnv} from 'mobx-state-tree';

export default function (): JSX.Element {
  const store = ((window as any).store = MainStore.create(
    {
    },
    {
      fetcher: async({url, method, data, config, headers}: any) => {
        config = config || {};
        config.headers = config.headers || headers || {};
        config.withCredentials = false;

        if (method !== 'post' && method !== 'put' && method !== 'patch') {
          if (data) {
            config.params = data;
          }
          return (axios as any)[method](url, config);
        } else if (data && data instanceof FormData) {
          // config.headers = config.headers || {};
          // config.headers['Content-Type'] = 'multipart/form-data';
        } else if (
          data &&
          typeof data !== 'string' &&
          !(data instanceof Blob) &&
          !(data instanceof ArrayBuffer)
        ) {
          data = JSON.stringify(data);
          config.headers['Content-Type'] = 'application/json';
        }
        console.log('config', config);
        console.log('data', typeof data, data);
        if (method === "post" || method === "put" || method === "patch") {
          if (data && typeof data === 'string') {
            data = JSON.parse(data);
          }
        }
        config.headers = headers
          ? {...config.headers, ...headers}
          : config.headers ?? {};
        config.method = method;
        config.data = data;
        config.url = url;

        // return (axios as any)[method](url, data, config);
        // let response = await axios(config);
        // let response = (axios as any)[method](url, data, config);
        let response = await axios(config);
        response = await attachmentAdpator(response, (msg: string) => '');
        return response;
      },
      isCancel: (e: any) => axios.isCancel(e),
      notify: (type: 'success' | 'error' | 'info', msg: string, conf: any) => {
        // type === 'error' ? '系统错误' : '系统消息'
        toast[type]
          ? toast[type](msg, conf)
          : console.warn('[Notify]', type, msg);
        console.log('[notify]', type, msg);
      },
      alert,
      confirm,
      copy: (contents: string, options: any = {}) => {
        const ret = copy(contents, options);
        ret &&
        (!options || options.shutup !== true) &&
        toast.info('内容已拷贝到剪切板');
        return ret;
      }
    }
  ));

  return (
    <Provider store={store} globalStore={store}>
      <RootRoute store={store} />
    </Provider>
  );
}
