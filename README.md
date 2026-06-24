# Dynamo Log Report Task

This repository contains the corrected `log-report` Terminal-Bench 2 / Harbor task for the Project Dynamo assessment.

## Requirements

* Ubuntu/Linux shell
* Docker installed and running
* Harbor CLI installed

Check that Harbor is available:

```bash
harbor --help
```

Check that Docker is working:

```bash
docker run hello-world
```

## Project structure

```text
log-report/
├── environment/
│   └── Dockerfile
├── solution/
│   └── solution.sh
├── tests/
│   ├── test.sh
│   └── test_outputs.py
├── instruction.md
└── task.toml
```

## How to test

Run the reference solution:

```bash
harbor run -p log-report -a oracle
```

Expected result:

```text
Mean: 1.000
```

Run the no-op agent:

```bash
harbor run -p log-report --agent nop
```

Expected result:

```text
Mean: 0.000
```

## Expected behavior

The oracle agent should pass because it creates the required `/app/report.json` artifact with the correct values.

The no-op agent should fail because it does not create the required report.

A correct local verification result is:

```text
oracle -> reward 1
nop    -> reward 0
```

## Notes

Harbor may create a local `jobs/` directory after running tests. This directory contains run logs and should not be committed.
