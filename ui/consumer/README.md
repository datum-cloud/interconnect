# Interconnect Portal Plugin

Bare-bones scaffold for the interconnect service (`interconnect.datumapis.com`)
consumer-side Portal Plugin, shipped as a **Module Federation remote** that
the cloud portal loads at runtime — the
[Portal Plugin System](https://github.com/datum-cloud/cloud-portal/blob/main/docs/enhancements/portal-plugin-system.md).
Structural template: [`examples/sample-plugin/`](https://github.com/datum-cloud/cloud-portal/tree/main/examples/sample-plugin)
in the `cloud-portal` repo; shape mirrors `compute`'s `ui/consumer` plugin.

No pages yet — `public/plugin-manifest.json` declares only a `comingSoon`
`portal.nav/project` entry. Add `portal.page/project` extensions and
matching `exposes`/`exposedModules` entries as pages are built.

## Development

`ui/consumer/` has its own `package.json` and lockfile, independent of the
rest of this repo:

```bash
cd ui/consumer
bun install
bun run dev        # Vite dev server (:7779, HMR) — standalone/direct
bun run preview    # built dist/ served (:7779) — proxy-safe
bun run build      # static dist/ (remoteEntry.js + plugin-manifest.json + chunks)
bun run typecheck  # tsc --noEmit
```
