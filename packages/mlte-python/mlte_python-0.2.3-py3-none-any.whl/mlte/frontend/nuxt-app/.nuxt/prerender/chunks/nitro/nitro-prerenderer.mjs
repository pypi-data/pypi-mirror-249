globalThis._importMeta_=globalThis._importMeta_||{url:"file:///_entry.js",env:process.env};import 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/node-fetch-native/dist/polyfill.mjs';
import { defineEventHandler, handleCacheHeaders, isEvent, createEvent, getRequestHeader, splitCookiesString, eventHandler, setHeaders, sendRedirect, proxyRequest, setResponseStatus, setResponseHeader, send, getRequestHeaders, removeResponseHeader, createError, getResponseHeader, createApp, createRouter as createRouter$1, toNodeListener, fetchWithEvent, lazyEventHandler } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/h3/dist/index.mjs';
import { createFetch as createFetch$1, Headers as Headers$1 } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/ofetch/dist/node.mjs';
import destr from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/destr/dist/index.mjs';
import { createCall, createFetch } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/unenv/runtime/fetch/index.mjs';
import { createHooks } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/hookable/dist/index.mjs';
import { snakeCase } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/scule/dist/index.mjs';
import { klona } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/klona/dist/index.mjs';
import defu, { defuFn } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/defu/dist/defu.mjs';
import { hash } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/ohash/dist/index.mjs';
import { parseURL, withoutBase, joinURL, getQuery, withQuery, decodePath, withLeadingSlash, withoutTrailingSlash } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/ufo/dist/index.mjs';
import { createStorage, prefixStorage } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/unstorage/dist/index.mjs';
import unstorage_47drivers_47fs from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/unstorage/drivers/fs.mjs';
import unstorage_47drivers_47memory from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/unstorage/drivers/memory.mjs';
import unstorage_47drivers_47lru_45cache from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/unstorage/drivers/lru-cache.mjs';
import unstorage_47drivers_47fs_45lite from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/unstorage/drivers/fs-lite.mjs';
import { toRouteMatcher, createRouter } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/radix3/dist/index.mjs';
import { promises } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'file:///home/kad/dev/mlte/mlte/frontend/nuxt-app/node_modules/pathe/dist/index.mjs';

const inlineAppConfig = {
  "nuxt": {}
};



const appConfig = defuFn(inlineAppConfig);

const _inlineRuntimeConfig = {
  "app": {
    "baseURL": "/",
    "buildAssetsDir": "/_nuxt/",
    "cdnURL": ""
  },
  "nitro": {
    "envPrefix": "NUXT_",
    "routeRules": {
      "/__nuxt_error": {
        "cache": false
      },
      "/api/**": {
        "proxy": {
          "to": "http://localhost:8080/api/**",
          "_proxyStripBase": "/api"
        }
      },
      "/_nuxt/**": {
        "headers": {
          "cache-control": "public, max-age=31536000, immutable"
        }
      }
    }
  },
  "public": {}
};
const ENV_PREFIX = "NITRO_";
const ENV_PREFIX_ALT = _inlineRuntimeConfig.nitro.envPrefix ?? process.env.NITRO_ENV_PREFIX ?? "_";
const _sharedRuntimeConfig = _deepFreeze(
  _applyEnv(klona(_inlineRuntimeConfig))
);
function useRuntimeConfig(event) {
  if (!event) {
    return _sharedRuntimeConfig;
  }
  if (event.context.nitro.runtimeConfig) {
    return event.context.nitro.runtimeConfig;
  }
  const runtimeConfig = klona(_inlineRuntimeConfig);
  _applyEnv(runtimeConfig);
  event.context.nitro.runtimeConfig = runtimeConfig;
  return runtimeConfig;
}
_deepFreeze(klona(appConfig));
function _getEnv(key) {
  const envKey = snakeCase(key).toUpperCase();
  return destr(
    process.env[ENV_PREFIX + envKey] ?? process.env[ENV_PREFIX_ALT + envKey]
  );
}
function _isObject(input) {
  return typeof input === "object" && !Array.isArray(input);
}
function _applyEnv(obj, parentKey = "") {
  for (const key in obj) {
    const subKey = parentKey ? `${parentKey}_${key}` : key;
    const envValue = _getEnv(subKey);
    if (_isObject(obj[key])) {
      if (_isObject(envValue)) {
        obj[key] = { ...obj[key], ...envValue };
      }
      _applyEnv(obj[key], subKey);
    } else {
      obj[key] = envValue ?? obj[key];
    }
  }
  return obj;
}
function _deepFreeze(object) {
  const propNames = Object.getOwnPropertyNames(object);
  for (const name of propNames) {
    const value = object[name];
    if (value && typeof value === "object") {
      _deepFreeze(value);
    }
  }
  return Object.freeze(object);
}
new Proxy(/* @__PURE__ */ Object.create(null), {
  get: (_, prop) => {
    console.warn(
      "Please use `useRuntimeConfig()` instead of accessing config directly."
    );
    const runtimeConfig = useRuntimeConfig();
    if (prop in runtimeConfig) {
      return runtimeConfig[prop];
    }
    return void 0;
  }
});

const serverAssets = [{"baseName":"server","dir":"/home/kad/dev/mlte/mlte/frontend/nuxt-app/server/assets"}];

const assets$1 = createStorage();

for (const asset of serverAssets) {
  assets$1.mount(asset.baseName, unstorage_47drivers_47fs({ base: asset.dir }));
}

const storage = createStorage({});

storage.mount('/assets', assets$1);

storage.mount('internal:nuxt:prerender', unstorage_47drivers_47memory({"driver":"memory"}));
storage.mount('internal:nuxt:prerender:island', unstorage_47drivers_47lru_45cache({"driver":"lruCache","max":1000}));
storage.mount('internal:nuxt:prerender:payload', unstorage_47drivers_47lru_45cache({"driver":"lruCache","max":1000}));
storage.mount('data', unstorage_47drivers_47fs_45lite({"driver":"fsLite","base":"/home/kad/dev/mlte/mlte/frontend/nuxt-app/.data/kv"}));
storage.mount('root', unstorage_47drivers_47fs({"driver":"fs","readOnly":true,"base":"/home/kad/dev/mlte/mlte/frontend/nuxt-app","ignore":["**/node_modules/**","**/.git/**"]}));
storage.mount('src', unstorage_47drivers_47fs({"driver":"fs","readOnly":true,"base":"/home/kad/dev/mlte/mlte/frontend/nuxt-app/server","ignore":["**/node_modules/**","**/.git/**"]}));
storage.mount('build', unstorage_47drivers_47fs({"driver":"fs","readOnly":false,"base":"/home/kad/dev/mlte/mlte/frontend/nuxt-app/.nuxt","ignore":["**/node_modules/**","**/.git/**"]}));
storage.mount('cache', unstorage_47drivers_47fs({"driver":"fs","readOnly":false,"base":"/home/kad/dev/mlte/mlte/frontend/nuxt-app/.nuxt/cache","ignore":["**/node_modules/**","**/.git/**"]}));

function useStorage(base = "") {
  return base ? prefixStorage(storage, base) : storage;
}

const defaultCacheOptions = {
  name: "_",
  base: "/cache",
  swr: true,
  maxAge: 1
};
function defineCachedFunction(fn, opts = {}) {
  opts = { ...defaultCacheOptions, ...opts };
  const pending = {};
  const group = opts.group || "nitro/functions";
  const name = opts.name || fn.name || "_";
  const integrity = hash([opts.integrity, fn, opts]);
  const validate = opts.validate || (() => true);
  async function get(key, resolver, shouldInvalidateCache, event) {
    const cacheKey = [opts.base, group, name, key + ".json"].filter(Boolean).join(":").replace(/:\/$/, ":index");
    const entry = await useStorage().getItem(cacheKey) || {};
    const ttl = (opts.maxAge ?? opts.maxAge ?? 0) * 1e3;
    if (ttl) {
      entry.expires = Date.now() + ttl;
    }
    const expired = shouldInvalidateCache || entry.integrity !== integrity || ttl && Date.now() - (entry.mtime || 0) > ttl || !validate(entry);
    const _resolve = async () => {
      const isPending = pending[key];
      if (!isPending) {
        if (entry.value !== void 0 && (opts.staleMaxAge || 0) >= 0 && opts.swr === false) {
          entry.value = void 0;
          entry.integrity = void 0;
          entry.mtime = void 0;
          entry.expires = void 0;
        }
        pending[key] = Promise.resolve(resolver());
      }
      try {
        entry.value = await pending[key];
      } catch (error) {
        if (!isPending) {
          delete pending[key];
        }
        throw error;
      }
      if (!isPending) {
        entry.mtime = Date.now();
        entry.integrity = integrity;
        delete pending[key];
        if (validate(entry)) {
          const promise = useStorage().setItem(cacheKey, entry).catch((error) => {
            useNitroApp().captureError(error, { event, tags: ["cache"] });
          });
          if (event && event.waitUntil) {
            event.waitUntil(promise);
          }
        }
      }
    };
    const _resolvePromise = expired ? _resolve() : Promise.resolve();
    if (expired && event && event.waitUntil) {
      event.waitUntil(_resolvePromise);
    }
    if (opts.swr && entry.value) {
      _resolvePromise.catch((error) => {
        useNitroApp().captureError(error, { event, tags: ["cache"] });
      });
      return entry;
    }
    return _resolvePromise.then(() => entry);
  }
  return async (...args) => {
    const shouldBypassCache = opts.shouldBypassCache?.(...args);
    if (shouldBypassCache) {
      return fn(...args);
    }
    const key = await (opts.getKey || getKey)(...args);
    const shouldInvalidateCache = opts.shouldInvalidateCache?.(...args);
    const entry = await get(
      key,
      () => fn(...args),
      shouldInvalidateCache,
      args[0] && isEvent(args[0]) ? args[0] : void 0
    );
    let value = entry.value;
    if (opts.transform) {
      value = await opts.transform(entry, ...args) || value;
    }
    return value;
  };
}
const cachedFunction = defineCachedFunction;
function getKey(...args) {
  return args.length > 0 ? hash(args, {}) : "";
}
function escapeKey(key) {
  return String(key).replace(/\W/g, "");
}
function defineCachedEventHandler(handler, opts = defaultCacheOptions) {
  const variableHeaderNames = (opts.varies || []).filter(Boolean).map((h) => h.toLowerCase()).sort();
  const _opts = {
    ...opts,
    getKey: async (event) => {
      const customKey = await opts.getKey?.(event);
      if (customKey) {
        return escapeKey(customKey);
      }
      const _path = event.node.req.originalUrl || event.node.req.url || event.path;
      const _pathname = escapeKey(decodeURI(parseURL(_path).pathname)).slice(0, 16) || "index";
      const _hashedPath = `${_pathname}.${hash(_path)}`;
      const _headers = variableHeaderNames.map((header) => [header, event.node.req.headers[header]]).map(([name, value]) => `${escapeKey(name)}.${hash(value)}`);
      return [_hashedPath, ..._headers].join(":");
    },
    validate: (entry) => {
      if (entry.value.code >= 400) {
        return false;
      }
      if (entry.value.body === void 0) {
        return false;
      }
      return true;
    },
    group: opts.group || "nitro/handlers",
    integrity: [opts.integrity, handler]
  };
  const _cachedHandler = cachedFunction(
    async (incomingEvent) => {
      const variableHeaders = {};
      for (const header of variableHeaderNames) {
        variableHeaders[header] = incomingEvent.node.req.headers[header];
      }
      const reqProxy = cloneWithProxy(incomingEvent.node.req, {
        headers: variableHeaders
      });
      const resHeaders = {};
      let _resSendBody;
      const resProxy = cloneWithProxy(incomingEvent.node.res, {
        statusCode: 200,
        writableEnded: false,
        writableFinished: false,
        headersSent: false,
        closed: false,
        getHeader(name) {
          return resHeaders[name];
        },
        setHeader(name, value) {
          resHeaders[name] = value;
          return this;
        },
        getHeaderNames() {
          return Object.keys(resHeaders);
        },
        hasHeader(name) {
          return name in resHeaders;
        },
        removeHeader(name) {
          delete resHeaders[name];
        },
        getHeaders() {
          return resHeaders;
        },
        end(chunk, arg2, arg3) {
          if (typeof chunk === "string") {
            _resSendBody = chunk;
          }
          if (typeof arg2 === "function") {
            arg2();
          }
          if (typeof arg3 === "function") {
            arg3();
          }
          return this;
        },
        write(chunk, arg2, arg3) {
          if (typeof chunk === "string") {
            _resSendBody = chunk;
          }
          if (typeof arg2 === "function") {
            arg2();
          }
          if (typeof arg3 === "function") {
            arg3();
          }
          return this;
        },
        writeHead(statusCode, headers2) {
          this.statusCode = statusCode;
          if (headers2) {
            for (const header in headers2) {
              this.setHeader(header, headers2[header]);
            }
          }
          return this;
        }
      });
      const event = createEvent(reqProxy, resProxy);
      event.context = incomingEvent.context;
      const body = await handler(event) || _resSendBody;
      const headers = event.node.res.getHeaders();
      headers.etag = headers.Etag || headers.etag || `W/"${hash(body)}"`;
      headers["last-modified"] = headers["Last-Modified"] || headers["last-modified"] || (/* @__PURE__ */ new Date()).toUTCString();
      const cacheControl = [];
      if (opts.swr) {
        if (opts.maxAge) {
          cacheControl.push(`s-maxage=${opts.maxAge}`);
        }
        if (opts.staleMaxAge) {
          cacheControl.push(`stale-while-revalidate=${opts.staleMaxAge}`);
        } else {
          cacheControl.push("stale-while-revalidate");
        }
      } else if (opts.maxAge) {
        cacheControl.push(`max-age=${opts.maxAge}`);
      }
      if (cacheControl.length > 0) {
        headers["cache-control"] = cacheControl.join(", ");
      }
      const cacheEntry = {
        code: event.node.res.statusCode,
        headers,
        body
      };
      return cacheEntry;
    },
    _opts
  );
  return defineEventHandler(async (event) => {
    if (opts.headersOnly) {
      if (handleCacheHeaders(event, { maxAge: opts.maxAge })) {
        return;
      }
      return handler(event);
    }
    const response = await _cachedHandler(event);
    if (event.node.res.headersSent || event.node.res.writableEnded) {
      return response.body;
    }
    if (handleCacheHeaders(event, {
      modifiedTime: new Date(response.headers["last-modified"]),
      etag: response.headers.etag,
      maxAge: opts.maxAge
    })) {
      return;
    }
    event.node.res.statusCode = response.code;
    for (const name in response.headers) {
      event.node.res.setHeader(name, response.headers[name]);
    }
    return response.body;
  });
}
function cloneWithProxy(obj, overrides) {
  return new Proxy(obj, {
    get(target, property, receiver) {
      if (property in overrides) {
        return overrides[property];
      }
      return Reflect.get(target, property, receiver);
    },
    set(target, property, value, receiver) {
      if (property in overrides) {
        overrides[property] = value;
        return true;
      }
      return Reflect.set(target, property, value, receiver);
    }
  });
}
const cachedEventHandler = defineCachedEventHandler;

function hasReqHeader(event, name, includes) {
  const value = getRequestHeader(event, name);
  return value && typeof value === "string" && value.toLowerCase().includes(includes);
}
function isJsonRequest(event) {
  return hasReqHeader(event, "accept", "application/json") || hasReqHeader(event, "user-agent", "curl/") || hasReqHeader(event, "user-agent", "httpie/") || hasReqHeader(event, "sec-fetch-mode", "cors") || event.path.startsWith("/api/") || event.path.endsWith(".json");
}
function normalizeError(error) {
  const cwd = typeof process.cwd === "function" ? process.cwd() : "/";
  const stack = (error.stack || "").split("\n").splice(1).filter((line) => line.includes("at ")).map((line) => {
    const text = line.replace(cwd + "/", "./").replace("webpack:/", "").replace("file://", "").trim();
    return {
      text,
      internal: line.includes("node_modules") && !line.includes(".cache") || line.includes("internal") || line.includes("new Promise")
    };
  });
  const statusCode = error.statusCode || 500;
  const statusMessage = error.statusMessage ?? (statusCode === 404 ? "Not Found" : "");
  const message = error.message || error.toString();
  return {
    stack,
    statusCode,
    statusMessage,
    message
  };
}
function _captureError(error, type) {
  console.error(`[nitro] [${type}]`, error);
  useNitroApp().captureError(error, { tags: [type] });
}
function trapUnhandledNodeErrors() {
  process.on(
    "unhandledRejection",
    (error) => _captureError(error, "unhandledRejection")
  );
  process.on(
    "uncaughtException",
    (error) => _captureError(error, "uncaughtException")
  );
}
function joinHeaders(value) {
  return Array.isArray(value) ? value.join(", ") : String(value);
}
function normalizeFetchResponse(response) {
  if (!response.headers.has("set-cookie")) {
    return response;
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: normalizeCookieHeaders(response.headers)
  });
}
function normalizeCookieHeader(header = "") {
  return splitCookiesString(joinHeaders(header));
}
function normalizeCookieHeaders(headers) {
  const outgoingHeaders = new Headers();
  for (const [name, header] of headers) {
    if (name === "set-cookie") {
      for (const cookie of normalizeCookieHeader(header)) {
        outgoingHeaders.append("set-cookie", cookie);
      }
    } else {
      outgoingHeaders.set(name, joinHeaders(header));
    }
  }
  return outgoingHeaders;
}

const config = useRuntimeConfig();
const _routeRulesMatcher = toRouteMatcher(
  createRouter({ routes: config.nitro.routeRules })
);
function createRouteRulesHandler(ctx) {
  return eventHandler((event) => {
    const routeRules = getRouteRules(event);
    if (routeRules.headers) {
      setHeaders(event, routeRules.headers);
    }
    if (routeRules.redirect) {
      return sendRedirect(
        event,
        routeRules.redirect.to,
        routeRules.redirect.statusCode
      );
    }
    if (routeRules.proxy) {
      let target = routeRules.proxy.to;
      if (target.endsWith("/**")) {
        let targetPath = event.path;
        const strpBase = routeRules.proxy._proxyStripBase;
        if (strpBase) {
          targetPath = withoutBase(targetPath, strpBase);
        }
        target = joinURL(target.slice(0, -3), targetPath);
      } else if (event.path.includes("?")) {
        const query = getQuery(event.path);
        target = withQuery(target, query);
      }
      return proxyRequest(event, target, {
        fetch: ctx.localFetch,
        ...routeRules.proxy
      });
    }
  });
}
function getRouteRules(event) {
  event.context._nitro = event.context._nitro || {};
  if (!event.context._nitro.routeRules) {
    event.context._nitro.routeRules = getRouteRulesForPath(
      withoutBase(event.path.split("?")[0], useRuntimeConfig().app.baseURL)
    );
  }
  return event.context._nitro.routeRules;
}
function getRouteRulesForPath(path) {
  return defu({}, ..._routeRulesMatcher.matchAll(path).reverse());
}

const plugins = [
  
];

const errorHandler = (async function errorhandler(error, event) {
  const { stack, statusCode, statusMessage, message } = normalizeError(error);
  const errorObject = {
    url: event.path,
    statusCode,
    statusMessage,
    message,
    stack: "",
    data: error.data
  };
  if (error.unhandled || error.fatal) {
    const tags = [
      "[nuxt]",
      "[request error]",
      error.unhandled && "[unhandled]",
      error.fatal && "[fatal]",
      Number(errorObject.statusCode) !== 200 && `[${errorObject.statusCode}]`
    ].filter(Boolean).join(" ");
    console.error(tags, errorObject.message + "\n" + stack.map((l) => "  " + l.text).join("  \n"));
  }
  if (event.handled) {
    return;
  }
  setResponseStatus(event, errorObject.statusCode !== 200 && errorObject.statusCode || 500, errorObject.statusMessage);
  if (isJsonRequest(event)) {
    setResponseHeader(event, "Content-Type", "application/json");
    return send(event, JSON.stringify(errorObject));
  }
  const isErrorPage = event.path.startsWith("/__nuxt_error");
  const res = !isErrorPage ? await useNitroApp().localFetch(withQuery(joinURL(useRuntimeConfig().app.baseURL, "/__nuxt_error"), errorObject), {
    headers: getRequestHeaders(event),
    redirect: "manual"
  }).catch(() => null) : null;
  if (!res) {
    const { template } = await import('../error-500.mjs');
    if (event.handled) {
      return;
    }
    setResponseHeader(event, "Content-Type", "text/html;charset=UTF-8");
    return send(event, template(errorObject));
  }
  const html = await res.text();
  if (event.handled) {
    return;
  }
  for (const [header, value] of res.headers.entries()) {
    setResponseHeader(event, header, value);
  }
  setResponseStatus(event, res.status && res.status !== 200 ? res.status : void 0, res.statusText);
  return send(event, html);
});

const assets = {
  "/favicon.ico": {
    "type": "image/vnd.microsoft.icon",
    "etag": "\"f32-MDecMy/zcNpvc6LCU+k41vItjbc\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 3890,
    "path": "../../.output/public/favicon.ico"
  },
  "/_nuxt/Latin-Merriweather-Bold.398a4098.woff2": {
    "type": "font/woff2",
    "etag": "\"533c-fDn9srVRlzs1xlViMIEAwPfNKdE\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 21308,
    "path": "../../.output/public/_nuxt/Latin-Merriweather-Bold.398a4098.woff2"
  },
  "/_nuxt/Latin-Merriweather-BoldItalic.47048032.woff2": {
    "type": "font/woff2",
    "etag": "\"4c70-uOxgZzB6lIll4Z9sLKrk6hZ5sC4\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 19568,
    "path": "../../.output/public/_nuxt/Latin-Merriweather-BoldItalic.47048032.woff2"
  },
  "/_nuxt/Latin-Merriweather-Italic.a0e8dae2.woff2": {
    "type": "font/woff2",
    "etag": "\"4b34-BujfkNaxx7TNEuZ1MK0Kucb4XvQ\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 19252,
    "path": "../../.output/public/_nuxt/Latin-Merriweather-Italic.a0e8dae2.woff2"
  },
  "/_nuxt/Latin-Merriweather-Light.85e700ae.woff2": {
    "type": "font/woff2",
    "etag": "\"530c-0ZXNKZVglfiNdLLPWvKLzRGgGRY\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 21260,
    "path": "../../.output/public/_nuxt/Latin-Merriweather-Light.85e700ae.woff2"
  },
  "/_nuxt/Latin-Merriweather-LightItalic.d755b836.woff2": {
    "type": "font/woff2",
    "etag": "\"4a20-ZBuD8IFWmmAHytnWy4vm9ZvXUUA\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 18976,
    "path": "../../.output/public/_nuxt/Latin-Merriweather-LightItalic.d755b836.woff2"
  },
  "/_nuxt/Latin-Merriweather-Regular.928176d9.woff2": {
    "type": "font/woff2",
    "etag": "\"54bc-GuhGOP95GIu92F9OoMCUKcdTkJM\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 21692,
    "path": "../../.output/public/_nuxt/Latin-Merriweather-Regular.928176d9.woff2"
  },
  "/_nuxt/MLTE_Logo_Color.ad27a5ac.svg": {
    "type": "image/svg+xml",
    "etag": "\"61cc-vi8sdwnRlTLHAtPIyfcNTRXcEdM\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 25036,
    "path": "../../.output/public/_nuxt/MLTE_Logo_Color.ad27a5ac.svg"
  },
  "/_nuxt/add.4dc55478.svg": {
    "type": "image/svg+xml",
    "etag": "\"88-9hUZWob7i0whgrjwvOUMGtYB2JU\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 136,
    "path": "../../.output/public/_nuxt/add.4dc55478.svg"
  },
  "/_nuxt/add_circle.cfacf439.svg": {
    "type": "image/svg+xml",
    "etag": "\"c9-FQN9Gt9NNEI9i/80ZFFo0PEkLng\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 201,
    "path": "../../.output/public/_nuxt/add_circle.cfacf439.svg"
  },
  "/_nuxt/arrow_back.ad23ffb6.svg": {
    "type": "image/svg+xml",
    "etag": "\"a1-g/XD3lIuu11EZfAlkm96Yg2h9m4\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 161,
    "path": "../../.output/public/_nuxt/arrow_back.ad23ffb6.svg"
  },
  "/_nuxt/artifact-validation.f44b645e.js": {
    "type": "application/javascript",
    "etag": "\"16aa7-FdaT96RhvFQXm4t8JOYVkhz6HaA\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 92839,
    "path": "../../.output/public/_nuxt/artifact-validation.f44b645e.js"
  },
  "/_nuxt/base-layout.b0a6153c.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"2b0-tP5SvutX+q2VoJUEkphSREaZ7Mk\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 688,
    "path": "../../.output/public/_nuxt/base-layout.b0a6153c.css"
  },
  "/_nuxt/base-layout.f9ed431f.js": {
    "type": "application/javascript",
    "etag": "\"486-qilt799tDAvfG0LBnk8WPwCSTZs\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 1158,
    "path": "../../.output/public/_nuxt/base-layout.f9ed431f.js"
  },
  "/_nuxt/calendar_today.cc23d005.svg": {
    "type": "image/svg+xml",
    "etag": "\"d3-nQgL/5He3O2vxZCgSR0ObHCHyUk\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 211,
    "path": "../../.output/public/_nuxt/calendar_today.cc23d005.svg"
  },
  "/_nuxt/check--blue-60v.2fa4117a.svg": {
    "type": "image/svg+xml",
    "etag": "\"ca-TmiAA5Pv0b1MHaQUZ8sW8yu5Bf0\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 202,
    "path": "../../.output/public/_nuxt/check--blue-60v.2fa4117a.svg"
  },
  "/_nuxt/check_circle.2222ca5b.svg": {
    "type": "image/svg+xml",
    "etag": "\"d9-w++A9n7iOreQEAt42Ajb8rHAXSI\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 217,
    "path": "../../.output/public/_nuxt/check_circle.2222ca5b.svg"
  },
  "/_nuxt/close.1abf0e0a.svg": {
    "type": "image/svg+xml",
    "etag": "\"ca-T1lE/14rsknNtcuedcKZeQ6L4Us\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 202,
    "path": "../../.output/public/_nuxt/close.1abf0e0a.svg"
  },
  "/_nuxt/correct8-alt.68c4a313.svg": {
    "type": "image/svg+xml",
    "etag": "\"25f-/LeIIykTo46HVyr5OftkKvcbTPM\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 607,
    "path": "../../.output/public/_nuxt/correct8-alt.68c4a313.svg"
  },
  "/_nuxt/correct8.7d30903a.svg": {
    "type": "image/svg+xml",
    "etag": "\"258-nA2Gg2m+6It4z2EZ5TP6f5x8oJ4\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 600,
    "path": "../../.output/public/_nuxt/correct8.7d30903a.svg"
  },
  "/_nuxt/delete.40cfa49b.svg": {
    "type": "image/svg+xml",
    "etag": "\"b2-JKR3eBq69WyUX30RIW2aFiab7PM\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 178,
    "path": "../../.output/public/_nuxt/delete.40cfa49b.svg"
  },
  "/_nuxt/entry.2568e06b.js": {
    "type": "application/javascript",
    "etag": "\"577d7-lFzI9zgxdN/nZwkGoFt1hdGASCA\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 358359,
    "path": "../../.output/public/_nuxt/entry.2568e06b.js"
  },
  "/_nuxt/entry.fcf912fd.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"7e3b8-R3u95AfuRICqVv+9dvoUw4dx34Q\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 517048,
    "path": "../../.output/public/_nuxt/entry.fcf912fd.css"
  },
  "/_nuxt/error--white.d55dac06.svg": {
    "type": "image/svg+xml",
    "etag": "\"f6-LF6aUEIOvh7W53oP7CfyCewlEfA\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 246,
    "path": "../../.output/public/_nuxt/error--white.d55dac06.svg"
  },
  "/_nuxt/error-404.7fc72018.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"e2e-iNt1cqPQ0WDudfCTZVQd31BeRGs\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 3630,
    "path": "../../.output/public/_nuxt/error-404.7fc72018.css"
  },
  "/_nuxt/error-404.f6079996.js": {
    "type": "application/javascript",
    "etag": "\"8f5-f8pvFtm3t5sv3kKPqy/L8rARXFo\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 2293,
    "path": "../../.output/public/_nuxt/error-404.f6079996.js"
  },
  "/_nuxt/error-500.a90cd5e0.js": {
    "type": "application/javascript",
    "etag": "\"77e-i0kIcr7rA4PfuH6Bf8/r5rLNCYY\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 1918,
    "path": "../../.output/public/_nuxt/error-500.a90cd5e0.js"
  },
  "/_nuxt/error-500.c5df6088.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"79e-ByRo+49BgcevWdRjJy3CMx2IA5k\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 1950,
    "path": "../../.output/public/_nuxt/error-500.c5df6088.css"
  },
  "/_nuxt/error-handling.fae63081.js": {
    "type": "application/javascript",
    "etag": "\"2f0e-11/JuwJrIxgrtXnEHf27MKoHcJQ\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 12046,
    "path": "../../.output/public/_nuxt/error-handling.fae63081.js"
  },
  "/_nuxt/error.4ab47484.svg": {
    "type": "image/svg+xml",
    "etag": "\"c5-JyjfbiUkF7fe8bP+++gr5S01toU\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 197,
    "path": "../../.output/public/_nuxt/error.4ab47484.svg"
  },
  "/_nuxt/expand_less.e364a85f.svg": {
    "type": "image/svg+xml",
    "etag": "\"92-KjEiXudLJ+zHsc0N+fHGHQqKTHs\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 146,
    "path": "../../.output/public/_nuxt/expand_less.e364a85f.svg"
  },
  "/_nuxt/expand_more.bc1d8378.svg": {
    "type": "image/svg+xml",
    "etag": "\"91-oXIaAxvgVqNMBk0exOGEb6W7e4A\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 145,
    "path": "../../.output/public/_nuxt/expand_more.bc1d8378.svg"
  },
  "/_nuxt/file-excel.89c8dce1.svg": {
    "type": "image/svg+xml",
    "etag": "\"292-pnqe5E7wSNltgsb+6jsJoxkDzKQ\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 658,
    "path": "../../.output/public/_nuxt/file-excel.89c8dce1.svg"
  },
  "/_nuxt/file-pdf.186ca8c6.svg": {
    "type": "image/svg+xml",
    "etag": "\"388-/Hman38L2B3OaW4+bPII101cGJc\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 904,
    "path": "../../.output/public/_nuxt/file-pdf.186ca8c6.svg"
  },
  "/_nuxt/file-video.98ea6ce4.svg": {
    "type": "image/svg+xml",
    "etag": "\"23e-1oLH9im2MwuwpLsd6oyolrTpOAI\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 574,
    "path": "../../.output/public/_nuxt/file-video.98ea6ce4.svg"
  },
  "/_nuxt/file-word.52d8af54.svg": {
    "type": "image/svg+xml",
    "etag": "\"2f8-m6/uMuqYprQdnn0YRhpNNBT8QD4\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 760,
    "path": "../../.output/public/_nuxt/file-word.52d8af54.svg"
  },
  "/_nuxt/file.2b1fcfa0.svg": {
    "type": "image/svg+xml",
    "etag": "\"11b-fRWiWsg4JkjUJSoL7BHt4JBBmIE\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 283,
    "path": "../../.output/public/_nuxt/file.2b1fcfa0.svg"
  },
  "/_nuxt/hero.d5779c5c.jpg": {
    "type": "image/jpeg",
    "etag": "\"23c81-848oEJ4s3ZEXr2KYrN3Y0Tembk4\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 146561,
    "path": "../../.output/public/_nuxt/hero.d5779c5c.jpg"
  },
  "/_nuxt/highlight_off.05ec8ad0.svg": {
    "type": "image/svg+xml",
    "etag": "\"14e-xOww3ACPB1KvA4cAowLpXllw2Ck\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 334,
    "path": "../../.output/public/_nuxt/highlight_off.05ec8ad0.svg"
  },
  "/_nuxt/index.035ebad2.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"c0-dQVNvEHyj2AprNv62seA2U4T4VM\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 192,
    "path": "../../.output/public/_nuxt/index.035ebad2.css"
  },
  "/_nuxt/index.bc3664f8.js": {
    "type": "application/javascript",
    "etag": "\"2782-3BZQBWrfVhbMOqsxg+C8lRKVD18\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 10114,
    "path": "../../.output/public/_nuxt/index.bc3664f8.js"
  },
  "/_nuxt/info.2e1a5c0f.svg": {
    "type": "image/svg+xml",
    "etag": "\"c5-PckgQl6KYgOm2FaBbWqepSQJRbc\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 197,
    "path": "../../.output/public/_nuxt/info.2e1a5c0f.svg"
  },
  "/_nuxt/launch--white.c9b3df9d.svg": {
    "type": "image/svg+xml",
    "etag": "\"114-/pMGfVKZOQuAu2CBGn4mZdslb/w\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 276,
    "path": "../../.output/public/_nuxt/launch--white.c9b3df9d.svg"
  },
  "/_nuxt/launch.eb2ab393.svg": {
    "type": "image/svg+xml",
    "etag": "\"e3-3L+EOk4gA6Ph/RBMxio1Y1RK7GI\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 227,
    "path": "../../.output/public/_nuxt/launch.eb2ab393.svg"
  },
  "/_nuxt/loader.db0ccf10.svg": {
    "type": "image/svg+xml",
    "etag": "\"6b1-2FalphscaQX+GFIu3AiB/BYiLq8\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 1713,
    "path": "../../.output/public/_nuxt/loader.db0ccf10.svg"
  },
  "/_nuxt/navigate_before.d33e6c88.svg": {
    "type": "image/svg+xml",
    "etag": "\"92-o7xu4XxWp7SqZCNHRDA2cTVEnNU\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 146,
    "path": "../../.output/public/_nuxt/navigate_before.d33e6c88.svg"
  },
  "/_nuxt/navigate_far_before.c46ef64d.svg": {
    "type": "image/svg+xml",
    "etag": "\"b7-CuSJPH6Rr6a4/HxDUFZtuqTJYBo\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 183,
    "path": "../../.output/public/_nuxt/navigate_far_before.c46ef64d.svg"
  },
  "/_nuxt/navigate_far_next.f2b07a08.svg": {
    "type": "image/svg+xml",
    "etag": "\"be-NFIX+9Ps31shDIclQTPLNmzHCoA\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 190,
    "path": "../../.output/public/_nuxt/navigate_far_next.f2b07a08.svg"
  },
  "/_nuxt/navigate_next.5093c8bc.svg": {
    "type": "image/svg+xml",
    "etag": "\"93-1kBXE5e9X3dBxs9bCNVBz8qPKco\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 147,
    "path": "../../.output/public/_nuxt/navigate_next.5093c8bc.svg"
  },
  "/_nuxt/negotiation-card.b00d611b.js": {
    "type": "application/javascript",
    "etag": "\"55f1-KjHX4qOLNRsUrUQ6qUsWUDxbuZA\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 22001,
    "path": "../../.output/public/_nuxt/negotiation-card.b00d611b.js"
  },
  "/_nuxt/nuxt-link.e26df02c.js": {
    "type": "application/javascript",
    "etag": "\"fdb-mW55YdwqzwAQ5WdhG6U0R1hiULg\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 4059,
    "path": "../../.output/public/_nuxt/nuxt-link.e26df02c.js"
  },
  "/_nuxt/remove.d7b1b4b4.svg": {
    "type": "image/svg+xml",
    "etag": "\"76-8cMWYKfnyuo3YLWjF1EVGaXDbRE\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 118,
    "path": "../../.output/public/_nuxt/remove.d7b1b4b4.svg"
  },
  "/_nuxt/report.0ce7b076.js": {
    "type": "application/javascript",
    "etag": "\"2f89-YRZyT1iN8EjqGwMUyRoZswlTPAY\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 12169,
    "path": "../../.output/public/_nuxt/report.0ce7b076.js"
  },
  "/_nuxt/roboto-mono-v5-latin-300.b77be948.woff2": {
    "type": "font/woff2",
    "etag": "\"3ffc-eK+BYzvG3QfjD4ECL8Qs8ClJ7Wo\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 16380,
    "path": "../../.output/public/_nuxt/roboto-mono-v5-latin-300.b77be948.woff2"
  },
  "/_nuxt/roboto-mono-v5-latin-300italic.71dce22b.woff2": {
    "type": "font/woff2",
    "etag": "\"43bc-B2VNqcRSGeM6jIiGi738eFIHW+w\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 17340,
    "path": "../../.output/public/_nuxt/roboto-mono-v5-latin-300italic.71dce22b.woff2"
  },
  "/_nuxt/roboto-mono-v5-latin-700.8a46001f.woff2": {
    "type": "font/woff2",
    "etag": "\"3e54-yMnVir0Kmz4TDBnSTfxhJ5ySiL8\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 15956,
    "path": "../../.output/public/_nuxt/roboto-mono-v5-latin-700.8a46001f.woff2"
  },
  "/_nuxt/roboto-mono-v5-latin-700italic.3fc14b71.woff2": {
    "type": "font/woff2",
    "etag": "\"43b8-zwf69gpFY9BSehV/TFF30/UEDZo\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 17336,
    "path": "../../.output/public/_nuxt/roboto-mono-v5-latin-700italic.3fc14b71.woff2"
  },
  "/_nuxt/roboto-mono-v5-latin-italic.6328a2e9.woff2": {
    "type": "font/woff2",
    "etag": "\"43a0-+EGXOVZzy4ncPlirHOXK1TQV6Ww\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 17312,
    "path": "../../.output/public/_nuxt/roboto-mono-v5-latin-italic.6328a2e9.woff2"
  },
  "/_nuxt/roboto-mono-v5-latin-regular.e432bb82.woff2": {
    "type": "font/woff2",
    "etag": "\"3e9c-ZOpkvJ5bgF5cToRtKVJclOsnW1A\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 16028,
    "path": "../../.output/public/_nuxt/roboto-mono-v5-latin-regular.e432bb82.woff2"
  },
  "/_nuxt/search.7101b573.svg": {
    "type": "image/svg+xml",
    "etag": "\"12f-7SIQXgPCjjpuRY8uEOQS7YKFrC4\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 303,
    "path": "../../.output/public/_nuxt/search.7101b573.svg"
  },
  "/_nuxt/sourcesanspro-bold-webfont.83f67df6.woff2": {
    "type": "font/woff2",
    "etag": "\"4f90-S6Pz6jXU8oh8vH2IH2Li0mntOIE\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 20368,
    "path": "../../.output/public/_nuxt/sourcesanspro-bold-webfont.83f67df6.woff2"
  },
  "/_nuxt/sourcesanspro-bolditalic-webfont.a3311377.woff2": {
    "type": "font/woff2",
    "etag": "\"4020-3rn4Hh5+QvydVgqegvZvlC5QHTk\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 16416,
    "path": "../../.output/public/_nuxt/sourcesanspro-bolditalic-webfont.a3311377.woff2"
  },
  "/_nuxt/sourcesanspro-italic-webfont.8a6e1d4b.woff2": {
    "type": "font/woff2",
    "etag": "\"3ff4-mjZ4mCrX3jCKS6Xna7+fa5fbnt4\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 16372,
    "path": "../../.output/public/_nuxt/sourcesanspro-italic-webfont.8a6e1d4b.woff2"
  },
  "/_nuxt/sourcesanspro-light-webfont.45a3eaa2.woff2": {
    "type": "font/woff2",
    "etag": "\"4fbc-RpXwbIsbasuAicH8GPxCH1zxkM4\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 20412,
    "path": "../../.output/public/_nuxt/sourcesanspro-light-webfont.45a3eaa2.woff2"
  },
  "/_nuxt/sourcesanspro-lightitalic-webfont.0efc29b2.woff2": {
    "type": "font/woff2",
    "etag": "\"3fbc-YcaJTr/hJHG8BKHRysFFGKH+WbA\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 16316,
    "path": "../../.output/public/_nuxt/sourcesanspro-lightitalic-webfont.0efc29b2.woff2"
  },
  "/_nuxt/sourcesanspro-regular-webfont.8792619b.woff2": {
    "type": "font/woff2",
    "etag": "\"503c-8dOwxHg4SjXwdm2dGDmuqBoWSz8\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 20540,
    "path": "../../.output/public/_nuxt/sourcesanspro-regular-webfont.8792619b.woff2"
  },
  "/_nuxt/todo.0331d31c.js": {
    "type": "application/javascript",
    "etag": "\"70-WQJf65qKNT0wbnYDt8kH5aOTaRE\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 112,
    "path": "../../.output/public/_nuxt/todo.0331d31c.js"
  },
  "/_nuxt/unfold_more.b6bd1f0c.svg": {
    "type": "image/svg+xml",
    "etag": "\"dc-uL0wXrPpwuVlPJLVEWYbpVhh4JY\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 220,
    "path": "../../.output/public/_nuxt/unfold_more.b6bd1f0c.svg"
  },
  "/_nuxt/vue.f36acd1f.8aab8e99.js": {
    "type": "application/javascript",
    "etag": "\"181-Yk+LIbtdlOQ7yyAyfrP+H4KvlFU\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 385,
    "path": "../../.output/public/_nuxt/vue.f36acd1f.8aab8e99.js"
  },
  "/_nuxt/warning.e800748c.svg": {
    "type": "image/svg+xml",
    "etag": "\"97-VOdqpq/MB5059lY4UWE4Ud7XALc\"",
    "mtime": "2024-01-03T21:33:48.514Z",
    "size": 151,
    "path": "../../.output/public/_nuxt/warning.e800748c.svg"
  }
};

function readAsset (id) {
  const serverDir = dirname(fileURLToPath(globalThis._importMeta_.url));
  return promises.readFile(resolve(serverDir, assets[id].path))
}

const publicAssetBases = {"/_nuxt":{"maxAge":31536000}};

function isPublicAssetURL(id = '') {
  if (assets[id]) {
    return true
  }
  for (const base in publicAssetBases) {
    if (id.startsWith(base)) { return true }
  }
  return false
}

function getAsset (id) {
  return assets[id]
}

const METHODS = /* @__PURE__ */ new Set(["HEAD", "GET"]);
const EncodingMap = { gzip: ".gz", br: ".br" };
const _f4b49z = eventHandler((event) => {
  if (event.method && !METHODS.has(event.method)) {
    return;
  }
  let id = decodePath(
    withLeadingSlash(withoutTrailingSlash(parseURL(event.path).pathname))
  );
  let asset;
  const encodingHeader = String(
    getRequestHeader(event, "accept-encoding") || ""
  );
  const encodings = [
    ...encodingHeader.split(",").map((e) => EncodingMap[e.trim()]).filter(Boolean).sort(),
    ""
  ];
  if (encodings.length > 1) {
    setResponseHeader(event, "Vary", "Accept-Encoding");
  }
  for (const encoding of encodings) {
    for (const _id of [id + encoding, joinURL(id, "index.html" + encoding)]) {
      const _asset = getAsset(_id);
      if (_asset) {
        asset = _asset;
        id = _id;
        break;
      }
    }
  }
  if (!asset) {
    if (isPublicAssetURL(id)) {
      removeResponseHeader(event, "Cache-Control");
      throw createError({
        statusMessage: "Cannot find static asset " + id,
        statusCode: 404
      });
    }
    return;
  }
  const ifNotMatch = getRequestHeader(event, "if-none-match") === asset.etag;
  if (ifNotMatch) {
    setResponseStatus(event, 304, "Not Modified");
    return "";
  }
  const ifModifiedSinceH = getRequestHeader(event, "if-modified-since");
  const mtimeDate = new Date(asset.mtime);
  if (ifModifiedSinceH && asset.mtime && new Date(ifModifiedSinceH) >= mtimeDate) {
    setResponseStatus(event, 304, "Not Modified");
    return "";
  }
  if (asset.type && !getResponseHeader(event, "Content-Type")) {
    setResponseHeader(event, "Content-Type", asset.type);
  }
  if (asset.etag && !getResponseHeader(event, "ETag")) {
    setResponseHeader(event, "ETag", asset.etag);
  }
  if (asset.mtime && !getResponseHeader(event, "Last-Modified")) {
    setResponseHeader(event, "Last-Modified", mtimeDate.toUTCString());
  }
  if (asset.encoding && !getResponseHeader(event, "Content-Encoding")) {
    setResponseHeader(event, "Content-Encoding", asset.encoding);
  }
  if (asset.size > 0 && !getResponseHeader(event, "Content-Length")) {
    setResponseHeader(event, "Content-Length", asset.size);
  }
  return readAsset(id);
});

const _lazy_viTD02 = () => import('../renderer.mjs');

const handlers = [
  { route: '', handler: _f4b49z, lazy: false, middleware: true, method: undefined },
  { route: '/**', handler: _lazy_viTD02, lazy: true, middleware: false, method: undefined }
];

function createNitroApp() {
  const config = useRuntimeConfig();
  const hooks = createHooks();
  const captureError = (error, context = {}) => {
    const promise = hooks.callHookParallel("error", error, context).catch((_err) => {
      console.error("Error while capturing another error", _err);
    });
    if (context.event && isEvent(context.event)) {
      const errors = context.event.context.nitro?.errors;
      if (errors) {
        errors.push({ error, context });
      }
      if (context.event.waitUntil) {
        context.event.waitUntil(promise);
      }
    }
  };
  const h3App = createApp({
    debug: destr(false),
    onError: (error, event) => {
      captureError(error, { event, tags: ["request"] });
      return errorHandler(error, event);
    },
    onRequest: async (event) => {
      await nitroApp.hooks.callHook("request", event).catch((error) => {
        captureError(error, { event, tags: ["request"] });
      });
    },
    onBeforeResponse: async (event, response) => {
      await nitroApp.hooks.callHook("beforeResponse", event, response).catch((error) => {
        captureError(error, { event, tags: ["request", "response"] });
      });
    },
    onAfterResponse: async (event, response) => {
      await nitroApp.hooks.callHook("afterResponse", event, response).catch((error) => {
        captureError(error, { event, tags: ["request", "response"] });
      });
    }
  });
  const router = createRouter$1({
    preemptive: true
  });
  const localCall = createCall(toNodeListener(h3App));
  const _localFetch = createFetch(localCall, globalThis.fetch);
  const localFetch = (...args) => {
    return _localFetch(...args).then(
      (response) => normalizeFetchResponse(response)
    );
  };
  const $fetch = createFetch$1({
    fetch: localFetch,
    Headers: Headers$1,
    defaults: { baseURL: config.app.baseURL }
  });
  globalThis.$fetch = $fetch;
  h3App.use(createRouteRulesHandler({ localFetch }));
  h3App.use(
    eventHandler((event) => {
      event.context.nitro = event.context.nitro || { errors: [] };
      const envContext = event.node.req?.__unenv__;
      if (envContext) {
        Object.assign(event.context, envContext);
      }
      event.fetch = (req, init) => fetchWithEvent(event, req, init, { fetch: localFetch });
      event.$fetch = (req, init) => fetchWithEvent(event, req, init, {
        fetch: $fetch
      });
      event.waitUntil = (promise) => {
        if (!event.context.nitro._waitUntilPromises) {
          event.context.nitro._waitUntilPromises = [];
        }
        event.context.nitro._waitUntilPromises.push(promise);
        if (envContext?.waitUntil) {
          envContext.waitUntil(promise);
        }
      };
      event.captureError = (error, context) => {
        captureError(error, { event, ...context });
      };
    })
  );
  for (const h of handlers) {
    let handler = h.lazy ? lazyEventHandler(h.handler) : h.handler;
    if (h.middleware || !h.route) {
      const middlewareBase = (config.app.baseURL + (h.route || "/")).replace(
        /\/+/g,
        "/"
      );
      h3App.use(middlewareBase, handler);
    } else {
      const routeRules = getRouteRulesForPath(
        h.route.replace(/:\w+|\*\*/g, "_")
      );
      if (routeRules.cache) {
        handler = cachedEventHandler(handler, {
          group: "nitro/routes",
          ...routeRules.cache
        });
      }
      router.use(h.route, handler, h.method);
    }
  }
  h3App.use(config.app.baseURL, router.handler);
  const app = {
    hooks,
    h3App,
    router,
    localCall,
    localFetch,
    captureError
  };
  for (const plugin of plugins) {
    try {
      plugin(app);
    } catch (err) {
      captureError(err, { tags: ["plugin"] });
      throw err;
    }
  }
  return app;
}
const nitroApp = createNitroApp();
const useNitroApp = () => nitroApp;

const localFetch = nitroApp.localFetch;
trapUnhandledNodeErrors();

export { useRuntimeConfig as a, useStorage as b, getRouteRules as g, localFetch as l, useNitroApp as u };
//# sourceMappingURL=nitro-prerenderer.mjs.map
