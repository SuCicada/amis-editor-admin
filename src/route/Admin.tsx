import React, {useEffect} from 'react';
import {observer, inject} from 'mobx-react';
import {IMainStore} from '../store';
import {Button, AsideNav, Layout, confirm} from 'amis';
import {RouteComponentProps, matchPath, Switch, Route} from 'react-router';
import {Link, Redirect} from 'react-router-dom';
import NotFound from './NotFound';
import {API_HOST} from "@/config";
import {AppPage, AppSchema} from "amis/lib/renderers/App";
import AdminPreview from "@/route/AdminPreview";

function isActive(link: any, location: any) {
  const ret = matchPath(location?.pathname, {
    path: link ? link.replace(/\?.*$/, '') : '',
    exact: true,
    strict: true
  });

  return !!ret;
}

export default inject('store')(
  observer(function ({
                       store,
                       location,
                       history
                     }: { store: IMainStore } & RouteComponentProps) {
    let [pages, setPages] = React.useState<AppPage[]>([])
    useEffect(() => {
      (async () => {
        let response = await fetch(`${API_HOST}/pages/site.json`)
        let data = await response.json()
        let appSchema: AppSchema = data.data
        let _pages = appSchema.pages

        if (_pages) {
          if (!Array.isArray(_pages)) {
            // setPages([_pages])
            _pages = [_pages]
          }
          // _pages.forEach((item: AppPage) => {
          for (let item of _pages) {
            if (item.children) {
              setPages(item.children)
              return
            }
          }
        }
      })()
    }, [])


    function renderHeader() {
      return (
        <>
          <div className={`cxd-Layout-brandBar`}>
            <div className="cxd-Layout-brand text-ellipsis">
              <i className="fa fa-paw"></i>
              <span className="hidden-folded m-l-sm">AMIS 示例</span>
            </div>
          </div>
          <div className={`cxd-Layout-headerBar`}>
            <div className="hidden-xs p-t-sm ml-auto px-2">
              <Button size="sm" className="m-r-xs" level="success" disabled>
                全部导出
              </Button>
              <Button
                size="sm"
                level="info"
                onClick={() => store.setAddPageIsOpen(true)}
              >
                新增页面
              </Button>
            </div>
          </div>
        </>
      );
    }

    function renderAside() {
      // console.log('store.pages', store);
      // console.log('location', location);

      const navigations = pages.map(item => ({
        label: item.label,
        path: `/admin${item.url}`,
        icon: item.icon,
        url: item.url
        // name:
      }));

      // const paths = {}
      // pages.forEach(item=>{
      //   paths[item.url] = item.
      // })
      // console.log('store.asideFolded', store.asideFolded);
      return (
        <AsideNav
          key={store.asideFolded ? 'folded-aside' : 'aside'}
          navigations={[
            {
              label: '导航',
              children: navigations
            }
          ]}
          renderLink={({link, toggleExpand, classnames: cx, depth}: any) => {
            // 这个link和navigations内容一样的

            // console.log(link)
            if (link.hidden) {
              return null;
            }

            let children = [];

            if (link.children) {
              children.push(
                <span
                  key="expand-toggle"
                  className={cx('AsideNav-itemArrow')}
                  onClick={e => toggleExpand(link, e)}
                ></span>
              );
            }

            link.badge &&
            children.push(
              <b
                key="badge"
                className={cx(
                  `AsideNav-itemBadge`,
                  link.badgeClassName || 'bg-info'
                )}
              >
                {link.badge}
              </b>
            );

            if (link.icon) {
              children.push(
                <i key="icon" className={cx(`AsideNav-itemIcon`, link.icon)}/>
              );
            } else if (store.asideFolded && depth === 1) {
              children.push(
                <i
                  key="icon"
                  className={cx(
                    `AsideNav-itemIcon`,
                    link.children ? 'fa fa-folder' : 'fa fa-info'
                  )}
                />
              );
            }

            // link.active ||
            // children.push(
            //   <i
            //     key="delete"
            //     data-tooltip="删除"
            //     data-position="bottom"
            //     className={'navbtn fa fa-times'}
            //     onClick={(e: React.MouseEvent) => {
            //       e.preventDefault();
            //       confirm('确认要删除').then(confirmed => {
            //         confirmed && store.removePageAt(paths.indexOf(link.path));
            //       });
            //     }}
            //   />
            // );

            children.push(
              <i
                key="edit"
                data-tooltip="编辑"
                data-position="bottom"
                className={'navbtn fa fa-pencil'}
                onClick={(e: React.MouseEvent) => {
                  e.preventDefault();
                  history.push(`/edit${link.url}`);
                }}
              />
            );

            children.push(
              <span key="label" className={cx('AsideNav-itemLabel')}>
                {link.label}
              </span>
            );

            return link.path ? (
              link.active ? (
                <a>{children}</a>
              ) : (
                // @ts-ignore
                <Link to={link.path[0] === '/' ? link.path : `${link.path}`}>
                  {children}
                </Link>
              )
            ) : (
              <a
                onClick={
                  link.onClick
                    ? link.onClick
                    : link.children
                      ? () => toggleExpand(link)
                      : undefined
                }
              >
                {children}
              </a>
            );
          }}
          isActive={(link: any) =>
            isActive(
              link.path && link.path[0] === '/' ? link.path : `${link.path}`,
              location
            )
          }
        />
      );
    }

    function handleConfirm(value: { label: string; icon: string; path: string }) {
      store.addPage({
        ...value,
        schema: {
          type: 'page',
          title: value.label,
          body: '这是你刚刚新增的页面。'
        }
      });
      store.setAddPageIsOpen(false);
    }

    // console.log('store.pages', store.pages);

    return (
      <Layout
        aside={renderAside()}
        header={renderHeader()}
        folded={store.asideFolded}
        offScreen={store.offScreen}
      >
        <Switch>
          {pages.length > 0 && (
          <Redirect to={`/admin${pages[0].url}`} from={`/admin`} exact />
          )}

          {pages.map((item: AppPage) => {
            // console.log('item', item);
            return (
              <Route
                key={item.label}
                path={`/admin${item.url}`}
                render={() => <AdminPreview schemaApi={item.schemaApi}/>}
              />
            )
          })}
          <Route component={NotFound}/>
        </Switch>
        {/*<AddPageModal*/}
        {/*  show={store.addPageIsOpen}*/}
        {/*  onClose={() => store.setAddPageIsOpen(false)}*/}
        {/*  onConfirm={handleConfirm}*/}
        {/*  pages={store.pages.concat()}*/}
        {/*/>*/}
      </Layout>
    );
  })
)
