# Restart Policy Demo — Unikraft Cloud

A simple Python HTTP server used to demonstrate and test the three restart policies available on Unikraft Cloud: `never`, `always`, and `on-failure`.

---

## Prerequisites

- [`kraft`](https://unikraft.org/docs/cli) / [`unikraft`](https://unikraft.com/docs/cli) CLI installed
- A [Unikraft Cloud](https://unikraft.cloud) account with an API token
- `curl` and `jq` installed

---

## Setup

```bash
# Set your API token
export UKC_TOKEN=<your-token>

# Set your metro
export UKC_METRO=fra

# Login to Unikraft Cloud
unikraft login
```

---

## Server Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Returns `Hello from restart-demo!` |
| `GET /exit?code=N` | Calls `sys.exit(N)` — simulates crash or clean exit |

---

## Testing with kraft / unikraft CLI

Both CLIs work the same way, just swap `kraft cloud` with `unikraft`.

### Deploy the 3 instances

```bash
# kraft CLI
kraft cloud deploy -M 256M -p 443:8080/http+tls --name restart-never    --restart never      .
kraft cloud deploy -M 256M -p 443:8080/http+tls --name restart-always   --restart always     .
kraft cloud deploy -M 256M -p 443:8080/http+tls --name restart-on-failure --restart on-failure .

# unikraft CLI — build first, then run
unikraft build . --output restart-never:latest
unikraft build . --output restart-always:latest
unikraft build . --output restart-on-failure:latest

unikraft run --metro fra -m 256M -p 443:8080/http+tls --restart never        --name restart-never      --image restart-never:latest
unikraft run --metro fra -m 256M -p 443:8080/http+tls --restart always       --name restart-always     --image restart-always:latest
unikraft run --metro fra -m 256M -p 443:8080/http+tls --restart on-failure   --name restart-on-failure --image restart-on-failure:latest
```

### Check instances

```bash
# kraft CLI
kraft cloud instance list

# unikraft CLI
unikraft instances list
```

### Trigger scenarios

```bash
# hello world — confirm server is up
curl https://<fqdn>/

# simulate crash (exit code 1)
curl https://<fqdn>/exit?code=1

# simulate clean exit (exit code 0)
curl https://<fqdn>/exit?code=0
```

### Check Restart Behavior & Table

```bash
# wait 2-3 seconds then check state
kraft cloud instance list
# or
unikraft instances list
```

---

## Testing via API (bash scripts)

### Create an instance

```bash
chmod +x api/create.sh
./api/create.sh <name> <image> <policy> [memory_mb]

# Examples
./api/create.sh restart-never     restart-demo:latest never
./api/create.sh restart-always    restart-demo:latest always
./api/create.sh restart-on-failure restart-demo:latest on-failure
```

### List all instances

```bash
./api/list.sh

# compact view
./api/list.sh | jq '.data.instances[] | {name, state, restart_policy, fqdn: .service_group.domains[0].fqdn}'
```

### Interact with the server

```bash
chmod +x api/interact.sh

# hello world
./api/interact.sh <fqdn> hello

# simulate crash
./api/interact.sh <fqdn> exit 1

# simulate clean exit
./api/interact.sh <fqdn> exit 0
```

### Delete an instance

```bash
chmod +x api/delete.sh
./api/delete.sh <uuid>
```

---

## Expected Behavior

| Policy | exit code 0 | exit code != 0 | Use case |
|--------|-------------|----------------|----------|
| `never` | ❌ does not restart | ❌ does not restart | One-shot jobs, batch tasks |
| `always` | ✅ restarts | ✅ restarts | Critical services, always-on |
| `on-failure` | ❌ does not restart | ✅ restarts | Production servers, resilient workloads |

---

## Test Scenarios Summary

### Scenario 1 — `never`

```bash
# deploy
kraft cloud deploy -M 256M -p 443:8080/http+tls --name restart-never --restart never .

# trigger crash
curl https://<fqdn>/exit?code=1

# check — instance should be stopped and stay stopped
kraft cloud instance list
```

### Scenario 2 — `on-failure`

```bash
# deploy
kraft cloud deploy -M 256M -p 443:8080/http+tls --name restart-on-failure --restart on-failure .

# trigger crash — should restart
curl https://<fqdn>/exit?code=1
sleep 3 && kraft cloud instance list   # STATE: running ✅

# clean exit — should NOT restart
curl https://<fqdn>/exit?code=0
sleep 3 && kraft cloud instance list   # STATE: stopped ✅
```

### Scenario 3 — `always`

```bash
# deploy
kraft cloud deploy -M 256M -p 443:8080/http+tls --name restart-always --restart always .

# clean exit — should restart anyway
curl https://<fqdn>/exit?code=0
sleep 3 && kraft cloud instance list   # STATE: running ✅

# crash — should also restart
curl https://<fqdn>/exit?code=1
sleep 3 && kraft cloud instance list   # STATE: running ✅
```

---

## Cleanup

```bash
# kraft CLI
kraft cloud instance remove restart-never
kraft cloud instance remove restart-always
kraft cloud instance remove restart-on-failure

# or via API
./api/delete.sh <uuid>
```