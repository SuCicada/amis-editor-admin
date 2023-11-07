import {Renderer, RendererProps} from "amis";
import React from "react";
// @ts-ignore
import Popup from "@/libs/popup-js/popup.js";
import "@/libs/popup-js/popup.css";
import {API_HOST} from "@/config";
import Viewer from "viewerjs";
import "viewerjs/dist/viewer.css";
import {getMaterialType} from "@/utils/file";
import {inject, observer} from "mobx-react";
import {IMainStore} from "@/store";
import Image from "amis/lib/renderers/Image";
import {ClassValue} from "amis-core/lib/theme";

// let ReactDOM = amisRequire('react-dom');
function useSessionStorage(key: string, initialValue: any) {
  // 从 sessionStorage 中获取初始值，如果不存在则使用 initialValue
  const [storedValue, setStoredValue] = React.useState(() => {
    try {
      const item = window.sessionStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(error);
      return initialValue;
    }
  });

  // 在组件渲染时监听 key 的变化，并将新值存储到 sessionStorage 中
  React.useEffect(() => {
    try {
      window.sessionStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.error(error);
    }
  }, [key, storedValue]);

  // 返回存储值的状态和一个更新它的函数
  return [storedValue, setStoredValue];
}

// function video_make_image_select() {
// interface ImageVideoShowProps {
// }
function ImageVideoShow(props: {
  type: string,
  fatherDomId: string,
  imgVidId: string,
  imageOrVideo: string,
  // video?: string
}) {
  let {type, fatherDomId, imgVidId, imageOrVideo} = props
  let ImageVideoElement = (<></>)
  let clickFunction = () => {
    console.error("clickFunction not set")
  }
  console.log(type, fatherDomId, imgVidId, imageOrVideo);

  if (type === 'image') {
    let imageEleId = `ImageVideoShow-image-${fatherDomId}-${imgVidId}`
    let url = `${API_HOST}${imageOrVideo}`
    console.log("url", url)
    ImageVideoElement = (
      <img className="cxd-Image-image" id={imageEleId}
           alt={imageEleId}
           src={url}
      />
      // <Image
      //   type={"image"}
      // id={imageEleId}
      // src={"http://localhost:10930/image/08a95550065b815311a8c2656db7e7a2.jpg"}
      //        enlargeAble={true}
      // />
    )
    clickFunction = () => {
      document.getElementById(imageEleId)?.click()
    }
  }

  if (type === "video") {
    let videoEleId = `ImageVideoShow-video-${fatherDomId}-${imgVidId}`
    let url = `${API_HOST}${imageOrVideo}`
    const myPopup = new Popup({
      // id: videoEleId,
      title: "",
      // fixedHeight:true,
      // heightMultiplier:1,
      html: `<video
          id="${videoEleId}"
          controls
          preload="auto"
          width="640"
          height="360"
          src="${url}"
        ></video>`,
      hideCallback: function () {
        console.log('hide', videoEleId);
        // @ts-ignore
        document.getElementById(videoEleId).pause()
      },
      showCallback: function () {
        console.log('show', videoEleId);
        // @ts-ignore
        document.getElementById(videoEleId).play()
      },
      disableScroll: true,
    });

    ImageVideoElement = (<video
      className="cxd-Image-image"
      // className="video-js"
      preload="metadata"
      width="100%"
      height="100%"
      src={url}
    ></video>)
    clickFunction = () => {
      myPopup.show()
    }
  }


  return <React.Fragment>
    <div className="cxd-Image cxd-Image--thumb cxd-Images-item">
      <div className="cxd-Image-thumbWrap">
        <div
          style={{
            height: "27vh",
            width: "20vh",
          }}
          className="cxd-Image-thumb cxd-Image-thumb--contain cxd-Image-thumb--1-1">

          {ImageVideoElement}

        </div>
        <div className="cxd-Image-overlay" onClick={() => {
          clickFunction()
        }}>
          <a data-tooltip="查看大图" data-position="bottom"
             target="_blank">
            <svg viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"
                 className="icon icon-view">
              <path
                d="M8 3c3.989 0 7 3.873 7 5 0 .883-3.011 5-7 5-4.04 0-7-4.117-7-5 0-1.127 2.96-5 7-5Zm0 1C4.733 4 2.218 7.086 2.009 7.973 2.275 8.771 4.719 12 7.999 12c3.21 0 5.735-3.269 5.994-4.037C13.807 7.126 11.27 4 8 4ZM7.975 5.88a2 2 0 1 1 0 4 2 2 0 0 1 0-4Zm0 1a1.001 1.001 0 0 0 0 2 1.001 1.001 0 0 0 0-2Z"
                fill="currentColor" fillRule="evenodd"></path>
            </svg>
          </a>
        </div>
      </div>
      {/*<input type="radio" name={radioName} value={image_id}*/}
      {/*       className="cxd-Images-radio"*/}
      {/*       checked={is_selected}*/}
      {/*       onChange={radioOnChange}*/}
      {/*/>*/}
      {/*{radio_tag}*/}
    </div>
  </React.Fragment>
}

// 自定义组件，props 中可以拿到配置中的所有参数，比如 props.label 是 'Name'
function ImageVideoSelectComponent(props: { globalStore: IMainStore } & RendererProps) {
  let store = props.globalStore
  console.log(store.utils.fileType)
  console.log(store.utils.getMaterialType("sdasfasf.png"))
  console.log("props", props);

  // dom.current.innerHTML = props
  // 而 props 中能拿到这个
  let id = props.data.id
  // let is_selected = props.data.is_selected
  let table_image = props.data.path


  // let radio_api = props.radio_api
  // image id == column id
  let table_images = {[id]: table_image}
  let images = table_images ? table_images : {}
  let domId = `ImageVideoSelectComponent-${id}-${Date.now()}`
  let radioName = `video_make_image_select-images-radio`
  console.log(images);

  // if (preDom) {
  //     return (<React.Fragment></React.Fragment>)
  // }
  // console.log("radio_api", radio_api);
  console.log(domId);
  console.log(document.getElementById(domId))
  // let _selectedImage = sessionStorage.getItem('video_make_image_select')
  // React.useEffect(function () {
  //     console.log("set selected image:", selectedImage);
  //     // setSelectedImage(_selectedImage)
  //
  // }, [selectedImage]);

  let preDom = document.getElementById(domId)
  React.useEffect(function () {
    console.log(props);
    // if (is_selected) {
    //   sessionStorage.setItem('video_make_image_select', id)
    // }
    if (preDom) {
    }
  }, []);


  React.useEffect(function () {
    if (table_images == null) {
      return
    }
    console.log(table_images);
    // setImages(table_images)

    if (Object.keys(table_images).length > 0) {
      // console.log(domId);
      let dd = document.getElementById(domId)
      // console.log(dd);
      if (dd == null) {
        return
      }
      var _viewer = new Viewer(dd, {
        transition: false,
        // @ts-ignore
        title: function (image) {
          // @ts-ignore
          return image.alt + ' (' + (this.index + 1) + '/' + this.length + ')';
        },
      });
    }
    // console.log(_viewer);
  }, [table_image]);

  let needRender = preDom !== undefined

  // async function radioOnChange(event: React.ChangeEvent<HTMLInputElement>) {
  //   console.log(event);
  //   const selected_image_id = event.target.value;
  //   await fetch(radio_api, {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify({
  //       // id: id,
  //       selected_image: selected_image_id,
  //     })
  //   })
  //
  //   props.env.notify('success', '选择了图片')
  //   // console.log(event);
  //   // setSelectedImage(selected_image_id)
  // }

  // return (<></>)

  let html = (
    <div className="cxd-ImagesField">
      <div className="cxd-Image my-Image" id={domId}>

        {Object.keys(images).length === 0 ? (
          <div>
            图片还没有生成
          </div>
        ) : (
          <React.Fragment>
          </React.Fragment>)}

        {Object.entries(images).map(([imgVidId, path], index) => {
          // {_images.map((image, index) => {
          // image_id = index
          // image = `data:image/png;base64,${image}`
          // let {path, type} = material
          // let path
          let type = store.utils.getMaterialType(path)
          console.log(path, type);
          return (
            <ImageVideoShow
              type={type ?? ''}
              fatherDomId={domId}
              imgVidId={imgVidId}
              imageOrVideo={path}
            />)
        })}
      </div>
    </div>
  )
  // if(preDom ===undefined){
  // return ""
  // }
  return (needRender ? html : <React.Fragment></React.Fragment>)
}

let ImageVideoSelectComponentInject =
  inject('globalStore')(observer(
    // React.forwardRef(()
// React.forwardRef((props, ref) => {
    // ... 使用 ref 和 props
    // console.log(props)
    // console.log(ref)
    // return <ImageVideoSelectComponentInject {...props}/>
// })
    ImageVideoSelectComponent
  ))

Renderer({
  test: /(^|\/)ImageVideoSelect/,
  type: "ImageVideoSelect"
})(ImageVideoSelectComponentInject);
// }

// video_make_image_select()
