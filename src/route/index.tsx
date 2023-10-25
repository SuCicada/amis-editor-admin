import React, {useEffect} from 'react';
import {ToastComponent, AlertComponent, Spinner} from 'amis';
/**
 * BrowserRouter: history 路由模式
 * HashRouter: hash 路由模式
 */
import {Route, Switch, Redirect, BrowserRouter as Router} from 'react-router-dom';
import {observer} from 'mobx-react';
import {IMainStore} from '../store/index';
// import Preview from './Preview';
// import Editor from './Editor';
// import '../renderer/MyRenderer';
// import '../renderer/my';
// import '../renderer/video_make_image_select';
// import('../renderer/table_section')
import "../renderer/index";

const Admin = React.lazy(() => import('./Admin'));
const Editor = React.lazy(() => import('./Editor'));
const Preview = React.lazy(() => import('./Preview'));
const Editor0 = React.lazy(() => import('../trash/Editor0'));

export default observer(function ({store}: {store: IMainStore}) {
    // useEffect(() => {
    //     let aa = $(".cxd-AsideNav-item")
    //     console.log('aa', aa);
    //     let bb = document.getElementsByClassName("cxd-AsideNav-item")
    //     console.log('bb', bb);
    // }, []);

    return (
    <Router>
      <div className="routes-wrapper">
        <ToastComponent key="toast" position={'top-right'} />
        <AlertComponent key="alert" />
        <React.Suspense
          fallback={<Spinner overlay className="m-t-lg" size="lg" />}
        >
          <Switch>
            <Redirect to={`/admin`} from={`/`} exact />
            <Route path="/admin" component={Admin} />
            <Route path="/edit/:id*" component={Editor} />
            <Route path="/preview" component={Preview} />
            <Route path="/edit0/:id" component={Editor0} />
          </Switch>
        </React.Suspense>
      </div>
    </Router>
  );
});
