"use strict";
(() => {
  var __knownSymbol = (name, symbol) => {
    if (symbol = Symbol[name])
      return symbol;
    throw Error("Symbol." + name + " is not defined");
  };
  var __async = (__this, __arguments, generator) => new Promise((resolve, reject) => {
    var fulfilled = (value) => {
      try {
        step(generator.next(value));
      } catch (e) {
        reject(e);
      }
    }, rejected = (value) => {
      try {
        step(generator.throw(value));
      } catch (e) {
        reject(e);
      }
    }, step = (x) => x.done ? resolve(x.value) : Promise.resolve(x.value).then(fulfilled, rejected);
    step((generator = generator.apply(__this, __arguments)).next());
  }), __await = function(promise, isYieldStar) {
    this[0] = promise, this[1] = isYieldStar;
  }, __asyncGenerator = (__this, __arguments, generator) => {
    var resume = (k, v, yes, no) => {
      try {
        var x = generator[k](v), isAwait = (v = x.value) instanceof __await, done = x.done;
        Promise.resolve(isAwait ? v[0] : v).then((y) => isAwait ? resume(k === "return" ? k : "next", v[1] ? { done: y.done, value: y.value } : y, yes, no) : yes({ value: y, done })).catch((e) => resume("throw", e, yes, no));
      } catch (e) {
        no(e);
      }
    }, method = (k) => it[k] = (x) => new Promise((yes, no) => resume(k, x, yes, no)), it = {};
    return generator = generator.apply(__this, __arguments), it[Symbol.asyncIterator] = () => it, method("next"), method("throw"), method("return"), it;
  }, __yieldStar = (value) => {
    var obj = value[__knownSymbol("asyncIterator")], isAwait = !1, method, it = {};
    return obj == null ? (obj = value[__knownSymbol("iterator")](), method = (k) => it[k] = (x) => obj[k](x)) : (obj = obj.call(value), method = (k) => it[k] = (v) => {
      if (isAwait) {
        if (isAwait = !1, k === "throw")
          throw v;
        return v;
      }
      return isAwait = !0, {
        done: !1,
        value: new __await(new Promise((resolve) => {
          var x = obj[k](v);
          if (!(x instanceof Object))
            throw TypeError("Object expected");
          resolve(x);
        }), 1)
      };
    }), it[__knownSymbol("iterator")] = () => it, method("next"), "throw" in obj ? method("throw") : it.throw = (x) => {
      throw x;
    }, "return" in obj && method("return"), it;
  }, __forAwait = (obj, it, method) => (it = obj[__knownSymbol("asyncIterator")]) ? it.call(obj) : (obj = obj[__knownSymbol("iterator")](), it = {}, method = (key, fn) => (fn = obj[key]) && (it[key] = (arg) => new Promise((yes, no, done) => (arg = fn.call(obj, arg), done = arg.done, Promise.resolve(arg.value).then((value) => yes({ value, done }), no)))), method("next"), method("return"), it);

  // tooldrawer/lib/condition.ts
  var Condition = class {
    constructor() {
      this._resolve = () => {
      };
      this.notify_all();
    }
    notify_all() {
      this._resolve(), this._promise = new Promise((resolve) => {
        this._resolve = resolve;
      });
    }
    wait() {
      return this._promise;
    }
  }, condition_default = Condition;

  // tooldrawer/lib/server-sent-events.ts
  function sseDataStream(url, options) {
    return __asyncGenerator(this, null, function* () {
      let queue = new Array(), condition = new condition_default(), eventSource = new EventSource(url);
      eventSource.addEventListener("message", (event) => {
        queue.push(JSON.parse(event.data)), condition.notify_all();
      });
      let name = (options == null ? void 0 : options.name) || "sseDataStream";
      for (eventSource.addEventListener("open", () => {
        console.debug(`\u{1F60E} ${name} connected to ${url}`);
      }), eventSource.addEventListener("error", () => {
        console.debug(`\u{1F61E} ${name} connection to ${url} failed`);
      }); ; )
        yield* __yieldStar(queue.splice(0)), yield new __await(condition.wait());
    });
  }

  // tooldrawer/livereload-worker.ts
  function worker(_0) {
    return __async(this, arguments, function* ({ eventsUrl }) {
      let broadcastChannel = new BroadcastChannel("live-reload"), broadcast = (message) => broadcastChannel.postMessage(message), prevVID;
      try {
        for (var iter = __forAwait(sseDataStream(eventsUrl, {
          name: self.name
        })), more, temp, error; more = !(temp = yield iter.next()).done; more = !1) {
          let sse = temp.value;
          switch (sse.type) {
            case "reload":
              broadcast(sse);
              break;
            case "ping":
              prevVID && sse.versionId !== prevVID && (console.debug("\u{1F501} live-reload triggering reload."), broadcast({ type: "restart" })), prevVID = sse.versionId;
              break;
          }
        }
      } catch (temp) {
        error = [temp];
      } finally {
        try {
          more && (temp = iter.return) && (yield temp.call(iter));
        } finally {
          if (error)
            throw error[0];
        }
      }
    });
  }
  function getConfig() {
    return new Promise((resolve) => {
      self.addEventListener("connect", (event) => {
        let port = event.ports[0];
        port.addEventListener(
          "message",
          (event2) => resolve(event2.data),
          { once: !0 }
        ), port.start();
      });
    });
  }
  getConfig().then((config) => worker(config)).catch(console.error);
})();
//# sourceMappingURL=livereload-worker.js.map
