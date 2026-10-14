import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    // Setting server.allowedHosts to true allows any website to send requests
    // to your dev server through DNS rebinding attacks, allowing them to
    // download your source code and content. We recommend always using an
    // explicit list of allowed hosts.
    //
    // See GHSA-vg6x-rcgg-rjx6 for more details[0].
    //
    // [0]: https://vite.dev/config/server-options.html#server-allowedhosts
    allowedHosts: true
  }
});
