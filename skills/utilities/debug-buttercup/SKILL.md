---
name: debug-buttercup
description: Debugs the Buttercup CRS (Cyber Reasoning System) running on Kubernetes. Use when diagnosing pod crashes, restart loops, Redis failures, resource pressure, or service misbehavior in the crs namespace.
allowed-tools: Bash Read
---

# Debug Buttercup

Debugs the Buttercup CRS (Cyber Reasoning System) running on Kubernetes in the `crs` namespace.

## When to Use

- Pods in `crs` namespace in CrashLoopBackOff, OOMKilled, or restarting
- Multiple services restart simultaneously (cascade failure)
- Redis unresponsive or showing AOF warnings
- Queues growing but tasks not progressing
- Nodes show DiskPressure, MemoryPressure, or PID pressure
- Build-bot cannot reach Docker daemon (DinD failures)
- Scheduler stuck and not advancing task state
- Health check probes failing unexpectedly

## When NOT to Use

- Deploying or upgrading Buttercup
- Debugging issues outside the `crs` namespace
- Performance tuning without a failure symptom

## Service Map

| Layer | Services |
|-------|----------|
| Infra | redis, dind, litellm, registry-cache |
| Orchestration | scheduler, task-server, task-downloader, scratch-cleaner |
| Fuzzing | build-bot, fuzzer-bot, coverage-bot, tracer-bot, merger-bot |
| Analysis | patcher, seed-gen, program-model, pov-reproducer |
| Interface | competition-api, ui |

## Triage Workflow

```bash
# Step 1: Get pod overview
kubectl get pods -n crs -o wide

# Step 2: Check recent events
kubectl get events -n crs --sort-by='.lastTimestamp'
kubectl get events -n crs --field-selector type=Warning --sort-by='.lastTimestamp'

# Step 3: Check failed pod details
kubectl describe pod -n crs <pod-name> | grep -A8 'Last State:'

# Step 4: Check recent logs
kubectl logs -n crs <pod-name> --previous --tail=200
kubectl logs -n crs <pod-name> --tail=200
```

## Cascade Detection

If all `--previous` logs show `redis.exceptions.ConnectionError`, **debug Redis first** before investigating other services.

## Redis Debugging

```bash
kubectl exec -n crs <redis-pod> -- redis-cli

# Inside redis-cli:
INFO memory
INFO persistence
INFO clients
INFO stats
CLIENT LIST
DBSIZE
```

## Queue Inspection

```bash
# Check queue length
kubectl exec -n crs <redis-pod> -- redis-cli XLEN fuzzer_build_queue

# Check consumer groups
kubectl exec -n crs <redis-pod> -- redis-cli XINFO GROUPS fuzzer_build_queue
```

**Key queues**: `fuzzer_build_queue`, `fuzzer_crash_queue`, `confirmed_vulnerabilities_queue`, `tasks_ready_queue`, `patches_queue`

## Health Check Mechanism

Pods write timestamps to `/tmp/health_check_alive`. Liveness probe checks file freshness.

```bash
kubectl exec -n crs <pod-name> -- cat /tmp/health_check_alive
```

## Diagnostic Script

```bash
bash scripts/diagnose.sh
bash scripts/diagnose.sh --full
```

## Reference

See [failure-patterns.md](references/failure-patterns.md) for known failure modes and their remediation.
