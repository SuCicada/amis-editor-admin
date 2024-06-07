import React, {useEffect} from 'react';
import {Editor, ShortcutKey} from 'amis-editor';
import {inject, observer} from 'mobx-react';
import {RouteComponentProps, useParams} from 'react-router-dom';
import {toast, Select, SchemaObject} from 'amis';
import {currentLocale} from 'i18n-runtime';
import {Icon} from '../icons/index';
import {IMainStore} from '../store';
import '../editor/DisabledEditorPlugin'; // 用于隐藏一些不需要的Editor预置组件
import {API_HOST} from '../config';
import _ from "lodash";
import '../renderer/MyRenderer';
import MyRendererPlugin from '../editor/MyRenderer';
import ImageVideoSelect from '../editor/ImageVideoSelect';
const plugins = [MyRendererPlugin,ImageVideoSelect];
let currentIndex = -1;

let host = `${window.location.protocol}//${window.location.host}`;

// 如果在 gh-pages 里面
if (/^\/amis-editor-demo/.test(window.location.pathname)) {
  host += '/amis-editor';
}

const schemaUrl = `${host}/schema.json`;

const editorLanguages = [
  {
    label: '简体中文',
    value: 'zh-CN'
  },
  {
    label: 'English',
    value: 'en-US'
  }
];

export default inject('store')(
  observer(function (
    {
      store,
      location,
      history,
      match
    }: { store: IMainStore } & RouteComponentProps<{ id: string }>) {
    let [schema, setSchema] = React.useState<SchemaObject>(null as any)
    let [loadOver, setLoadOver] = React.useState(false)
    const id = match.params.id;
    // const {id} = useParams();
    // console.log(match)
    // console.log(params)


    useEffect(() => {
      (async function () {
        let response = await fetch(`${API_HOST}/pages/schema/${id}`)
        let _schema = await response.json()
        setSchema(_schema)
        toast.success('加载成功', '提示');
        setLoadOver(true)
      })()
    }, []);

    const index: number = parseInt(match.params.id, 10);
    const curLanguage = currentLocale(); // 获取当前语料类型

    if (index !== currentIndex) {
      currentIndex = index;
      // store.updateSchema(store.pages[index].schema);

    }

    async function saveToServer(_schema: any = {}) {
      // console.log('_schema', _schema);
      if (!loadOver) {
        return
      }
      if (!_schema || _.isEmpty(_schema)) {
        return
      }
      await fetch(`${API_HOST}/pages/schema/${id}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(_schema)
      }).then(response => {
        let conf = {
          position: 'top-left',
        }
        if (response.ok) {
          toast.success('保存成功', conf);
        } else {
          toast.error('保存失败', conf);
        }
      })
    }

    useEffect(() => {
      // if (schema && !_.isEmpty(schema)){
      saveToServer(schema)
      // }
    }, [schema])

    async function save() {
      await saveToServer(schema)
      store.updatePageSchemaAt(id);
      // store.notify('success', '保存成功', {
      // toast.success('保存成功111',{
      //   // position: 'top-center',
      //   position: 'top-left',
      //   className: "theme-toast-action-scope",
      //   closeButton: false,
      // });
    }

    function onChange(value: any) {
      if (_.isEqual(value, schema)) {
        return
      }
      setSchema(value)
      store.updateSchema(value);
      store.updatePageSchemaAt(id);
    }

    function changeLocale(value: string) {
      localStorage.setItem('suda-i18n-locale', value);
      window.location.reload();
    }

    function exit() {
      // history.push(`/${store.pages[index].path}`);
      history.push(`/admin/${id}`);
    }

    let editor = (
      <div className="Editor-Demo">
        <div className="Editor-header">
          <div className="Editor-title">amis 可视化编辑器</div>
          <div className="Editor-view-mode-group-container">
            <div className="Editor-view-mode-group">
              <div
                className={`Editor-view-mode-btn editor-header-icon ${
                  !store.isMobile ? 'is-active' : ''
                }`}
                onClick={() => {
                  store.setIsMobile(false);
                }}
              >
                <Icon icon="pc-preview" title="PC模式"/>
              </div>
              <div
                className={`Editor-view-mode-btn editor-header-icon ${
                  store.isMobile ? 'is-active' : ''
                }`}
                onClick={() => {
                  store.setIsMobile(true);
                }}
              >
                <Icon icon="h5-preview" title="移动模式"/>
              </div>
            </div>
          </div>

          <div className="Editor-header-actions">
            <ShortcutKey/>
            <Select
              className="margin-left-space"
              options={editorLanguages}
              value={curLanguage}
              clearable={false}
              onChange={(e: any) => changeLocale(e.value)}
            />
            <div
              className={`header-action-btn m-1 ${
                store.preview ? 'primary' : ''
              }`}
              onClick={() => {
                store.setPreview(!store.preview);
              }}
            >
              {store.preview ? '编辑' : '预览'}
            </div>
            {!store.preview && (
              <div className={`header-action-btn exit-btn`} onClick={exit}>
                退出
              </div>
            )}
          </div>
        </div>
        <div className="Editor-inner">
          <Editor
            plugins={plugins}
            theme={'cxd'}
            preview={store.preview}
            isMobile={store.isMobile}
            value={schema}
            onChange={onChange}
            onPreview={() => {
              store.setPreview(true);
            }}
            onSave={save}
            className="is-fixed"
            $schemaUrl={schemaUrl}
            showCustomRenderersPanel={true}
            amisEnv={{
              fetcher: store.fetcher,
              notify: store.notify,
              alert: store.alert,
              copy: store.copy
            }}
            ctx={{
              API_HOST: API_HOST,
            }}
          />
        </div>
      </div>
    );
    if (schema && !_.isEmpty(schema)) {
      return editor
    } else {
      return <h1 style={{
        display: "flex",
        justifyContent: 'center'
      }}>等等🙏，疯狂生成中</h1>
    }
  })
);
