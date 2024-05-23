import {defineConfig, loadEnv, ConfigEnv, UserConfig, PluginOption} from "vite";
import react from "@vitejs/plugin-react";
import svgr from "vite-plugin-svgr";
import path from "path";


// import viteEasyMock from "vite-easy-mock";
// import viteCompression from "vite-plugin-compression";
// import MonacoWebpackPlugin from "monaco-editor-webpack-plugin";
// import monacoEditorPlugin from 'vite-plugin-monaco-editor';
import monacoEditorPlugin from 'vite-plugin-monaco-editor';

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
    // base: "http://localhost:8000",
    // alias config
    base: "/",
    resolve: {
      extensions: [".js", ".ts", ".tsx", ".json", "*.svg"],
      // alias: [{find: "@", replacement: "./src/"}],
      alias: {
        '@': path.resolve(__dirname, 'src'), // 添加path并使用path.resolve确保路径正确
      }
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
        plugins: []
      }
    },
    // server config
    server: {
      host: "0.0.0.0", // The server hostname, if external access is allowed, can be set to"0.0.0.0"
      port: 58760,
      open: false,
      cors: true,
      // hmr: false,
      hmr: true,
      // https: false,
      // Proxy cross-domain (mock does not need to be configured, this is just a matter)
      proxy: {}
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
      monacoEditorPlugin({
        // 你可以在这里配置需要的语言和其他选项
        languageWorkers: ['editorWorkerService', 'css', 'html', 'json', 'typescript']
      }),
      // viteEasyMock(),
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

      // viteCompression({
      //     verbose: true,
      //     disable: false,
      //     threshold: 10240,
      //     algorithm: 'gzip',
      //     ext: '.gz',
      //     deleteOriginFile: true
      // })
    ],
    build: {
      target: "es2015",
      outDir: "./dist",
      emptyOutDir: true,  // 清空输出目录
      // esbuild Packaging is faster, but cannot remove console.log, remove console and use terser mode
      minify: "esbuild",
      rollupOptions: {
        // input: {
        //   main: './src/index.html',
        //   app: './src/index.tsx', // default
        // },
        output: {
          // Enable parallel builds
          manualChunks: undefined,
          chunkFileNames: 'js/[name]-[hash].js',  // 引入文件名的名称
          entryFileNames: 'js/[name]-[hash].js',  // 包的入口文件名称
          assetFileNames: 'assets/[name]-[hash].[ext]' // 资源文件像 字体，图片等
        }
      },
      // terserOptions: {
      //   compress: {
      //     drop_console: true,
      //     drop_debugger: true
      //   },
      // },
      sourcemap: false,
    }
  };
});
