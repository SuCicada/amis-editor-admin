import React, {useEffect, useRef} from 'react';

import '@fortawesome/fontawesome-free/css/all.css';
import '@fortawesome/fontawesome-free/css/v4-shims.css';

import 'amis/lib/themes/cxd.css';
import 'amis/lib/helper.css';
import 'amis/sdk/iconfont.css';
import axios from 'axios';
import copy from 'copy-to-clipboard';

import {render as renderAmis, ToastComponent, AlertComponent} from 'amis';
import {alert, confirm, toast} from 'amis-ui';
import {inject, observer} from "mobx-react";
import {IMainStore} from "./store";
import {RouteComponentProps} from "react-router";
import ReactDOM from 'react-dom';
import {API_HOST} from "@/config";

const AMISComponent = (
  {
    store,
    location,
    history
  }: { store: IMainStore } & RouteComponentProps
) => {
  console.log(history)

// amis 环境配置
  const env = {
    // 下面三个接口必须实现
    fetcher: ({
                url, // 接口地址
                method, // 请求方法 get、post、put、delete
                data, // 请求数据
                responseType,
                config, // 其他配置
                headers // 请求头
              }: any) => {
      config = config || {};
      config.withCredentials = true;
      responseType && (config.responseType = responseType);

      if (config.cancelExecutor) {
        config.cancelToken = new (axios as any).CancelToken(
          config.cancelExecutor
        );
      }

      config.headers = headers || {};

      if (method !== 'post' && method !== 'put' && method !== 'patch') {
        if (data) {
          config.params = data;
        }
        return (axios as any)[method](url, config);
      } else if (data && data instanceof FormData) {
        config.headers = config.headers || {};
        config.headers['Content-Type'] = 'multipart/form-data';
      } else if (
        data &&
        typeof data !== 'string' &&
        !(data instanceof Blob) &&
        !(data instanceof ArrayBuffer)
      ) {
        data = JSON.stringify(data);
        config.headers = config.headers || {};
        config.headers['Content-Type'] = 'application/json';
      }

      return (axios as any)[method](url, data, config);
    },
    isCancel: (value: any) => (axios as any).isCancel(value),
    copy: (content: string) => {
      copy(content);
      toast.success('内容已复制到粘贴板');
    },


    // 后面这些接口可以不用实现

    // 默认是地址跳转
    // jumpTo: (
    //     location: string /*目标地址*/,
    //     action: any /* action对象*/
    // ) => {
    //     // 用来实现页面跳转, actionType:link、url 都会进来。
    //     if (location)
    //         console.log('location', location);
    //     console.log('action', action);
    //     if (location.startsWith("/gen")) {
    //         location = "/admin" + location
    //         console.log(history)
    //         history.push(location)
    //     }
    // },

    // updateLocation: (
    //   location: string /*目标地址*/,
    //   replace: boolean /*是replace，还是push？*/
    // ) => {
    //   // 地址替换，跟 jumpTo 类似
    // },

    // isCurrentUrl: (
    //   url: string /*url地址*/,
    // ) => {
    //   // 用来判断是否目标地址当前地址
    // },

    // notify: (
    //   type: 'error' | 'success' /**/,
    //   msg: string /*提示内容*/
    // ) => {
    //   toast[type]
    //     ? toast[type](msg, type === 'error' ? '系统错误' : '系统消息')
    //     : console.warn('[Notify]', type, msg);
    // },
    // alert,
    // confirm,
  };

// class AMISComponentmy extends React.Component<any, any> {
//   render() {
  const myRef = useRef(null);

  // function aa() {
  //     // 定义观察器回调函数
  //     const observerCallback = (mutations: MutationRecord[], observer: MutationObserver) => {
  //         for (const mutation of mutations) {
  //             if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
  //                 // 这里可以处理元素出现后的逻辑
  //                 console.log('cxd-AsideNav-item 出现了');
  //                 console.log('mutation', mutation);
  //                 // 停止观察
  //                 observer.disconnect();
  //
  //                 mutation.addedNodes.forEach((node) => {
  //                     let urlPath = node.getElementsByTagName("a")[0].pathname
  //                     console.log('node', node);
  //                 })
  //             }
  //         }
  //     };
  //
  //     // 创建 MutationObserver 实例
  //     const observer = new MutationObserver(observerCallback);
  //
  //     // 监听根节点（你的组件的父元素）
  //     // let bb = document.getElementsByClassName("cxd-AsideNav-list")
  //     let bb = document.querySelector(".cxd-AsideNav-list") as HTMLUListElement
  //     // const rootElement = document.getElementById('root'); // 你的根元素的 ID
  //     // Array.from(bb).forEach((bb) => {
  //     observer.observe(bb, {childList: true, subtree: true});
  //     // })
  //
  //     // 在组件卸载时停止观察
  //     return () => {
  //         observer.disconnect();
  //     };
  // }
  useEffect(() => {
    // setTimeout(() => {
    let timer = setInterval(() => {
      console.log(document.querySelectorAll(".cxd-AsideNav-list .cxd-AsideNav-item"))
      let success = modifyAsideNav()
      if (success) {
        clearInterval(timer);
      }
    }, 500)
    return () => {
      clearInterval(timer);
    }
  }, []);

  function modifyAsideNav() {
    const element = myRef.current as unknown as HTMLElement;
    let success=false;
    if (element) {
      console.log('element', element);
      let list = element.querySelectorAll(".cxd-AsideNav-list .cxd-AsideNav-item")
      console.log('list', list);
      console.log(element.getElementsByClassName("cxd-AsideNav-item"));
      list.forEach((item) => {
        let aDom = item.getElementsByTagName("a")[0]
        let urlPath = aDom.pathname
        console.log('urlPath', urlPath);
        let edit = (
          <i data-tooltip="编辑" data-position="bottom" className="navbtn fa fa-pencil"
             onClick={(e) => {
               let arr = urlPath.split("/")
               let name = arr[arr.length-1]
               console.log('urlPath', urlPath,name);
                history.push(`/edit/${name}`)
             }}
          ></i>
        )
        let container = document.createElement("span")
        ReactDOM.render(edit, container)
        console.log('container', container);
        aDom.appendChild(container)
        success = true
      })
      // let list = element.getElementsByClassName("cxd-AsideNav-list")
      // list.
      // console.log('a', a);
    }
      return success
  }

  useEffect(() => {
    modifyAsideNav()
  }, [myRef.current]);
  // useEffect(() => {
  //     let aa = $(".cxd-AsideNav-item")
  //     console.log('aa', aa);
  //     console.log('bb.length', bb.length);
  //     for (let i = 0; i < bb.length; i++) {
  //         let element = bb[i];
  //         console.log('element', element);
  //     }
  //     console.log('bb', bb);
  // }, [bb]);
  const app = {
    type: 'app',
    brandName: 'Admin',
    logo: `${API_HOST}/public/logo.png`,
    header: {
      type: 'tpl',
      inline: false,
      className: 'w-full',
      tpl: '<div class="flex justify-between"><div>顶部区域左侧</div><div>顶部区域右侧</div></div>'
    },
    footer: '<div class="p-2 text-center bg-light">底部区域</div>',
    asideBefore: '<div class="p-2 text-center">菜单前面区域</div>',
    asideAfter: '<div class="p-2 text-center">菜单后面区域</div>',
    api: `${API_HOST}/pages/site.json`
  };
  // const history = History.createHashHistory();
  // history.listen(state => {
  //   console.log('state', state);
  // amisInstance.updateProps({
  //   location: state.location || state
  // });
  // });
  let res = renderAmis(
    // 这里是 amis 的 Json 配置。
    app,
    {
      "type": "page"
      // props...
    },
    env
  );
  // }
  return (<span ref={myRef}>{res}</span>);
}
export default inject('store')(
  observer(function (props: { store: IMainStore } & RouteComponentProps) {
// class APP extends React.Component<any, any> {
//   render() {
//         history.listen(state => {
//             console.log('state', state);
//         });
    console.log(props)

    return (
      <>
        {/*<ToastComponent key="toast" position={'top-right'}/>*/}
        {/*<AlertComponent key="alert"/>*/}
        {/*<AMISComponentmy/>*/}
        <AMISComponent {...props} />
      </>
    );
    // }
  }));

// export default APP;
