# Unikraft Cloud Autoscaling Framework

This repository provides a comprehensive blueprint for configuring, deploying, and auditing elastic autoscaling policies on Unikraft Cloud. It captures the three primary infrastructure methodologies—Imperative, Programmatic, and Declarative—tailored specifically to handle high-performance microkernels with dynamic workload adjustments.

---

## Repository Structure

```text
.
├── api/
│   ├── deploy.sh
│   └── scale.sh
├── app/
│   ├── .unikraft/
│   │   ├── build/
│   │   │   └── initramfs-x86_64.cpio
│   │   └── rootfs-cache/
│   │       ├── blobs/sha256/
│   │       ├── ingest/
│   │       ├── index.json
│   │       └── oci-layout
│   ├── Dockerfile
│   ├── Kraftfile
│   └── main.go
├── kraft/
│   ├── deploy.sh
│   └── scale.sh
├── unikraft/
│   ├── .unikraft/build/
│   ├── deploy.sh
│   ├── kraft.yaml
│   └── scale.sh
└── README.md
```

## Prerequisites

Before interacting with any configuration layers, ensure your local station meets the following requirements:

- **`kraft` CLI**: Version `0.12.14` or newer installed and authenticated.
- **System Utilities**: `curl` and `jq` binaries available in your system path.
- **Account Access**: An active Unikraft Cloud token with authorization privileges.

---

## Quick Start & Token Setup

Load your operational variables into your local shell session before executing any deployment routines:

```bash
# Load authentication tokens and target routing parameters
export UKC_TOKEN="your_unikraft_cloud_token_here"
export UKC_METRO="fra"

# Verify local CLI session state
kraft login
```

## Core Infrastructure Parameters

The deployment scripts are hardcoded to enforce the following infrastructure topography to maintain consistency across all three test paradigms:

| Parameter | Value | Description |
| :--- | :--- | :--- |
| `GROUP_NAME` | `my-scaling-group` | The designated target Service Group |
| `TEMPLATE_NAME` | `my-first-instance` | The base catalog template/matrix image used for scale allocation |
| `METRIC` | `cpu` | The primary resource tracking metric monitored by the cloud hypervisor |
| `MIN_SIZE` / `MAX_SIZE` | `0` / `1` | Boundaries limiting the scaling pool (allows complete scaling down to 0) |

## Detailed Operations

### Method 1: Imperative Configuration via KraftKit CLI (`kraft/`)

This approach modifies the remote hypervisor rules incrementally using sequential command line utilities.

#### 1. Initialize the Base Scale Profile

The initial configuration establishes the size boundaries of the scale group and assigns the base execution template:

```bash
chmod +x kraft/deploy.sh
./kraft/deploy.sh
```

*Inside the script:*
```bash
kraft cloud scale init my-scaling-group --min-size 0 --max-size 1 --template my-first-instance
```

#### 2. Apply the Layered Step Metrics

The second step injects the exact mathematical thresholds where instances are added or subtracted from the active pool:

```bash
chmod +x kraft/scale.sh
./kraft/scale.sh
```
*Inside the script:*

```bash
# Appends step boundaries to the active profile
kraft cloud scale add my-scaling-group \\
  --name my-cpu-policy \\
  --metric cpu \\
  --adjustment percent \\
  --step 600:800/50 \\
  --step 800:/100
```

### Method 2: Programmatic Configuration via REST API (`api/`)

This approach bypasses all local wrapper binaries and communicates directly via JSON over HTTPS with the core infrastructure endpoints located at `https://api.fra.unikraft.cloud/v1/services/autoscale.`

#### Exact Request Payload Schema

The REST API parser expects strict database-level naming definitions which differ slightly from CLI wrappers. Note the required structures for root names, nested template objects, and `adjustment_type` naming conventions:

```JSON
{
  "name": "my-scaling-group",
  "min_size": 0,
  "max_size": 1,
  "create_args": {
    "template": {
      "name": "my-first-instance"
    }
  },
  "policies": [
    {
      "name": "my-cpu-policy",
      "type": "step",
      "metric": "cpu",
      "adjustment_type": "percent",
      "steps": [
        { "lower_bound": 600, "upper_bound": 800, "adjustment": 50 },
        { "lower_bound": 800, "adjustment": 100 }
      ]
    }
  ]
}
```

-------------------------------

### Understanding the Scaling Logic (Step Metrics)

The autoscaling policies use a boundary-based calculation (known as Step Scaling) to determine exactly when and by how much to adjust the number of active instances. The `--step` flag syntax might look like an equation at first glance, but it follows a strict, predictable format: `[lower_bound]:[upper_bound]/[adjustment]`.

Here is a detailed breakdown using the configuration `--step 600:800/50` as an example:

* **Lower Bound (`600`)**: The minimum metric threshold (e.g., concurrent network requests or CPU load units) where this specific rule becomes active.
* **Upper Bound (`800`)**: The maximum metric threshold for this rule. If the metric exceeds this number, the system will move on to the next defining step.
* **Adjustment (`/50`)**: The exact action to take when the tracked metric falls between the lower and upper bounds. Because we specified `--adjustment percent` in our CLI command, this means the active instance pool size is increased by **50%**.

-------------------------------

#### Executing the API Routine

To wipe any old configurations and push the raw JSON body to the service controller endpoint, run:

```bash
chmod +x api/scale.sh
./api/scale.sh
```
### Method 3: Direct Synchronous Deployment via Unikraft (`unikraft/`)

This strategy leverages the synchronized app deployment layer to instantiate the service group, declare performance constraints (memory allocations), map routing layers, and configure scale-to-zero behaviors simultaneously.

#### Overcoming Synchronization & Terminal Renderer Latency

When launching using `deploy`, KraftKit checks live deployment steps against edge network components, resulting in rapid status changes (`deploying` / `propagating`). The production scripts safely decouple visual terminal renderer bottlenecks and configure precise execution constraints using specific operational flags:

-  --log-type basic: Disables reactive terminal spinner updates, preserving memory and preventing context cancellation faults.

- --timeout 3m: Enhances the connection window to accommodate external TLS propagation timelines.

- --memory 128: Explicitly provisions mandatory runtime resources.

#### Running the Production Deploy

```bash
chmod +x unikraft/deploy.sh
./unikraft/deploy.sh
```

*Inside the script:*

```bash
# Deploys using explicit positional cloud image structures
kraft cloud deploy \\
  --service "my-scaling-group" \\
  --port 443:8080 \\
  --memory 128 \\
  --scale-to-zero on \\
  --timeout 3m \\
  --log-type basic \\
  "nginx:latest"
```

## Verification & Status Control

To audit and fetch the active state of your configurations independently of the method used to create them, utilize the unified status verification scripts:

```bash
# Runs a live check against the current metrics engine
./unikraft/scale.sh
```

### Expected Output Structure

A successfully provisioned and active scaling group will return a structured state data object similar to this:

```Plaintext
uuid: 3b71c362-3a94-42d6-9fb6-171f982c348d
name: my-scaling-group
enabled: true
template: 38d95efa-fe13-4443-b7d3-f32e957d81a7
policies:
  - name: my-cpu-policy
    metric: cpu
    type: step
    adjustment_type: percent
    steps:
      - lower_bound: 600
        upper_bound: 800
        adjustment: 50
      - lower_bound: 800
        adjustment: 100
```

## State Cleanup

To release active allocations and reset the operational state back to a clean configuration base, execute the following reset utility:

```bash
kraft cloud scale reset my-scaling-group
```

## Troubleshooting

* **Authentication Errors (401 Unauthorized)**: Ensure your `UKC_TOKEN` is exported correctly and hasn't expired. Run `kraft login` to verify.
* **Deployment Timeouts**: If `unikraft/deploy.sh` hangs, ensure your network allows egress traffic on port 443 and that the `--timeout` flag is set to at least `3m`.
* **Resource Not Found**: Ensure you are targeting the correct metro (e.g., `fra` for Frankfurt) using `export UKC_METRO="fra"`, as scale groups are isolated per region.












