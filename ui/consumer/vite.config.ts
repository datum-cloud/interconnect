import { federation } from '@module-federation/vite';
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';

// Interconnect Portal Plugin — a Module Federation remote loaded by the
// cloud-portal host at runtime. Structural template: examples/sample-plugin/
// in the cloud-portal repo (see its README.md and
// docs/enhancements/portal-plugin-system.md there).
//
// Bare-bones scaffold: no pages exposed yet. Add entries to `exposes` below
// (and mirror them in public/plugin-manifest.json's exposedModules) as pages
// are built.
export default defineConfig({
  server: {
    port: 7779,
    strictPort: true,
    cors: true,
  },
  preview: {
    port: 7779,
    strictPort: true,
    cors: true,
  },
  build: {
    target: 'esnext',
    minify: false,
  },
  plugins: [
    react(),
    federation({
      // MUST equal the manifest `name` — the host keys the remote by this id.
      name: 'interconnect.datumapis.com',
      // The manifest's `remoteEntry` field points the host at this filename.
      filename: 'remoteEntry.js',
      manifest: true,
      exposes: {
        './Assistant': './src/pages/assistant.tsx',
      },
      // Host-pinned singletons — the host provides all of these, so plugin
      // queries share the host's QueryClient cache.
      shared: {
        react: { singleton: true, requiredVersion: '^19.0.0' },
        'react-dom': { singleton: true, requiredVersion: '^19.0.0' },
        // React 19's createRoot/hydrateRoot live in this subpath, which MF
        // treats as its own distinct shared module from 'react-dom'. Left
        // undeclared, MF crashes with React's "incompatible react/react-dom
        // versions" invariant instead of just using a local fallback — see
        // assistant/ui/consumer/vite.config.ts's comment on this, where it
        // bit that plugin first. Needs a matching host-side entry in
        // cloud-portal's federation-host.ts hostShared().
        'react-dom/client': { singleton: true, requiredVersion: '^19.0.0' },
        'react-router': { singleton: true, requiredVersion: '^7.0.0' },
        '@tanstack/react-query': { singleton: true, requiredVersion: '^5.0.0' },
        // Must be shared, not bundled: useProjectContext()/usePluginFetch()
        // read a React Context defined inside this module, which is only the
        // host's PortalPluginHostProvider's Context if every consumer
        // resolves the host's exact module instance instead of this plugin's
        // own copy (see assistant/ui/consumer/vite.config.ts, same
        // requirement there).
        '@datum-cloud/portal-plugin-sdk': { singleton: true, requiredVersion: '^1.0.0' },
      },
    }),
  ],
});
