import {defineConfig, loadEnv, ConfigEnv, UserConfig, PluginOption} from "vite";
import react from "@vitejs/plugin-react";
import viteEasyMock from "vite-easy-mock";

import svgr from "vite-plugin-svgr";

export default defineConfig((mode: ConfigEnv): UserConfig => {
  // const env = loadEnv(mode.mode, process.cwd());
  // const viteEnv = wrapperEnv(env);
  return {
    // root: './src',  // 设置项目根目录为 ./src
    // base: './src',  // 设置基础公共路径为当前目录
    // build: {
    //   outDir: './dist',  // 设置构建输出目录为 ../dist
    //   emptyOutDir: true,  // 清空输出目录
    // },
    // base: viteEnv.VITE_BASE_URL,
    // alias config
    base: "/",
    resolve: {
      extensions: [".js", ".ts", ".tsx", ".json", "*.svg"],
      alias: [{find: "@", replacement: "/src/"}],
    },
    // global css
    css: {
      preprocessorOptions: {
        less: {
          javascriptEnabled: true,
          additionalData: `@import "@/styles/var.less";`
        }
      },
      postcss: {
        plugins: [
        ]
      }
    },
    // server config
    server: {
      host: "0.0.0.0", // The server hostname, if external access is allowed, can be set to"0.0.0.0"
      port: 58760,
      open: false,
      cors: true,
      hmr: false,
      // https: false,
      // Proxy cross-domain (mock does not need to be configured, this is just a matter)
      proxy: {
      }
    },
    optimizeDeps: {
      esbuildOptions: {
        plugins: [],
      },
      include: [
        `monaco-editor/esm/vs/language/json/json.worker`,
        `monaco-editor/esm/vs/language/css/css.worker`,
        `monaco-editor/esm/vs/language/html/html.worker`,
        `monaco-editor/esm/vs/language/typescript/ts.worker`,
        `monaco-editor/esm/vs/editor/editor.worker`
      ],
    },
    // plugins
    plugins: [
      viteEasyMock(),
      // visualizer({ open: true }),
      svgr({
        exportAsDefault: true,
        svgrOptions: {
          svgProps: {
            className: 'icon'
          },
          prettier: false,
          dimensions: false
        }
      }),
      // exportAsDefault: true
      react(),
    ],
    build: {
      target: "es2015",
      outDir: "dist",
      // esbuild Packaging is faster, but cannot remove console.log, remove console and use terser mode
      minify: "esbuild",
      rollupOptions: {
        // input: {
        //   app: './src/index.html', // default
        // },
        output: {
          // Enable parallel builds
          manualChunks: undefined,
        }
      }
    }
  };
});
