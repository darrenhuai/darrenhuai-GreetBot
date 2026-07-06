# Testing Notes

This project has both software and hardware-adjacent behavior, so testing should be split into small layers.

## Software checks

Run import and syntax checks before testing with physical hardware:

```bash
python -m compileall .
```

If tests are added later, run:

```bash
python -m pytest
```

## Camera workflow checks

Test camera startup separately from robot motion. This helps isolate whether a failure is caused by camera permissions, image processing, serial communication, or mechanical behavior.

## Hardware workflow checks

When testing robot movement:

- Start with small movement ranges.
- Keep the robot on a stable surface.
- Confirm wiring before powering motors.
- Test one subsystem at a time.
- Stop immediately if a servo stalls or overheats.

## Suggested future tests

- Unit tests for pure helper functions.
- Mocked tests for serial communication.
- Smoke tests for loading configuration.
- Demo scripts that can run without connected hardware.
